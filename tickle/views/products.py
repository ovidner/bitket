# -*- coding: utf-8 -*-
from django.utils.translation import ugettext_lazy as _
from django.views.generic import ListView, DeleteView, FormView
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.core.urlresolvers import reverse_lazy
from django.contrib import messages
from django.http import Http404
from django.shortcuts import render_to_response

from guardian.mixins import LoginRequiredMixin, PermissionRequiredMixin

from tickle.models import Holding, Product, ShoppingCart, Person, Delivery
from tickle.forms import TurboDeliveryForm


class TurboDeliveryAjaxView(PermissionRequiredMixin, FormView):
    form_class = TurboDeliveryForm
    template_name = 'tickle/turbo_delivery_ajax.html'

    accept_global_perms = True
    permission_required = 'tickle.add_delivery'

    def form_valid(self, form):
        try:
            person = form.get_person()
            person_error = None
            # Forces queryset evaluation by calling list()
            historic_deliveries = list(form.get_auto_holdings().delivered())
            delivery = form.deliver_auto_holdings()
        except Person.DoesNotExist:
            person = None
            person_error = _('Person not found.')
            delivery = None
            historic_deliveries = None
        except Person.MultipleObjectsReturned:
            person = None
            person_error = _('Multiple people found.')
            delivery = None
            historic_deliveries = None

        return render_to_response(
            self.get_template_names(),
            self.get_context_data(person=person, person_error=person_error, delivery=delivery,
                                  historic_deliveries=historic_deliveries))


class TurboDeliveryView(TurboDeliveryAjaxView):
    template_name = 'tickle/turbo_delivery.html'


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

        if product.has_reached_quota():
            messages.warning(request, _('Sorry but %s is out of stock.') % product)
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

        try:
            shopping_cart.purchase()
        except Exception as e:
            messages.warning(request, _('Sorry but %s is out of stock.') % e.args)
            return redirect('tickle:purchase')

        return redirect('tickle:purchase_completed_success')

    raise Http404()
