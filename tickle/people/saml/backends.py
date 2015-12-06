from __future__ import absolute_import, unicode_literals

from saml_service_provider.auth_backend import (SAMLServiceProviderBackend,
                                                SAMLUserProxy)
from .constants import claims


class LiuAdfsUserProxy(SAMLUserProxy):
    nameid_field = 'liu_id'

    def get_liu_id(self):
        return self.attributes[claims.CLAIM_IMMUTABLE_ID][0]

    def get_user_kwargs(self):
        return {self.nameid_field: self.get_liu_id()}

    def get_or_create_user(self):
        user = super(LiuAdfsUserProxy, self).get_or_create_user()
        user.fill_kobra_data()
        user.save()
        return user


class LiuAdfsBackend(SAMLServiceProviderBackend):
    user_proxy_class = LiuAdfsUserProxy
