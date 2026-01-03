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
    path("courses/", CourseListView.as_view(), name="course-list"),
    path('courses/top-choice/', TopChoiceCourseListAPIView.as_view(), name='top-choice-courses'),
    path("courses/<slug:id>/", CourseDetailView.as_view(), name="course-detail"),
    path("courses/create", CourseCreateView.as_view(), name="course-create"),
    path("courses/<slug:id>/update/", CourseUpdateView.as_view(), name="course-update"),
    path("courses/<slug:id>/delete/", CourseDeleteView.as_view(), name="course-delete"),
    path('courses/<slug:id>/toggle-top-choice/', ToggleTopChoiceView.as_view(), name='toggle-top-choice'),

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
    path('ug-programs/<int:id>/update/', UGProgramUpdateAPIView.as_view(), name='ug-program-update'),
    path('ug-programs/<int:id>/delete/', UGProgramDeleteAPIView.as_view(), name='ug-program-delete'),

    # PG
    path('pg-programs/', PGProgramListAPIView.as_view(), name='pg-program-list'),
    path('pg-programs/<int:id>/', PGProgramDetailAPIView.as_view(), name='pg-program-detail'),
    path('pg-programs/create/', PGProgramCreateAPIView.as_view(), name='pg-program-create'),
    path('pg-programs/<int:id>/update/', PGProgramUpdateAPIView.as_view(), name='pg-program-update'),
    path('pg-programs/<int:id>/delete/', PGProgramDeleteAPIView.as_view(), name='pg-program-delete'),

    # Gallery
    path('gallery/list/', GalleryItemListAPIView.as_view(), name='gallery-list'),
    path('gallery/', GalleryItemListTwoAPIView.as_view(), name='gallery-list-two'),
    path('gallery/<int:id>/', GalleryItemDetailAPIView.as_view(), name='gallery-detail'),
    path('gallery/create/', GalleryItemCreateAPIView.as_view(), name='gallery-create'),
    path('gallery/<int:id>/update/', GalleryItemUpdateAPIView.as_view(), name='gallery-update'),
    path('gallery/<int:id>/delete/', GalleryItemDeleteAPIView.as_view(), name='gallery-delete'),

    # Event
    path('events/', EventListAPIView.as_view(), name='event-list'),
    path('events/<int:id>/', EventDetailAPIView.as_view(), name='event-detail'),
    path('events/create/', EventCreateAPIView.as_view(), name='event-create'),
    path('events/<int:id>/update/', EventUpdateAPIView.as_view(), name='event-update'),
    path('events/<int:id>/delete/', EventDeleteAPIView.as_view(), name='event-delete'),

    # Blog
    path('blogs/', BlogListView.as_view(), name='blog-list'),
    path('blogs/create/', BlogCreateView.as_view(), name='blog-create'),
    path('blogs/<int:id>/', BlogDetailView.as_view(), name='blog-detail-id'),  # Admin uses id
    path('blogs/<slug:slug>/', BlogDetailView.as_view(), name='blog-detail-slug'),  # Public uses slug
    path('blogs/<int:id>/update/', BlogUpdateView.as_view(), name='blog-update'),
    path('blogs/<int:id>/delete/', BlogDeleteView.as_view(), name='blog-delete'),
]
