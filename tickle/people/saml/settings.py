from __future__ import absolute_import, unicode_literals

from django.conf import settings
from django.core.urlresolvers import reverse, reverse_lazy

from saml_service_provider.settings import SAMLServiceProviderSettings
from onelogin.saml2.constants import OneLogin_Saml2_Constants


LIU_ADFS_SETTINGS = {
    'strict': settings.SAML_STRICT,
    'debug': settings.SAML_DEBUG,
    'sp': {
        'entityId': 'https://www.liubiljett.se/_saml/metadata/',
        'assertionConsumerService': {
            'url': 'https://www.liubiljett.se/_saml/login/complete/',
            'binding': OneLogin_Saml2_Constants.BINDING_HTTP_POST
        },
        'singleLogoutService': {
            'url': 'https://www.liubiljett.se/_saml/logout/',
            'binding': OneLogin_Saml2_Constants.BINDING_HTTP_REDIRECT
        },
        'NameIDFormat': OneLogin_Saml2_Constants.NAMEID_UNSPECIFIED,
        'x509cert': settings.SAML_SP_CERT,
        'privateKey': settings.SAML_SP_KEY
    },
    'idp': {
        'entityId': 'http://fs.liu.se/adfs/services/trust',
        'singleSignOnService': {
            'url': 'https://fs.liu.se/adfs/ls/',
            'binding': OneLogin_Saml2_Constants.BINDING_HTTP_REDIRECT
        },
        'singleLogoutService': {
            'url': 'https://fs.liu.se/adfs/ls/',
            'binding': OneLogin_Saml2_Constants.BINDING_HTTP_REDIRECT
        },
        # CN=fssigning.liu.se
        'x509cert': """-----BEGIN CERTIFICATE-----
MIIFOTCCBCGgAwIBAgIQAdlHVjMUXk6RFVjqYeenpjANBgkqhkiG9w0BAQsFADBkMQswCQYDVQQGEwJOTDEWMBQGA1UECBMNTm9vcmQtSG9sbGFuZDESMBAGA1UEBxMJQW1zdGVyZGFtMQ8wDQYDVQQKEwZURVJFTkExGDAWBgNVBAMTD1RFUkVOQSBTU0wgQ0EgMzAeFw0xNTAxMDcwMDAwMDBaFw0xODAxMTExMjAwMDBaMIGJMQswCQYDVQQGEwJTRTEXMBUGA1UECAwOw5ZzdGVyZ8O2dGxhbmQxEzARBgNVBAcMCkxpbmvDtnBpbmcxIDAeBgNVBAoMF0xpbmvDtnBpbmdzIHVuaXZlcnNpdGV0MQ8wDQYDVQQLEwZMaVUtSVQxGTAXBgNVBAMTEGZzc2lnbmluZy5saXUuc2UwggEiMA0GCSqGSIb3DQEBAQUAA4IBDwAwggEKAoIBAQCS5bpEkEcbJAsNdgyK1QYAbuq5PKl8bAcujqKIRZAr4uixWudDxRVhwOxDyZMTZGN0vNVdf+ZtUZQ9NWYaLcgEvzxhNbsA0fmTSwRlMvxj0R/JbDs5Slmew11wZ6rxgX7wRv8rjB3PSdf/SVc5LKgcDuCCGCLv+OE7d4K13OfKBxUv/vrD7upz6lgT79OWX6udFhU8sXmP8u8P/mID83o5N32hwxymRuEmjnLiVIrUR4cF5EwgblrpoqQKeGKdkroZApU0EJxvtopesVgUEGXW4tkogTJ8qtSPQK8iPEeteR6YpFCIxIbE0gpwDgo0bubt8T+FkQE71SLvbhv9RcZBAgMBAAGjggG/MIIBuzAfBgNVHSMEGDAWgBRn/YggFCeYxwnSJRm76VERY3VQYjAdBgNVHQ4EFgQU8vPdaPx+JhyN970NWqrTcbU/c0MwGwYDVR0RBBQwEoIQZnNzaWduaW5nLmxpdS5zZTAOBgNVHQ8BAf8EBAMCBaAwHQYDVR0lBBYwFAYIKwYBBQUHAwEGCCsGAQUFBwMCMGsGA1UdHwRkMGIwL6AtoCuGKWh0dHA6Ly9jcmwzLmRpZ2ljZXJ0LmNvbS9URVJFTkFTU0xDQTMuY3JsMC+gLaArhilodHRwOi8vY3JsNC5kaWdpY2VydC5jb20vVEVSRU5BU1NMQ0EzLmNybDBCBgNVHSAEOzA5MDcGCWCGSAGG/WwBATAqMCgGCCsGAQUFBwIBFhxodHRwczovL3d3dy5kaWdpY2VydC5jb20vQ1BTMG4GCCsGAQUFBwEBBGIwYDAkBggrBgEFBQcwAYYYaHR0cDovL29jc3AuZGlnaWNlcnQuY29tMDgGCCsGAQUFBzAChixodHRwOi8vY2FjZXJ0cy5kaWdpY2VydC5jb20vVEVSRU5BU1NMQ0EzLmNydDAMBgNVHRMBAf8EAjAAMA0GCSqGSIb3DQEBCwUAA4IBAQCgqdZfizsQZYpLif+sV+mgkkln6WVGv1KVw2xvRDO9jF192qjkL9zmB081qOydPtt8aLbXQHp13M/URoFK2Vvdikq5WQMkGxJu3zLtQD4lJsJXAaGdm7nSwWS4NHHIf5yg0rWC5kQBJnWhAHhPedFzfgGR9lUohhvnLJJ/PFuvN0sCsYYpRraQT880RdTq1imsFB3wAUHjN9tQCS3Ss9Cf6MOvwHb3flDe4OLwxxMZfI3oGwoUJHltib7xFuT7w5hOYts3Js+BBtsSskGSp/dz8PiH6NDQZG/9USNN1biuUCDxrhTBgSHIAeB3h7k6wue5C30EE8SCLfZ6Xxsmk1rn
-----END CERTIFICATE-----"""
    },
    'security': {
        'nameIdEncrypted': False,
        'authnRequestsSigned': True,
        'logoutRequestSigned': True,
        'logoutResponseSigned': True,

        'signMetadata': True,
        'wantAssertionsSigned': True,
        'wantMessagesSigned': False,
        'wantNameIdEncrypted': False,
        'requestedAuthnContext': False,
        'signatureAlgorithm': OneLogin_Saml2_Constants.RSA_SHA256
    },
    'contactPerson': {
        'support': {
            'givenName': 'Olle Vidner',
            'emailAddress': 'olle@liubiljett.se'
        }
    },
    'organization': {
        'sv-SE': {
            'name': 'liubiljett.se',
            'displayname': 'liubiljett.se',
            'url': 'https://www.liubiljett.se/'
        }
    }
}
