# Đánh giá Độ tin cậy Hệ thống & A/A Testing (Tuần 5)

## 1. Mục tiêu Đánh giá (Objective)
Trước khi đưa vào triển khai bất kỳ thí nghiệm A/B Testing nào, việc kiểm định tính ổn định của hệ thống phân bổ ngẫu nhiên (Randomization Pipeline) và công cụ phân tích thống kê là yêu cầu bắt buộc. Quá trình này được thực hiện thông qua A/A Testing — một thí nghiệm giả lập nơi không có bất kỳ sự can thiệp (Voucher) nào được áp dụng cho cả hai nhóm. 

Mục tiêu cốt lõi là xác minh Tỷ lệ Dương tính giả (False Positive Rate - Type I Error) của hệ thống hội tụ chính xác về mức lý thuyết ($\alpha = 0.05$), đồng thời đảm bảo không có sự thiên vị trong việc phân bổ mẫu.

## 2. Phương pháp Thực hiện (Methodology)
Dự án áp dụng phương pháp Mô phỏng Monte Carlo. Tập khách hàng mục tiêu (`Suburban Commuters`) được phân bổ ngẫu nhiên thành hai nhóm (A và A') qua 5.000 vòng lặp độc lập. Các chỉ số thống kê được ghi nhận ở mỗi vòng lặp để phân tích hành vi của hệ thống.

## 3. Các Chỉ số Đánh giá & Kết quả

### 3.1. Kiểm tra Lỗi Cân bằng Mẫu (Sample Ratio Mismatch - SRM)
- **Phương pháp:** Sử dụng Kiểm định Chi-Square ($X^2$) Goodness-of-Fit để đối chiếu quy mô mẫu thực tế với quy mô mẫu kỳ vọng (tỷ lệ 50/50).
- **Ngưỡng tiêu chuẩn:** Tỷ lệ số vòng lặp trả về P-value < 0.05 không được vượt quá xa mốc 5.0%.
- **Kết quả đo lường:** Tỷ lệ cảnh báo SRM trong 5.000 vòng lặp là 4.82%.
- **Kết luận:** ĐẠT (PASS). Thuật toán Hashing/Randomization hoạt động ổn định, không ghi nhận xu hướng phân bổ lệch trọng số.

### 3.2. Kiểm tra Độ Cân bằng Đặc trưng (Covariate Balance)
- **Phương pháp:** Sử dụng Independent T-Test để kiểm tra sự khác biệt của các biến hiệp phương sai trước thí nghiệm (như `age`, `monthly_rides_history`).
- **Ngưỡng tiêu chuẩn:** P-value liên tục duy trì ở mức > 0.05 qua các tập mẫu ngẫu nhiên.
- **Kết quả đo lường:** Hệ thống duy trì sự cân bằng đặc trưng ổn định, phân phối nền của các biến số tương đồng giữa hai nhóm.
- **Kết luận:** ĐẠT (PASS). Hệ thống loại trừ thành công các rủi ro liên quan đến Thiên kiến chọn mẫu (Selection Bias).

### 3.3. Kiểm tra Tỷ lệ Dương tính giả (False Positive Rate - FPR)
- **Phương pháp:** Đo lường tỷ lệ các vòng lặp A/A Test trả về P-value < 0.05. Đối với dữ liệu đếm rời rạc (Count Data), kiểm định KS-Test bị loại bỏ do vi phạm giả định phân phối liên tục, dẫn đến phân phối P-value bậc thang (Stepped Distribution).
- **Ngưỡng tiêu chuẩn:** Tỷ lệ FPR kỳ vọng dao động an toàn quanh mốc 5.0% (dung sai 3.5% - 6.5% với 5.000 vòng lặp).
- **Kết quả đo lường:** Tỷ lệ FPR thực tế đạt 4.74%.
- **Kết luận:** ĐẠT (PASS). Động cơ tính toán thống kê (Statistical Engine) hoạt động chính xác, kiểm soát tuyệt đối nhiễu hệ thống.

## 4. Kết luận Tổng thể
Hệ thống Thử nghiệm (Experimentation Platform) đã vượt qua toàn bộ các tiêu chí kiểm định ngặt nghèo trong danh sách Trust Checklist. Pipeline dữ liệu minh bạch, vô tư và chuẩn xác về mặt toán học. Mọi kết quả phân tích A/B Testing được chạy trên nền tảng này hoàn toàn đủ độ tin cậy để phục vụ cho các quyết định vận hành thực tế.
