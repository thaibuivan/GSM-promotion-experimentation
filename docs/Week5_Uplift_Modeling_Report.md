# BÁO CÁO KỸ THUẬT TUẦN 7: UPLIFT MODELING

### 1. Mục tiêu
Áp dụng thuật toán Machine Learning (Uplift Modeling) để xác định chính xác những cá nhân nào trong nhóm khách hàng bị lỗ nặng (Urban Cash) có khả năng sinh lời nếu được tặng Voucher. Mục tiêu là chuyển từ câu hỏi "Khách hàng nào sẽ đi xe?" sang "Khách hàng nào sẽ ĐI THÊM nhờ có Voucher?".

### 2. Phương pháp & Mô hình
- **Thuật toán:** R-Learner (Residual Learner) kết hợp với XGBoost Regressor.
- **Dữ liệu:** Chia tập Train (60%), Validation (20%) có sử dụng Early Stopping (chống Overfitting), và Test (20%).
- **Chỉ số CATE (Conditional Average Treatment Effect):** Lấy kết quả dự đoán khi có mã (Treatment Model) trừ đi kết quả dự đoán khi không có mã (Control Model).

### 3. Đánh giá Mô hình (Model Evaluation)
- **Qini Curve & AUUC:** Đường Qini Curve của R-Learner vồng lên rõ rệt so với đường ngẫu nhiên (Random Allocation), chứng tỏ mô hình có khả năng xếp hạng (Ranking) rất tốt những người có độ nhạy cảm cao với khuyến mãi.

### 4. Đánh giá Lợi nhuận Kinh doanh (Business Evaluation)
- Hệ thống tự động quét qua các ngưỡng cắt (Top 10%, 20%, 30%...) để tìm đỉnh lợi nhuận.
- **Phát hiện quan trọng:** Ngay cả khi tối ưu hóa, việc phát Voucher cho nhóm này vẫn gây lỗ. 
- **Ngưỡng hòa vốn (Break-even CATE):** Với chi phí Voucher là 15,000 VND và biên lợi nhuận 20,000 VND, khách hàng phải đạt CATE > 0.75 chuyến mới có lãi. Tập Urban Cash không có bất kỳ ai vượt qua được ngưỡng này.
- **Kết luận:** Mô hình khuyên ngừng hoàn toàn chiến dịch cho nhóm Urban Cash để bảo toàn vốn.

---
