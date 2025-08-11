from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import UpdateView
from django.http import HttpResponse
from django.template.loader import render_to_string
from project.models import Project
from project.forms import EditForm


class ProjectUpdateView(LoginRequiredMixin, UpdateView):
    """View for updating project titles via HTMX."""
    model = Project
    form_class = EditForm
    template_name = 'project/edit.html'

    def get_queryset(self):
        """Only projects for current user."""
        return Project.objects.for_user(self.request.user)

    def form_valid(self, form):
        project = form.save()
        # Return the title element in display mode, not the form
        html = f'<h4 class="mb-0 project-title" hx-target="this" hx-swap="outerHTML" style="cursor: pointer;" title="Click to edit title">{project.title}</h4>'
        return HttpResponse(html)

    def form_invalid(self, form):
        # Return form with errors
        html = render_to_string(
            'project/edit.html',
            {
                'form': form
            },
            request=self.request
        )
        return HttpResponse(html, status=422)
