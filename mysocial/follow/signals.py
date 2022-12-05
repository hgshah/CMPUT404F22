from django.db.models.signals import post_delete, pre_save
from django.dispatch import receiver

from follow.models import Follow
from mysocial.settings import base
from remote_nodes.team12_local import Team12Local


@receiver(pre_save, sender=Follow)
def on_change(sender, instance: Follow, **kwargs):
    # from https://stackoverflow.com/a/54653160/17836168
    if instance.id is None:  # new object will be created
        pass  # write your code here
    else:
        try:
            previous = Follow.objects.get(id=instance.id)
            if previous.has_accepted != instance.has_accepted and not previous.has_accepted:
                host = instance.get_author_actor().host
                node_config: Team12Local = base.REMOTE_CONFIG.get(host)
                if node_config is not None and node_config.team_metadata_tag == 'team12':
                    node_config.team12_accept(instance.get_author_actor(), instance.get_author_target())
        except Exception:
            pass  # it's fine lol


@receiver(post_delete, sender=Follow)
def on_delete(sender, instance: Follow, **kwargs):
    # from https://stackoverflow.com/a/54653160/17836168
    actor_host = instance.get_author_actor().host
    node_config: Team12Local = base.REMOTE_CONFIG.get(actor_host)
    if node_config is not None and node_config.team_metadata_tag == 'team12':
        node_config.team12_unfollow(instance.get_author_actor(), instance.get_author_target())
        node_config.team12_reject(instance.get_author_actor(), instance.get_author_target())

    target_host = instance.get_author_target().host
    node_config: Team12Local = base.REMOTE_CONFIG.get(target_host)
    if node_config is not None and node_config.team_metadata_tag == 'team12':
        node_config.team12_reject(instance.get_author_actor(), instance.get_author_target())
