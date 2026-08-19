# BÁO CÁO KỸ THUẬT: STRESS TEST & CHAMPION-CHALLENGER (TUẦN 6)

## 1. Mục tiêu (Objective)
Stress Test kiểm tra khung đo lường A/B Testing và mô hình thống kê có phản ứng phù hợp với lý thuyết trong các synthetic scenarios đã thiết kế hay không. Kiến trúc Champion-Challenger minh họa cách một candidate policy có thể được kiểm chứng công bằng với baseline rule-based trong pilot tương lai.

## 2. Các Kịch bản Stress Test đã thực hiện
Dự án sử dụng mô phỏng Monte Carlo để đưa pipeline phân tích qua các kịch bản đã chọn:

1. **Kiểm tra Kích thước mẫu (Sample Size Scale-up):**
   - **Kịch bản:** Khảo sát ATE khi mẫu tăng từ 10.000 lên 50.000 và 100.000.
   - **Kết quả:** Con số ATE cốt lõi duy trì ổn định không đổi, nhưng khoảng tin cậy (Confidence Interval) ngày càng hội tụ và thu hẹp, chứng minh tính nhất quán tiệm cận (asymptotic consistency) của thuật toán OLS HC1.

2. **Kiểm tra A/A Test (False Positive Check):**
   - **Kịch bản:** Ép True Effect = 0 (Giả lập Voucher bị lỗi không có tác dụng).
   - **Kết quả:** Ước lượng ATE tập trung quanh 0 qua nhiều lần chạy. False Positive Rate là 5,08%, gần mức alpha 5% đã thiết kế.

3. **Kiểm tra Tỷ lệ chia mẫu lệch (Imbalanced Treatment Ratio):**
   - **Kịch bản:** Ép tỷ lệ chia nhóm Control/Treatment thành 90/10 thay vì 50/50.
   - **Kết quả:** Với tỷ lệ 90/10, ước lượng có thể dao động đáng kể trong một lần chạy. Rủi ro chính là phương sai lớn hơn và statistical power thấp hơn khi nhóm Treatment bị mỏng đi.

4. **Kiểm tra Bơm Nhiễu (Gaussian Noise Injection):**
   - **Kịch bản:** Bơm thêm độ nhiễu loạn ngẫu nhiên vào biến mục tiêu (Mô phỏng yếu tố thời tiết, kẹt xe...).
   - **Kết quả:** Nhiễu ngoại sinh làm tăng uncertainty và làm yếu tín hiệu. Theo kỳ vọng qua nhiều lần randomization, nhiễu không tạo directional bias có hệ thống, nhưng một lần chạy riêng lẻ vẫn có thể dao động.

## 3. Kiến trúc Đấu trường (Champion-Challenger Architecture)
Để kiểm chứng liệu AI Profit Targeting (Challenger) có vượt phương pháp truyền thống (Champion), dự án phác thảo thiết kế A/B/C Test cho một pilot tương lai. Thiết kế này chưa phải kế hoạch production đã được phê duyệt:

- **Group A (Holdout - 10%):** Không nhận Voucher. Dùng để làm Base Control đo lường Incremental Baseline cho cả 2 nhóm còn lại.
- **Group B (Champion - 45%):** Áp dụng Segment Targeting. (Ví dụ: Chỉ phát cho tệp Suburban dựa trên rule-based persona).
- **Group C (Challenger - 45%):** Áp dụng AI Profit Targeting bằng simplified R-Learner-style residual model, chỉ phát cho user có $EV > 0$.

**Luật quyết định:** Chỉ cân nhắc mở rộng traffic cho Group C nếu Incremental Profit cao hơn Group B với ý nghĩa thống kê và guardrail không xấu đi; không tự động rollout 100%.

## 4. Kết luận Vững chắc
Khung đánh giá Causal Inference và A/B Testing không bộc lộ sai số cấu trúc rõ ràng trong các synthetic scenarios đã thử. Kết luận này chỉ có phạm vi trong DGP và stress settings hiện tại.

Hệ thống hiện tại là synthetic sandbox, chưa production-ready. Bước tiếp theo là hoàn thiện experiment contract và chạy **Randomized Real-world Validation** trên dữ liệu GSM thật trước mọi quyết định mở rộng.
