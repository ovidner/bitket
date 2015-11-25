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
            'url': settings.SAML_SP_ACS_URL,
            'binding': OneLogin_Saml2_Constants.BINDING_HTTP_POST
        },
        'singleLogoutService': {
            'url': settings.SAML_SP_SLO_URL,
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
        'x509cert': (
            '-----BEGIN CERTIFICATE-----'
            'MIIFOTCCBCGgAwIBAgIQAdlHVjMUXk6RFVjqYeenpjANBgkqhkiG9w0BAQsFADBkM'
            'QswCQYDVQQGEwJOTDEWMBQGA1UECBMNTm9vcmQtSG9sbGFuZDESMBAGA1UEBxMJQW'
            '1zdGVyZGFtMQ8wDQYDVQQKEwZURVJFTkExGDAWBgNVBAMTD1RFUkVOQSBTU0wgQ0E'
            'gMzAeFw0xNTAxMDcwMDAwMDBaFw0xODAxMTExMjAwMDBaMIGJMQswCQYDVQQGEwJT'
            'RTEXMBUGA1UECAwOw5ZzdGVyZ8O2dGxhbmQxEzARBgNVBAcMCkxpbmvDtnBpbmcxI'
            'DAeBgNVBAoMF0xpbmvDtnBpbmdzIHVuaXZlcnNpdGV0MQ8wDQYDVQQLEwZMaVUtSV'
            'QxGTAXBgNVBAMTEGZzc2lnbmluZy5saXUuc2UwggEiMA0GCSqGSIb3DQEBAQUAA4I'
            'BDwAwggEKAoIBAQCS5bpEkEcbJAsNdgyK1QYAbuq5PKl8bAcujqKIRZAr4uixWudD'
            'xRVhwOxDyZMTZGN0vNVdf+ZtUZQ9NWYaLcgEvzxhNbsA0fmTSwRlMvxj0R/JbDs5S'
            'lmew11wZ6rxgX7wRv8rjB3PSdf/SVc5LKgcDuCCGCLv+OE7d4K13OfKBxUv/vrD7u'
            'pz6lgT79OWX6udFhU8sXmP8u8P/mID83o5N32hwxymRuEmjnLiVIrUR4cF5Ewgblr'
            'poqQKeGKdkroZApU0EJxvtopesVgUEGXW4tkogTJ8qtSPQK8iPEeteR6YpFCIxIbE'
            '0gpwDgo0bubt8T+FkQE71SLvbhv9RcZBAgMBAAGjggG/MIIBuzAfBgNVHSMEGDAWg'
            'BRn/YggFCeYxwnSJRm76VERY3VQYjAdBgNVHQ4EFgQU8vPdaPx+JhyN970NWqrTcb'
            'U/c0MwGwYDVR0RBBQwEoIQZnNzaWduaW5nLmxpdS5zZTAOBgNVHQ8BAf8EBAMCBaA'
            'wHQYDVR0lBBYwFAYIKwYBBQUHAwEGCCsGAQUFBwMCMGsGA1UdHwRkMGIwL6AtoCuG'
            'KWh0dHA6Ly9jcmwzLmRpZ2ljZXJ0LmNvbS9URVJFTkFTU0xDQTMuY3JsMC+gLaArh'
            'ilodHRwOi8vY3JsNC5kaWdpY2VydC5jb20vVEVSRU5BU1NMQ0EzLmNybDBCBgNVHS'
            'AEOzA5MDcGCWCGSAGG/WwBATAqMCgGCCsGAQUFBwIBFhxodHRwczovL3d3dy5kaWd'
            'pY2VydC5jb20vQ1BTMG4GCCsGAQUFBwEBBGIwYDAkBggrBgEFBQcwAYYYaHR0cDov'
            'L29jc3AuZGlnaWNlcnQuY29tMDgGCCsGAQUFBzAChixodHRwOi8vY2FjZXJ0cy5ka'
            'WdpY2VydC5jb20vVEVSRU5BU1NMQ0EzLmNydDAMBgNVHRMBAf8EAjAAMA0GCSqGSI'
            'b3DQEBCwUAA4IBAQCgqdZfizsQZYpLif+sV+mgkkln6WVGv1KVw2xvRDO9jF192qj'
            'kL9zmB081qOydPtt8aLbXQHp13M/URoFK2Vvdikq5WQMkGxJu3zLtQD4lJsJXAaGd'
            'm7nSwWS4NHHIf5yg0rWC5kQBJnWhAHhPedFzfgGR9lUohhvnLJJ/PFuvN0sCsYYpR'
            'raQT880RdTq1imsFB3wAUHjN9tQCS3Ss9Cf6MOvwHb3flDe4OLwxxMZfI3oGwoUJH'
            'ltib7xFuT7w5hOYts3Js+BBtsSskGSp/dz8PiH6NDQZG/9USNN1biuUCDxrhTBgSH'
            'IAeB3h7k6wue5C30EE8SCLfZ6Xxsmk1rn'
            '-----END CERTIFICATE-----')
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
