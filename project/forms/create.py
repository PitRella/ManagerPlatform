from django import forms
from project.models import Project

class CreateForm(forms.ModelForm):
    """Form for creating and editing projects."""

    class Meta:
        model = Project
        fields = ['title']
        widgets = {
            'title': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Enter project title...',
                    'maxlength': '64'
                }
            )
        }

    def clean_title(self):
        """Validate that title is unique for the current user."""
        title = self.cleaned_data.get('title')
        if title:
            title = title.strip()
            if not title:
                raise forms.ValidationError('Project title cannot be empty.')
        return title
