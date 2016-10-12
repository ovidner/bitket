# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth.views import logout

from tickle.routers import urlpatterns as api_router_urlpatterns
from tickle.views import ClientView, StripeConnectRequestView, \
    StripeConnectCallbackView

api_urlpatterns = [
    url(r'^', include(api_router_urlpatterns)),
    url(r'^login/', include('rest_social_auth.urls_jwt')),
]

client_urlpatterns = [
    url(r'^$', ClientView.as_view(), name='home'),
    url(r'^holdings/(?P<pk>[0-9a-fA-F-]{36})/', ClientView.as_view(), name='holding-detail'),
    #url(r'^.*/$', ClientView.as_view())
]

urlpatterns = [
    url('', include('social.apps.django_app.urls', namespace='social')),
    url(r'^api/', include(api_urlpatterns)),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^stripe/connect/(?P<organizer>[\w-]+)/$', StripeConnectRequestView.as_view()),
    url(r'^stripe/connect-callback/$', StripeConnectCallbackView.as_view()),

    url(r'^logout/$', logout, name='logout'),

    url(r'^', include(client_urlpatterns, namespace='client')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
