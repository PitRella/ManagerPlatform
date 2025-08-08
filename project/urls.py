from django.urls import path
from project.views import DashboardView

urlpatterns = [
    path('', DashboardView.as_view(), name='dashboard')
]
