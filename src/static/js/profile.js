document.addEventListener('DOMContentLoaded', function() {

    // --- DOM Elements ---
    const infoForm = document.getElementById('update-info-form');
    const passwordForm = document.getElementById('update-password-form');
    const flashContainer = document.getElementById('flash-message-container');
    
    // Display elements
    const displayUsername = document.getElementById('display-username');
    const displayEmail = document.getElementById('display-email');
    const avatarInitials = document.getElementById('avatar-initials');

    // Input elements
    const usernameInput = document.getElementById('username');
    const emailInput = document.getElementById('email');

    // --- Initial Setup ---
    function updateDisplay(username, email) {
        displayUsername.textContent = username;
        displayEmail.textContent = email;
        if (username) {
            avatarInitials.textContent = username.charAt(0).toUpperCase();
        }
    }
    
    // Initialize display with form values
    updateDisplay(usernameInput.value, emailInput.value);

    // --- Flash Message Logic ---
    function showFlashMessage(message, type = 'success') {
        flashContainer.textContent = message;
        flashContainer.className = `flash-message ${type}`;
        
        // Scroll to top to make it visible
        window.scrollTo({ top: 0, behavior: 'smooth' });

        // Hide after 3 seconds
        setTimeout(() => {
            flashContainer.style.display = 'none';
        }, 3000);
    }

    // --- Form Handlers ---

    // Handle user information update
    infoForm.addEventListener('submit', function(e) {
        e.preventDefault();

        const newUsername = usernameInput.value.trim();
        const newEmail = emailInput.value.trim();

        // Basic validation
        if (newUsername.length < 3) {
            showFlashMessage('Tên người dùng phải có ít nhất 3 ký tự!', 'error');
            return;
        }

        // Simulate API call
        console.log('Updating info to:', { username: newUsername, email: newEmail });
        
        // Update UI
        updateDisplay(newUsername, newEmail);
        showFlashMessage('Cập nhật thông tin thành công!', 'success');
    });

    // Handle password update
    passwordForm.addEventListener('submit', function(e) {
        e.preventDefault();

        const currentPassword = document.getElementById('current_password').value;
        const newPassword = document.getElementById('new_password').value;
        const confirmPassword = document.getElementById('confirm_password').value;

        // Basic validation
        if (!currentPassword || !newPassword || !confirmPassword) {
            showFlashMessage('Vui lòng điền đầy đủ các trường mật khẩu!', 'error');
            return;
        }

        if (newPassword.length < 6) {
            showFlashMessage('Mật khẩu mới phải có ít nhất 6 ký tự!', 'error');
            return;
        }
        
        if (newPassword !== confirmPassword) {
            showFlashMessage('Mật khẩu mới và xác nhận mật khẩu không khớp!', 'error');
            return;
        }

        // Simulate API call
        console.log('Updating password...');
        
        // Reset form and show success message
        passwordForm.reset();
        showFlashMessage('Đổi mật khẩu thành công!', 'success');
    });
});