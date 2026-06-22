import json

from django.core.management.base import BaseCommand, CommandError

from restaurants.d1 import D1Error, query_d1


class Command(BaseCommand):
    help = 'Run a SQL query against Cloudflare D1 using CFACCOUNTID, CFDBID/CFDATABASEID, and CFAPITOKEN/CFTOKEN.'

    def add_arguments(self, parser):
        parser.add_argument('sql')

    def handle(self, *args, **options):
        try:
            result = query_d1(options['sql'])
        except D1Error as exc:
            raise CommandError(str(exc)) from exc

        self.stdout.write(json.dumps(result, ensure_ascii=False, indent=2))
