import json
import os
from django.core.management.base import BaseCommand
from django.conf import settings
from django.utils.dateparse import parse_datetime
from core.models import EdwinTalk

class Command(BaseCommand):
    help = "Add EdwinTalk data from JSON file (with optional created_at and updated_at)"

    def handle(self, *args, **kwargs):
        json_path = os.path.join(settings.BASE_DIR, 'data', 'edwintalks.json')

        if not os.path.exists(json_path):
            self.stdout.write(self.style.ERROR(f"❌ JSON file not found at {json_path}"))
            return

        with open(json_path, 'r', encoding='utf-8') as file:
            data = json.load(file)

        created_count = 0
        updated_count = 0

        for item in data:
            created_at = parse_datetime(item.get("created_at")) if item.get("created_at") else None
            updated_at = parse_datetime(item.get("updated_at")) if item.get("updated_at") else None

            talk, created = EdwinTalk.objects.get_or_create(
                title=item["title"],
                defaults={
                    "image": item["image"],
                    "created_at": created_at,
                    "updated_at": updated_at
                }
            )

            if created:
                created_count += 1
                self.stdout.write(self.style.SUCCESS(f"Added: {talk}"))
            else:
                updated_count += 1
                self.stdout.write(self.style.WARNING(f"Already exists: {talk}"))

        self.stdout.write(
            self.style.SUCCESS(
                f"\nSuccessfully loaded EdwinTalks\nCreated: {created_count}\nAlready existed: {updated_count}"
            )
        )
