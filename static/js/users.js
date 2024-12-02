
// Add interactivity to toggle dropdown visibility
document.querySelectorAll('.three-dots').forEach(button => {
  button.addEventListener('click', (event) => {
    const dropdown = event.target.nextElementSibling;
    dropdown.classList.toggle('show');
  });
});

// Close dropdown if clicked outside
window.addEventListener('click', (event) => {
  if (!event.target.matches('.three-dots')) {
    document.querySelectorAll('.dropdown-menu').forEach(menu => {
      menu.classList.remove('show');
    });
  }
});
