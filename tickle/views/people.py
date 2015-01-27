# -*- coding: utf-8 -*-
from django.views.generic import FormView, DetailView
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login
from django.shortcuts import resolve_url

from guardian.mixins import PermissionRequiredMixin
from guardian.shortcuts import get_objects_for_user

from tickle.forms import LoginFormHelper
from tickle.models.people import Person


class ProfileView(PermissionRequiredMixin, DetailView):
    model = Person
    template_name = 'people/profile.html'
    context_object_name = 'person'

    # Guardian settings
    permission_required = 'tickle.view_person'
    accept_global_perms = True

    def get_context_data(self, **kwargs):
        context = super(ProfileView, self).get_context_data(**kwargs)

        # For the sake of loose coupling, this probably shouldn't be here.
        # todo: solve in a more elegant way.
        context['membership_approvable_orchestras'] = get_objects_for_user(self.object.user, 'orchard.approve_orchestra_members')

        return context


class LoginView(FormView):
    form_class = AuthenticationForm
    template_name = 'people/login.html'

    _user = None

    def get_success_url(self):
        if hasattr(self.request.GET, 'next'):
            return self.request.GET['next']
        return resolve_url('profile', pk=self._user.person.pk)


    def get_context_data(self, **kwargs):
        context = super(LoginView, self).get_context_data(**kwargs)

        context['form_helper'] = LoginFormHelper()

        return context

    def form_valid(self, form):
        login(self.request, form.get_user())

        # Save the user pk in the view instance so get_success_url() can use it
        self._user = form.get_user()

        return super(LoginView, self).form_valid(form)