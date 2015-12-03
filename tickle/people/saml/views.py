from __future__ import absolute_import, unicode_literals

from braces.views import CsrfExemptMixin
from django.core.urlresolvers import reverse
from django.http.response import HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt

from saml_service_provider.views import (InitiateAuthenticationView,
                                         CompleteAuthenticationView,
                                         MetadataView)

from .settings import LIU_ADFS_SETTINGS


class SamlSettingsMixin(object):
    saml_settings = LIU_ADFS_SETTINGS

    def get_saml_settings(self):
        return self.saml_settings


class InitiateSamlLoginView(SamlSettingsMixin, InitiateAuthenticationView):
    pass


class CompleteSamlLoginView(CsrfExemptMixin, SamlSettingsMixin,
                            CompleteAuthenticationView):
    def get(self, request):
        return HttpResponseRedirect(reverse('client:home'))


class SamlMetadataView(SamlSettingsMixin, MetadataView):
    pass
