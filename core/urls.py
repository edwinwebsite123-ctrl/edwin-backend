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
]