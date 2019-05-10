"""
My Django authentication backend.
"""
from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.models import User
#from django.conf import settings

from . import ldap

UserModel = get_user_model()

class LDAPBackend(ModelBackend):

    """
    An authentication backend that delegates to an LDAP Active Directory server.
    User models authenticated with LDAP are created on the fly.
    """

    def authenticate(self, request, username=None, password=None, **kwargs):
        if username is None:
            username = kwargs.get(UserModel.USERNAME_FIELD)
        try:
            user = UserModel._default_manager.get_by_natural_key(username)
        except UserModel.DoesNotExist:
            # Run the default password hasher once to reduce the timing
            # difference between an existing and a nonexistent user (#20760).
            UserModel().set_password(password)
            print('Exception: Login User \'%s\' does not exist in local DB' % username)
        else:
            if self.user_can_authenticate(user):
                if user.is_superuser:
                    if user.check_password(password):
                        print('Info: User \'%s\' has logged in as superuser' % username)
                        return user
                else:
                    print('Info: Performing LDAP authentication for user \'%s\'' % username)
                    # Connect to LDAP.
                    ldap_conn = ldap.LDAPConnection()
                    if ldap_conn.authenticate(username, password) == True:
                        search_data = ldap_conn.search()
                        ldap_conn.unbind()
                        #Update User profile
                        cn = search_data['entries'][0]['attributes']['cn'][0]
                        cn = cn.split()
                        user.first_name = cn[0]
                        user.last_name = cn[1]
                        user.email = search_data['entries'][0]['attributes']['mail'][0]
                        user.save()
                        print('Info: User \'%s\' has logged in via LDAP' % username)
                    return user

