# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib import admin
from rest_social_auth.views import SocialJWTOnlyAuthView
from rest_framework.routers import DefaultRouter as _DefaultRouter
from rest_framework_jwt.views import (refresh_jwt_token)

from . import views


class DefaultRouter(_DefaultRouter):
    include_format_suffixes = False


router = DefaultRouter()
router.register(r'access-codes', views.AccessCodeViewSet)
router.register(r'events', views.EventViewSet)
router.register(r'organizations', views.OrganizationViewSet)
router.register(r'tickets', views.TicketViewSet)
router.register(r'ticket-types', views.TicketTypeViewSet)
router.register(r'variations', views.VariationViewSet)
router.register(r'variation-choices', views.VariationChoiceViewSet)

api_urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^purchases/$', views.PurchaseView.as_view(), name='purchase-list'),
    url(r'^auth-token/$', SocialJWTOnlyAuthView.as_view()),
    url(r'^auth-token/refresh/$', refresh_jwt_token)
]

urlpatterns = [
    url(r'^api/', include(api_urlpatterns)),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^stripe/connect/(?P<organizer>[\w-]+)/$', views.StripeConnectRequestView.as_view()),
    url(r'^stripe/connect-callback/$', views.StripeConnectCallbackView.as_view()),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
