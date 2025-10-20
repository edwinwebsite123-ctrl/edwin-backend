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
