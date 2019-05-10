"""
Configuration parameters for LDAP

1. Create object ldap_settings from calss LDAPSettings
2. Try to load LDAP configuration from Django web application settings.py
3. If it cause Exception - leave default parameters for object
"""

class LDAPSettings:
    def __init__(self):
        # Name or IP or the complete url in the scheme://hostname:hostport format of the server
        # Port and scheme (ldap or ldaps) defined here have precedence over the parameters
        # LDAP_AUTH_PORT and LDAP_AUTH_USE_SSL
        #LDAP_AUTH_URL = 'ldap://localhost:389'
        self.LDAP_AUTH_URL = '10.254.10.10'

        # Specifies if the connection is on a secure port (defaults to False).
        # When True the secure port is usually set to 636.
        self.LDAP_AUTH_USE_SSL = False

        # Specifies authentication protocol Kerberos or NTLM
        self.LDAP_AUTH_PROTOCOL = 'Kerberos'

        # The domain string which is used for Kerberos: <user>@domain.com
        # or NTLM: domain\<user>
        #LDAP_AUTH_ACTIVE_DIRECTORY_DOMAIN = 'wellcome\\'
        self.LDAP_AUTH_ACTIVE_DIRECTORY_DOMAIN = '@my.wellcome.com'

        #The base of the search request
        self.LDAP_AUTH_SEARCH_BASE = 'OU=Users new,DC=MY,DC=WELLCOME,DC=COM'

        # The filter of the search request. It must conform to the LDAP filter
        # syntax specified in RFC4515.
        self.LDAP_AUTH_SEARCH_FILTER = 'sAMAccountName'

        # A single attribute or a list of attributes to be returned by the search.
        self.LDAP_AUTH_SEARCH_ATRIBUTES = ['cn', 'mail']

def print_warrning(param: str):
    print('LDAPException: Warrning - %s is missed in settings.py file. Default value from LDAPSettings class is used' % param)

ldap_settings = LDAPSettings()

try:
    from django.conf import settings
except Exception as err:
    print('LDAPException:', str(err))
else:
    try:
        if hasattr(settings, 'LDAP_AUTH_PROTOCOL'):
            ldap_settings.LDAP_AUTH_PROTOCOL = settings.LDAP_AUTH_PROTOCOL
    except Exception:
        print_warrning('LDAP_AUTH_PROTOCOL')

    try:
        if hasattr(settings, 'LDAP_AUTH_URL'):
            ldap_settings.LDAP_AUTH_URL = settings.LDAP_AUTH_URL
    except Exception:
        print_warrning('LDAP_AUTH_URL')

    try:
        if hasattr(settings, 'LDAP_AUTH_ACTIVE_DIRECTORY_DOMAIN'):
            ldap_settings.LDAP_AUTH_ACTIVE_DIRECTORY_DOMAIN = settings.LDAP_AUTH_ACTIVE_DIRECTORY_DOMAIN
    except Exception:
        print_warrning('LDAP_AUTH_ACTIVE_DIRECTORY_DOMAIN')

    try:
        if hasattr(settings, 'LDAP_AUTH_SEARCH_BASE'):
            ldap_settings.LDAP_AUTH_SEARCH_BASE = settings.LDAP_AUTH_SEARCH_BASE
    except Exception:
        print_warrning('LDAP_AUTH_SEARCH_BASE')

    try:
        if hasattr(settings, 'LDAP_AUTH_SEARCH_FILTER'):
            ldap_settings.LDAP_AUTH_SEARCH_FILTER = settings.LDAP_AUTH_SEARCH_FILTER
    except Exception:
        print_warrning('LDAP_AUTH_SEARCH_FILTER')

    try:
        if hasattr(settings, 'LDAP_AUTH_SEARCH_ATRIBUTES'):
            ldap_settings.LDAP_AUTH_SEARCH_ATRIBUTES = settings.LDAP_AUTH_SEARCH_ATRIBUTES
    except Exception:
        print_warrning('LDAP_AUTH_SEARCH_ATRIBUTES')

    try:
        if hasattr(settings, 'LDAP_AUTH_USE_SSL'):
            ldap_settings.LDAP_AUTH_USE_SSL = settings.LDAP_AUTH_USE_SSL
    except Exception:
        print_warrning('LDAP_AUTH_USE_SSL')
