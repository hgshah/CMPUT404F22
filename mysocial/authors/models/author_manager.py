import logging

from django.contrib.auth.base_user import BaseUserManager

logger = logging.getLogger(__name__)


class AuthorManager(BaseUserManager):
    """
    from https://simpleisbetterthancomplex.com/tutorial/2016/07/22/how-to-extend-django-user-model.html
    """

    def _helper_create_user(self, email: str, password: str, **kwargs):
        email = self.normalize_email(email)
        try:
            kwargs['host'] = kwargs['host'].rstrip('/')
            user = self.model(email=email, password=password, **kwargs)
            user.set_password(password)  # encrypts the password
            user.save()
            return user
        except Exception as e:
            logger.info(e)
            return None

    def create_user(self, email: str, password: str, **kwargs):
        for key in ("is_staff", "is_superuser"):
            if key in kwargs:
                kwargs.pop(key)

        return self._helper_create_user(email=email, password=password, **kwargs)

    def create_superuser(self, email: str, password: str, **kwargs):
        for key in ("is_staff", "is_superuser"):
            kwargs[key] = True

        return self._helper_create_user(email=email, password=password, **kwargs)
