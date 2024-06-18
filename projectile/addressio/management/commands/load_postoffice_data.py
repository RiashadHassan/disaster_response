import json
import os

from django.core.management import BaseCommand
from tqdm import tqdm

from addressio.models import Upazila, PostOffice


class Command(BaseCommand):
    help = "Save data into District"

    def handle(self, *args, **options):
        file_path = os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            "data/bangladesh-geojson-master/bd-postcodes.json",
        )

        with open(file_path, "r", encoding="utf-8") as f:
            base_data = json.load(f)

        self.stdout.write(self.style.SUCCESS(f"Creating Post Office ... "))
        not_found = []

        for data in tqdm(base_data["postcodes"]):
            try:
                upazila = Upazila.objects.get(name__iexact=data["upazila"])
            except Upazila.MultipleObjectsReturned:
                upazila = Upazila.objects.filter(name__iexact=data["upazila"]).first()
            except Upazila.DoesNotExist:
                upazila = None
                not_found.append(data["upazila"])
            if upazila:
                PostOffice.objects.create(
                    upazila=upazila,
                    district_id=data["district_id"],
                    division_id=data["division_id"],
                    name=data["postOffice"],
                    code=int(data["postCode"]),
                )

        self.stdout.write(
            self.style.SUCCESS(
                f"Successfully created post offices for Post Office model"
            )
        )
