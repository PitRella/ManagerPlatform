/**
 * HTMX Event Handlers
 * Handles post-swap cleanup and reinitialization
 */

class HtmxHandlers {
    constructor() {
        this.init();
    }

    init() {
        document.addEventListener('htmx:afterSwap', this.handleAfterSwap.bind(this));
    }

    /**
     * Handle HTMX afterSwap event
     * @param {Event} event - HTMX afterSwap event
     */
    handleAfterSwap(event) {
        const target = event.target;
        
        // Check if the swapped element is a tasks container
        if (target.id && target.id.startsWith('tasks-container-')) {
            this.cleanupTasksContainer(target);
        }
    }

    /**
     * Clean up tasks container after swap
     * @param {HTMLElement} container - The tasks container element
     */
    cleanupTasksContainer(container) {
        const projectId = this.extractProjectId(container.id);
        if (!projectId) return;

        // Clear search input
        this.clearSearchInput(projectId);
        
        // Remove no-tasks message if it exists
        this.removeNoTasksMessage(projectId);
        
        // Reinitialize dashboard manager if available
        this.reinitializeDashboardManager();
    }

    /**
     * Extract project ID from container ID
     * @param {string} containerId - Container ID (e.g., "tasks-container-123")
     * @returns {string|null} Project ID or null if not found
     */
    extractProjectId(containerId) {
        const match = containerId.match(/tasks-container-(\d+)/);
        return match ? match[1] : null;
    }

    /**
     * Clear search input for the project
     * @param {string} projectId - Project ID
     */
    clearSearchInput(projectId) {
        const wrap = document.querySelector(`[data-project-id="${projectId}"]`);
        if (!wrap) return;

        const input = wrap.querySelector(`#searchInput-${projectId}`);
        if (input) {
            input.value = '';
        }
    }

    /**
     * Remove no-tasks message if it exists
     * @param {string} projectId - Project ID
     */
    removeNoTasksMessage(projectId) {
        const msg = document.getElementById(`no-tasks-message-${projectId}`);
        if (msg) {
            msg.remove();
        }
    }

    /**
     * Reinitialize dashboard manager if available
     */
    reinitializeDashboardManager() {
        if (window.dashboardManager) {
            window.dashboardManager.rebindEventHandlers();
            window.dashboardManager.initSortableLists();
        }
    }
}

// Initialize HTMX handlers when DOM is ready
document.addEventListener('DOMContentLoaded', () => {
    window.htmxHandlers = new HtmxHandlers();
});

// Also initialize if DOM is already loaded
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', () => {
        window.htmxHandlers = new HtmxHandlers();
    });
} else {
    window.htmxHandlers = new HtmxHandlers();
}
