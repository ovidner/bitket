from __future__ import absolute_import, unicode_literals

from uuid import UUID

from django.conf import settings
from django.core import signing
from django.core.exceptions import SuspiciousOperation
from django.http.response import HttpResponseRedirect, Http404, HttpResponseBadRequest
from django.utils.http import urlencode
from django.utils.translation import ugettext_lazy as _
from django.views.generic import FormView, TemplateView, UpdateView, RedirectView
from django.views.generic.detail import SingleObjectMixin

from braces.views import LoginRequiredMixin, PermissionRequiredMixin
from rest_framework.status import HTTP_400_BAD_REQUEST
from six import text_type

from tickle.common.views import ModelViewSet
from .models import Organizer
from .serializers import OrganizerSerializer


def sign_state(organizer_pk, session_key):
    # Casts the UUID object to str
    if isinstance(organizer_pk, UUID):
        organizer_pk = text_type(organizer_pk)

    return signing.dumps([organizer_pk, session_key])


def unsign_state(state, max_age=None):
    if max_age is None:
        max_age = settings.STRIPE_OAUTH_SIGN_MAX_AGE

    return signing.loads(state, max_age=max_age)


class InvalidSession(Exception):
    pass


class StripeConnectPermissionMixin(LoginRequiredMixin,
                                   PermissionRequiredMixin):
    permission_required = 'organizers.manage_organizer_stripe'


class StripeConnectRequestView(StripeConnectPermissionMixin, SingleObjectMixin,
                               RedirectView):
    model = Organizer
    slug_url_kwarg = 'organizer'
    permanent = False

    def get_redirect_url(self, *args, **kwargs):
        session_key = self.request.session.session_key
        params = {
            'client_id': settings.STRIPE_CLIENT_ID,
            'response_type': 'code',
            'scope': 'read_write',
            'state': sign_state(self.get_object().pk, session_key)
        }
        return '{url}?{params}'.format(url=settings.STRIPE_OAUTH_AUTHORIZE_URL,
                                       params=urlencode(params))


class StripeConnectCallbackView(StripeConnectPermissionMixin,
                                SingleObjectMixin, TemplateView):
    model = Organizer
    template_name = 'dummy.html'
    http_method_names = ['get']

    def get_object(self, queryset=None):
        if queryset is None:
            queryset = self.get_queryset()

        try:
            organizer_pk, state_session_key = unsign_state(self.signed_state)
        except signing.BadSignature:
            raise Http404(_('Invalid or expired request signature. Cannot '
                            'connect account.'))

        # Ensures the connection is initiated and finished in the same session.
        if not state_session_key == self.request.session.session_key:
            raise Http404(_('Invalid session key in request. Cannot connect '
                            'account.'))

        try:
            obj = queryset.get(pk=organizer_pk)
        except queryset.model.ObjectNotFound:
            raise Http404(_('Cannot find organizer.'))

        return obj

    def get(self, request, *args, **kwargs):
        try:
            self.auth_code = request.GET['code']
            self.scope = request.GET['scope']
            self.signed_state = request.GET['state']
        except KeyError:
            raise SuspiciousOperation(_('Required parameters missing from '
                                        'request.'))

        self.object = self.get_object()
        self.object.authorize_stripe(self.auth_code)

        return super(StripeConnectCallbackView, self).get(
            request, *args, **kwargs)


class OrganizerViewSet(ModelViewSet):
    queryset = Organizer.objects.all()
    serializer_class = OrganizerSerializer
    lookup_field = 'slug'
