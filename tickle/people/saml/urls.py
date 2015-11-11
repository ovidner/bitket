from __future__ import absolute_import, unicode_literals

from django.conf.urls import url

from .views import (InitiateSamlLoginView, CompleteSamlLoginView,
                    SamlMetadataView)

urlpatterns = [
    url(r'^metadata/$', SamlMetadataView.as_view(), name='metadata'),
    url(r'^login/$', InitiateSamlLoginView.as_view(), name='initiate_login'),
    url(r'^login/complete/$', CompleteSamlLoginView.as_view(), name='complete_login'),
]
