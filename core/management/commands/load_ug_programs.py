import json
import os
from django.core.management.base import BaseCommand
from django.conf import settings
from core.models import UGProgram

class Command(BaseCommand):
    help = "Load UG Programs from JSON file"

    def handle(self, *args, **kwargs):
        json_path = os.path.join(settings.BASE_DIR, 'data', 'ugPrograms.json')
        if not os.path.exists(json_path):
            self.stdout.write(self.style.ERROR(f"File not found: {json_path}"))
            return

        with open(json_path, 'r', encoding='utf-8') as file:
            data = json.load(file)

        created_count, skipped_count = 0, 0

        for item in data:
            program, created = UGProgram.objects.get_or_create(
                code=item["code"],
                defaults={
                    "name": item["name"],
                    "subtitle": item["subtitle"],
                    "description": item["description"],
                    "duration": item["duration"],
                    "specializations": item["specializations"],
                    "eligibility": item["eligibility"],
                    "students": item["students"],
                    "modules": item["modules"],
                    "rating": item["rating"],
                    "image": item["image"],
                }
            )
            if created:
                created_count += 1
            else:
                skipped_count += 1

        self.stdout.write(self.style.SUCCESS(f"UG Programs loaded successfully"))
        self.stdout.write(f"Created: {created_count} | Skipped: {skipped_count}")
