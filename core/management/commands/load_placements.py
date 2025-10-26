import json
import os
from django.core.management.base import BaseCommand
from django.conf import settings
from core.models import Placement

class Command(BaseCommand):
    help = "Add placement data from JSON file"

    def handle(self, *args, **kwargs):
        json_path = os.path.join(settings.BASE_DIR, 'data', 'placements.json')

        if not os.path.exists(json_path):
            self.stdout.write(self.style.ERROR(f"❌ JSON file not found at {json_path}"))
            return

        with open(json_path, 'r', encoding='utf-8') as file:
            data = json.load(file)

        created_count = 0
        updated_count = 0

        for item in data:
            placement, created = Placement.objects.get_or_create(
                name=item["name"],
                role=item["role"],
                company=item["company"],
                defaults={
                    "company_logo": item["companyLogo"],  # camelCase from JSON
                    "student_image": item["studentImage"],
                    "background_image": item["backgroundImage"],
                },
            )

            # If already exists, update the fields
            if not created:
                placement.company_logo = item["companyLogo"]
                placement.student_image = item["studentImage"]
                placement.background_image = item["backgroundImage"]
                placement.save()
                updated_count += 1
                self.stdout.write(self.style.SUCCESS(f'↻ Updated: {placement}'))
            else:
                created_count += 1
                self.stdout.write(self.style.SUCCESS(f'✓ Created: {placement}'))

        self.stdout.write(
            self.style.SUCCESS(
                f'\nSuccessfully loaded {created_count + updated_count} placements\n'
                f'Created: {created_count}\nUpdated: {updated_count}'
            )
        )
