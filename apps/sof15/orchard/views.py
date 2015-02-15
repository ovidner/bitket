from django.shortcuts import render
from django.forms.formsets import formset_factory
from orchard.forms import SOF15OrchestraMemberRegistrationForm
from orchard.models import OrchestraMember, OrchestraMembership
from tickle.forms import SOF15PersonRegistrationForm


def registration(request):
    """ View for orchestra member registration form. Both get and post atm. """

    person_registration_form = SOF15PersonRegistrationForm(request.POST or None)
    orchestra_member_registration_formset = formset_factory(SOF15OrchestraMemberRegistrationForm, extra=3)

    if request.method == 'POST':
        registration_formset = orchestra_member_registration_formset(request.POST, request.FILES)

        if registration_formset.is_valid() and person_registration_form.is_valid():
            person = person_registration_form.save()
            orchestra_member = OrchestraMember.objects.create(person=person)

            for cleaned_data in registration_formset.cleaned_data:
                if len(cleaned_data) > 0:
                    orchestra = cleaned_data['orchestra']
                    active = cleaned_data['active']
                    primary = cleaned_data['primary']

                    OrchestraMembership(orchestra=orchestra, member=orchestra_member,
                                        active=active, primary=primary).save()
    else:
        registration_formset = orchestra_member_registration_formset()

    return render(request, 'base.html', {'orchestra_member_registration_formset': registration_formset,
                                         'person_registration_form': person_registration_form})