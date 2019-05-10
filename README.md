# Django-LDAPBackend
My customized Django-LDAPBackend for users authentication in Active Directory

First of all it use django.contrib.admin and django.contrib.auth. You have to add this applications to your Django project and create users in admin page (your local DB). 

Firstly it is checked if the user exist in local DB. If user doesn't exixt in local DB the access will be denied. 

If user exists it checks if user is superuser. If user is superuser it is authenticated by local password. 
If user is not superuser LDAP query is performed to Active Directory (AD) and if authentication passes successfully acces is cratnted and first name, last name and email address copied from the user account in AD and stored in local DB as an additional information about the user.   

---

## How to use it
1. Copy ldap folder into your Django project directory
2. Change line 6 in ldap\ldap.py file 
```python
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "yourapp.settings")
```
replace **yourapp** with the name of your Django application. It is needed to use setting file from your application

3. Add following lines into your Django project settings.py 
```python
# Setup the AUTHENTICATION BACKEND
AUTHENTICATION_BACKENDS = ['ldap.auth.LDAPBackend']
```
4. You can set LDAPBackend configuration parameters by puting them directly into settings.py file 
```python
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
```
or by editing them in ldap\conf.py file
