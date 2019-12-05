import os

from django.db.utils import IntegrityError
from django.core.management import base, call_command
from django.conf import settings


class Command(base.BaseCommand):

    """
    This is a helper method that helps with loading of default data.
    """

    help = "Load authserver default data"

    def handle(self, *args, **options):
        data_files = os.path.join(
            settings.BASE_DIR, 'khro_app/regions/data/location_data.json')
        try:
            call_command('loaddata', data_files)
        except IntegrityError as ie:
            self.stderr.write(
                'Default data cannot be loaded. '
            )
            self.stderr.write(str(ie))
