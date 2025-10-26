import json
import os
from django.core.management.base import BaseCommand
from django.conf import settings
from core.models import Course


class Command(BaseCommand):
    help = 'Load courses from allCoursesData.json into the database'

    def add_arguments(self, parser):
        parser.add_argument(
            '--file',
            type=str,
            default='allCoursesData.json',
            help='Path to the JSON file (default: allCoursesData.json)'
        )
        parser.add_argument(
            '--clear',
            action='store_true',
            help='Clear all existing courses before loading'
        )

    def handle(self, *args, **kwargs):
        file_name = kwargs['file']
        clear_existing = kwargs['clear']
        file_path = os.path.join(settings.BASE_DIR, 'data', file_name)

        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                courses_data = json.load(file)

            if clear_existing:
                deleted_count = Course.objects.count()
                Course.objects.all().delete()
                self.stdout.write(
                    self.style.WARNING(f'Deleted {deleted_count} existing courses')
                )

            created_count = 0
            updated_count = 0

            for course_data in courses_data:
                course, created = Course.objects.update_or_create(
                    id=course_data['id'],
                    defaults={
                        'title': course_data.get('title', ''),
                        'short_description': course_data.get('shortDescription', ''),
                        'category': course_data.get('category', ''),
                        'duration': course_data.get('duration', ''),
                        'level': course_data.get('level', ''),
                        'mode': course_data.get('mode', ''),
                        'certification': course_data.get('certification', ''),
                        'image': course_data.get('image', ''),
                        'overview': course_data.get('overview', '').strip(),
                        'modules': course_data.get('modules', []),
                        'career_opportunities': course_data.get('careerOpportunities', []),
                        'tools': course_data.get('tools', []),
                        'highlights': course_data.get('highlights', []),
                    }
                )

                if created:
                    created_count += 1
                    self.stdout.write(self.style.SUCCESS(f'✓ Created: {course.title}'))
                else:
                    updated_count += 1
                    self.stdout.write(self.style.SUCCESS(f'↻ Updated: {course.title}'))

            self.stdout.write(
                self.style.SUCCESS(
                    f'\nSuccessfully loaded {created_count + updated_count} courses\n'
                    f'Created: {created_count}\nUpdated: {updated_count}'
                )
            )

        except FileNotFoundError:
            self.stdout.write(self.style.ERROR(f'File not found: {file_path}'))
        except json.JSONDecodeError as e:
            self.stdout.write(self.style.ERROR(f'Invalid JSON format: {str(e)}'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error: {str(e)}'))