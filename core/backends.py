from django.contrib.auth.models import User
from django.db.models import Q


class EmailOrUsernameBackend:
    def authenticate(self, request, username=None, password=None):
        try:
            user = User.objects.filter(Q(email=username)|Q(username=username)).distinct().first()
            if user and user.check_password(password):
                return user
        except User.DoesNotExist:
            return None
        return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
