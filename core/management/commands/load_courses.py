import json
from django.core.management.base import BaseCommand
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

    def handle(self, *args, **options):
        file_path = options['file']
        
        try:
            # Read and parse the properly formatted JSON file
            with open(file_path, 'r', encoding='utf-8') as file:
                courses_data = json.load(file)
            
            # Clear existing courses if requested
            if options['clear']:
                deleted_count = Course.objects.all().count()
                Course.objects.all().delete()
                self.stdout.write(
                    self.style.WARNING(f'Deleted {deleted_count} existing courses')
                )
            
            # Load/update courses
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
            
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error: {str(e)}'))
