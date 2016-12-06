from __future__ import absolute_import, unicode_literals

from braces.views import LoginRequiredMixin, PermissionRequiredMixin
from django.conf import settings
from django.core import signing
from django.core.exceptions import SuspiciousOperation
from django.core.signing import BadSignature
from django.http import Http404
from django.utils.http import urlencode
from django.utils.translation import ugettext_lazy as _
from django.views.generic import TemplateView, RedirectView
from django.views.generic.detail import SingleObjectMixin

from rest_framework import generics, views, viewsets, status, mixins
from rest_framework.decorators import detail_route
from rest_framework.filters import DjangoFilterBackend
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_social_auth.views import JWTAuthMixin, BaseSocialAuthView

from tickle.filters import HoldingPermissionFilterBackend, HoldingFilterSet
from tickle.models import Event, Organization, Ticket, TicketType, Variation, \
    VariationChoice
from tickle.renderers import QrRenderer
from tickle.utils.signing import sign_state, unsign_state

from . import models, serializers


class StripeConnectPermissionMixin(LoginRequiredMixin,
                                   PermissionRequiredMixin):
    permission_required = 'organizers.manage_organizer_stripe'


class StripeConnectRequestView(StripeConnectPermissionMixin, SingleObjectMixin,
                               RedirectView):
    model = Organization
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
    model = Organization
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


class EventViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Event.objects.all()
    serializer_class = serializers.EventSerializer


class OrganizationViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Organization.objects.all()
    serializer_class = serializers.OrganizationSerializer


class AccessCodeViewSet(mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    queryset = models.AccessCode.objects.all()
    serializer_class = serializers.AccessCodeSerializer

    lookup_field = 'token'
    lookup_url_kwarg = 'token'
    lookup_value_regex = '[^/]+'  # Same as default, just includes .

    def get_object(self):
        try:
            return super().get_object()
        except BadSignature as exc:
            raise Http404


class PurchaseView(views.APIView):
    def post(self, request, *args, **kwargs):
        serializer = serializers.PurchaseSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_207_MULTI_STATUS)


class TicketViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Ticket.objects.all()
    serializer_class = serializers.TicketSerializer


class TicketTypeViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = TicketType.objects.published()
    serializer_class = serializers.TicketTypeSerializer


class VariationViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Variation.objects.all()
    serializer_class = serializers.VariationSerializer


class VariationChoiceViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = VariationChoice.objects.all()
    serializer_class = serializers.VariationChoiceSerializer
