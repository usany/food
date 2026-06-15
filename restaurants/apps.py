from django.apps import AppConfig
import os

class RestaurantsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'restaurants'

    def ready(self):
        # Prevent scheduler from running multiple times when auto-reloading
        if os.environ.get('RUN_MAIN', None) != 'true':
            from . import scheduler
            scheduler.start()
