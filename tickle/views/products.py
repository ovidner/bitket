# -*- coding: utf-8 -*-
from django.utils.translation import ugettext_lazy as _
from django.views.generic import ListView, DeleteView, UpdateView, FormView
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.core.urlresolvers import reverse_lazy
from django.core.exceptions import PermissionDenied
from django.contrib import messages
from django.http import Http404
from django.db.transaction import atomic

from datetime import datetime

from guardian.mixins import LoginRequiredMixin

from tickle.forms import IdentifyForm, SearchPersonForm
from tickle.models.products import Holding, Purchase, Product, ShoppingCart
from tickle.utils.mail import TemplatedEmail


class PurchaseView(LoginRequiredMixin, ListView):
    model = Product
    template_name = 'tickle/purchase.html'

    def get_queryset(self):
        return Product.objects.published()

    def get_context_data(self, **kwargs):
        context = super(PurchaseView, self).get_context_data(**kwargs)
        person = self.request.user.person
        context['person'] = person

        return context


@login_required()
def add_to_shopping_cart(request, pk):
    # TODO: Convert to CreateView with Holding as model?
    if request.POST:
        try:
            product = Product.objects.published().get(pk=pk)
        except Product.NotFound:
            messages.warning(request, _('Product not available.'))
            return redirect('tickle:purchase')

        person = request.user.person

        if product.quantitative:
            quantity = int(request.POST.get('quantity', None))

            if not quantity or quantity < 0:
                messages.warning(request, _(u'Invalid quantity specified.'))

                return redirect('tickle:purchase')

            holding, created = Holding.objects.get_or_create(person=person, product=product,
                                                             shopping_cart=person.shopping_cart)
            if not created:
                holding.quantity += quantity
                holding.save()
        else:
            holding, created = Holding.objects.get_or_create(person=person, product=product,
                                                             defaults={'shopping_cart': person.shopping_cart})
            if not created:
                messages.warning(request, _(u'You can only buy one %s product.') % product.public_name)
        return redirect('tickle:purchase')
    raise Http404()


class ShoppingCartView(LoginRequiredMixin, ListView):
    # TODO: Merge shopping cart stuff to one class?
    model = Holding
    template_name = 'tickle/shopping_cart.html'

    def get_queryset(self):
        person = self.request.user.person
        if not hasattr(person, 'shopping_cart'):
            ShoppingCart.objects.create(person=person)
        return person.shopping_cart.holdings.all()


class ShoppingCartDeleteView(LoginRequiredMixin, DeleteView):
    model = Holding
    success_url = reverse_lazy('tickle:purchase')

    def get(self, request, *args, **kwargs):
        return redirect('tickle:purchase')  # Only POST delete.

    def post(self, request, *args, **kwargs):
        holding = self.get_object()
        if holding.person == request.user.person:
            return super(ShoppingCartDeleteView, self).post(request, *args, **kwargs)
        return redirect('tickle:purchase')


@login_required()
def complete_purchase(request):
    # TODO: Convert to CreateView with Purchase as model?
    # TODO: Convert to UpdateView with Holding as model?
    if request.POST:
        shopping_cart = request.user.person.shopping_cart

        if shopping_cart.holdings.count() < 1:
            messages.warning(request, _(u'Add at least one product to your shopping cart before you try to make a purchase.'))
            return redirect('tickle:purchase')

        shopping_cart.purchase()
        return redirect('tickle:purchase_completed_success')

    raise Http404()


class ExchangeView(LoginRequiredMixin, UpdateView):
    model = Holding
    form_class = SearchPersonForm
    template_name = 'tickle/transfer.html'

    def verify(self, holding):
        person = self.request.user.person
        if holding.person != person or holding.purchase.person != person or not holding.transferable:
            raise PermissionDenied

    def get(self, request, *args, **kwargs):
        self.verify(self.get_object())
        return super(ExchangeView, self).get(request, *args, **kwargs)

    def form_valid(self, form):
        holding = self.get_object()
        self.verify(holding)

        person = form.get_person()
        holding.transferee = person
        holding.save()

        msg = TemplatedEmail(
            to=[person.pretty_email],
            from_email='Biljett SOF15 <biljett@sof15.se>',
            subject_template='tickle/email/transfer_subject.txt',
            body_template_html='tickle/email/transfer.html',
            context={
                'holding': holding,
            },
            tags=['tickle', 'ticket', 'transfer'])
        msg.send()
        return redirect('tickle:transfer_ticket_success')


class ConfirmExchangeView(LoginRequiredMixin, UpdateView):
    model = Holding
    fields = []
    template_name = 'tickle/transfer_confirm.html'

    def verify(self, holding):
        person = self.request.user.person
        if holding.transferee != person or not holding.transferable:
            raise PermissionDenied

    def get(self, request, *args, **kwargs):
        self.verify(self.get_object())
        return super(ConfirmExchangeView, self).get(request, *args, **kwargs)

    def form_valid(self, form):
        holding = self.get_object()
        self.verify(holding)

        if '_confirm' in self.request.POST:
            transferee = holding.transferee
            person = holding.person
            purchase = holding.purchase
            discounted_total = holding.discounted_total

            with atomic():
                holding.person = transferee
                holding.transferee = None
                if purchase.holdings.count() > 1:
                    holding.purchase = Purchase.objects.create(person=transferee, purchased=purchase.purchased)  # Now or previous purchase time?
                else:
                    purchase.person = transferee
                    purchase.save()
                    holding.purchase = purchase
                # Recalculate discounts.
                holding.holding_discounts.all().delete()
                holding.product.product_discounts.eligible(transferee).copy_to_holding_discounts(holding)
                holding.save()

                if discounted_total - holding.discounted_total != 0:
                    # Price difference, invoice original owner with the difference.
                    # TODO: Make it properly working.
                    Purchase.objects.create(person=person, purchase=datetime.now())

            return redirect('tickle:transfer_ticket_confirm_success')
        elif '_decline' in self.request.POST:
            holding.transferee = None
            holding.save()
        return redirect('profile', pk=self.request.user.person.pk)