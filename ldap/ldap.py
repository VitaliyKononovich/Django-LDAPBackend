"""
Low-level LDAP hooks.


import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "sqm.settings")
from django.conf import settings
# print(settings.LDAP_AUTH_ACTIVE_DIRECTORY_DOMAIN)
from polls.ldap.ldap import LDAPConnection

"""
from ldap3.core.exceptions import LDAPException
from ldap3 import Server, Connection, NTLM, SIMPLE, NONE
from types import GeneratorType
#from pprint import pprint

try:
    from . import conf
    ldap_settings = conf.ldap_settings
except Exception as err:
    print('LDAPException: ldap_settings ', err)
    from conf import ldap_settings

SEQUENCE_TYPES = (set, list, tuple, GeneratorType, type(dict().keys()))


class LDAPConnection:
    def __init__(self):
        if ldap_settings.LDAP_AUTH_PROTOCOL == 'NTLM':
            self._authentication = NTLM
        else:
            self._authentication = SIMPLE

        self._username = None
        self._conn = None
        self._is_bind = False

    def authenticate(self, username: str, password: str):
        if self._is_bind:
            self.unbind()
        self._username = username
        if ldap_settings.LDAP_AUTH_PROTOCOL == 'Kerberos':
            user = username + ldap_settings.LDAP_AUTH_ACTIVE_DIRECTORY_DOMAIN
        elif ldap_settings.LDAP_AUTH_PROTOCOL == 'NTLM':
            user = ldap_settings.LDAP_AUTH_ACTIVE_DIRECTORY_DOMAIN + '\\' + username
        else:
            user = username
        try:
            #Connect to LDAP
            server = Server(ldap_settings.LDAP_AUTH_URL, get_info=NONE, use_ssl=ldap_settings.LDAP_AUTH_USE_SSL)
            self._conn = Connection(server, user=user, password=password,
                                authentication=self._authentication, auto_bind=True)
            self._is_bind = True
        except LDAPException as err:
            print('LDAPException:', str(err))
            return False
        return True

    def search(self) -> dict:
        # print('Searching...')
        if not self._is_bind:
            raise Exception('LDAP Conection is not bind. Search is not possible')
        if (ldap_settings.LDAP_AUTH_SEARCH_FILTER == None or ldap_settings.LDAP_AUTH_SEARCH_ATRIBUTES == None
                    or ldap_settings.LDAP_AUTH_SEARCH_BASE == None):
            raise Exception('Some of LDAP_AUTH_SEARCH_* settings are not configured in settings.py')
        try:
            search_filter = '(%s=%s)' % (ldap_settings.LDAP_AUTH_SEARCH_FILTER, self._username)
            self._conn.search(ldap_settings.LDAP_AUTH_SEARCH_BASE, search_filter, attributes=ldap_settings.LDAP_AUTH_SEARCH_ATRIBUTES)
        except LDAPException as err:
            print('LDAPException:', str(err))
        else:
            search_result = self._conn.response
            if isinstance(search_result, SEQUENCE_TYPES):
                result_dict = dict()
                result_dict['entries'] = []

                for response in search_result:
                    if response['type'] == 'searchResEntry':
                        entry = dict()
                        entry['dn'] = response['dn']
                        entry['attributes'] = dict(response['attributes'])
                        result_dict['entries'].append(entry)
                #pprint(result_dict)
                return result_dict

    def unbind(self):

        if self._is_bind:
            self._conn.unbind()
            self._is_bind = False

    def __del__(self):
        self.unbind()
