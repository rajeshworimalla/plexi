
  // Get modal element
  const modal = document.getElementById('filter-modal');
  // Get open modal button
  const openModalBtn = document.getElementById('open-filter-modal');
  // Get close button
  const closeButton = document.querySelector('.close-button');

  // Open modal
  openModalBtn.addEventListener('click', () => {
    modal.style.display = 'block';
  });

  // Close modal
  closeButton.addEventListener('click', () => {
    modal.style.display = 'none';
  });

  // Close modal when clicking outside of it
  window.addEventListener('click', (event) => {
    if (event.target === modal) {
      modal.style.display = 'none';
    }
  });
