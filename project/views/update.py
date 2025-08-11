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
        # Return the full title element so HTMX swaps the form back to display mode
        html = render_to_string(
            'project/edit.html', {
                'project': project
            }, request=self.request)
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
