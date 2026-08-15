# BÁO CÁO KỸ THUẬT: STRESS TEST & KIỂM ĐỊNH TÍNH VỮNG

### 1. Mục tiêu
Stress Test đóng vai trò là "Lá chắn thép" để kiểm tra tính bền vững (Robustness) của khung đo lường A/B Testing và mô hình thống kê trước khi mang ra áp dụng thực tế ở quy mô lớn, đối mặt với các điều kiện dữ liệu khắc nghiệt.

### 2. Các Kịch bản Stress Test đã thực hiện
1. **Kiểm tra Kích thước mẫu (Sample Size Scale-up):**
   - **Thao tác:** Khảo sát ATE khi mẫu tăng từ 10.000 lên 50.000 và 100.000.
   - **Kết quả:** Con số ATE cốt lõi (Effect size) duy trì ổn định không đổi, nhưng P-value (Độ tin cậy) ngày càng mạnh và Khoảng tin cậy (Confidence Interval) ngày càng hội tụ. 
2. **Kiểm tra A/A Test (False Positive Check):**
   - **Thao tác:** Ép True Effect = 0 (Giả lập Voucher bị lỗi không có tác dụng).
   - **Kết quả:** Hệ thống báo cáo ATE xoay quanh 0 và P-value > 0.05, không bị đánh lừa (Không có False Positive).
3. **Kiểm tra Tỷ lệ chia mẫu lệch (Imbalanced Treatment Ratio):**
   - **Thao tác:** Ép tỷ lệ chia nhóm Control/Treatment thành 90/10 thay vì 50/50.
   - **Kết quả:** ATE đo được vẫn chính xác, mặc dù phương sai (Variance) cao hơn do mẫu Treatment bị mỏng đi.
4. **Kiểm tra Bơm Nhiễu (Gaussian Noise Injection):**
   - **Thao tác:** Bơm thêm độ nhiễu loạn ngẫu nhiên vào biến mục tiêu (Mô phỏng yếu tố thời tiết, kẹt xe...).
   - **Kết quả:** ATE đo được có sai số không đáng kể. Cơ chế ngẫu nhiên hóa (Randomization) của A/B Test đã tự động triệt tiêu các yếu tố nhiễu ở cả 2 nhóm.

### 3. Kết luận
Khung đánh giá Causal Inference và A/B Testing của dự án đã vượt qua tất cả các bài Stress Test. Mặc dù các Stress tests chưa phát hiện failure nghiêm trọng trong các scenarios đã kiểm tra, hệ thống hiện tại vẫn là một môi trường giả lập (Synthetic Sandbox). Quá trình Real-world Deployment thực tế vẫn cần phải tiến hành Randomized Production Validation (A/B Test thật) để khẳng định mức độ hiệu quả cuối cùng.

---
