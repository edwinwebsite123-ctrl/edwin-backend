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
]
