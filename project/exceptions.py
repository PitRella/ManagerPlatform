"""Custom exceptions for the project app."""


class ProjectError(Exception):
    """Base exception for project-related errors."""
    pass


class ProjectNotFoundError(ProjectError):
    """Raised when a project is not found."""
    pass


class ProjectPermissionError(ProjectError):
    """Raised when user doesn't have permission to perform action on project."""
    pass


class ProjectValidationError(ProjectError):
    """Raised when project validation fails."""
    pass


class ProjectConflictError(ProjectError):
    """Raised when there's a conflict with project data."""
    pass

