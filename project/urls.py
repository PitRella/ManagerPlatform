from django.urls import path
from project.views import DashboardView
from project.views.project_create import ProjectCreateView

app_name = 'projects'
urlpatterns = [
    path('', DashboardView.as_view(), name='dashboard'),
    path('/create', ProjectCreateView.as_view(), name='create')
]
