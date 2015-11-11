from __future__ import absolute_import, unicode_literals

from braces.views import CsrfExemptMixin
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
    def post(self, request):
        import base64
        from onelogin.saml2.response import OneLogin_Saml2_Response
        #raw_saml_response = base64.b64decode(request.POST['SAMLResponse'])

        #saml_response = OneLogin_Saml2_Response(self.saml_settings, raw_saml_response)


        return super(CompleteSamlLoginView, self).post(request)


class SamlMetadataView(SamlSettingsMixin, MetadataView):
    pass
