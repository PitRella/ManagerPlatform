from django.contrib import admin
from django.urls import include, path

from project.views import HomeView

urlpatterns = [
    path('', include('project.urls')),
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
    path('tasks/', include('task.urls')),
]
