"""Constants for the project app."""

# Project title constraints
PROJECT_TITLE_MIN_LENGTH = 3
PROJECT_TITLE_MAX_LENGTH = 64

# Pagination
DEFAULT_PROJECTS_PER_PAGE = 10
MAX_PROJECTS_PER_PAGE = 100

# Search
MIN_SEARCH_QUERY_LENGTH = 2
MAX_SEARCH_QUERY_LENGTH = 50

# Project status
PROJECT_STATUS_ACTIVE = 'active'
PROJECT_STATUS_ARCHIVED = 'archived'

# Error messages
ERROR_PROJECT_TITLE_EMPTY = "Project title cannot be empty."
ERROR_PROJECT_TITLE_TOO_SHORT = f"Project title must be at least {PROJECT_TITLE_MIN_LENGTH} characters long."
ERROR_PROJECT_TITLE_TOO_LONG = f"Project title cannot exceed {PROJECT_TITLE_MAX_LENGTH} characters."
ERROR_PROJECT_TITLE_INVALID_CHARS = "Project title contains invalid characters."
ERROR_PROJECT_ALREADY_EXISTS = "Project with title '{title}' already exists for this user."
ERROR_PROJECT_NOT_FOUND = "Project not found."
ERROR_PROJECT_NO_PERMISSION = "You don't have permission to perform this action on this project."
ERROR_PROJECT_HAS_ACTIVE_TASKS = "Cannot delete project with active tasks. Archive it instead."
