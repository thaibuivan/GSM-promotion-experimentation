# Báo cáo Kỹ thuật: Phân tích Cấu trúc Nhân quả & Sinh dữ liệu mô phỏng (Tuần 2)

## 1. Mở đầu và Mục tiêu
Dữ liệu quan sát (Observational Data) thường chứa đựng các sai lệch nội tại do sự tác động của biến nhiễu (Confounding Variables). Điều này làm cho dữ liệu quan sát không đủ độ tin cậy để đo lường trực tiếp tác động nhân quả. Ví dụ: mối tương quan thuận giữa việc sử dụng Voucher và tần suất đặt xe có thể bị nhiễu bởi các yếu tố ngoại cảnh như thời tiết hoặc nhu cầu trong giờ cao điểm.

Nhằm thiết lập một nền tảng vững chắc cho quá trình A/B Testing và đánh giá tính chính xác của hệ thống phân tích, giai đoạn này tập trung vào việc xây dựng Mô hình Cấu trúc Nhân quả (Structural Causal Model - SCM) và tạo ra một tập dữ liệu mô phỏng (Synthetic Data). Phương pháp này cho phép thiết lập trước một "tác động can thiệp" (Treatment Effect) chuẩn, từ đó tạo cơ sở để kiểm định độ chính xác của các thuật toán thống kê ở các tuần tiếp theo.

## 2. Thiết kế Mô hình Cấu trúc Nhân quả (SCM) & Tích hợp Dữ liệu Thực tế
Quy trình sinh dữ liệu mô phỏng được thực hiện tại file `notebooks/week2_synthetic_data/2_complex_data_generation.ipynb`. Một bước tiến lớn của mô hình là việc **Kế thừa các tham số từ kết quả EDA Tuần 1 (Yellow Taxi Data)** để đảm bảo tính thực tế:

### 2.1. Mô phỏng Hồ sơ Khách hàng (User Profile)
Các đặc tính của người dùng được mô phỏng dựa trên các phân phối xác suất sát với thực tế nhân khẩu học:
- **Độ tuổi (Age):** Khởi tạo theo Phân phối chuẩn (Normal Distribution).
- **Thu nhập (Income):** Khởi tạo theo Phân phối Log-normal để phản ánh đặc tính phân bổ lệch phải.
- **Tần suất đi xe & Doanh thu:** Nội suy từ độ tuổi và thu nhập, sử dụng biến **OEC (Overall Evaluation Criterion)** từ Tuần 1 (Avg Fare = $17.60, Median Fare = $13.50).

### 2.2. Tích hợp Biến nhiễu (Confounders)
Mô hình tích hợp các biến nhiễu sau để thử thách các thuật toán Machine Learning sau này:
- **Hệ số Nhu cầu theo giờ (Hour Demand Multiplier):** Phản ánh sự gia tăng nhu cầu trong khung giờ cao điểm (07:00-09:00 và 17:00-19:00).
- **Điều kiện thời tiết (Weather Conditions):** Biến nhị thức mô phỏng xác suất trời mưa, làm tăng đột biến nhu cầu đặt xe độc lập với Voucher.

### 2.3. Thiết lập Biến Kết quả & Kiểm định (Covariate Balance)
Mô hình SCM định nghĩa hai biến kết quả chính để cô lập tác động nhân quả:
1. **Kết quả Quan sát (`y_obs`):** Số chuyến đi tự nhiên không có Voucher.
2. **Kết quả Thực nghiệm (`y_rand`):** Số chuyến đi trong môi trường Thử nghiệm RCT. Tác động của Voucher tuân theo **Hiệu ứng Dị thể (Heterogeneous Treatment Effect - HTE)**:
   - **Nhóm Cầu co giãn mạnh (Suburban Card - Ngoại ô dùng Thẻ):** Được thiết lập là nhóm phản ứng mạnh mẽ nhất với Voucher (Tác động kỳ vọng ATE > 1.2 chuyến).
   - **Nhóm Cầu không co giãn (Urban Regulars - Đi lại thường xuyên Nội thành):** Bị ràng buộc bởi nhu cầu cứng, họ sẽ đi xe kể cả khi không có Voucher (Tác động kỳ vọng ATE < 1.0 chuyến).

Đặc biệt, hệ thống đã thực hiện bước **Kiểm tra Covariate Balance**, xác nhận rằng các biến số (Covariates) phân bổ hoàn toàn đồng đều giữa nhóm Treatment và Control, tạo tiền đề vững chắc cho việc thực thi A/A Test ở Tuần 5.

## 3. Kết luận
Bằng việc thiết kế một tập dữ liệu mô phỏng với cấu trúc nhân quả rõ ràng, kết hợp chặt chẽ với số liệu EDA thực tế (Avg Fare $17.60), dự án đã phân tách thành công tác động thực sự của Voucher khỏi các yếu tố nhiễu loạn. Tập dữ liệu này đóng vai trò là một môi trường Sandbox tiêu chuẩn, đảm bảo rằng các mô hình Causal Inference sau này đủ mạnh mẽ để nhận diện chính xác ITE (Individual Treatment Effect).
