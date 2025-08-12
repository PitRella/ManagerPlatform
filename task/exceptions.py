"""Custom exceptions for the task app."""


class TaskError(Exception):
    """Base exception for task-related errors."""
    pass


class TaskNotFoundError(TaskError):
    """Raised when a task is not found."""
    pass


class TaskPermissionError(TaskError):
    """Raised when user doesn't have permission to perform action on task."""
    pass


class TaskValidationError(TaskError):
    """Raised when task validation fails."""
    pass


class TaskConflictError(TaskError):
    """Raised when there's a conflict with task data."""
    pass


class ProjectNotFoundError(TaskError):
    """Raised when a project is not found."""
    pass


class TaskReorderError(TaskError):
    """Raised when task reordering fails."""
    pass


class TaskToggleError(TaskError):
    """Raised when task toggle operation fails."""
    pass
