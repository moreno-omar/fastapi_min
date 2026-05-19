/* Form Validation and Submission Handler */

document.addEventListener('DOMContentLoaded', function() {
    const contactForm = document.getElementById('contactForm');
    
    if (contactForm) {
        contactForm.addEventListener('submit', function(e) {
            e.preventDefault();
            
            // Clear previous errors
            clearErrors();
            
            // Validate form
            if (validateForm()) {
                // If valid, submit the form
                this.submit();
            }
        });
        
        // Real-time validation
        document.getElementById('name')?.addEventListener('blur', validateName);
        document.getElementById('email')?.addEventListener('blur', validateEmail);
        document.getElementById('subject')?.addEventListener('blur', validateSubject);
        document.getElementById('message')?.addEventListener('blur', validateMessage);
    }
});

function validateForm() {
    let isValid = true;
    
    isValid &= validateName();
    isValid &= validateEmail();
    isValid &= validateSubject();
    isValid &= validateMessage();
    
    return isValid;
}

function validateName() {
    const nameInput = document.getElementById('name');
    const nameError = document.getElementById('nameError');
    const name = nameInput.value.trim();
    
    if (name.length === 0) {
        showError(nameError, 'Name is required');
        return false;
    }
    
    if (name.length < 2) {
        showError(nameError, 'Name must be at least 2 characters');
        return false;
    }
    
    if (name.length > 100) {
        showError(nameError, 'Name must not exceed 100 characters');
        return false;
    }
    
    clearError(nameError);
    return true;
}

function validateEmail() {
    const emailInput = document.getElementById('email');
    const emailError = document.getElementById('emailError');
    const email = emailInput.value.trim();
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    
    if (email.length === 0) {
        showError(emailError, 'Email is required');
        return false;
    }
    
    if (!emailRegex.test(email)) {
        showError(emailError, 'Please enter a valid email address');
        return false;
    }
    
    clearError(emailError);
    return true;
}

function validateSubject() {
    const subjectInput = document.getElementById('subject');
    const subjectError = document.getElementById('subjectError');
    const subject = subjectInput.value.trim();
    
    if (subject.length === 0) {
        showError(subjectError, 'Subject is required');
        return false;
    }
    
    if (subject.length < 3) {
        showError(subjectError, 'Subject must be at least 3 characters');
        return false;
    }
    
    if (subject.length > 200) {
        showError(subjectError, 'Subject must not exceed 200 characters');
        return false;
    }
    
    clearError(subjectError);
    return true;
}

function validateMessage() {
    const messageInput = document.getElementById('message');
    const messageError = document.getElementById('messageError');
    const message = messageInput.value.trim();
    
    if (message.length === 0) {
        showError(messageError, 'Message is required');
        return false;
    }
    
    if (message.length < 10) {
        showError(messageError, 'Message must be at least 10 characters');
        return false;
    }
    
    if (message.length > 5000) {
        showError(messageError, 'Message must not exceed 5000 characters');
        return false;
    }
    
    clearError(messageError);
    return true;
}

function showError(element, message) {
    if (element) {
        element.textContent = message;
        element.style.display = 'block';
    }
}

function clearError(element) {
    if (element) {
        element.textContent = '';
        element.style.display = 'none';
    }
}

function clearErrors() {
    const errorElements = document.querySelectorAll('.error-message');
    errorElements.forEach(element => {
        clearError(element);
    });
}
