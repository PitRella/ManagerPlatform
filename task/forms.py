from django import forms
from task.models import Task


class TaskForm(forms.ModelForm):
    """Form for creating and editing tasks."""

    class Meta:
        model = Task
        fields = ['text', 'priority']
        widgets = {
            'text': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter task description...',
                'maxlength': '32'
            }),
            'priority': forms.Select(attrs={
                'class': 'form-select'
            })
        }

    def clean_text(self):
        """Validate that text is not empty."""
        text = self.cleaned_data.get('text')
        if not text or not text.strip():
            raise forms.ValidationError('Task description cannot be empty.')
        return text.strip()


class TaskEditForm(forms.ModelForm):
    """Form for inline editing of task text."""

    class Meta:
        model = Task
        fields = ['text']
        widgets = {
            'text': forms.TextInput(
                attrs={
                    'class': 'task-text-input',
                    'style': (
                        'border: 1px solid rgba(255,255,255,0.9); '
                        'background: transparent; '
                        'font-weight: 600; font-size: 1rem; '
                        'color: inherit; padding: 0 .25rem; outline: none; '
                        'text-shadow: inherit; width: 100%; '
                        'border-radius: .25rem;'
                    ),
                    'maxlength': '64',
                    'autofocus': 'autofocus',
                    'aria-label': 'Edit task text'
                }
            )
        }
