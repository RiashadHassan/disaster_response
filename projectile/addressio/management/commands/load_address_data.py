from django.core.management import BaseCommand, call_command
from django.db import transaction


class Command(BaseCommand):
    help = "address data"

    def handle(self, *args, **options):
        with transaction.atomic():
            self.stdout.write("Loading address data")

            call_command("load_division_data")
            call_command("load_district_data")
            call_command("load_upazila_data")
            call_command("load_postoffice_data")

            self.stdout.write("All addresses created successfully")
