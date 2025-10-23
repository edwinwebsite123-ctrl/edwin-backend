from django.db import models

class Application(models.Model):
    # Personal details
    first_name = models.CharField(max_length=100, blank=True, null=True)
    last_name = models.CharField(max_length=100, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    mobile_number = models.CharField(max_length=15, blank=True, null=True) 
    place = models.CharField(max_length=200, blank=True, null=True)
    
    interested_course = models.CharField(max_length=200, blank=True, null=True)
    
    # Course mode (Online/Offline)
    course_mode_choices = [
        ('Online', 'Online'),
        ('Offline', 'Offline'),
    ]
    course_mode = models.CharField(max_length=10, choices=course_mode_choices, default='Offline', blank=True, null=True)
    
    select_center = models.CharField(max_length=200, blank=True, null=True)
    
    # Additional message (optional)
    additional_message = models.TextField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True) 
    updated_at = models.DateTimeField(auto_now=True) 
    
    def __str__(self):
        return f"Application from {self.first_name} {self.last_name}"


class ContactMessage(models.Model):
    name = models.CharField(max_length=100, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    subject = models.CharField(max_length=200, blank=True, null=True)
    message = models.TextField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.subject}"


class Course(models.Model):
    id = models.SlugField(primary_key=True, unique=True)
    title = models.CharField(max_length=255)
    short_description = models.TextField()
    category = models.CharField(max_length=255)
    duration = models.CharField(max_length=100)
    level = models.CharField(max_length=100)
    mode = models.CharField(max_length=100)
    certification = models.CharField(max_length=255)
    image = models.ImageField(upload_to='courses/', blank=True, null=True)
    overview = models.TextField()

    # JSON fields for nested data
    modules = models.JSONField(default=list, blank=True)
    career_opportunities = models.JSONField(default=list, blank=True)
    tools = models.JSONField(default=list, blank=True)
    highlights = models.JSONField(default=list, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Course"
        verbose_name_plural = "Courses"

    def __str__(self):
        return self.title
