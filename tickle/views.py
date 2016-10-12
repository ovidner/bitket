from __future__ import absolute_import, unicode_literals

from braces.views import LoginRequiredMixin, PermissionRequiredMixin
from django.conf import settings
from django.core import signing
from django.core.exceptions import SuspiciousOperation
from django.http import Http404
from django.utils.http import urlencode
from django.utils.translation import ugettext_lazy as _
from django.views.generic import TemplateView, RedirectView
from django.views.generic.detail import SingleObjectMixin
from dry_rest_permissions.generics import (DRYPermissions,
                                           DRYPermissionFiltersBase)
from rest_framework import viewsets
from rest_framework.decorators import list_route, detail_route
from rest_framework.filters import DjangoFilterBackend
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.reverse import reverse
from tickle.organizers.serializers import OrganizerSerializer
from tickle.organizers.views import unsign_state

from tickle.filters import CartFilterBackend, HoldingPermissionFilterBackend, \
    HoldingFilterSet
from tickle.models import MainEvent, Organizer, Person, StudentUnion, Cart, \
    Holding, Product, ProductVariation, ProductVariationChoice
from tickle.renderers import QrRenderer
from tickle.routers import parent_lookups
from tickle.serializers import MainEventSerializer, OrganizerSerializer, \
    PersonSerializer, StudentUnionSerializer, CartSerializer, \
    CartPurchaseSerializer, HoldingSerializer, ProductSerializer, \
    ProductVariationSerializer, ProductVariationChoiceSerializer
from tickle.utils import sign_state, unsign_state


class ClientView(TemplateView):
    template_name = 'base.html'

    def get_context_data(self, **kwargs):
        context = super(ClientView, self).get_context_data(**kwargs)
        context['stripe_public_key'] = settings.STRIPE_PUBLIC_KEY
        context['sentry_release'] = settings.RAVEN_CONFIG['release']
        context['google_analytics_id'] = settings.GOOGLE_ANALYTICS_ID
        return context


class ModelViewSet(viewsets.ModelViewSet):
    parent_lookups = {}
    permission_classes = (DRYPermissions,)

    def get_queryset(self):
        queryset = super(ModelViewSet, self).get_queryset()
        select_related_args = []
        filter_kwargs = {}

        for kwarg, orm_lookup in self.parent_lookups.iteritems():
            try:
                filter_kwargs[orm_lookup] = self.kwargs[kwarg]

                # pk fields can't be select_related
                select_related_args.append(orm_lookup.rstrip('__pk'))
            except KeyError:
                continue

        return queryset.filter(**filter_kwargs).select_related(*select_related_args)


class MainEventViewSet(ModelViewSet):
    queryset = MainEvent.objects.all()
    serializer_class = MainEventSerializer
    lookup_field = 'slug'
    parent_lookups = parent_lookups.MAIN_EVENT


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


class PersonFilterBackend(DRYPermissionFiltersBase):
    def filter_list_queryset(self, request, queryset, view):
        return queryset.filter(pk=request.user.pk)


class PersonViewSet(ModelViewSet):
    queryset = Person.objects.all()
    serializer_class = PersonSerializer
    filter_backends = (PersonFilterBackend,)

    @list_route()
    def current(self, request):
        qs = self.filter_queryset(self.get_queryset())
        obj = get_object_or_404(qs, pk=request.user.pk)
        serializer = self.get_serializer(obj)
        return Response(serializer.data)


class StudentUnionViewSet(ModelViewSet):
    queryset = StudentUnion.objects.all()
    serializer_class = StudentUnionSerializer
    lookup_field = 'slug'


class CartViewSet(ModelViewSet):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer
    filter_backends = (CartFilterBackend,)
    parent_lookups = parent_lookups.CART

    def get_purchase_serializer(self, *args, **kwargs):
        serializer_class = CartPurchaseSerializer
        kwargs['context'] = self.get_serializer_context()
        return serializer_class(*args, **kwargs)

    @detail_route(['patch'])
    def purchase(self, request, pk=None):
        instance = self.get_object()
        purchase_serializer = self.get_purchase_serializer(instance, data=request.data, partial=True)
        purchase_serializer.is_valid(raise_exception=True)
        self.perform_update(purchase_serializer)

        serializer = self.get_serializer(instance)
        return Response(serializer.data)


class HoldingViewSet(ModelViewSet):
    queryset = Holding.objects.all()
    serializer_class = HoldingSerializer
    filter_backends = (HoldingPermissionFilterBackend, DjangoFilterBackend)
    filter_class = HoldingFilterSet
    parent_lookups = parent_lookups.HOLDING

    @detail_route(['get'], renderer_classes=[QrRenderer])
    def qr(self, request, pk=None):
        url = reverse('client:holding-detail', kwargs={'pk': pk}, request=request)
        return Response(url)

    @detail_route(['post', 'patch'])
    def utilize(self, request, pk=None):
        instance = self.get_object()
        instance.utilize()
        instance.save()
        return self.retrieve(request, pk=pk)

    @detail_route(['post', 'patch'])
    def unutilize(self, request, pk=None):
        instance = self.get_object()
        instance.unutilize()
        instance.save()
        return self.retrieve(request, pk=pk)


class ProductViewSet(ModelViewSet):
    queryset = Product.objects.published()
    serializer_class = ProductSerializer
    lookup_field = 'slug'
    parent_lookups = parent_lookups.PRODUCT


class ProductVariationViewSet(ModelViewSet):
    queryset = ProductVariation.objects.all()
    serializer_class = ProductVariationSerializer
    parent_lookups = parent_lookups.PRODUCT_VARIATION


class ProductVariationChoiceViewSet(ModelViewSet):
    queryset = ProductVariationChoice.objects.all()
    serializer_class = ProductVariationChoiceSerializer
    parent_lookups = parent_lookups.PRODUCT_VARIATION_CHOICE
