import json
import os
from django.core.management.base import BaseCommand
from django.conf import settings
from core.models import PlacementPoster

class Command(BaseCommand):
    help = "Add placement poster data from JSON file"

    def handle(self, *args, **kwargs):
        json_path = os.path.join(settings.BASE_DIR, 'data', 'placementPosters.json')

        if not os.path.exists(json_path):
            self.stdout.write(self.style.ERROR(f"JSON file not found at {json_path}"))
            return

        with open(json_path, 'r', encoding='utf-8') as file:
            data = json.load(file)

        created_count = 0
        updated_count = 0

        for item in data:
            poster, created = PlacementPoster.objects.update_or_create(
                id=item["id"],
                defaults={
                    "image": item["image"],
                    "alt": item["alt"],
                }
            )
            if created:
                created_count += 1
                self.stdout.write(self.style.SUCCESS(f"Added: {poster.alt}"))
            else:
                updated_count += 1
                self.stdout.write(self.style.WARNING(f"Updated: {poster.alt}"))

        self.stdout.write(
            self.style.SUCCESS(
                f"\nCompleted: {created_count} created, {updated_count} updated\n"
            )
        )
