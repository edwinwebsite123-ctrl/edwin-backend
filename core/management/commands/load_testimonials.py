import json
import os
from django.core.management.base import BaseCommand
from django.conf import settings
from core.models import Testimonial

class Command(BaseCommand):
    help = "Load testimonial data from JSON (handle images like EdwinTalk)"

    def handle(self, *args, **kwargs):
        json_path = os.path.join(settings.BASE_DIR, 'data', 'testimonials.json')

        if not os.path.exists(json_path):
            self.stdout.write(self.style.ERROR(f"❌ JSON file not found at {json_path}"))
            return

        with open(json_path, 'r', encoding='utf-8') as file:
            data = json.load(file)

        created_count = 0
        updated_count = 0

        for item in data:
            # Compute image path relative to MEDIA
            image_path = item.get("image")
            if image_path:
                # Remove any 'media/' prefix
                image_path = image_path.replace('media/', '')
            else:
                image_path = None

            testimonial, created = Testimonial.objects.update_or_create(
                name=item["name"],
                role=item["role"],
                defaults={
                    "text": item["text"],
                    "image": image_path  # Just store the path relative to MEDIA_ROOT
                }
            )

            if created:
                created_count += 1
                self.stdout.write(self.style.SUCCESS(f'✓ Created: {testimonial}'))
            else:
                updated_count += 1
                self.stdout.write(self.style.SUCCESS(f'↻ Updated: {testimonial}'))

        self.stdout.write(
            self.style.SUCCESS(
                f'\nSuccessfully loaded {created_count + updated_count} testimonials\n'
                f'Created: {created_count}\nUpdated: {updated_count}'
            )
        )
