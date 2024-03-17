from django.core.management.base import BaseCommand

from common.utils import setup_countries


class Command(BaseCommand):
    def handle(self, *args, **options):
        setup_countries()
