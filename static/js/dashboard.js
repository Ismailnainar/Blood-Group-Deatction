document.addEventListener('DOMContentLoaded', () => {

    // Sidebar Toggle
    const sidebar = document.getElementById('sidebar');
    const overlay = document.getElementById('sidebarOverlay');
    const openBtn = document.getElementById('openSidebar');
    const closeBtn = document.getElementById('closeSidebar');

    function toggleSidebar() {
        sidebar.classList.toggle('open');
        overlay.classList.toggle('active');
    }

    if (openBtn) openBtn.addEventListener('click', toggleSidebar);
    if (closeBtn) closeBtn.addEventListener('click', toggleSidebar);
    if (overlay) overlay.addEventListener('click', toggleSidebar);

    // Color code confidence bars
    const confBars = document.querySelectorAll('.confidence-bar-fill');
    confBars.forEach(bar => {
        const width = parseFloat(bar.style.width);
        if (width >= 90) bar.style.backgroundColor = '#00ff00';
        else if (width >= 70) bar.style.backgroundColor = '#ffcc00';
        else bar.style.backgroundColor = '#ff0000';
    });

    // Auto-active functionality for nav items (simple demo)
    const navItems = document.querySelectorAll('.nav-item');
    navItems.forEach(item => {
        item.addEventListener('click', (e) => {
            // Prevent default if href=#
            if (item.getAttribute('href') === '#') e.preventDefault();

            navItems.forEach(n => n.classList.remove('active'));
            item.classList.add('active');
        });
    });
});
