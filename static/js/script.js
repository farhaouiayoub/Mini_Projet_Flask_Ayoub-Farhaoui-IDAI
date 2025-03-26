// Form validation and UI enhancements
document.addEventListener('DOMContentLoaded', function() {
    // Form validation
    const forms = document.querySelectorAll('form');
    
    forms.forEach(form => {
        form.addEventListener('submit', function(event) {
            const passwordField = form.querySelector('input[name="password"]');
            const confirmPasswordField = form.querySelector('input[name="confirm_password"]');
            
            // Password confirmation validation for registration
            if (passwordField && confirmPasswordField) {
                if (passwordField.value !== confirmPasswordField.value) {
                    event.preventDefault();
                    showToast('Passwords do not match!', 'danger');
                }
            }
            
            // Edit profile form validation
            if (form.id === 'edit-profile-form') {
                const newPasswordField = form.querySelector('#new_password');
                const confirmNewPasswordField = form.querySelector('#confirm_password');
                
                if (newPasswordField && confirmNewPasswordField) {
                    // Only validate if a new password is being set
                    if (newPasswordField.value && newPasswordField.value !== confirmNewPasswordField.value) {
                        event.preventDefault();
                        showToast('New passwords do not match!', 'danger');
                    }
                }
            }
        });
    });
    
    // Auto-hide alerts after 5 seconds
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(alert => {
        setTimeout(() => {
            if (alert) {
                const closeButton = alert.querySelector('.close');
                if (closeButton) closeButton.click();
            }
        }, 5000);
    });
    
    // Add animation to cards
    document.querySelectorAll('.card').forEach(card => {
        card.classList.add('fade-in');
    });
    
    // Password strength meter
    const passwordInputs = document.querySelectorAll('input[type="password"]');
    passwordInputs.forEach(input => {
        if (input.id === 'password' || input.id === 'new_password') {
            input.addEventListener('input', function() {
                checkPasswordStrength(this);
            });
        }
    });
});

// Function to show toast notifications
function showToast(message, type) {
    // Create toast container if it doesn't exist
    let toastContainer = document.querySelector('.toast-container');
    if (!toastContainer) {
        toastContainer = document.createElement('div');
        toastContainer.className = 'toast-container position-fixed top-0 end-0 p-3';
        document.body.appendChild(toastContainer);
    }
    
    // Create toast element
    const toast = document.createElement('div');
    toast.className = `toast bg-${type} text-white`;
    toast.setAttribute('role', 'alert');
    toast.setAttribute('aria-live', 'assertive');
    toast.setAttribute('aria-atomic', 'true');
    
    toast.innerHTML = `
        <div class="toast-header bg-${type} text-white">
            <strong class="me-auto">Notification</strong>
            <button type="button" class="btn-close btn-close-white" data-dismiss="toast" aria-label="Close"></button>
        </div>
        <div class="toast-body">
            ${message}
        </div>
    `;
    
    toastContainer.appendChild(toast);
    
    // Initialize and show toast
    $(toast).toast({
        delay: 5000
    });
    $(toast).toast('show');
    
    // Remove toast when hidden
    $(toast).on('hidden.bs.toast', function() {
        toast.remove();
    });
}

// Check password strength
function checkPasswordStrength(inputElement) {
    const password = inputElement.value;
    let strength = 0;
    let strengthText = '';
    let strengthClass = '';
    
    // If password field is empty, remove any existing strength meter
    if (password.length === 0) {
        const existingMeter = inputElement.parentElement.querySelector('.password-strength');
        if (existingMeter) existingMeter.remove();
        return;
    }
    
    // Length check
    if (password.length >= 8) {
        strength += 1;
    }
    
    // Contains uppercase
    if (password.match(/[A-Z]/)) {
        strength += 1;
    }
    
    // Contains lowercase
    if (password.match(/[a-z]/)) {
        strength += 1;
    }
    
    // Contains numbers
    if (password.match(/[0-9]/)) {
        strength += 1;
    }
    
    // Contains special characters
    if (password.match(/[^a-zA-Z0-9]/)) {
        strength += 1;
    }
    
    // Set strength text and class
    switch(strength) {
        case 0:
        case 1:
            strengthText = 'Weak';
            strengthClass = 'bg-danger';
            break;
        case 2:
        case 3:
            strengthText = 'Medium';
            strengthClass = 'bg-warning';
            break;
        case 4:
        case 5:
            strengthText = 'Strong';
            strengthClass = 'bg-success';
            break;
    }
    
    // Remove any existing strength meter
    const existingMeter = inputElement.parentElement.querySelector('.password-strength');
    if (existingMeter) existingMeter.remove();
    
    // Create and append strength meter
    const strengthMeter = document.createElement('div');
    strengthMeter.className = 'password-strength mt-2';
    strengthMeter.innerHTML = `
        <div class="progress" style="height: 5px;">
            <div class="progress-bar ${strengthClass}" role="progressbar" 
                style="width: ${(strength / 5) * 100}%" 
                aria-valuenow="${(strength / 5) * 100}" 
                aria-valuemin="0" 
                aria-valuemax="100">
            </div>
        </div>
        <small class="mt-1 ${strengthClass.replace('bg-', 'text-')}">${strengthText} password</small>
    `;
    
    inputElement.parentElement.appendChild(strengthMeter);
}
