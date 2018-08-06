from django.test import TestCase

from core.backends import *
from testing_data import USER_DATA, SUPERUSER_DATA


class BackendTestCase(TestCase):

    @classmethod
    def setUpClass(cls):
        super(BackendTestCase, cls).setUpClass()
        user, created = User.objects.get_or_create(username=SUPERUSER_DATA.get('username'),
                                                  email=SUPERUSER_DATA.get('email'),
                                                  is_superuser=1,
                                                  is_staff=1)
        if created:
            user.set_password(SUPERUSER_DATA.get(('password')))

    def test_user_login_auth(self):
        pass

