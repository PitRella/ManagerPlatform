from .create import TaskCreateView
from .update import TaskUpdateView
from .delete import TaskDeleteView
from .reorder import TaskReorderView
from .toggle import TaskToggleView

__all__ = [
    'TaskCreateView',
    'TaskUpdateView',
    'TaskDeleteView',
    'TaskReorderView',
    'TaskToggleView',
]
