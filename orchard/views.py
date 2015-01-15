# -*- coding: utf-8 -*-

from django.shortcuts import render
from django.forms.formsets import formset_factory
from django.forms.models import inlineformset_factory
from django.views.generic import CreateView, UpdateView
from django.http.response import HttpResponseRedirect

from orchard.forms import OrchestraMembershipForm, OrchestraMemberForm, ApproveOrchestraMemberForm, \
    OrchestraMemberFormSet, OrchestraMemberRegistrationForm, InlineFormSetHelper, PersonFormHelper, OrchestraTicketFormHelper, OrchestraStuffForm
from orchard.models import Orchestra, OrchestraMember, OrchestraMembership
from tickle.forms import PersonForm
from tickle.models.people import Person
from tickle.models.products import Holding, Purchase, Product


class ApproveOrchestraMemberView(UpdateView):
    form_class = ApproveOrchestraMemberForm
    template_name = 'orchard/approve_members.html'
    model = Orchestra

    def get_context_data(self, **kwargs):
        context = super(ApproveOrchestraMemberView, self).get_context_data(**kwargs)

        context['member_formset'] = OrchestraMemberFormSet(self.request.POST or None, instance=self.object)

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
    form_class = OrchestraMemberRegistrationForm
    template_name = 'orchard/register_member.html'
    model = Purchase

    def get_stuff_queryset(self):
        return Product.objects.exclude(ticket_type__isnull=False)

    def get_stuff_formset_initial_data(self):
        data = []
        for i in self.get_stuff_queryset():
            data.append({'product_object': i, 'product': i.pk, 'quantity': 0})
        return data

    def get_context_data(self, **kwargs):
        context = super(RegisterOrchestraMemberView, self).get_context_data(**kwargs)

        context['person_form'] = PersonForm(self.request.POST or None)

        context['orchestra_membership_formset'] = inlineformset_factory(Person,
                                                                        OrchestraMembership,
                                                                        min_num=1,
                                                                        extra=5,
                                                                        can_delete=False,
                                                                        form=OrchestraMembershipForm,
                                                                        fields=['orchestra', 'active', 'primary'])(self.request.POST or None)

        context['stuff_formset'] = inlineformset_factory(Person,
                                                         Holding,
                                                         extra=self.get_stuff_queryset().count(),
                                                         can_delete=False,
                                                         form=OrchestraStuffForm,
                                                         fields=['product', 'quantity'],)(self.request.POST or None,
                                                                                          initial=self.get_stuff_formset_initial_data())

        context['person_form_helper'] = PersonFormHelper()
        context['ticket_form_helper'] = OrchestraTicketFormHelper()
        context['inline_formset_helper'] = InlineFormSetHelper()

        return context

    def form_valid(self, form):
        context = self.get_context_data()

        person_form = context['person_form']
        orchestra_membership_formset = context['orchestra_membership_formset']

        if person_form.is_valid() and orchestra_membership_formset.is_valid():
            person = person_form.save()

            orchestra_membership_formset.instance = person
            orchestra_membership_formset.save()

            form.instance.person = person
            form.save()

            return HttpResponseRedirect(self.get_success_url())

        else:
            return self.render_to_response(self.get_context_data(form=form))


def registration(request):
    """ View for orchestra member registration form. Both get and post atm. """

    person_registration_form = PersonForm(request.POST or None)

    orchestra_member_form = OrchestraMemberForm(request.POST or None)
    orchestra_membership_formset = formset_factory(OrchestraMembershipForm, extra=3)

    HoldingFormset = inlineformset_factory(Person, Holding, extra=1, max_num=1, min_num=1, can_delete=False, fields=['person', 'product'])

    if request.method == 'POST':
        registration_formset = orchestra_membership_formset(request.POST, request.FILES)
        holding_formset = HoldingFormset(request.POST, request.FILES)

        if registration_formset.is_valid() and person_registration_form.is_valid() and orchestra_member_form.is_valid() and holding_formset.is_valid():
            person = person_registration_form.save()

            orchestra_member = orchestra_member_form.save(commit=False)
            orchestra_member.person = person
            orchestra_member.save()

            holding_formset.instance = person
            holdings = holding_formset.save(commit=False)

            for holding in holdings:
                holding.confirmed = False
                holding.save()

            # orchestra_member = OrchestraMember.objects.create(person=person)

            for cleaned_data in registration_formset.cleaned_data:
                if len(cleaned_data) > 0:
                    orchestra = cleaned_data['orchestra']
                    active = cleaned_data['active']
                    primary = cleaned_data['primary']

                    OrchestraMembership(orchestra=orchestra, member=orchestra_member,
                                        active=active, primary=primary).save()
    else:
        registration_formset = orchestra_membership_formset()
        holding_formset = HoldingFormset()

    return render(request, 'orchard/_register_member.html', {'orchestra_member_registration_formset': registration_formset,
                                         'person_registration_form': person_registration_form, 'orchestra_member_form': orchestra_member_form,
                                         'holding_formset': holding_formset})