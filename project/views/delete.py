from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import DeleteView

from core.mixins.views import HTMXDeleteMixin
from project.models import Project


class ProjectDeleteView(LoginRequiredMixin, HTMXDeleteMixin, DeleteView):
    model = Project
    template_name = 'project/delete.html'

