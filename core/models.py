from django.db import models

class Application(models.Model):
    # Personal details
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    mobile_number = models.CharField(max_length=15) 
    place = models.CharField(max_length=200)
    
    interested_course = models.CharField(max_length=200)
    
    # Course mode (Online/Offline)
    course_mode_choices = [
        ('Online', 'Online'),
        ('Offline', 'Offline'),
    ]
    course_mode = models.CharField(max_length=10, choices=course_mode_choices, default='Offline')
    
    select_center = models.CharField(max_length=200)
    
    # Additional message (optional)
    additional_message = models.TextField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True) 
    updated_at = models.DateTimeField(auto_now=True) 
    
    def __str__(self):
        return f"Application from {self.first_name} {self.last_name}"
