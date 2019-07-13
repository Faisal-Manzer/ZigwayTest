# core/auth/urls.py > Faisal
from django.urls import path
from .views import *

urlpatterns = [
    path('sign-in/', SignInView.as_view(), name='get-token'),
    path('refresh/', TokenRefreshView.as_view(), name='refresh-token'),

    path('username/available/', is_username_available, name='username-available'),
    path('sign-up/', CreateUserView.as_view(), name='sign-up')
]

app_name = 'auth'
