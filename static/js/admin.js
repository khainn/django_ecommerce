document.addEventListener('DOMContentLoaded', function() {
    // Add active class to current menu item
    const currentPath = window.location.pathname;
    const menuItems = document.querySelectorAll('#changelist-filter a');
    
    menuItems.forEach(item => {
        if (item.getAttribute('href') === currentPath) {
            item.classList.add('active');
        }
    });

    // Initialize tooltips
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });

    // Add responsive table wrapper
    const tables = document.querySelectorAll('.module table');
    tables.forEach(table => {
        const wrapper = document.createElement('div');
        wrapper.className = 'table-responsive';
        table.parentNode.insertBefore(wrapper, table);
        wrapper.appendChild(table);
    });

    // Add card styling to modules
    const modules = document.querySelectorAll('.module');
    modules.forEach(module => {
        module.classList.add('card');
        const header = module.querySelector('h2, caption');
        if (header) {
            header.classList.add('card-header');
        }
        const content = module.querySelector('.module-content');
        if (content) {
            content.classList.add('card-body');
        }
    });
}); 