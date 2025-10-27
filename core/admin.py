from django.contrib import admin
from .models import Application, ContactMessage, Course, Placement, EdwinTalk, Testimonial, Faculty, PlacementPoster, UGProgram, PGProgram, Event, GalleryItem

class ApplicationAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'email', 'interested_course', 'course_mode', 'select_center', 'place')
    search_fields = ('first_name', 'last_name', 'email', 'interested_course', 'select_center')
    list_filter = ('course_mode', 'select_center')
    ordering = ('-id',)

admin.site.register(Application, ApplicationAdmin)

@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "phone", "subject", "created_at")
    search_fields = ("name", "email", "subject")
    list_filter = ("created_at",)

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'level', 'mode', 'duration', 'top_choice', 'created_at')
    search_fields = ('title', 'category', 'level')
    list_filter = ('category', 'level', 'mode', 'top_choice', 'created_at')

@admin.register(Placement)
class PlacementAdmin(admin.ModelAdmin):
    list_display = ('name', 'role', 'company', 'created_at')
    search_fields = ('name', 'role', 'company')
    list_filter = ('company', 'created_at')

@admin.register(EdwinTalk)
class EdwinTalkAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at', 'updated_at')
    search_fields = ('title',)
    list_filter = ('created_at', 'updated_at')

@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ('name', 'role', 'created_at')
    search_fields = ('name', 'role')
    list_filter = ('created_at',)

@admin.register(Faculty)
class FacultyAdmin(admin.ModelAdmin):
    list_display = ('name', 'title', 'created_at')
    search_fields = ('name', 'title')
    list_filter = ('created_at',)

@admin.register(PlacementPoster)
class PlacementPosterAdmin(admin.ModelAdmin):
    list_display = ('alt', 'created_at')
    search_fields = ('alt',)
    list_filter = ('created_at',)

@admin.register(UGProgram)
class UGProgramAdmin(admin.ModelAdmin):
    list_display = ('code', 'name', 'duration', 'rating', 'created_at')
    search_fields = ('code', 'name')
    list_filter = ('duration', 'rating', 'created_at')

@admin.register(PGProgram)
class PGProgramAdmin(admin.ModelAdmin):
    list_display = ('code', 'name', 'duration', 'rating', 'created_at')
    search_fields = ('code', 'name')
    list_filter = ('duration', 'rating', 'created_at')

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('title', 'date', 'location', 'is_active', 'created_at')
    search_fields = ('title', 'location')
    list_filter = ('date', 'is_active', 'created_at')

@admin.register(GalleryItem)
class GalleryItemAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'date', 'created_at')
    search_fields = ('title', 'category')
    list_filter = ('category', 'created_at')
