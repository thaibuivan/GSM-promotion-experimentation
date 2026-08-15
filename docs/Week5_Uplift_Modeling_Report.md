# BÁO CÁO KỸ THUẬT: UPLIFT MODELING

### 1. Mục tiêu
Áp dụng thuật toán Machine Learning (Uplift Modeling) để xác định chính xác những cá nhân nào trong tập khách hàng có khả năng sinh lời cao nhất nếu được tặng Voucher. Mục tiêu là chuyển từ câu hỏi "Khách hàng nào sẽ đi xe?" sang "Khách hàng nào sẽ ĐI THÊM nhờ có Voucher?".

### 2. Phương pháp & Mô hình
- **Thuật toán:** R-Learner (Residual Learner) kết hợp với XGBoost Regressor.
- **Dữ liệu:** Chia tập Train (60%), Validation (20%), Test (20%); Test set được giữ riêng cho final evaluation. Validation split được reserved cho model selection/tuning.
- **Chỉ số CATE (Conditional Average Treatment Effect):** R-Learner không tính CATE bằng cách lấy mô hình Treatment trừ đi mô hình Control (T-Learner), mà trực tiếp dự đoán hiệu ứng nhân quả (Causal Effect) thông qua việc residualize cả kết quả (Outcome) và biến can thiệp (Treatment), giúp khử nhiễu (Base Outcome Bias) tốt hơn.

### 3. Đánh giá Mô hình (Model Evaluation)
- **Qini Curve & AUUC:** Đường Qini Curve của R-Learner vồng lên rõ rệt so với đường ngẫu nhiên (Random Allocation), chứng tỏ mô hình có khả năng xếp hạng (Ranking) rất tốt những người có độ nhạy cảm cao với khuyến mãi.
- **Calibration:** Mô hình phân loại tốt nhóm CATE cao (Uplift lớn) và CATE thấp, khớp với hiệu ứng nhân quả Ground-Truth CATE có trong môi trường mô phỏng (Synthetic Sandbox).

### 4. Đánh giá Lợi nhuận Kinh doanh (Business Evaluation)
- Hệ thống tự động quét qua các ngưỡng cắt (Top 10%, 20%, 30%...) để tìm cấu hình mang lại lợi nhuận biên cao nhất.
- **Profit Targeting:** Bằng cách chỉ phân phối Voucher cho những người có `Expected_Incremental_Profit > 0` (ngưỡng hòa vốn), chính sách Uplift Targeting tạo ra mức lợi nhuận tối ưu và giảm thiểu lãng phí ngân sách (Cannibalization) so với việc tặng đại trà (Mass Voucher).

---
