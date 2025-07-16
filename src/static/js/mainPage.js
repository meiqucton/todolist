document.addEventListener('DOMContentLoaded', () => {
    
    // --- KHAI BÁO BIẾN ---
    const modal = document.getElementById('auth-modal');
    const loginTab = document.getElementById('login-tab');
    const registerTab = document.getElementById('register-tab');
    const loginForm = document.getElementById('login-form');
    const registerForm = document.getElementById('register-form');

    // --- SMOOTH SCROLL CHO CÁC LIÊN KẾT NAV ---
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const targetId = this.getAttribute('href');
            const targetElement = document.querySelector(targetId);

            if (targetElement) {
                // Tạm thời bỏ active class ở tất cả các link
                document.querySelectorAll('.header__nav a').forEach(link => link.classList.remove('active'));
                // Thêm active class cho link được click
                this.classList.add('active');
                
                const headerOffset = document.querySelector('.header').offsetHeight;
                const elementPosition = targetElement.getBoundingClientRect().top;
                const offsetPosition = elementPosition + window.pageYOffset - headerOffset;

                window.scrollTo({
                    top: offsetPosition,
                    behavior: "smooth"
                });
            }
        });
    });

    // --- CÁC HÀM ĐIỀU KHIỂN MODAL ---
    window.showAuthModal = (showRegisterForm = false) => {
        modal.style.display = 'block';
        document.body.style.overflow = 'hidden'; // Ngăn cuộn trang nền
        if (showRegisterForm) {
            switchForm('register');
        } else {
            switchForm('login');
        }
    };

    window.hideAuthModal = () => {
        modal.style.display = 'none';
        document.body.style.overflow = 'auto';
    };

    // --- HÀM CHUYỂN ĐỔI FORM ---
    window.switchForm = (formName) => {
        const isLogin = formName === 'login';
        
        loginTab.classList.toggle('active', isLogin);
        registerTab.classList.toggle('active', !isLogin);
        loginForm.classList.toggle('active', isLogin);
        registerForm.classList.toggle('active', !isLogin);
    };

    // --- CÁC EVENT LISTENER ---
    // Đóng modal khi click ra ngoài
    window.addEventListener('click', (event) => {
        if (event.target === modal) {
            hideAuthModal();
        }
    });

    // Đóng modal khi nhấn phím Escape
    window.addEventListener('keydown', (event) => {
        if (event.key === 'Escape') {
            hideAuthModal();
        }
    });

    // Tự động đóng flash messages sau 5 giây
    setTimeout(() => {
        document.querySelectorAll('.flash-message').forEach(msg => {
            msg.style.transition = 'opacity 0.5s ease, transform 0.5s ease';
            msg.style.opacity = '0';
            msg.style.transform = 'translateX(20px)';
            setTimeout(() => msg.remove(), 500);
        });
    }, 5000);

});