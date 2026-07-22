# Tiêu chuẩn Cấp phép Triển khai & Hệ thống A/A Testing (The Trust Checklist)

Đây là tài liệu đánh giá sức khỏe của toàn bộ quy trình thiết kế và hệ thống phân bổ ngẫu nhiên (Randomization Pipeline). Dựa theo khuyến nghị của Ch.19 (Trustworthy Online Controlled Experiments), mọi hệ thống Experimentation đều phải vượt qua bài test A/A Testing trước khi được cấp phép tiến hành các chiến dịch A/B Testing thật sự (như tặng Voucher).

---

## 1. Mục tiêu (Objective)
- Đảm bảo rằng cơ chế Randomization hoàn toàn vô tư, không bị lỗi kỹ thuật, và phân chia khách hàng một cách đồng đều.
- Đảm bảo rằng các chỉ số bảo vệ (Invariant Metrics / Covariates) không bị thay đổi ngầm.
- Chứng minh rằng Tỷ lệ Cảnh báo giả (False Positive Rate) của hệ thống thống kê chính xác ở mức 5% (Mức ý nghĩa $\alpha = 0.05$).

## 2. Các Bài Test Đánh Giá (The A/A Simulation Results)
Chúng tôi đã sử dụng phương pháp Mô phỏng Monte Carlo để giả lập phân bổ ngẫu nhiên A/A Test 1000 lần liên tiếp trên tệp khách hàng mục tiêu `Suburban Commuters`.

### 2.1. Kiểm tra Lỗi Cân bằng Mẫu (Sample Ratio Mismatch - SRM Check)
- **Kiểm định sử dụng:** Chi-Square ($X^2$) Goodness-of-Fit Test.
- **Tiêu chuẩn (Expected):** Tỷ lệ chênh lệch số lượng User giữa 2 nhóm phải bám sát mức lý tưởng 50/50. Số lần P-value < 0.05 không được vượt quá ~5%.
- **Kết quả thực tế (Observed):** Mô phỏng cho thấy tỷ lệ lỗi SRM xoay quanh mốc 5%.
- **Kết luận:** ✅ ĐẠT (PASS). Thuật toán Hash/Randomization hoạt động hoàn hảo, không có bug kỹ thuật đẩy dư thừa User vào bất kỳ nhóm nào.

### 2.2. Kiểm tra Độ Cân Bằng Đặc Trưng (Covariate Balance)
- **Kiểm định sử dụng:** Independent T-Test (P-value > 0.05).
- **Tiêu chuẩn:** Tuổi trung bình (`age`) và Hành vi đặt xe trong lịch sử (`monthly_rides_history`) phải gần như giống hệt nhau ở cả 2 nhóm.
- **Kết quả thực tế:** Tuần 4 và Tuần 5 đều cho thấy P-value của các chỉ số này > 0.05.
- **Kết luận:** ✅ ĐẠT (PASS). Hệ thống không thiên vị (Bias) ngầm đối với bất kỳ nhóm khách hàng cụ thể nào.

### 2.3. Kiểm định Hành vi P-value (P-Value Uniformity Test)
- **Kiểm định sử dụng:** Kolmogorov-Smirnov (KS-test) để so sánh phân phối P-value của Metric (Số chuyến xe) với đường Phân phối đều (Uniform Distribution).
- **Tiêu chuẩn:** Phân phối P-value từ 1000 lần A/A test phải tạo thành một hình chữ nhật phẳng. Cụ thể, tỷ lệ các trường hợp có P-value < 0.05 (False Positive Rate) phải xấp xỉ đúng 5%.
- **Kết quả thực tế:** 
  - Biểu đồ Histogram tạo thành đường phẳng như mức kỳ vọng.
  - Tỷ lệ False Positive Rate (FPR) xoay quanh mốc 5%.
  - KS-Test P-value > 0.05.
- **Kết luận:** ✅ ĐẠT (PASS). Pipeline tính toán T-test của chúng ta hoàn toàn đáng tin cậy. Nếu sau này chúng ta phát hiện ra một sự khác biệt (P-value < 0.05) trong A/B Test, chúng ta có thể tự tin 95% rằng đó là tác động THỰC SỰ của Voucher chứ không phải do lỗi hệ thống.

---

## 3. Kết luận Cuối cùng (Final Verdict)
Hệ thống Experimentation Pipeline đã chính thức VƯỢT QUA toàn bộ các bài "Stress-test".

🚀 **Trạng thái hệ thống:** SẴN SÀNG (TRUSTWORTHY).
Đội ngũ hoàn toàn tự tin mang kết quả A/B Test (ROI và OEC) của chiến dịch Khuyến mãi Voucher vào báo cáo cuối kỳ để thuyết phục Ban Giám Đốc triển khai Roll-out.
