# Báo cáo Kỹ thuật: Phân tích Cấu trúc Nhân quả & Sinh dữ liệu mô phỏng (Tuần 2)

## 1. Mở đầu và Mục tiêu
Dữ liệu quan sát (Observational Data) thường chứa đựng các sai lệch nội tại do sự tác động của biến nhiễu (Confounding Variables). Điều này làm cho dữ liệu quan sát không đủ độ tin cậy để đo lường trực tiếp tác động nhân quả. Ví dụ: mối tương quan thuận giữa việc sử dụng Voucher và tần suất đặt xe có thể bị nhiễu bởi các yếu tố ngoại cảnh như thời tiết hoặc nhu cầu trong giờ cao điểm.

Nhằm thiết lập một nền tảng vững chắc cho quá trình A/B Testing và đánh giá tính chính xác của hệ thống phân tích, giai đoạn này tập trung vào việc xây dựng Mô hình Cấu trúc Nhân quả (Structural Causal Model - SCM) và tạo ra một tập dữ liệu mô phỏng (Synthetic Data). Phương pháp này cho phép thiết lập trước một "tác động can thiệp" (Treatment Effect) chuẩn, từ đó tạo cơ sở để kiểm định độ chính xác của các thuật toán thống kê ở các tuần tiếp theo.

## 2. Thiết kế Mô hình Cấu trúc Nhân quả (SCM)
Quy trình sinh dữ liệu mô phỏng được thực hiện tại file `notebooks/week2_synthetic_data/2_complex_data_generation.ipynb`. Phương pháp thực hiện bao gồm các thành phần sau:

### 2.1. Mô phỏng Hồ sơ Khách hàng (User Profile)
Các đặc tính của người dùng được mô phỏng dựa trên các phân phối xác suất nhằm phản ánh sát với thực tế nhân khẩu học:
- **Độ tuổi (Age):** Được khởi tạo theo Phân phối chuẩn (Normal Distribution).
- **Thu nhập (Income):** Được khởi tạo theo Phân phối Log-normal để mô phỏng đặc tính phân bổ lệch phải (Right-skewness) thường thấy ở dữ liệu thu nhập thực tế.
- **Tần suất đi xe lịch sử (Historical Ride Frequency):** Được tính toán nội suy dựa trên độ tuổi và phân khúc thu nhập.

### 2.2. Tích hợp Biến nhiễu (Confounders)
Để mô phỏng các yếu tố môi trường có khả năng tác động đồng thời lên cả việc nhận Voucher (Treatment) và số chuyến xe (Outcome), mô hình đã tích hợp các biến nhiễu sau:
- **Hệ số Nhu cầu theo giờ (Hour Demand Multiplier):** Hệ số chuỗi thời gian phản ánh sự gia tăng nhu cầu trong khung giờ cao điểm (ví dụ: 07:00-09:00 và 17:00-19:00).
- **Điều kiện thời tiết (Weather Conditions):** Biến nhị thức (Binomial) mô phỏng xác suất trời mưa, đóng vai trò như một cú sốc tích cực làm tăng đột biến nhu cầu đặt xe.

### 2.3. Thiết lập Biến Kết quả (Outcome Variable)
Mô hình SCM định nghĩa hai biến kết quả chính để cô lập tác động nhân quả:
1. **Kết quả Quan sát (`y_obs`):** Số chuyến đi tự nhiên của khách hàng. Biến này là hàm số phụ thuộc vào hồ sơ khách hàng và các biến nhiễu, hoàn toàn không có tác động của Voucher.
2. **Kết quả Thực nghiệm (`y_rand`):** Số chuyến đi trong môi trường Thử nghiệm ngẫu nhiên có đối chứng (RCT). Một hằng số `treatment_effect` được cộng thêm vào `y_obs` nhưng chỉ áp dụng nghiêm ngặt cho những người dùng được phân bổ ngẫu nhiên vào nhóm Treatment.

## 3. Kết luận
Bằng việc thiết kế một tập dữ liệu mô phỏng với cấu trúc nhân quả được định nghĩa sẵn, dự án đã phân tách thành công tác động thực sự của Voucher khỏi các yếu tố nhiễu loạn của dữ liệu quan sát. Tập dữ liệu này đóng vai trò là một môi trường thử nghiệm tiêu chuẩn cho các phân tích Phân cụm và A/B Testing, đảm bảo rằng các mô hình thống kê được sử dụng có đủ khả năng nhận diện chính xác tác động nhân quả bất chấp sự hiện diện của biến nhiễu.
