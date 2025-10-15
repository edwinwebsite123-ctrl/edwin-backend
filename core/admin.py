from django.contrib import admin
from .models import Application

class ApplicationAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'email', 'interested_course', 'course_mode', 'select_center', 'place')
    search_fields = ('first_name', 'last_name', 'email', 'interested_course', 'select_center')
    list_filter = ('course_mode', 'select_center')
    ordering = ('-id',)

admin.site.register(Application, ApplicationAdmin)
