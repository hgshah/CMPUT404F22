from django.db import models


class NodeStatus(models.TextChoices):
    """Yeah I know I could use a bool but you might now know lol"""
    ACTIVE = "active"
    INACTIVE = "inactive"


class RemoteNode(models.Model):
    """
    Details we will use to communicate with the other team
    """
    remote_username = models.CharField(max_length=100)
    remote_password = models.CharField(max_length=100)
    status = models.CharField(choices=NodeStatus.choices, default=NodeStatus.ACTIVE, max_length=30)
