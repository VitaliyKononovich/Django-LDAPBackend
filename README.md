# Django-LDAPBackend
My customized Django-LDAPBackend for users authentication in Active Directory


```python
# ------------------------------------------------------------------------------
# Setup the AUTHENTICATION BACKEND
AUTHENTICATION_BACKENDS = ['ldap.auth.LDAPBackend']

# LDAPBackend configuration parameters
# Name or IP or the complete url in the scheme://hostname:hostport format of the server
# Port and scheme (ldap or ldaps) defined here have precedence over the parameters
# LDAP_AUTH_PORT and LDAP_AUTH_USE_SSL
# LDAP_AUTH_URL = 'ldap://localhost:389'
LDAP_AUTH_URL = '10.254.10.10'

# The port where the DSA server is listening
# LDAP_AUTH_PORT = '389'

# Specifies if the connection is on a secure port (defaults to False).
# When True the secure port is usually set to 636.
LDAP_AUTH_USE_SSL = False

# Specifies authentication protocol Kerberos or NTLM
LDAP_AUTH_PROTOCOL = 'Kerberos'

# The domain string which is used for Kerberos: <user>@domain.com
# or NTLM: domain\<user>
# LDAP_AUTH_ACTIVE_DIRECTORY_DOMAIN = 'WELLCOME\\'
LDAP_AUTH_ACTIVE_DIRECTORY_DOMAIN = '@my.wellcome.com'

# The base of the search request
LDAP_AUTH_SEARCH_BASE = 'OU=Users new,DC=MY,DC=WELCOME,DC=COM'

# The filter of the search request. It must conform to the LDAP filter
# syntax specified in RFC4515.
LDAP_AUTH_SEARCH_FILTER = 'sAMAccountName'

# A single attribute or a list of attributes to be returned by the search.
LDAP_AUTH_SEARCH_ATRIBUTES = ['cn', 'mail']
# ------------------------------------------------------------------------------
```
