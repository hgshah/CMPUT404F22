from django.db.models.signals import post_save
from django.dispatch import receiver   
from authors.models.author import Author
from inbox.models import Inbox

@receiver(post_save, sender = Author)
def create_inbox(sender, instance, created, **kwargs):
    if created:
        inbox = Inbox.objects.create(author = instance)
        inbox.save()
