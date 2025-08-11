class DashboardManager {
    constructor() {
        this.dragSrcEl = null;
        // Bind methods to preserve context
        this.handleTaskDelete = this.handleTaskDelete.bind(this);
        this.handleTaskEdit = this.handleTaskEdit.bind(this);
        this.handleProjectDelete = this.handleProjectDelete.bind(this);
        this.handleProjectEdit = this.handleProjectEdit.bind(this);
        this.handleDragStart = this.handleDragStart.bind(this);
        this.handleDragEnd = this.handleDragEnd.bind(this);
        this.handleDragOver = this.handleDragOver.bind(this);
        this.handleDrop = this.handleDrop.bind(this);
        this.handleChange = this.handleChange.bind(this);
        this.init();
    }

    init() {
        try {
            this.bindEvents();
            this.initSortableLists();
            this.rebindEventHandlers();
        } catch (error) {
            console.warn('Error initializing DashboardManager:', error);
        }
    }

    bindEvents() {
        document.addEventListener('click', this.handleClick.bind(this));
        document.addEventListener('change', this.handleChange.bind(this));
        document.addEventListener('htmx:afterRequest', this.handleHtmxResponse.bind(this));
        document.addEventListener('htmx:afterSwap', this.handleHtmxAfterSwap.bind(this));
        document.addEventListener('htmx:load', this.handleHtmxLoad.bind(this));
    }

    handleClick(e) {
        if (e.target.classList.contains('delete-project-btn')) {
            this.handleProjectDelete(e);
        } else if (e.target.classList.contains('edit-project-btn')) {
            this.handleProjectEdit(e);
        } else if (e.target.classList.contains('delete-task-btn')) {
            this.handleTaskDelete(e);
        } else if (e.target.classList.contains('edit-task-btn')) {
            this.handleTaskEdit(e);
        }
    }

    handleChange(e) {
        if (e.target.classList.contains('task-checkbox')) {
            this.handleTaskToggle(e);
        }
    }

    handleTaskToggle(e) {
        const taskId = e.target.dataset.taskId;
        const isCompleted = e.target.checked;
        
        console.log('Task toggle:', taskId, 'completed:', isCompleted);
        
        // TODO: Implement task completion toggle functionality
        console.log('Task completion toggle not implemented yet');
    }

    handleProjectDelete(e) {
        e.preventDefault();
        e.stopPropagation();

        // Prevent multiple clicks
        if (e.target.disabled) {
            return;
        }

        const projectId = e.target.dataset.projectId;

        if (confirm('Are you sure you want to delete this project?')) {
            // Disable the button to prevent multiple clicks
            e.target.disabled = true;
            this.deleteProject(projectId);
        }
    }

    handleProjectEdit(e) {
        e.preventDefault();
        e.stopPropagation();

        // Prevent multiple clicks
        if (e.target.disabled) {
            return;
        }

        const projectId = e.target.dataset.projectId;
        const titleElement = e.target.closest('.header-text-shadow').querySelector('.project-title');

        // Disable the button to prevent multiple clicks
        e.target.disabled = true;
        this.editProject(projectId, titleElement);
    }

    deleteProject(projectId) {
        const csrfToken = this.getCsrfToken();
        if (!csrfToken) {
            console.error('Cannot delete project: CSRF token is missing');
            return;
        }

        fetch(`/dashboard/${projectId}/delete/`, {
            method: 'POST',
            headers: {
                'X-CSRFToken': csrfToken
            }
        }).then(response => {
            if (response.ok) {
                this.removeProjectFromDOM(projectId);
            } else {
                console.error('Error deleting project:', response.status, response.statusText);
                // Re-enable the button if deletion failed
                this.reenableButtons();
            }
        }).catch(error => {
            console.error('Error deleting project:', error);
            // Re-enable the button if deletion failed
            this.reenableButtons();
        });
    }

    editProject(projectId, titleElement) {
        htmx.ajax('GET', `/dashboard/${projectId}/update/`, {
            target: titleElement,
            swap: 'outerHTML'
        }).then(() => {
            this.reenableButtons();
        });
    }

    handleTaskEdit(e) {
        e.preventDefault();
        e.stopPropagation();

        // Prevent multiple clicks
        if (e.target.disabled) {
            return;
        }

        const taskId = e.target.dataset.taskId;
        console.log('Task edit clicked, taskId:', taskId);

        // Disable the button to prevent multiple clicks
        e.target.disabled = true;
        
        // TODO: Implement task editing functionality
        console.log('Task editing not implemented yet');
        
        // Re-enable the button
        e.target.disabled = false;
    }

    handleTaskDelete(e) {
        e.preventDefault();
        e.stopPropagation();

        // Prevent multiple clicks
        if (e.target.disabled) {
            return;
        }

        const taskId = e.target.dataset.taskId;

        console.log('Task delete clicked, taskId:', taskId);

        if (confirm('Are you sure you want to delete this task?')) {
            console.log('Confirming deletion of task:', taskId);
            // Disable the button to prevent multiple clicks
            e.target.disabled = true;
            this.deleteTask(taskId);
        } else {
            console.log('Task deletion cancelled');
        }
    }

    deleteTask(taskId) {
        console.log('Starting deletion of task:', taskId);
        const csrfToken = this.getCsrfToken();
        console.log('CSRF token:', csrfToken ? 'Found' : 'Missing');

        if (!csrfToken) {
            console.error('Cannot delete task: CSRF token is missing');
            return;
        }

        fetch(`/tasks/${taskId}/delete/`, {
            method: 'DELETE',
            headers: {
                'X-CSRFToken': csrfToken
            }
        }).then(response => {
            console.log('Delete response:', response.status, response.statusText);
            if (response.ok) {
                console.log('Task deleted successfully, removing from DOM');
                this.removeTaskFromDOM(taskId);
            } else {
                console.error('Error deleting task:', response.status, response.statusText);
                // Re-enable the button if deletion failed
                this.reenableButtons();
            }
        }).catch(error => {
            console.error('Error deleting task:', error);
            // Re-enable the button if deletion failed
            this.reenableButtons();
        });
    }

    removeProjectFromDOM(projectId) {
        const projectElement = document.querySelector(`[data-project-id="${projectId}"].todo-list-project`);
        if (projectElement) {
            projectElement.remove();
        }
    }

    getCsrfToken() {
        const tokenElement = document.querySelector('[name=csrfmiddlewaretoken]');
        if (!tokenElement) {
            console.error('CSRF token element not found');
            return null;
        }
        const token = tokenElement.value;
        if (!token) {
            console.error('CSRF token value is empty');
            return null;
        }
        return token;
    }

    handleHtmxResponse(event) {
        if (event.detail.xhr.status === 200 && event.detail.elt.matches('form[hx-post*="create"]')) {
            this.closeCreateModal();
        }
        // Re-enable buttons after any HTMX response
        this.reenableButtons();
    }

    handleHtmxAfterSwap(event) {
        // Re-initialize sortable lists after HTMX updates
        try {
            this.initSortableLists();
            // Re-bind event handlers for newly loaded content
            this.rebindEventHandlers();
            // Re-enable all buttons
            this.reenableButtons();
        } catch (error) {
            console.warn('Error reinitializing after HTMX swap:', error);
        }
    }

    handleHtmxLoad(event) {
        // Handle newly loaded content
        try {
            this.rebindEventHandlers();
            this.reenableButtons();
        } catch (error) {
            console.warn('Error handling HTMX load:', error);
        }
    }

    reenableButtons() {
        // Re-enable all buttons that might have been disabled
        const allButtons = document.querySelectorAll('.delete-task-btn, .edit-task-btn, .delete-project-btn, .edit-project-btn');
        allButtons.forEach(btn => {
            btn.disabled = false;
        });
    }

    rebindEventHandlers() {
        // Re-bind click handlers for newly loaded content
        const deleteTaskBtns = document.querySelectorAll('.delete-task-btn');
        const editTaskBtns = document.querySelectorAll('.edit-task-btn');
        const deleteProjectBtns = document.querySelectorAll('.delete-project-btn');
        const editProjectBtns = document.querySelectorAll('.edit-project-btn');

        console.log(`Rebinding event handlers: ${deleteTaskBtns.length} delete task buttons, ${editTaskBtns.length} edit task buttons`);

        // Remove existing event listeners to prevent duplicates
        deleteTaskBtns.forEach(btn => {
            if (btn && !btn.dataset.taskId) {
                console.warn('Button missing data-task-id:', btn);
                return;
            }
            console.log('Binding delete handler to button:', btn.dataset.taskId);
            btn.removeEventListener('click', this.handleTaskDelete);
            btn.addEventListener('click', this.handleTaskDelete);
        });

        editTaskBtns.forEach(btn => {
            if (btn && !btn.dataset.taskId) {
                console.warn('Button missing data-task-id:', btn);
                return;
            }
            btn.removeEventListener('click', this.handleTaskEdit);
            btn.addEventListener('click', this.handleTaskEdit);
        });

        deleteProjectBtns.forEach(btn => {
            if (btn && !btn.dataset.projectId) {
                console.warn('Button missing data-project-id:', btn);
                return;
            }
            btn.removeEventListener('click', this.handleProjectDelete);
            btn.addEventListener('click', this.handleProjectDelete);
        });

        editProjectBtns.forEach(btn => {
            if (btn && !btn.dataset.projectId) {
                console.warn('Button missing data-project-id:', btn);
                return;
            }
            btn.removeEventListener('click', this.handleProjectEdit);
            btn.addEventListener('click', this.handleProjectEdit);
        });
    }

    closeCreateModal() {
        const modal = bootstrap.Modal.getInstance(document.getElementById('createProjectModal'));
        if (modal) {
            modal.hide();
        }
    }

    // Drag and drop functionality
    initSortableLists() {
        const lists = document.querySelectorAll('.todo-list');
        console.log(`Found ${lists.length} sortable lists`);

        if (lists.length === 0) return; // Exit if no lists found

        lists.forEach((list, index) => {
            console.log(`Initializing list ${index + 1}`);
            this.initSortableList(list);
        });
    }

    initSortableList(list) {
        if (!list) return; // Exit if list is null

        // Remove existing event listeners to prevent duplicates
        const handles = list.querySelectorAll('.handle');
        if (handles.length === 0) return; // Exit if no handles found

        console.log(`Initializing sortable list with ${handles.length} handles`);

        handles.forEach(handle => {
            if (handle) {
                handle.removeEventListener('dragstart', this.handleDragStart);
                handle.removeEventListener('dragend', this.handleDragEnd);
                handle.addEventListener('dragstart', this.handleDragStart);
                handle.addEventListener('dragend', this.handleDragEnd);
            }
        });

        // Remove existing list event listeners
        list.removeEventListener('dragover', this.handleDragOver);
        list.removeEventListener('drop', this.handleDrop);

        // Add new list event listeners
        list.addEventListener('dragover', this.handleDragOver);
        list.addEventListener('drop', this.handleDrop);
    }

    handleDragStart(e) {
        console.log('Drag start');
        this.dragSrcEl = e.target.closest('.row');
        if (!this.dragSrcEl || !this.dragSrcEl.dataset.taskId) {
            console.warn('Invalid drag source element');
            e.preventDefault();
            return;
        }

        console.log('Dragging task:', this.dragSrcEl.dataset.taskId);
        e.dataTransfer.effectAllowed = 'move';
        e.dataTransfer.setData('text/plain', this.dragSrcEl.dataset.taskId);
        this.dragSrcEl.classList.add('dragging');
    }

    handleDragEnd(e) {
        console.log('Drag end');
        const row = e.target.closest('.row');
        if (row) {
            row.classList.remove('dragging');
        }
        this.dragSrcEl = null;
    }

    handleDragOver(e) {
        e.preventDefault();
        e.dataTransfer.dropEffect = 'move';
    }

    handleDrop(e) {
        e.preventDefault();
        console.log('Drop event');

        if (!this.dragSrcEl) {
            console.warn('No drag source element');
            return;
        }

        const list = e.currentTarget;
        const afterElement = this.getDragAfterElement(list, e.clientY);

        console.log('Dropping task:', this.dragSrcEl.dataset.taskId);

        if (afterElement == null) {
            list.appendChild(this.dragSrcEl);
        } else {
            list.insertBefore(this.dragSrcEl, afterElement);
        }

        // Persist the new order
        this.persistOrder(list);
    }

    getDragAfterElement(container, y) {
        const draggableElements = [...container.querySelectorAll('.row[data-task-id]:not(.dragging)')];

        if (draggableElements.length === 0) {
            return null;
        }

        return draggableElements.reduce((closest, child) => {
            const box = child.getBoundingClientRect();
            const offset = y - box.top - box.height / 2;
            if (offset < 0 && offset > closest.offset) {
                return { offset, element: child };
            } else {
                return closest;
            }
        }, { offset: Number.NEGATIVE_INFINITY }).element;
    }

    persistOrder(list) {
        const projectId = list.closest('.todo-list-project').dataset.projectId;
        const order = Array.from(list.querySelectorAll('.row[data-task-id]'))
            .map((row, index) => ({ id: row.dataset.taskId, position: index + 1 }));

        console.log('Persisting order for project:', projectId, 'Order:', order);

        fetch(`/tasks/reorder/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': this.getCsrfToken(),
            },
            body: JSON.stringify({ projectId, order })
        }).then(response => {
            if (response.ok) {
                console.log('Order saved successfully');
            } else {
                console.error('Error saving order:', response.status, response.statusText);
            }
        }).catch(error => {
            console.error('Error saving task order:', error);
        });
    }
}

// Инициализация при загрузке DOM
document.addEventListener('DOMContentLoaded', function() {
    console.log('DOM loaded, initializing DashboardManager');
    window.dashboardManager = new DashboardManager();
    console.log('addTask function available:', typeof window.addTask);
});
