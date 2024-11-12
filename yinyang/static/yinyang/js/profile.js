document.addEventListener('DOMContentLoaded', () => {
  const tooltips = document.querySelectorAll('[data-bs-toggle="tooltip"]');
  tooltips.forEach((tooltip) => {
    new bootstrap.Tooltip(tooltip);
  });

  document.getElementById('edit-image-btn').onclick = () => {
    const editProfileImageModal = document.getElementById('edit-image-modal');
    const myModal = new bootstrap.Modal( editProfileImageModal);
    myModal.show();
  }
});



