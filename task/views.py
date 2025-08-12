# Import all task views from the new modular structure
from .views.create import TaskCreateView, TaskCreateSimpleView
from .views.update import TaskUpdateView
from .views.delete import TaskDeleteView
from .views.reorder import TaskReorderView
from .views.toggle import TaskToggleView

# Export all views for backward compatibility
__all__ = [
    'TaskCreateView',
    'TaskCreateSimpleView',
    'TaskUpdateView', 
    'TaskDeleteView',
    'TaskReorderView',
    'TaskToggleView',
]