from rest_framework import serializers
from .models import *

class ApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Application
        fields = '__all__'

class ContactMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactMessage
        fields = "__all__"

class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = '__all__'

class PlacementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Placement
        fields = '__all__'

class EdwinTalkSerializer(serializers.ModelSerializer):
    class Meta:
        model = EdwinTalk
        fields = '__all__'

class TestimonialSerializer(serializers.ModelSerializer):
    class Meta:
        model = Testimonial
        fields = '__all__'

class FacultySerializer(serializers.ModelSerializer):
    class Meta:
        model = Faculty
        fields = "__all__"

class PlacementPosterSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlacementPoster
        fields = "__all__"


class UGProgramSerializer(serializers.ModelSerializer):
    class Meta:
        model = UGProgram
        fields = '__all__'


class PGProgramSerializer(serializers.ModelSerializer):
    class Meta:
        model = PGProgram
        fields = '__all__'


class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = '__all__'


class GalleryItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = GalleryItem
        fields = '__all__'


class BlogSerializer(serializers.ModelSerializer):
    class Meta:
        model = Blog
        fields = '__all__'