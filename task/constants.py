
# Task text constraints
TASK_TEXT_MIN_LENGTH = 1
TASK_TEXT_MAX_LENGTH = 64

# Task priority constraints
TASK_PRIORITY_MIN = 1
TASK_PRIORITY_MAX = 1000

# Pagination
DEFAULT_TASKS_PER_PAGE = 20
MAX_TASKS_PER_PAGE = 100

# Search
MIN_SEARCH_QUERY_LENGTH = 1
MAX_SEARCH_QUERY_LENGTH = 50

# Error messages
ERROR_TASK_TEXT_EMPTY = "Task text cannot be empty."
ERROR_TASK_TEXT_TOO_SHORT = f"Task text must be at least {TASK_TEXT_MIN_LENGTH} character long."
ERROR_TASK_TEXT_TOO_LONG = f"Task text cannot exceed {TASK_TEXT_MAX_LENGTH} characters."
ERROR_TASK_TEXT_INVALID_CHARS = "Task text contains invalid characters."
ERROR_TASK_NOT_FOUND = "Task not found."
ERROR_TASK_NO_PERMISSION = "You don't have permission to perform this action on this task."
ERROR_PROJECT_NOT_FOUND = "Project not found."
ERROR_TASK_PRIORITY_INVALID = f"Task priority must be between {TASK_PRIORITY_MIN} and {TASK_PRIORITY_MAX}."
ERROR_TASK_REORDER_FAILED = "Failed to reorder tasks."
ERROR_TASK_TOGGLE_FAILED = "Failed to toggle task completion status."
