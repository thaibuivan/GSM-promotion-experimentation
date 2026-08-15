# Data Contract: GSM Promotion Experimentation

**Version:** 1.0
**Owner:** Data Science Team
**Consumers:** Data Engineering, Marketing Operations

## 1. Mục đích (Purpose)
Bản hợp đồng dữ liệu này quy định rõ schema, nguồn cấp, và ranh giới thời gian (Time Cutoff) của các trường dữ liệu được phép sử dụng trong dự án `GSM-promotion-experimentation`. Mục tiêu tối thượng là **chống rò rỉ dữ liệu (Data Leakage)** giữa thời điểm trước (Pre-treatment) và sau (Post-treatment) khi chạy chiến dịch.

## 2. Ranh giới Thời gian (Time Cutoff Rules)
Bất kỳ mô hình Machine Learning nào (K-Means, X-Learner) cũng phải đáng tin cậy tuân thủ trục thời gian (T) sau:

- **T < 0 (Historical Window):** Khoảng thời gian thu thập Feature. Ví dụ: Lịch sử đi lại 90 ngày trước chiến dịch.
- **T = 0 (Randomization & Assignment):** Thời điểm chia nhóm A/B và phát Voucher.
- **T > 0 (Outcome Window):** Khoảng thời gian đo lường hành vi (14 ngày).

> [!WARNING]
> Tuyệt đối KHÔNG sử dụng bất kỳ hành vi nào sinh ra ở `T > 0` (như `redemption_flag`, `post_treatment_rides`) làm Feature đầu vào để dự đoán CATE.

## 3. Schema Đầu vào Chuẩn (Pre-Treatment Features)

| Cột Dữ Liệu | Kiểu | Mô tả | Nguồn | Ràng buộc |
| :--- | :--- | :--- | :--- | :--- |
| `user_id` | String | Mã định danh duy nhất của KH | Backend DB | Khóa chính, Not Null |
| `experiment_id` | String | Mã chiến dịch A/B Test | AB Testing Platform | Not Null |
| `assignment_timestamp` | Datetime | Thời điểm KH được phân bổ vào nhóm | AB Testing Platform | T=0 |
| `age` | Integer | Tuổi của KH | User Profile | Từ 15 - 90 |
| `is_urban` | Boolean | Có ở thành thị không | User Profile | 0 hoặc 1 |
| `preferred_hour` | Integer | Giờ đi xe phổ biến nhất | Ride History (T<0) | 0 - 23 |
| `is_rush_hour` | Boolean | Hay đi vào giờ cao điểm | Ride History (T<0) | 0 hoặc 1 |
| `is_airport_trip` | Boolean | Hay đi sân bay | Ride History (T<0) | 0 hoặc 1 |
| `monthly_rides_history` | Float | Tần suất đi xe trung bình tháng | Ride History (T<0) | >= 0 |
| `avg_fare_per_trip` | Float | Giá cước trung bình mỗi chuyến | Ride History (T<0) | > 0 |

## 4. Schema Kết quả (Post-Treatment Outcomes)

| Cột Dữ Liệu | Kiểu | Mô tả | Nguồn | Ràng buộc |
| :--- | :--- | :--- | :--- | :--- |
| `treatment_rand` | Boolean | Cờ nhận Voucher (1=Có, 0=Không) | AB Testing Platform | T=0 |
| `exposure_flag` | Boolean | KH đã mở app và nhìn thấy Voucher | App Telemetry | T>0 |
| `Y_rand` | Float | Tổng số chuyến đi trong 14 ngày tới | Ride History (T>0) | Outcome Metric, >=0 |
| `voucher_cost` | Float | Chi phí thực tế công ty phải trả | Billing (T>0) | Dựa trên config |
| `margin_per_ride` | Float | Lợi nhuận gộp sinh ra | Billing (T>0) | Dựa trên config |

## 5. Quy tắc Xử lý Dữ liệu Lỗi (Missing & Outlier Rules)
- **Missing Values:** 
  - Các biến nhân khẩu học (Age, Urban) nếu thiếu sẽ được điền bằng Median/Mode của tập train.
  - Các biến hành vi nếu thiếu (user mới) sẽ mặc định bằng 0.
- **Outliers:** 
  - `monthly_rides_history` vượt quá 99th percentile (ví dụ > 100 chuyến/tháng) sẽ bị Capping để tránh nhiễu mô hình.
