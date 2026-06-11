from django.core.management.base import BaseCommand
from restaurants.models import MenuItem
from restaurants.views import FIXED_MENU


class Command(BaseCommand):
    help = 'Seed the database with fixed menu items from FIXED_MENU in views.py'

    def handle(self, *args, **options):
        created_count = 0
        updated_count = 0

        for place, items in FIXED_MENU.items():
            for item in items:
                for meal in item.get('time_category', []):
                    item_id = f"{item['id']}-{place}"

                    defaults = {
                        'main': item['main'],
                        'enmain': item.get('enmain', ''),
                        'side': item.get('side') or '',
                        'enside': item.get('enside') or '',
                        'place': place,
                        'meal': meal,
                        'day': item.get('day') or '',
                        'price': str(item.get('price', '')),
                        'extra': item.get('extra') or '',
                        'enextra': item.get('enextra') or '',
                        'date': '',
                        'stamp': item.get('stamp', False),
                    }

                    obj, created = MenuItem.objects.update_or_create(
                        id=item_id,
                        defaults=defaults,
                    )

                    if created:
                        created_count += 1
                    else:
                        updated_count += 1

        self.stdout.write(self.style.SUCCESS(
            f'Done. Created {created_count}, updated {updated_count} fixed menu items.'
        ))
