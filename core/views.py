from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework import status
from django.contrib.auth.models import User
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from .serializers import *
from .models import *
from rest_framework import generics

class LoginView(APIView):
    def post(self, request):
        # Get username and password from the request
        username = request.data.get('username')
        password = request.data.get('password')

        try:
            user = User.objects.get(username=username)
            if user.check_password(password):
                token, created = Token.objects.get_or_create(user=user)
                return Response({
                    'token': token.key,
                    'user': {
                        'username': user.username,
                        'is_superuser': user.is_superuser
                    }
                }, status=status.HTTP_200_OK)
            else:
                return Response({'detail': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
        except User.DoesNotExist:
            return Response({'detail': 'Invalid credentials'}, status=status.HTTP_404_NOT_FOUND)
        
class LogoutView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        # Get the user from the request and delete the token
        request.user.auth_token.delete()
        return Response({'detail': 'Logged out successfully'}, status=status.HTTP_200_OK)


class VerifyTokenView(APIView):
    """
    Verify if the token is valid.
    Frontend sends the token in Authorization header: "Token <token>"
    """
    def get(self, request):
        auth_header = request.headers.get("Authorization")
        if not auth_header or not auth_header.startswith("Token "):
            return Response({"detail": "Token not provided."}, status=status.HTTP_401_UNAUTHORIZED)

        token_key = auth_header.split()[1]

        try:
            token = Token.objects.get(key=token_key)
            user = token.user
            # Return some user info if needed
            return Response({
                "detail": "Token is valid",
                "username": user.username,
                "is_superuser": user.is_superuser
            }, status=status.HTTP_200_OK)
        except Token.DoesNotExist:
            return Response({"detail": "Invalid token."}, status=status.HTTP_401_UNAUTHORIZED)
        
    
# List all applications (GET) - requires authentication
class ApplicationListView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        applications = Application.objects.all().order_by('-created_at')
        serializer = ApplicationSerializer(applications, many=True)
        return Response(serializer.data)

# Retrieve or delete a specific application (GET, DELETE)
class ApplicationDetailView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        try:
            application = Application.objects.get(pk=pk)
            serializer = ApplicationSerializer(application)
            return Response(serializer.data)
        except Application.DoesNotExist:
            return Response({'detail': 'Not found.'}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, pk):
        try:
            application = Application.objects.get(pk=pk)
            application.delete()
            return Response({'detail': 'Application deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
        except Application.DoesNotExist:
            return Response({'detail': 'Not found.'}, status=status.HTTP_404_NOT_FOUND)

# Create a new application (POST)
class ApplicationCreateView(APIView):
    def post(self, request):
        serializer = ApplicationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DashboardCountsView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        total_applications = Application.objects.count()
        total_contacts = ContactMessage.objects.count()

        data = {
            'total_applications': total_applications,
            'total_contacts': total_contacts,
        }
        return Response(data, status=status.HTTP_200_OK)

class RecentLeadsView(APIView):
    def get(self, request):
        # Fetch the last 3 leads ordered by 'created_at' (most recent first)
        recent_leads = Application.objects.all().order_by('-created_at')[:4]
        serializer = ApplicationSerializer(recent_leads, many=True)
        return Response(serializer.data)
    
class ContactMessageCreateView(generics.CreateAPIView):
    queryset = ContactMessage.objects.all()
    serializer_class = ContactMessageSerializer

class ContactMessageListView(generics.ListAPIView):
    queryset = ContactMessage.objects.all().order_by("-created_at")
    serializer_class = ContactMessageSerializer

class RecentContactMessageListView(generics.ListAPIView):
    queryset = ContactMessage.objects.all().order_by("-created_at")[:3]
    serializer_class = ContactMessageSerializer

class ContactMessageDeleteView(generics.DestroyAPIView):
    queryset = ContactMessage.objects.all()
    serializer_class = ContactMessageSerializer


# Course API Views
class CourseListView(APIView):
    """
    GET: Public access - List all courses
    """
    def get(self, request):
        courses = Course.objects.all().order_by('-created_at')
        serializer = CourseSerializer(courses, many=True)
        return Response(serializer.data)

class TopChoiceCourseListAPIView(APIView):
    def get(self, request):
        courses = Course.objects.filter(top_choice=True).order_by('-created_at')
        serializer = CourseSerializer(courses, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class ToggleTopChoiceView(APIView):
    """
    Toggle the top_choice status of a course
    """
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, id):
        try:
            course = Course.objects.get(id=id)
            course.top_choice = not course.top_choice  # toggle the boolean
            course.save()
            serializer = CourseSerializer(course)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Course.DoesNotExist:
            return Response({"detail": "Course not found"}, status=status.HTTP_404_NOT_FOUND)


class CourseDetailView(APIView):
    """
    GET: Public access - Retrieve a specific course by id
    """
    def get(self, request, id):
        try:
            course = Course.objects.get(id=id)
            serializer = CourseSerializer(course)
            return Response(serializer.data)
        except Course.DoesNotExist:
            return Response({'detail': 'Course not found.'}, status=status.HTTP_404_NOT_FOUND)


class CourseCreateView(APIView):
    """
    POST: Requires authentication - Create a new course
    """
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = CourseSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CourseUpdateView(APIView):
    """
    PUT/PATCH: Requires authentication - Update an existing course
    """
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def put(self, request, id):
        try:
            course = Course.objects.get(id=id)
            serializer = CourseSerializer(course, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Course.DoesNotExist:
            return Response({'detail': 'Course not found.'}, status=status.HTTP_404_NOT_FOUND)

    def patch(self, request, id):
        try:
            course = Course.objects.get(id=id)
            serializer = CourseSerializer(course, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Course.DoesNotExist:
            return Response({'detail': 'Course not found.'}, status=status.HTTP_404_NOT_FOUND)


class CourseDeleteView(APIView):
    """
    DELETE: Requires authentication - Delete a course
    """
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def delete(self, request, id):
        try:
            course = Course.objects.get(id=id)
            course.delete()
            return Response({'detail': 'Course deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
        except Course.DoesNotExist:
            return Response({'detail': 'Course not found.'}, status=status.HTTP_404_NOT_FOUND)


# Placement API Views
class PlacementListView(APIView):
    """
    GET: Public access - List all Placements
    """
    def get(self, request):
        placements = Placement.objects.all().order_by('-created_at')
        serializer = PlacementSerializer(placements, many=True)
        return Response(serializer.data)


class PlacementDetailView(APIView):
    """
    GET: Public access - Retrieve a specific Placement by id
    """
    def get(self, request, id):
        try:
            placement = Placement.objects.get(id=id)
            serializer = PlacementSerializer(placement)
            return Response(serializer.data)
        except Placement.DoesNotExist:
            return Response({'detail': 'Placement not found.'}, status=status.HTTP_404_NOT_FOUND)


class PlacementCreateView(APIView):
    """
    POST: Requires authentication - Create a new Placement
    """
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = PlacementSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PlacementUpdateView(APIView):
    """
    PUT/PATCH: Requires authentication - Update an existing Placement
    """
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def put(self, request, id):
        try:
            placement = Placement.objects.get(id=id)
        except Placement.DoesNotExist:
            return Response({'detail': 'Placement not found.'}, status=status.HTTP_404_NOT_FOUND)

        serializer = PlacementSerializer(placement, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, id):
        try:
            placement = Placement.objects.get(id=id)
        except Placement.DoesNotExist:
            return Response({'detail': 'Placement not found.'}, status=status.HTTP_404_NOT_FOUND)

        serializer = PlacementSerializer(placement, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PlacementDeleteView(APIView):
    """
    DELETE: Requires authentication - Delete a Placement
    """
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def delete(self, request, id):
        try:
            placement = Placement.objects.get(id=id)
            placement.delete()
            return Response({'detail': 'Placement deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
        except Placement.DoesNotExist:
            return Response({'detail': 'Placement not found.'}, status=status.HTTP_404_NOT_FOUND)
        
# List all talks
class EdwinTalkListView(APIView):
    def get(self, request):
        talks = EdwinTalk.objects.all().order_by('-id')
        serializer = EdwinTalkSerializer(talks, many=True)
        return Response(serializer.data)


# Retrieve a single talk
class EdwinTalkDetailView(APIView):
    def get(self, request, id):
        try:
            talk = EdwinTalk.objects.get(id=id)
            serializer = EdwinTalkSerializer(talk)
            return Response(serializer.data)
        except EdwinTalk.DoesNotExist:
            return Response({'detail': 'Talk not found'}, status=status.HTTP_404_NOT_FOUND)


# Create a talk (auth required)
class EdwinTalkCreateView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = EdwinTalkSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Update talk
class EdwinTalkUpdateView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def put(self, request, id):
        try:
            talk = EdwinTalk.objects.get(id=id)
        except EdwinTalk.DoesNotExist:
            return Response({'detail': 'Talk not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = EdwinTalkSerializer(talk, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Delete talk
class EdwinTalkDeleteView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def delete(self, request, id):
        try:
            talk = EdwinTalk.objects.get(id=id)
            talk.delete()
            return Response({'detail': 'Talk deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
        except EdwinTalk.DoesNotExist:
            return Response({'detail': 'Talk not found'}, status=status.HTTP_404_NOT_FOUND)
        


# List all testimonials
class TestimonialListAPIView(APIView):
    def get(self, request):
        testimonials = Testimonial.objects.all().order_by('-id')
        serializer = TestimonialSerializer(testimonials, many=True)
        return Response(serializer.data)

# Retrieve a single testimonial
class TestimonialDetailAPIView(APIView):
    def get(self, request, id):
        try:
            testimonial = Testimonial.objects.get(id=id)
            serializer = TestimonialSerializer(testimonial)
            return Response(serializer.data)
        except Testimonial.DoesNotExist:
            return Response({'detail': 'Testimonial not found'}, status=status.HTTP_404_NOT_FOUND)

# Create a testimonial (auth required)
class TestimonialCreateAPIView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = TestimonialSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Update testimonial (auth required)
class TestimonialUpdateAPIView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def put(self, request, id):
        try:
            testimonial = Testimonial.objects.get(id=id)
        except Testimonial.DoesNotExist:
            return Response({'detail': 'Testimonial not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = TestimonialSerializer(testimonial, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Delete testimonial (auth required)
class TestimonialDeleteAPIView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def delete(self, request, id):
        try:
            testimonial = Testimonial.objects.get(id=id)
            testimonial.delete()
            return Response({'detail': 'Testimonial deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
        except Testimonial.DoesNotExist:
            return Response({'detail': 'Testimonial not found'}, status=status.HTTP_404_NOT_FOUND)
        

# List all Faculty
class FacultyListAPIView(APIView):
    def get(self, request):
        faculties = Faculty.objects.all().order_by("-id")
        serializer = FacultySerializer(faculties, many=True)
        return Response(serializer.data)


# Retrieve a single Faculty
class FacultyDetailAPIView(APIView):
    def get(self, request, id):
        try:
            faculty = Faculty.objects.get(id=id)
            serializer = FacultySerializer(faculty)
            return Response(serializer.data)
        except Faculty.DoesNotExist:
            return Response({"detail": "Faculty not found"}, status=status.HTTP_404_NOT_FOUND)


# Create a Faculty (auth required)
class FacultyCreateAPIView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = FacultySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Update Faculty (auth required)
class FacultyUpdateAPIView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def put(self, request, id):
        try:
            faculty = Faculty.objects.get(id=id)
        except Faculty.DoesNotExist:
            return Response({"detail": "Faculty not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = FacultySerializer(faculty, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Delete Faculty (auth required)
class FacultyDeleteAPIView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def delete(self, request, id):
        try:
            faculty = Faculty.objects.get(id=id)
            faculty.delete()
            return Response({"detail": "Faculty deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
        except Faculty.DoesNotExist:
            return Response({"detail": "Faculty not found"}, status=status.HTTP_404_NOT_FOUND)
        

# List all Posters
class PlacementPosterListAPIView(APIView):
    def get(self, request):
        posters = PlacementPoster.objects.all().order_by("-id")
        serializer = PlacementPosterSerializer(posters, many=True)
        return Response(serializer.data)


# Retrieve a single Poster
class PlacementPosterDetailAPIView(APIView):
    def get(self, request, id):
        try:
            poster = PlacementPoster.objects.get(id=id)
            serializer = PlacementPosterSerializer(poster)
            return Response(serializer.data)
        except PlacementPoster.DoesNotExist:
            return Response({'detail': 'Poster not found'}, status=status.HTTP_404_NOT_FOUND)


# Create Poster (auth required)
class PlacementPosterCreateAPIView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = PlacementPosterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Update Poster (auth required)
class PlacementPosterUpdateAPIView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def put(self, request, id):
        try:
            poster = PlacementPoster.objects.get(id=id)
        except PlacementPoster.DoesNotExist:
            return Response({'detail': 'Poster not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = PlacementPosterSerializer(poster, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Delete Poster (auth required)
class PlacementPosterDeleteAPIView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def delete(self, request, id):
        try:
            poster = PlacementPoster.objects.get(id=id)
            poster.delete()
            return Response({'detail': 'Poster deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
        except PlacementPoster.DoesNotExist:
            return Response({'detail': 'Poster not found'}, status=status.HTTP_404_NOT_FOUND)
        


# ---------- UG ----------
class UGProgramListAPIView(APIView):
    def get(self, request):
        programs = UGProgram.objects.all().order_by('-id')
        serializer = UGProgramSerializer(programs, many=True)
        return Response(serializer.data)


class UGProgramDetailAPIView(APIView):
    def get(self, request, id):
        try:
            program = UGProgram.objects.get(id=id)
            serializer = UGProgramSerializer(program)
            return Response(serializer.data)
        except UGProgram.DoesNotExist:
            return Response({'detail': 'UG Program not found'}, status=status.HTTP_404_NOT_FOUND)


class UGProgramCreateAPIView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = UGProgramSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UGProgramUpdateAPIView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def put(self, request, id):
        try:
            program = UGProgram.objects.get(id=id)
        except UGProgram.DoesNotExist:
            return Response({'detail': 'UG Program not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = UGProgramSerializer(program, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UGProgramDeleteAPIView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def delete(self, request, id):
        try:
            program = UGProgram.objects.get(id=id)
            program.delete()
            return Response({'detail': 'UG Program deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
        except UGProgram.DoesNotExist:
            return Response({'detail': 'UG Program not found'}, status=status.HTTP_404_NOT_FOUND)


# ---------- PG ----------
class PGProgramListAPIView(APIView):
    def get(self, request):
        programs = PGProgram.objects.all().order_by('-id')
        serializer = PGProgramSerializer(programs, many=True)
        return Response(serializer.data)


class PGProgramDetailAPIView(APIView):
    def get(self, request, id):
        try:
            program = PGProgram.objects.get(id=id)
            serializer = PGProgramSerializer(program)
            return Response(serializer.data)
        except PGProgram.DoesNotExist:
            return Response({'detail': 'PG Program not found'}, status=status.HTTP_404_NOT_FOUND)


class PGProgramCreateAPIView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = PGProgramSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PGProgramUpdateAPIView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def put(self, request, id):
        try:
            program = PGProgram.objects.get(id=id)
        except PGProgram.DoesNotExist:
            return Response({'detail': 'PG Program not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = PGProgramSerializer(program, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PGProgramDeleteAPIView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def delete(self, request, id):
        try:
            program = PGProgram.objects.get(id=id)
            program.delete()
            return Response({'detail': 'PG Program deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
        except PGProgram.DoesNotExist:
            return Response({'detail': 'PG Program not found'}, status=status.HTTP_404_NOT_FOUND)



# ---------- Gallery ----------
class GalleryItemListAPIView(APIView):
    def get(self, request):
        gallery_items = GalleryItem.objects.all().order_by('-id')
        serializer = GalleryItemSerializer(gallery_items, many=True)
        return Response(serializer.data)
    
class GalleryItemListTwoAPIView(APIView):
    def get(self, request):
        gallery_items = GalleryItem.objects.all().order_by('id')
        response_data = {
            "programs": [],
            "events": [],
            "convocations": [],
            "achievements": []
        }

        for item in gallery_items:
            serialized_item = {
                "id": item.id,
                "src": item.image.url if item.image else None,
                "title": item.title,
                "date": item.date
            }
            if item.category == "programs":
                response_data["programs"].append(serialized_item)
            elif item.category == "events":
                response_data["events"].append(serialized_item)
            elif item.category == "convocations":
                response_data["convocations"].append(serialized_item)
            elif item.category == "achievements":
                response_data["achievements"].append(serialized_item)

        return Response(response_data)


class GalleryItemDetailAPIView(APIView):
    def get(self, request, id):
        try:
            gallery_item = GalleryItem.objects.get(id=id)
            serializer = GalleryItemSerializer(gallery_item)
            return Response(serializer.data)
        except GalleryItem.DoesNotExist:
            return Response({'detail': 'Gallery Item not found'}, status=status.HTTP_404_NOT_FOUND)


class GalleryItemCreateAPIView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = GalleryItemSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GalleryItemUpdateAPIView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def put(self, request, id):
        try:
            gallery_item = GalleryItem.objects.get(id=id)
        except GalleryItem.DoesNotExist:
            return Response({'detail': 'Gallery Item not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = GalleryItemSerializer(gallery_item, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GalleryItemDeleteAPIView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def delete(self, request, id):
        try:
            gallery_item = GalleryItem.objects.get(id=id)
            gallery_item.delete()
            return Response({'detail': 'Gallery Item deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
        except GalleryItem.DoesNotExist:
            return Response({'detail': 'Gallery Item not found'}, status=status.HTTP_404_NOT_FOUND)


# ---------- Event ----------
class EventListAPIView(APIView):
    def get(self, request):
        events = Event.objects.all().order_by('-id')[:1]
        serializer = EventSerializer(events, many=True)
        return Response(serializer.data)


class EventDetailAPIView(APIView):
    def get(self, request, id):
        try:
            event = Event.objects.get(id=id)
            serializer = EventSerializer(event)
            return Response(serializer.data)
        except Event.DoesNotExist:
            return Response({'detail': 'Event not found'}, status=status.HTTP_404_NOT_FOUND)


class EventCreateAPIView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = EventSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class EventUpdateAPIView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def put(self, request, id):
        try:
            event = Event.objects.get(id=id)
        except Event.DoesNotExist:
            return Response({'detail': 'Event not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = EventSerializer(event, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class EventDeleteAPIView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def delete(self, request, id):
        try:
            event = Event.objects.get(id=id)
            event.delete()
            return Response({'detail': 'Event deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
        except Event.DoesNotExist:
            return Response({'detail': 'Event not found'}, status=status.HTTP_404_NOT_FOUND)
