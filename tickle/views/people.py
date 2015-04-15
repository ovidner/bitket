# -*- coding: utf-8 -*-
from django.utils.translation import ugettext_lazy as _
from django.views.generic import FormView, DetailView, CreateView, ListView, DeleteView
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.shortcuts import resolve_url, redirect
from django.core.urlresolvers import reverse_lazy
from django.contrib import messages
from django.http import Http404

from datetime import datetime

from guardian.shortcuts import get_objects_for_user
from guardian.mixins import LoginRequiredMixin

from tickle.forms import LoginFormHelper, PersonForm, PersonFormHelper, IdentifyForm
from tickle.models.people import Person
from tickle.models.products import Holding, Purchase, Product
from tickle.views.mixins import MeOrPermissionRequiredMixin
from tickle.utils.kobra import StudentNotFound, Unauthorized
from tickle.utils.mail import TemplatedEmail


class ProfileView(MeOrPermissionRequiredMixin, DetailView):
    model = Person
    template_name = 'people/profile.html'
    context_object_name = 'person'

    # Guardian settings
    permission_required = 'tickle.view_person'
    accept_global_perms = True
    user_attr = 'user'

    def get_context_data(self, **kwargs):
        context = super(ProfileView, self).get_context_data(**kwargs)

        # For the sake of loose coupling, this probably shouldn't be here.
        # todo: solve in a more elegant way.
        context['membership_approvable_orchestras'] = get_objects_for_user(self.object.user,
                                                                           'orchard.approve_orchestra_members')

        return context


class LoginView(FormView):
    form_class = AuthenticationForm
    template_name = 'people/login.html'

    _user = None

    def get_success_url(self):
        return self.request.GET.get('next', resolve_url('profile', pk=self._user.person.pk))

    def get_context_data(self, **kwargs):
        context = super(LoginView, self).get_context_data(**kwargs)

        context['form_helper'] = LoginFormHelper()

        return context

    def form_valid(self, form):
        login(self.request, form.get_user())

        # Save the user pk in the view instance so get_success_url() can use it
        self._user = form.get_user()

        return super(LoginView, self).form_valid(form)


class CreateUserView(CreateView):
    model = Person
    form_class = PersonForm
    template_name = 'people/create_user.html'

    _user = None

    def get_success_url(self):
        return self.request.GET.get('next', resolve_url('create_user_success'))

    def get_context_data(self, **kwargs):
        context = super(CreateUserView, self).get_context_data(**kwargs)
        context['form_helper'] = PersonFormHelper()
        return context

    def form_valid(self, form):
        person = form.save()
        person.create_user_and_login(self.request)
        return super(CreateUserView, self).form_valid(form)


class ChangePasswordView(FormView):
    form_class = PasswordChangeForm
    template_name = 'people/change_password.html'

    def get_form(self, form_class):
        """
        Returns an instance of the form to be used in this view.
        """
        return form_class(user=self.request.user, **self.get_form_kwargs())

    def get_success_url(self):
        return resolve_url('profile', pk=self.request.user.person.pk)

    def get_context_data(self, **kwargs):
        context = super(ChangePasswordView, self).get_context_data(**kwargs)

        context['form_helper'] = LoginFormHelper()

        return context

    def form_valid(self, form):
        form.save()

        messages.success(self.request, _('Your password has been changed. Please log in again.'))

        return super(ChangePasswordView, self).form_valid(form)


