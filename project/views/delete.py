from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import DeleteView
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_protect
from django.utils.decorators import method_decorator
from project.models import Project

@method_decorator(csrf_protect, name='dispatch')
class ProjectDeleteView(LoginRequiredMixin, DeleteView):
    model = Project
    template_name = 'project/delete.html'

    def post(self, request, *args, **kwargs):
        """Handle POST request via HTMX."""
        self.get_object().delete()
        return HttpResponse('', status=204)
