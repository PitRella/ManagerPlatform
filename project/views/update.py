from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.views.generic import UpdateView

from core.mixins.views import HTMXResponseMixin
from project.forms import EditForm
from project.models import Project


class ProjectUpdateView(
    LoginRequiredMixin,
    HTMXResponseMixin[Project],
    UpdateView
):
    model = Project
    form_class = EditForm
    template_name = 'project/edit.html'

    def get_queryset(self):
        return Project.objects.for_user(self.request.user)

    def render_htmx_response(self, instance: Project) -> HttpResponse:
        html = render_to_string(
            'project/edit_title.html',
            {
                'project':
                    instance
            },
            request=self.request
        )
        return HttpResponse(html)
