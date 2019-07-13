from django.contrib import admin
from django.urls import path, include

from core.views import UserDetails

urlpatterns = [
    path('auth/', include('auth.urls', namespace='auth')),
    path('user/meta/', UserDetails.as_view()),

    path('admin/', admin.site.urls),
]
