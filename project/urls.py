from django.urls import path

from project.views import (
                           DashboardView,
                           ProjectCreateView,
                           ProjectDeleteView,
                           ProjectUpdateView,
)

app_name = 'projects'
urlpatterns = [
    path('', DashboardView.as_view(), name='dashboard'),
    path('create', ProjectCreateView.as_view(), name='create'),
    path('<int:pk>/delete/', ProjectDeleteView.as_view(), name='delete'),
    path('<int:pk>/update/', ProjectUpdateView.as_view(), name='update'),

]
