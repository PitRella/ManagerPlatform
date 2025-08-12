from .create import TaskCreateView, TaskCreateSimpleView
from .update import TaskUpdateView
from .delete import TaskDeleteView
from .reorder import TaskReorderView
from .toggle import TaskToggleView

__all__ = [
    'TaskCreateView',
    'TaskCreateSimpleView', 
    'TaskUpdateView',
    'TaskDeleteView',
    'TaskReorderView',
    'TaskToggleView',
]
