# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth.views import logout

from tickle.common.views import ClientView
from tickle.organizers.views import (StripeConnectCallbackView,
                                     StripeConnectRequestView)
from tickle.common.routers import urlpatterns as api_router_urlpatterns

api_urlpatterns = [
    url(r'^', include(api_router_urlpatterns))
]

client_urlpatterns = [
    url(r'^$', ClientView.as_view(), name='home'),
    url(r'^holdings/(?P<pk>[0-9a-fA-F-]{36})/', ClientView.as_view(), name='holding-detail'),
    url(r'^.*/$', ClientView.as_view())
]

urlpatterns = [
    url(r'^api/', include(api_urlpatterns)),
    url(r'^auth/', include('allauth.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^stripe/connect/(?P<organizer>[\w-]+)/$', StripeConnectRequestView.as_view()),
    url(r'^stripe/connect-callback/$', StripeConnectCallbackView.as_view()),

    url(r'^_saml/', include('tickle.people.saml.urls', namespace='saml')),
    url(r'^logout/$', logout, name='logout'),

    url(r'^', include(client_urlpatterns, namespace='client')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    # This allows the error pages to be debugged during development, just visit
    # these url in browser to see how these error pages look like.
    urlpatterns += [
        url(r'^400/$', 'django.views.defaults.bad_request'),
        url(r'^403/$', 'django.views.defaults.permission_denied'),
        url(r'^404/$', 'django.views.defaults.page_not_found'),
        url(r'^500/$', 'django.views.defaults.server_error'),
    ]
