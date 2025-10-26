from django.urls import path
from .views import *

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('verify-token/', VerifyTokenView.as_view(), name='verify-token'),

    # Create application (POST)
    path('applications/', ApplicationCreateView.as_view(), name='application-create'),

    # List all applications (GET)
    path('applications/list/', ApplicationListView.as_view(), name='application-list'),

    # Detail/delete by pk
    path('applications/<int:pk>/', ApplicationDetailView.as_view(), name='application-detail'),

    path('dashboard/counts/', DashboardCountsView.as_view(), name='dashboard-counts'),

    path('dashboard/recent-leads/', RecentLeadsView.as_view(), name='dashboard-recent-leads'),

    path("contact/create/", ContactMessageCreateView.as_view(), name="contact-create"),
    path("contact/list/", ContactMessageListView.as_view(), name="contact-list"),
    path("contact/recent/", RecentContactMessageListView.as_view(), name="contact-recent"),
    path("contact/delete/<int:pk>/", ContactMessageDeleteView.as_view(), name="contact-delete"),

    # Course API endpoints
    path('courses/', CourseListView.as_view(), name='course-list'),  # GET - Public
    path('courses/<slug:id>/', CourseDetailView.as_view(), name='course-detail'),  # GET - Public
    path('courses/create/', CourseCreateView.as_view(), name='course-create'),  # POST - Auth required
    path('courses/<slug:id>/update/', CourseUpdateView.as_view(), name='course-update'),  # PUT/PATCH - Auth required
    path('courses/<slug:id>/delete/', CourseDeleteView.as_view(), name='course-delete'),  # DELETE - Auth required

    path('placements/', PlacementListView.as_view(), name='placement-list'),
    path('placements/<int:id>/', PlacementDetailView.as_view(), name='placement-detail'),
    path('placements/create/', PlacementCreateView.as_view(), name='placement-create'),
    path('placements/<int:id>/update/', PlacementUpdateView.as_view(), name='placement-update'),
    path('placements/<int:id>/delete/', PlacementDeleteView.as_view(), name='placement-delete'),

    path('edwintalks/', EdwinTalkListView.as_view(), name='edwintalk-list'),
    path('edwintalks/<int:id>/', EdwinTalkDetailView.as_view(), name='edwintalk-detail'),
    path('edwintalks/create/', EdwinTalkCreateView.as_view(), name='edwintalk-create'),
    path('edwintalks/<int:id>/update/', EdwinTalkUpdateView.as_view(), name='edwintalk-update'),
    path('edwintalks/<int:id>/delete/', EdwinTalkDeleteView.as_view(), name='edwintalk-delete'),

    path('testimonials/', TestimonialListAPIView.as_view(), name='testimonial-list'),
    path('testimonials/<int:id>/', TestimonialDetailAPIView.as_view(), name='testimonial-detail'),
    path('testimonials/create/', TestimonialCreateAPIView.as_view(), name='testimonial-create'),
    path('testimonials/<int:id>/update/', TestimonialUpdateAPIView.as_view(), name='testimonial-update'),
    path('testimonials/<int:id>/delete/', TestimonialDeleteAPIView.as_view(), name='testimonial-delete'),

    path("faculty/", FacultyListAPIView.as_view(), name="faculty-list"),
    path("faculty/<int:id>/", FacultyDetailAPIView.as_view(), name="faculty-detail"),
    path("faculty/create/", FacultyCreateAPIView.as_view(), name="faculty-create"),
    path("faculty/update/<int:id>/", FacultyUpdateAPIView.as_view(), name="faculty-update"),
    path("faculty/delete/<int:id>/", FacultyDeleteAPIView.as_view(), name="faculty-delete"),

    path("placement-posters/", PlacementPosterListAPIView.as_view(), name="poster-list"),
    path("placement-posters/<int:id>/", PlacementPosterDetailAPIView.as_view(), name="poster-detail"),
    path("placement-posters/create/", PlacementPosterCreateAPIView.as_view(), name="poster-create"),
    path("placement-posters/update/<int:id>/", PlacementPosterUpdateAPIView.as_view(), name="poster-update"),
    path("placement-posters/delete/<int:id>/", PlacementPosterDeleteAPIView.as_view(), name="poster-delete"),


    # UG
    path('ug-programs/', UGProgramListAPIView.as_view(), name='ug-program-list'),
    path('ug-programs/<int:id>/', UGProgramDetailAPIView.as_view(), name='ug-program-detail'),
    path('ug-programs/create/', UGProgramCreateAPIView.as_view(), name='ug-program-create'),
    path('ug-programs/update/<int:id>/', UGProgramUpdateAPIView.as_view(), name='ug-program-update'),
    path('ug-programs/delete/<int:id>/', UGProgramDeleteAPIView.as_view(), name='ug-program-delete'),

    # PG
    path('pg-programs/', PGProgramListAPIView.as_view(), name='pg-program-list'),
    path('pg-programs/<int:id>/', PGProgramDetailAPIView.as_view(), name='pg-program-detail'),
    path('pg-programs/create/', PGProgramCreateAPIView.as_view(), name='pg-program-create'),
    path('pg-programs/update/<int:id>/', PGProgramUpdateAPIView.as_view(), name='pg-program-update'),
    path('pg-programs/delete/<int:id>/', PGProgramDeleteAPIView.as_view(), name='pg-program-delete'),
]
