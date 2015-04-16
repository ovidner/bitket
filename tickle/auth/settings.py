# -*- coding: utf-8 -*-
import ldap
from django_auth_ldap.config import ActiveDirectoryGroupType
from django_auth_ldap.backend import LDAPSettings


class LiULDAPSettings(LDAPSettings):
    """
    Defines common settings for all LDAP connections to LiU Active Directory.

    Overrides *default* settings instead of defining them hard. This makes it possible to override them per project.
    """

    def __init__(self, *args, **kwargs):
        self.defaults.update({
            # Server and connection settings
            'SERVER_URI': 'ldap://ad.liu.se',
            'START_TLS': True,
            'CONNECTION_OPTIONS': {
                ldap.OPT_X_TLS_REQUIRE_CERT: ldap.OPT_X_TLS_NEVER,
            },

            'BIND_AS_AUTHENTICATING_USER': True,

            'GROUP_TYPE': ActiveDirectoryGroupType(),
        })

        super(LiULDAPSettings, self).__init__(*args, **kwargs)


class LiUStudentLDAPSettings(LiULDAPSettings):
    """
    Settings specifically for authenticating students.
    """
    def __init__(self, *args, **kwargs):
        self.defaults.update({
            'USER_DN_TEMPLATE': 'CN=%(user)s,OU=Students,OU=Accounts,DC=ad,DC=liu,DC=se',
        })

        super(LiUStudentLDAPSettings, self).__init__(*args, **kwargs)


class LiUEmployeeLDAPSettings(LiULDAPSettings):
    """
    Settings specifically for authenticating employees.
    """
    def __init__(self, *args, **kwargs):
        self.defaults.update({
            'USER_DN_TEMPLATE': 'CN=%(user)s,OU=Employees,OU=Accounts,DC=ad,DC=liu,DC=se',
            })

        super(LiUEmployeeLDAPSettings, self).__init__(*args, **kwargs)
