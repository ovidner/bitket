# -*- coding: utf-8 -*-

from django.db import transaction
from django.forms.models import inlineformset_factory
from django.views.generic import CreateView, UpdateView
from django.http.response import HttpResponseRedirect
from django.utils.timezone import now


from orchard.forms import (OrchestraMembershipForm, ApproveOrchestraMemberForm,
                           OrchestraMemberRegistrationForm, InlineFormSetHelper,
                           OrchestraTicketFormHelper, OrchestraStuffForm)
from orchard.models import Orchestra, OrchestraMembership, OrchestraMemberRegistration, OrchestraProduct
from tickle.forms import PersonForm, AcceptForm, AcceptFormHelper, PersonFormHelper
from tickle.models.people import Person
from tickle.models.products import Holding, Purchase, Product


class ApproveOrchestraMemberView(UpdateView):
    form_class = ApproveOrchestraMemberForm
    template_name = 'orchard/approve_members.html'
    model = Orchestra

    def get_context_data(self, **kwargs):
        context = super(ApproveOrchestraMemberView, self).get_context_data(**kwargs)

        context['member_formset'] = inlineformset_factory(Orchestra, OrchestraMembership, extra=0)(self.request.POST or None, instance=self.object)

        return context

    def form_valid(self, form):
        context = self.get_context_data()

        member_formset = context['member_formset']

        if member_formset.is_valid():
            member_formset.instance = self.object
            member_formset.save()

            return HttpResponseRedirect(self.get_success_url())

        else:
            return self.render_to_response(self.get_context_data(form=form))


class RegisterOrchestraMemberView(CreateView):
    model = Person
    form_class = PersonForm

    template_name = 'orchard/register_member.html'

    def get_stuff_queryset(self):
        return OrchestraProduct.objects.stuff()

    def get_stuff_formset_initial_data(self):
        data = []
        # todo: consider solving this with a ValueQuerySet instead
        for i in self.get_stuff_queryset():
            data.append({'product_object': i, 'product': i.pk, 'quantity': 0})
        return data

    def get_context_data(self, **kwargs):
        context = super(RegisterOrchestraMemberView, self).get_context_data(**kwargs)

        context['ticket_form'] = OrchestraMemberRegistrationForm(self.request.POST or None)

        context['membership_formset'] = inlineformset_factory(
            Person,
            OrchestraMembership,
            min_num=1,
            extra=4,
            can_delete=False,
            form=OrchestraMembershipForm,
            fields=['orchestra', 'active', 'primary'])(self.request.POST or None)

        context['stuff_formset'] = inlineformset_factory(
            Person,
            Holding,
            extra=self.get_stuff_queryset().count(),
            can_delete=False,
            form=OrchestraStuffForm,
            fields=['product', 'quantity'])(self.request.POST or None, initial=self.get_stuff_formset_initial_data())

        context['accept_form'] = AcceptForm(self.request.POST or None)

        context['person_form_helper'] = PersonFormHelper()
        context['ticket_form_helper'] = OrchestraTicketFormHelper()
        context['inline_formset_helper'] = InlineFormSetHelper()
        context['accept_form_helper'] = AcceptFormHelper()

        context['ticket_prices'] = None

        return context

    def form_valid(self, form):
        context = self.get_context_data()

        ticket_form = context['ticket_form']
        membership_formset = context['membership_formset']
        stuff_formset = context['stuff_formset']

        if ticket_form.is_valid() and membership_formset.is_valid() and stuff_formset.is_valid():
            with transaction.atomic():
                person = form.save()
                holdings = []

                holdings.append(
                    Holding.objects.create(
                        person=person,
                        product=ticket_form.cleaned_data['ticket_type'].ticket_type.product
                    )
                )

                if ticket_form.cleaned_data['food']:
                    holdings.append(
                        Holding.objects.create(
                            person=person,
                            product=ticket_form.cleaned_data['ticket_type'].food_ticket_type.product
                        )
                    )

                if ticket_form.cleaned_data['accommodation']:
                    holdings.append(
                        Holding.objects.create(
                            person=person,
                            product=ticket_form.cleaned_data['ticket_type'].accommodation_ticket_type.product
                        )
                    )

                if ticket_form.cleaned_data['dinner']:
                    holdings.append(
                        Holding.objects.create(
                            person=person,
                            product=ticket_form.cleaned_data['ticket_type'].dinner_ticket_type.product
                        )
                    )

                membership_formset.instance = person
                membership_formset.save()

                stuff_formset.instance = person
                stuff = stuff_formset.save()

                # Stuff might be None
                if stuff:
                    holdings.extend(stuff)

                purchase = Purchase.objects.create(person=person, purchased=now(), valid=False)
                purchase.holdings.add(*holdings)

                # Marks the Purchase object as an orchestra member registration
                OrchestraMemberRegistration.objects.create(purchase=purchase)

            return HttpResponseRedirect(self.get_success_url())

        else:
            return self.render_to_response(self.get_context_data(form=form))