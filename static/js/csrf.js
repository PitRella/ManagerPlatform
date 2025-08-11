// CSRF and HTMX configuration
document.addEventListener('DOMContentLoaded', function () {
    // Configure HTMX to include CSRF token in all requests
    document.body.addEventListener('htmx:configRequest', function (evt) {
        // Get CSRF token from meta tag or hidden input
        const token = document.querySelector('[name=csrfmiddlewaretoken]')?.value || 
                     document.querySelector('meta[name=csrf-token]')?.getAttribute('content');
        if (token) {
            evt.detail.headers['X-CSRFToken'] = token;
        }
    });
    
    // Also add CSRF token to all HTMX requests that don't have it
    document.addEventListener('htmx:beforeRequest', function (evt) {
        if (!evt.detail.headers['X-CSRFToken']) {
            const token = document.querySelector('[name=csrfmiddlewaretoken]')?.value || 
                         document.querySelector('meta[name=csrf-token]')?.getAttribute('content');
            if (token) {
                evt.detail.headers['X-CSRFToken'] = token;
            }
        }
    });
    
    // Handle HTMX after swap to restore functionality
    document.addEventListener('htmx:afterSwap', function (evt) {
        // If this is a project title that was just edited, restore its click functionality
        if (evt.detail.target.classList.contains('project-title')) {
            evt.detail.target.style.cursor = 'pointer';
            evt.detail.target.title = 'Click to edit title';
        }
    });
});
