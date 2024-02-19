# urls.py

from django.urls import path
from .views import CheckInListCreateAPIView, UserRegisterAPIView, UserLoginAPIView,CheckAdminStatus,CheckInListAPIView,UsersWith45HoursAPIView

urlpatterns = [
    path('checkins/', CheckInListCreateAPIView.as_view(), name='checkin-list-create'),
    path('register/', UserRegisterAPIView.as_view(), name='user-register'),
    path('login/', UserLoginAPIView.as_view(), name='user-login'),
    path('checkins/<int:pk>/',CheckInListCreateAPIView.as_view(), name='checkin-detail'),
    path('check_admin_status/', CheckAdminStatus.as_view(), name='checkin-admin-list'),
    path('all_checkins/', CheckInListAPIView.as_view(), name='checkin-admin-list'),
    path('users_with_45_hours/', UsersWith45HoursAPIView.as_view(), name='users-with-45-hours'),
    # Add other URL patterns as needed
]