class IdentifyView(FormView):
    form_class = IdentifyForm
    template_name = 'people/identify.html'

    person = None
    liu_id = None

    def get_create_user_url(self):
        next_url = self.request.GET.get('next', None)
        if next_url:
            return '%s?next=%s' % (resolve_url('create_user'), next_url)
        return resolve_url('create_user')

    def create_liu_user(self):
        try:
            person = Person(liu_id=self.liu_id, email='%s@student.liu.se' % self.liu_id)
            person.fill_kobra_data()
        except StudentNotFound:
            error_message = _(u'No student with the Liu ID %s was found.' % self.liu_id)
        except Unauthorized:
            error_message = _(u"It's temporally not possible to retrieve information for LiU IDs.")
        else:
            person.save()
            person.create_user_and_login(self.request)
            return resolve_url('create_user_success')

        messages.warning(self.request, u"%s %s" % (error_message, _(u'Please enter your personal information yourself.')))
        return self.get_create_user_url()

    def get_success_url(self):
        if self.person:
            next_url = self.request.GET.get('next', resolve_url('profile', pk=self.person.pk))
            if self.request.user.is_authenticated() and self.request.user.person == self.person:
                return next_url
            return '%s?next=%s' % (resolve_url('login'), next_url)
        elif self.liu_id:
            return self.create_liu_user()
        return self.get_create_user_url()

    def form_valid(self, form):
        person = form.get_existing_person_or_none()
        self.person = person
        self.liu_id = form.cleaned_data['liu_id']
        return super(IdentifyView, self).form_valid(form)


class PurchaseView(LoginRequiredMixin, ListView):
    model = Product
    template_name = 'tickle/purchase.html'
    login_url = reverse_lazy('identify')

    def get_queryset(self):
        return Product.objects.published()

    def get_context_data(self, **kwargs):
        context = super(PurchaseView, self).get_context_data(**kwargs)
        context['holding_list'] = self.request.user.person.holdings.filter(purchase__isnull=True)
        return context


@login_required(login_url=reverse_lazy('identify'))
def add_to_shopping_cart(request, pk):
    # TODO: Convert to CreateView with Holding as model?
    if request.POST:
        product = Product.objects.get(pk=pk)
        if product.quantitative:
            holding, created = Holding.objects.get_or_create(person=request.user.person, product=product,
                                                             purchase__isnull=True)
            if not created:
                holding.quantity += 1
                holding.save()
        else:
            holding, created = Holding.objects.get_or_create(person=request.user.person, product=product)
            if not created:
                messages.warning(request, _(u'You can only buy one %s product.') % product.public_name)

        return redirect('tickle:purchase')
    raise Http404()


class PurchaseCreateHoldingView(LoginRequiredMixin, CreateView):
    model = Holding
    success_url = reverse_lazy('tickle:purchase')

    def form_valid(self, form):
        pass


class ShoppingCartView(LoginRequiredMixin, ListView):
    # TODO: Full support for discounts.
    # TODO: Merge shopping cart stuff to one class?
    model = Holding
    template_name = 'tickle/shopping_cart.html'

    def get_queryset(self):
        return Holding.objects.filter(person=self.request.user.person, purchase__isnull=True)


class ShoppingCartDeleteView(LoginRequiredMixin, DeleteView):
    model = Holding
    success_url = reverse_lazy('tickle:shopping_cart')

    def get(self, request, *args, **kwargs):
        return redirect('tickle:shopping_cart')  # Only POST delete.


@login_required(login_url=reverse_lazy('identify'))
def complete_purchase(request):
    # TODO: Merge old purchases with new ones?
    # TODO: Convert to CreateView with Purchase as model?
    # TODO: Convert to UpdateView with Holding as model?
    if request.POST:
        person = request.user.person
        purchase = Purchase.objects.create(person=person, purchased=datetime.now())
        updated = person.holdings.filter(purchase__isnull=True).update(purchase=purchase)
        if updated:
            # TODO: Fill email body with correct information and test it.
            msg = TemplatedEmail(
                to=[person.pretty_email],
                from_email='Biljett SOF15 <biljett@sof15.se>',
                subject_template='tickle/email/purchase_success_subject.txt',
                body_template_html='tickle/email/purchase_success.html',
                context={
                    'person': person,
                    'purchase': purchase,
                },
                tags=['tickle'])
            msg.send()
            return redirect('tickle:purchase_completed_success')

        purchase.delete()
        messages.warning(request, _(u'Add at least one product to your shopping cart before you try to make a purchase.'))
        return redirect('tickle:purchase')
    raise Http404()