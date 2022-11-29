from django.core.management.base import BaseCommand

from authors.models.author import Author
from follow.models import Follow


class Command(BaseCommand):
    help = 'Custom command for Socioecon that clears all entries that are related to testing'

    def handle(self, *args, **options):
        for db in ['default', 'mirror']:
            self.stdout.write(f'Clearing tests in {db}')
            # from https://docs.djangoproject.com/en/4.1/topics/db/multi-db/#using-managers-with-multiple-databases
            test_actor: Author = Author.objects.db_manager(db).get(username='actor')
            test_target: Author = Author.objects.db_manager(db).get(username='target')
            follows = Follow.objects.db_manager(db).filter(target__contains=test_actor.get_id())
            follows |= Follow.objects.db_manager(db).filter(actor__contains=test_actor.get_id())
            follows |= Follow.objects.db_manager(db).filter(target__contains=test_target.get_id())
            follows |= Follow.objects.db_manager(db).filter(actor__contains=test_target.get_id())

            for item in follows.distinct():
                item.delete()

        self.stdout.write('Clearing tests complete!')
