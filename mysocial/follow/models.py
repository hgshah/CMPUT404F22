from django.core.exceptions import ValidationError
from django.db import models

from mysocial import settings


class Follow(models.Model):
    """
    actor follows target
    """
    FIELD_NAME_HAS_ACCEPTED = 'hasAccepted'

    actor = models.ForeignKey(settings.base.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='+')
    target = models.ForeignKey(settings.base.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='+')
    has_accepted = models.BooleanField(default=False)

    class Meta:
        unique_together = (('actor', 'target'),)
        get_latest_by = 'id'

    @staticmethod
    def get_serializer_field_name():
        return "Follow"

    def __str__(self):
        status = 'follows' if self.has_accepted else 'wants to follow'
        return f'{self.actor} {status} {self.target}'
