import json
import os
from django.core.management.base import BaseCommand
from django.conf import settings
from core.models import Faculty

class Command(BaseCommand):
    help = "Add Faculty data from JSON file"

    def handle(self, *args, **kwargs):
        json_path = os.path.join(settings.BASE_DIR, "data", "faculty.json")

        if not os.path.exists(json_path):
            self.stdout.write(self.style.ERROR(f"❌ JSON file not found at {json_path}"))
            return

        with open(json_path, "r", encoding="utf-8") as file:
            data = json.load(file)

        created_count = 0
        updated_count = 0

        for item in data:
            faculty, created = Faculty.objects.update_or_create(
                name=item["name"],
                defaults={
                    "title": item["title"],
                    "faculty_image": item["faculty_image"],
                    "bg_image": item["bg_image"],
                },
            )

            if created:
                created_count += 1
                self.stdout.write(self.style.SUCCESS(f"Added: {faculty}"))
            else:
                updated_count += 1
                self.stdout.write(self.style.WARNING(f"Updated: {faculty}"))

        self.stdout.write(
            self.style.SUCCESS(
                f"\nSuccessfully processed {created_count + updated_count} faculty members\n"
                f"Created: {created_count}\nUpdated: {updated_count}"
            )
        )
