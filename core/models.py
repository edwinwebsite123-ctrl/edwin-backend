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
    title = models.CharField(max_length=255, blank=True, null=True)
    short_description = models.TextField(blank=True, null=True)
    category = models.CharField(max_length=255, blank=True, null=True)
    duration = models.CharField(max_length=100, blank=True, null=True)
    level = models.CharField(max_length=100, blank=True, null=True)
    mode = models.CharField(max_length=100, blank=True, null=True)
    certification = models.CharField(max_length=255, blank=True, null=True)
    image = models.ImageField(upload_to='courses/', blank=True, null=True)
    overview = models.TextField(blank=True, null=True)

    modules = models.JSONField(default=list, blank=True, null=True)
    career_opportunities = models.JSONField(default=list, blank=True, null=True)
    tools = models.JSONField(default=list, blank=True, null=True)
    highlights = models.JSONField(default=list, blank=True, null=True)

    top_choice = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Course"
        verbose_name_plural = "Courses"

    def __str__(self):
        return self.title or "Unnamed Course"


class Placement(models.Model):
    name = models.CharField(max_length=100, blank=True, null=True)
    role = models.CharField(max_length=100, blank=True, null=True)
    company = models.CharField(max_length=150, blank=True, null=True)
    company_logo = models.ImageField(upload_to='placements/', blank=True, null=True)
    student_image = models.ImageField(upload_to='placements/', blank=True, null=True)
    background_image = models.ImageField(upload_to='placements/', blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name or 'Unknown'} - {self.role or 'N/A'} at {self.company or 'N/A'}"


class EdwinTalk(models.Model):
    title = models.CharField(max_length=200, blank=True, null=True)
    image = models.ImageField(upload_to='edwintalks/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True) 
    updated_at = models.DateTimeField(auto_now=True) 

    def __str__(self):
        return self.title or "Untitled Talk"


class Testimonial(models.Model):
    text = models.TextField(blank=True, null=True)
    name = models.CharField(max_length=150, blank=True, null=True)
    role = models.CharField(max_length=100, blank=True, null=True)
    image = models.ImageField(upload_to='testimonials/', blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name or 'Unknown'} - {self.role or 'N/A'}"


class Faculty(models.Model):
    name = models.CharField(max_length=100, blank=True, null=True)
    title = models.CharField(max_length=200, blank=True, null=True)
    faculty_image = models.ImageField(upload_to='faculty/', blank=True, null=True)
    bg_image = models.ImageField(upload_to='faculty/backgrounds/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name or 'Unknown'} - {self.title or 'N/A'}"


class PlacementPoster(models.Model):
    image = models.ImageField(upload_to='placements/old/', blank=True, null=True)
    alt = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.alt or "Placement Poster"


class UGProgram(models.Model):
    code = models.CharField(max_length=20, blank=True, null=True)
    name = models.CharField(max_length=200, blank=True, null=True)
    subtitle = models.CharField(max_length=255, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    duration = models.CharField(max_length=50, blank=True, null=True)
    specializations = models.JSONField(blank=True, null=True)
    eligibility = models.CharField(max_length=255, blank=True, null=True)
    students = models.CharField(max_length=50, blank=True, null=True)
    modules = models.PositiveIntegerField(blank=True, null=True)
    rating = models.DecimalField(max_digits=3, decimal_places=1, blank=True, null=True)
    image = models.ImageField(upload_to='programs/ug/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name or 'UG Program'} ({self.code or 'N/A'})"


class PGProgram(models.Model):
    code = models.CharField(max_length=20, blank=True, null=True)
    name = models.CharField(max_length=200, blank=True, null=True)
    subtitle = models.CharField(max_length=255, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    duration = models.CharField(max_length=50, blank=True, null=True)
    specializations = models.JSONField(blank=True, null=True)
    eligibility = models.CharField(max_length=255, blank=True, null=True)
    students = models.CharField(max_length=50, blank=True, null=True)
    modules = models.PositiveIntegerField(blank=True, null=True)
    rating = models.DecimalField(max_digits=3, decimal_places=1, blank=True, null=True)
    image = models.ImageField(upload_to='programs/pg/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name or 'PG Program'} ({self.code or 'N/A'})"
    
class GalleryItem(models.Model):
    CATEGORY_CHOICES = [
        ('programs', 'Programs'),
        ('events', 'Events'),
        ('convocations', 'Convocations'),
        ('achievements', 'Achievements'),
    ]

    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, null=True, blank=True)
    title = models.CharField(max_length=255, null=True, blank=True)
    date = models.CharField(max_length=50, null=True, blank=True)
    image = models.ImageField(upload_to='gallery/', null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title} ({self.category})" if self.title else "Unnamed Gallery Item"
