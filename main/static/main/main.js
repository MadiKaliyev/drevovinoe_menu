function toggleMenu(event, id) {
    event.preventDefault();
    const submenu = document.getElementById(`menu-${id}`);
    if (submenu) {
        submenu.style.display = submenu.style.display === 'none' ? 'block' : 'none';
    }
}
