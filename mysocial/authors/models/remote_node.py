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

    # prevent circular dependency
    author_class = None

    def author_name(self) -> str:
        try:
            author = RemoteNode.author_class.objects.get(node_detail=self.id)
            return str(author)
        except Exception:
            return "Invalid node!"

    def author_id(self) -> str:
        try:
            author = RemoteNode.author_class.objects.get(node_detail=self.id)
            return author.get_id()
        except Exception:
            return "Invalid node!"