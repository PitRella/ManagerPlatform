from django import forms

from project.models import Project


class EditForm(forms.ModelForm):  # type: ignore
    """Form for editing the project title inline."""

    class Meta:
        model = Project
        fields = ['title']
        widgets = {
            'title': forms.TextInput(
                attrs={
                    'class': 'project-title-input',
                    'style': (
                        'border: 1px solid rgba(255,255,255,0.9); '
                        'background: transparent; '
                        'font-weight: 700; font-size: 1.5rem; '
                        'color: inherit; padding: 0 .25rem; outline: none; '
                        'text-shadow: inherit; width: 100%; '
                        'border-radius: .25rem;'
                    ),
                    'maxlength': '64',
                    'autofocus': 'autofocus',
                    'aria-label': 'Edit project title'
                }
            )
        }
