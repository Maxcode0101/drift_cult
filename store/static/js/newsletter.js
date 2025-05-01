document.addEventListener('DOMContentLoaded', function() {
    const newsletterForm = document.getElementById('newsletter-form');
    const modalForm = document.getElementById('newsletter-modal-form');
  
    // Handle homepage form
    if (newsletterForm) {
      newsletterForm.addEventListener('submit', function(e) {
        e.preventDefault();
        const email = document.getElementById('newsletter-email').value;
        submitNewsletter(email, 'newsletter-success');
      });
    }
  
    // Handle modal form
    if (modalForm) {
      modalForm.addEventListener('submit', function(e) {
        e.preventDefault();
        const email = document.getElementById('modal-newsletter-email').value;
        submitNewsletter(email, null);
        const modal = bootstrap.Modal.getInstance(document.getElementById('newsletterModal'));
        modal.hide();
      });
    }
  
    function submitNewsletter(email, successElementId) {
      fetch('/newsletter-signup/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/x-www-form-urlencoded',
          'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
        },
        body: `email=${encodeURIComponent(email)}`
      })
      .then(response => response.json())
      .then(data => {
        if (data.success && successElementId) {
          document.getElementById(successElementId).classList.remove('d-none');
        }
      });
    }
  
    // Modal popup logic
    if (!localStorage.getItem('newsletterModalShown')) {
      setTimeout(() => {
        const modal = new bootstrap.Modal(document.getElementById('newsletterModal'));
        modal.show();
        localStorage.setItem('newsletterModalShown', 'true');
      }, 5000); // Show after 5 seconds
    }
  });
  