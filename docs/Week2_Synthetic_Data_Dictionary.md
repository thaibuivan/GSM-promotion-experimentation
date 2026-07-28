# Từ điển Dữ liệu Giả lập (Synthetic Data Dictionary)

Tài liệu này định nghĩa chi tiết các biến số (features) được mô phỏng trong tập dữ liệu `complex_simulation_data.csv` (20,000 khách hàng), phục vụ trực tiếp cho bài toán Phân cụm (K-Means) và Suy luận Nhân quả (Uplift Modeling).

## 1. Biến Định danh (Identifier)
| Tên biến | Kiểu dữ liệu | Mô tả chi tiết |
|---|---|---|
| `user_id` | String | Mã định danh duy nhất của mỗi khách hàng. |

## 2. Biến Nhân khẩu học & Hành vi (Covariates)
Đây là các biến độc lập (Independent Variables) được mô phỏng bằng các phân phối thống kê để phản ánh tệp khách hàng ngoài đời thực.

| Tên biến | Kiểu dữ liệu | Phân phối (Distribution) | Mô tả chi tiết |
|---|---|---|---|
| `age` | Integer | Normal (mean=35, std=10) | Độ tuổi của khách hàng (giới hạn từ 18 đến 70). |
| `income` | Float | Log-normal (mean=10.5, sigma=0.5) | Mức thu nhập hàng tháng (Proxy thông qua các phân phối thu nhập lệch phải). |
| `is_urban` | Binary (0/1) | Bernoulli (p=0.7) | `1` = Khách hàng sinh sống/hay đặt xe ở khu vực nội thành. `0` = Ngoại thành. |
| `fare_obs` | Float | Lognormal | Giá cước trung bình mỗi chuyến xe. Khách hàng `is_urban=1` thường có cước thấp hơn khách đi ngoại tỉnh. Biến này dùng làm Proxy cho sức mua (Purchasing Power). |
| `preferred_hour`| Integer | Weighted Probability (Dựa trên EDA Tuần 1) | Khung giờ khách hàng thường xuyên đặt xe nhất trong ngày. Đỉnh chóp rơi vào 7h-9h và 17h-19h. |
| `is_rush_hour` | Binary (0/1) | Phái sinh từ `preferred_hour` | `1` = Khách hay đi vào 7h-9h và 17h-19h. Đại diện cho nhóm đi làm (Commuters). |
| `is_airport_trip`| Binary (0/1) | Bernoulli (p=0.05) | `1` = Khách hàng có thói quen đi các cuốc xe ra sân bay. Nếu =1, `fare_obs` sẽ tự động nhân 4x. |
| `is_rain_rider` | Binary (0/1) | Bernoulli (p=0.2) | `1` = Khách hàng có xu hướng gọi xe cao bất thường khi thời tiết xấu (trời mưa). |
| `is_weekend_rider` | Binary (0/1) | Bernoulli (p=0.3) | `1` = Khách hàng hay gọi xe vào dịp cuối tuần để đi chơi. |
| `preferred_payment` | String | Categorical | Hình thức thanh toán: `Cash` (Tiền mặt), `Credit Card` (Thẻ tín dụng), hoặc `E-Wallet`. |
| `is_credit_card` | Binary (0/1) | Phái sinh từ `preferred_payment` | `1` = Khách dùng Thẻ tín dụng. (Nhóm này có tỷ lệ Tip cao hơn). |
| `is_frequent_tipper` | Binary (0/1) | Bernoulli | `1` = Khách hay tip tài xế. Tỷ lệ tip là 40% đối với khách xài Thẻ, và 5% đối với khách xài Tiền mặt. |
| `avg_trip_distance` | Float | Lognormal | Khoảng cách chuyến đi trung bình (km). Khách sân bay có khoảng cách rất xa (~15km). |
| `typical_passenger_count` | Integer | Poisson | Số lượng hành khách trung bình trong 1 chuyến (Thường là 1-4 người). |
| `monthly_rides_history` | Integer | Phụ thuộc thu nhập & tuổi | Tần suất đi xe trong tháng trước đó. |
| `recency_days` | Integer | Phân phối Poisson nghịch đảo | Số ngày kể từ lần cuối cùng khách hàng mở app đặt xe (0-30 ngày). |

## 3. Biến Can thiệp (Treatment Variables)
Mô phỏng 2 môi trường: Môi trường Quan sát (có thiên kiến) và Môi trường Thí nghiệm (ngẫu nhiên).

| Tên biến | Kiểu dữ liệu | Mô tả chi tiết |
|---|---|---|
| `treatment_obs` | Binary (0/1) | **Dữ liệu Quan sát (Observational):** Khách hàng có nhận được Voucher trong thực tế hay không. Bị nhiễu bởi `is_rush_hour` (giờ cao điểm ít phát mã) và `is_rain_rider` (trời mưa ít phát mã). |
| `treatment_rand`| Binary (0/1) | **Dữ liệu Thí nghiệm (RCT - A/B Test):** Khách hàng có nhận Voucher không (Tung đồng xu ngẫu nhiên 50/50). **Không bị nhiễu.** |

## 4. Biến Kết quả (Outcome Variables)
Biến mục tiêu (Target Variables) đại diện cho số chuyến đi khách hàng thực hiện trong 14 ngày theo dõi.

| Tên biến | Kiểu dữ liệu | Mô tả chi tiết |
|---|---|---|
| `y_obs` | Float | **Số chuyến đi ở Môi trường Tự nhiên:** Số chuyến đi khi bị thiên kiến bởi `treatment_obs`. Dùng để demo Simpson's Paradox. |
| `y_rand` | Float | **Số chuyến đi ở Môi trường Thử nghiệm:** Số chuyến đi khi áp dụng `treatment_rand`. Đây là thước đo chuẩn xác để đánh giá **Uplift Model** sau này. |
| `true_ite` | Float | **Tác động Nhân quả Thực sự (Ground Truth):** Tác động chính xác của Voucher lên số chuyến đi của một cá nhân, được mô phỏng bởi hệ thống SCM. Dữ liệu thực tế không bao giờ có cột này. Ta dùng nó để chấm điểm mô hình. |
