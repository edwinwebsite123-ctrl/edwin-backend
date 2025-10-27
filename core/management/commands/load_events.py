import json
import os
from django.core.management.base import BaseCommand
from django.conf import settings
from core.models import Event


class Command(BaseCommand):
    help = 'Load events from events.json into the database'

    def add_arguments(self, parser):
        parser.add_argument(
            '--file',
            type=str,
            default='events.json',
            help='Path to the JSON file (default: events.json)'
        )
        parser.add_argument(
            '--clear',
            action='store_true',
            help='Clear all existing events before loading'
        )

    def handle(self, *args, **kwargs):
        file_name = kwargs['file']
        clear_existing = kwargs['clear']
        file_path = os.path.join(settings.BASE_DIR, 'data', file_name)

        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                events_data = json.load(file)

            if clear_existing:
                deleted_count = Event.objects.count()
                Event.objects.all().delete()
                self.stdout.write(
                    self.style.WARNING(f'Deleted {deleted_count} existing events')
                )

            created_count = 0
            updated_count = 0

            for event_data in events_data:
                fields = event_data.get('fields', {})
                event, created = Event.objects.update_or_create(
                    pk=event_data['pk'],
                    defaults={
                        'title': fields.get('title', ''),
                        'description': fields.get('description', ''),
                        'date': fields.get('date'),
                        'location': fields.get('location', ''),
                        'phone_number': fields.get('phone_number', ''),
                        'registration_message': fields.get('registration_message', ''),
                        'is_active': fields.get('is_active', False),
                    }
                )

                if created:
                    created_count += 1
                    self.stdout.write(self.style.SUCCESS(f'✓ Created: {event.title}'))
                else:
                    updated_count += 1
                    self.stdout.write(self.style.SUCCESS(f'↻ Updated: {event.title}'))

            self.stdout.write(
                self.style.SUCCESS(
                    f'\nSuccessfully loaded {created_count + updated_count} events\n'
                    f'Created: {created_count}\nUpdated: {updated_count}'
                )
            )

        except FileNotFoundError:
            self.stdout.write(self.style.ERROR(f'File not found: {file_path}'))
        except json.JSONDecodeError as e:
            self.stdout.write(self.style.ERROR(f'Invalid JSON format: {str(e)}'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error: {str(e)}'))