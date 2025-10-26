import json
import os
from django.core.management.base import BaseCommand
from django.conf import settings
from core.models import PGProgram


class Command(BaseCommand):
    help = "Load PG Programs from JSON file"

    def handle(self, *args, **kwargs):
        json_path = os.path.join(settings.BASE_DIR, 'data', 'pgPrograms.json')

        if not os.path.exists(json_path):
            self.stdout.write(self.style.ERROR(f"JSON file not found at {json_path}"))
            return

        with open(json_path, 'r', encoding='utf-8') as file:
            data = json.load(file)

        created_count, skipped_count = 0, 0

        for item in data:
            program, created = PGProgram.objects.get_or_create(
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
                self.stdout.write(self.style.SUCCESS(f"Added: {program.name}"))
            else:
                skipped_count += 1
                self.stdout.write(self.style.WARNING(f"Already exists: {program.name}"))

        self.stdout.write(
            self.style.SUCCESS(
                f"\n🎉 Successfully processed PG Programs\nCreated: {created_count} | Skipped: {skipped_count}\n"
            )
        )
