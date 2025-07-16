document.addEventListener('DOMContentLoaded', function() {
    // Khởi tạo Flatpickr cho các input ngày giờ
    flatpickr(".datetime-picker", {
        enableTime: true,        // Cho phép chọn cả giờ
        dateFormat: "Y-m-d H:i", // Định dạng ngày tháng năm giờ:phút
        time_24hr: true,         // Sử dụng định dạng 24 giờ
        altInput: true,          // Hiển thị một input khác thân thiện hơn cho người dùng
        altFormat: "d/m/Y - H:i", // Định dạng hiển thị trong input thân thiện
        minDate: "today",        // Ngày nhỏ nhất có thể chọn là hôm nay
        // locale: "vn" // Bạn cần tải thêm file locale tiếng Việt cho Flatpickr nếu muốn dùng
    });

    // (Tùy chọn) Thêm hiệu ứng cho các thẻ công việc khi rê chuột vào
    const taskCards = document.querySelectorAll('.task-card');
    taskCards.forEach(card => {
        card.addEventListener('mouseenter', () => {
            card.style.transform = 'translateY(-5px)';
            card.style.boxShadow = '0 8px 15px rgba(0, 0, 0, 0.1)';
        });
        card.addEventListener('mouseleave', () => {
            card.style.transform = 'translateY(0)';
            card.style.boxShadow = 'var(--box-shadow)';
        });
    });
});