# Báo cáo Tuần 2: Tư duy Nhân quả (Causal Inference) & Sinh Dữ liệu Giả lập (Synthetic Data Generation)

Trong quá trình thực tế, các doanh nghiệp thường sở hữu lượng lớn dữ liệu lịch sử (Observational Data) - ví dụ: Dữ liệu những khách hàng từng áp mã giảm giá trong quá khứ. Tuy nhiên, việc lấy trực tiếp dữ liệu lịch sử này để đo lường hiệu quả Voucher là **cực kỳ nguy hiểm và sai lệch** do sự tồn tại của **Biến nhiễu (Confounding Variables)**.

Tuần 2 được thiết kế để giải quyết bài toán này. Thay vì dùng dữ liệu có sẵn, chúng ta đã chủ động thiết lập một **Mô hình Nhân quả (Structural Causal Model - SCM)** và tự tay sinh ra tập dữ liệu giả lập (Synthetic Data) nhằm mô phỏng lại chính xác quy luật của thị trường.

---

## 1. Bản chất của Biến nhiễu (Confounding)
Giả sử dữ liệu lịch sử cho thấy: *Những người dùng Voucher có số chuyến đi cao hơn hẳn những người không dùng.*
- **Kết luận ngây thơ (Naïve Conclusion):** Voucher làm tăng số chuyến đi.
- **Sự thật (Causal Reality):** Có thể do **Trời mưa (Biến nhiễu)**. Khi trời mưa, nhu cầu gọi xe tăng vọt, và người dùng cũng có xu hướng tiện tay bấm dùng Voucher nhiều hơn. Vậy sự tăng trưởng chuyến đi là do Trời mưa, chứ không phải do Voucher. 
👉 Biến "Trời mưa" tác động lên cả Nguyên nhân (Dùng voucher) và Kết quả (Số chuyến đi), tạo ra sự tương quan giả (Spurious Correlation).

---

## 2. Thiết lập Mô hình Causal (Structural Causal Model)
Để tạo ra dữ liệu phục vụ cho Tuần 3 và Tuần 4, chúng ta đã code file `2_complex_data_generation.ipynb` đóng vai trò là "Thượng Đế" quy định quy luật thị trường.

### A. Định nghĩa Khách hàng (User Profiles)
Thuật toán sinh ra hàng vạn khách hàng ngẫu nhiên dựa trên các phân phối thống kê chuẩn:
- **Tuổi (Age):** Sinh theo phân phối chuẩn (Normal Distribution).
- **Thu nhập (Income):** Sinh theo phân phối log-normal (Log-normal Distribution) để phản ánh thực tế thu nhập.
- **Lịch sử di chuyển (History Rides):** Được nội suy từ độ tuổi và thu nhập.

### B. Định nghĩa Yếu tố Môi trường (Confounders)
- **Hệ số Nhu cầu theo giờ (Hour Demand Multiplier):** Nhu cầu tăng vọt ở các mốc 7h-9h sáng và 17h-19h chiều (Giờ cao điểm - Rush Hour).
- **Thời tiết (Weather):** Sinh tỷ lệ ngẫu nhiên những ngày mưa/nắng, tác động trực tiếp lên xác suất khách hàng mở App.

### C. Cơ chế sinh Biến Kết quả (Outcome Generation)
SCM của chúng ta định nghĩa 2 cột kết quả vô cùng quan trọng:
1. `y_obs` **(Quan sát tự nhiên):** Số chuyến đi tự nhiên bị ảnh hưởng nặng nề bởi Giờ cao điểm và Thời tiết. Không hề có tác động của Voucher.
2. `y_rand` **(Kết quả của Thí nghiệm A/B Test):**
   - Chúng ta đưa vào biến `treatment_effect` (Ví dụ: Voucher giúp tăng cố định trung bình +1.5 chuyến).
   - `y_rand` = `y_obs` + `treatment_effect` (chỉ áp dụng cho những người được gán vào nhóm Treatment = 1).

---

## 3. Tại sao bước này tạo nên Đẳng cấp của Dự án?
Trong môi trường học thuật, sinh viên thường tải bộ dữ liệu có sẵn trên Kaggle về rồi phân tích. Điều đó khiến các bạn không hiểu được bản chất dữ liệu đến từ đâu.

Ngược lại, ở Tuần 2, chúng ta đã:
1. Tự tay thiết kế kiến trúc Dữ liệu từ con số 0.
2. Hiểu rõ biến nào tác động lên biến nào (Causal Graph).
3. Chủ động giấu một "Sự thật" (`treatment_effect`) vào trong dữ liệu, để rồi sang Tuần 4, chúng ta dùng A/B Testing để chứng minh rằng Thống kê học có thể "mò" ra đúng cái Sự thật bị giấu kín đó bất chấp nhiễu loạn của thị trường.

Đó chính là tư duy cốt lõi của **Experimentation & Causal Inference** mà các tập đoàn công nghệ lớn như Uber, Grab, Shopee đang ráo riết săn lùng!
