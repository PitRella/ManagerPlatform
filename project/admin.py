from django.contrib import admin

from project.models import Project


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    """
    Admin configuration for the Project model.

    Defines list display, filtering, search, read-only fields,
    and fieldsets for managing projects in the Django admin interface.
    """

    list_display = (
        'title',
        'owner',
        'created_at',
        'updated_at',
    )
    list_filter = (
        'owner',
        'created_at'
    )
    search_fields = (
        'title',
        'owner__username',
        'owner__email'
    )
    readonly_fields = (
        'created_at',
        'updated_at'
    )
