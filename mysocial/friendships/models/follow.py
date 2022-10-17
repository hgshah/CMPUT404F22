from django.db import models

from mysocial import settings


class Follow(models.Model):
    """
    actor follows target
    """
    actor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='+')
    target = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='+')
    is_pending = models.BooleanField(default=True)

    @staticmethod
    def get_serializer_field_name():
        return "follow"

    def __str__(self):
        status = "wants to follow" if self.is_pending else "follows"
        return f"{self.actor} {status} {self.target}"


