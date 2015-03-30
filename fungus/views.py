# -*- coding: utf-8 -*-
from django.shortcuts import render, resolve_url
from django.views.generic import FormView
from django.contrib import messages
from guardian.mixins import LoginRequiredMixin
from django.db.transaction import atomic


from fungus.models import ShiftRegistration
from fungus.forms import ChangeSelectedShiftsForm, ShiftForm, ShiftRegisterFormHelper, FunctionaryForm, FunctionaryFormHelper
from tickle.forms import PersonForm, PersonFormHelper, AcceptForm
from tickle.utils.mail import TemplatedEmail


class ShiftChangeView(FormView):
    form_class = ChangeSelectedShiftsForm
    template_name = 'fungus/change_selected_shift.html'
    model = ShiftRegistration
    success_url = '/admin/%s/%s/' % (model._meta.app_label, model._meta.model_name)

    def get(self, request, *args, **kwargs):
        selected = request.GET.get('ids')
        queryset = self.model.objects.filter(id__in=selected.split(','))
        form = self.form_class(initial={'shift_registration': queryset})
        context = dict(
            queryset=queryset,
            form=form,
            content_type=self.model._meta.verbose_name_plural.title(),
            list_description="Alla följande arbetspass kommer att bytas: ",
            form_description="Välj arbetspass att byta till.",
        )
        return render(request, self.template_name, context)

    def form_valid(self, form):
        shift = form.cleaned_data['shift']
        shift_registration = form.cleaned_data['shift_registration']
        rows_updated = shift_registration.update(shift=shift)
        if rows_updated == 1:
            model_name = self.model._meta.verbose_name
        else:
            model_name = self.model._meta.verbose_name_plural
        messages.add_message(self.request, messages.SUCCESS, u"%s %s ändrades." % (rows_updated, model_name))
        return super(ShiftChangeView, self).form_valid(form)


class RegisterFunctionaryView(FormView):
    template_name = 'fungus/register_functionary.html'
    form_class = ShiftForm

    def get_success_url(self):
        return resolve_url('fungus:register_functionary_success')

    def get_context_data(self, **kwargs):
        context = super(RegisterFunctionaryView, self).get_context_data(**kwargs)

        context['person_form_helper'] = PersonFormHelper()
        context['shift_form_helper'] = ShiftRegisterFormHelper()
        context['functionary_form_helper'] = FunctionaryFormHelper()

        context['person_form'] = PersonForm(self.request.POST or None)
        context['functionary_form'] = FunctionaryForm(self.request.POST or None)
        context['accept_form'] = AcceptForm(self.request.POST or None)

        return context

    def form_valid(self, form):
        context = self.get_context_data()
        person_form = context['person_form']
        functionary_form = context['functionary_form']
        accept_form = context['accept_form']

        if person_form.is_valid() and functionary_form.is_valid() and accept_form.is_valid():
            with atomic():
                person = person_form.save()
                functionary_form.instance.person = person
                functionary_form.save()

                for shift in form.cleaned_data['shifts']:
                    ShiftRegistration(person=person, shift=shift).save()

            msg = TemplatedEmail(
                to=[person.pretty_email],
                from_email='Funkissupport SOF15 <funkissupport@sof15.se>',
                subject_template='fungus/email/register_functionary_success_subject.txt',
                body_template_html='fungus/email/register_functionary_success.html',
                context={
                    'person': person,
                },
                tags=['fungus'])

            msg.send()

            return super(RegisterFunctionaryView, self).form_valid(form)

        else:
            return self.render_to_response(self.get_context_data(form=form))
