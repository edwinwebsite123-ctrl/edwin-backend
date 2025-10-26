import json
import os
from django.core.management.base import BaseCommand
from django.conf import settings
from core.models import GalleryItem

class Command(BaseCommand):
    help = "Add Gallery data from JSON file"

    def handle(self, *args, **kwargs):
        json_path = os.path.join(settings.BASE_DIR, "data", "galleryData.json")

        if not os.path.exists(json_path):
            self.stdout.write(self.style.ERROR(f"❌ JSON file not found at {json_path}"))
            return

        with open(json_path, "r", encoding="utf-8") as file:
            data = json.load(file)

        created_count = 0
        updated_count = 0

        for category, items in data.items():
            for item in items:
                gallery_item, created = GalleryItem.objects.update_or_create(
                    title=item["title"],
                    category=category,
                    defaults={
                        "date": item["date"],
                        "image": item["src"],
                    },
                )

                if created:
                    created_count += 1
                    self.stdout.write(self.style.SUCCESS(f"Added: {gallery_item}"))
                else:
                    updated_count += 1
                    self.stdout.write(self.style.WARNING(f"Updated: {gallery_item}"))

        self.stdout.write(
            self.style.SUCCESS(
                f"\nSuccessfully processed {created_count + updated_count} gallery items\n"
                f"Created: {created_count}\nUpdated: {updated_count}"
            )
        )