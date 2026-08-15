# BÁO CÁO KỸ THUẬT: STRESS TEST & CHAMPION-CHALLENGER (TUẦN 6)

## 1. Mục tiêu (Objective)
Stress Test đóng vai trò là "Lá chắn thép" để kiểm tra tính bền vững (Robustness) của khung đo lường A/B Testing và mô hình thống kê trước khi mang ra áp dụng thực tế ở quy mô lớn, đối mặt với các điều kiện dữ liệu khắc nghiệt. Bên cạnh đó, việc thiết kế mô phỏng kiến trúc Champion-Challenger giúp chứng minh phương pháp tiếp cận mới (AI Targeting) hoàn toàn có thể triển khai song song và cạnh tranh công bằng với quy trình hiện tại (Baseline Rule-based).

## 2. Các Kịch bản Stress Test đã thực hiện
Dự án đã sử dụng phương pháp mô phỏng Monte Carlo để đưa 파peline phân tích qua các kịch bản khắc nghiệt nhất:

1. **Kiểm tra Kích thước mẫu (Sample Size Scale-up):**
   - **Kịch bản:** Khảo sát ATE khi mẫu tăng từ 10.000 lên 50.000 và 100.000.
   - **Kết quả:** Con số ATE cốt lõi duy trì ổn định không đổi, nhưng khoảng tin cậy (Confidence Interval) ngày càng hội tụ và thu hẹp, chứng minh tính nhất quán tiệm cận (asymptotic consistency) của thuật toán OLS HC1.

2. **Kiểm tra A/A Test (False Positive Check):**
   - **Kịch bản:** Ép True Effect = 0 (Giả lập Voucher bị lỗi không có tác dụng).
   - **Kết quả:** Hệ thống báo cáo ATE xoay quanh 0 và P-value > 0.05. Tỷ lệ báo động giả (False Positive Rate) duy trì chính xác ở mức ~5%, chứng minh hệ thống không bị "thiên kiến" (bias) hay ghi nhận false positive.

3. **Kiểm tra Tỷ lệ chia mẫu lệch (Imbalanced Treatment Ratio):**
   - **Kịch bản:** Ép tỷ lệ chia nhóm Control/Treatment thành 90/10 thay vì 50/50.
   - **Kết quả:** ATE đo được vẫn chính xác và hội tụ về đúng Ground-truth. Tuy nhiên, phương sai (Variance) cao hơn do mẫu Treatment bị mỏng đi, cảnh báo về rủi ro thiếu Power nếu thu hẹp mẫu.

4. **Kiểm tra Bơm Nhiễu (Gaussian Noise Injection):**
   - **Kịch bản:** Bơm thêm độ nhiễu loạn ngẫu nhiên vào biến mục tiêu (Mô phỏng yếu tố thời tiết, kẹt xe...).
   - **Kết quả:** ATE đo được không bị sai lệch. Cơ chế ngẫu nhiên hóa (Randomization) của A/B Test giúp cân bằng exogenous noise một cách hoàn hảo theo kỳ vọng, mặc dù noise làm tăng uncertainty của estimator ở cả 2 nhóm.

## 3. Kiến trúc Đấu trường (Champion-Challenger Architecture)
Để chứng minh AI Profit Targeting (Challenger) vượt trội hơn phương pháp truyền thống (Champion), dự án đã phác thảo thiết kế A/B/C Test thực tiễn (Pilot Validation Setup) có thể triển khai ngay trên hệ thống thật:

- **Group A (Holdout - 10%):** Không nhận Voucher. Dùng để làm Base Control đo lường Incremental Baseline cho cả 2 nhóm còn lại.
- **Group B (Champion - 45%):** Áp dụng Segment Targeting. (Ví dụ: Chỉ phát cho tệp Suburban dựa trên rule-based persona).
- **Group C (Challenger - 45%):** Áp dụng AI Profit Targeting. (Sử dụng R-Learner để chấm điểm toàn bộ users, chỉ phát cho user có $EV > 0$).

**Luật quyết định (Rollout Decision):** Sẽ rollout (áp dụng 100%) Group C (AI) nếu Lợi nhuận gộp tăng thêm (Incremental Profit) của Group C cao hơn Group B với ý nghĩa thống kê (p-value < 0.05).

## 4. Kết luận Vững chắc
Khung đánh giá Causal Inference và A/B Testing của dự án đã vượt qua tất cả các bài Stress Test. Không có sai số mang tính cấu trúc nào được phát hiện trong các kịch bản mô phỏng.

Mặc dù hệ thống hiện tại là một môi trường giả lập (Synthetic Sandbox), kiến trúc đo lường và quy trình ra quyết định đã được thiết kế sẵn sàng cho môi trường Production. Bước tiếp theo là đưa Candidate Policy này vào **Randomized Real-world Validation (A/B Test thật)** để khẳng định mức độ hiệu quả cuối cùng trên người dùng GSM.
