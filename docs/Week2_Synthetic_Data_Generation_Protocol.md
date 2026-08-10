# Báo cáo Kỹ thuật: Cơ chế Mô phỏng Data Sinh học (Data Generating Protocol)

Tài liệu này giải thích cơ chế Toán học và Logic đằng sau việc tạo ra tập dữ liệu 20,000 khách hàng. Báo cáo này đặc biệt hữu ích để chứng minh độ tin cậy của tập dữ liệu trước khi đưa vào mô hình học máy.

## 1. Phương pháp luận
Thay vì sinh ngẫu nhiên toàn bộ các cột dữ liệu (Random Generation), chúng tôi áp dụng **Mô hình Nhân quả Cấu trúc (Structural Causal Models - SCM)**. Phương pháp này đảm bảo rằng các biến số trong tập dữ liệu có mối quan hệ tương quan logic với nhau, hệt như trong thế giới thực.

## 2. Quy trình Sinh Đặc điểm (Raw Features Generation)

### 2.1. Cụm Biến Địa lý & Giá trị cước (Spatial & Monetary)
- `is_urban`: Sinh bằng Bernoulli (p=0.7). Phần lớn khách hàng của hãng xe tập trung ở nội thành.
- `fare_obs`: Mức cước phí được sinh dựa trên `is_urban`. Khách nội thành thường đi chuyến ngắn (cước trung bình thấp hơn), khách ngoại thành đi chuyến xa (cước trung bình cao hơn). Được phân phối theo dải **Log-normal** để có chiếc đuôi dài (Long-tail) y hệt dữ liệu cước phí thực tế.
- **Quy tắc Ngoại lệ (Airport Multiplier):** Nếu `is_airport_trip = 1` (khoảng 5% khách hàng), mức cước `fare_obs` lập tức được nhân 4 (x4). 

### 2.2. Cụm Biến Thời gian (Temporal)
- `preferred_hour`: Phân phối **Có trọng số (Weighted Probability)** dựa trên `HOUR_DEMAND_MULTIPLIER`. Lấy cảm hứng từ EDA Tuần 1, xác suất rơi vào các khung giờ 7h-9h sáng và 17h-19h tối được ép đẩy lên rất cao (Rush Hours), trong khi các giờ rạng sáng bị ép xuống thấp.
- `is_rush_hour`: Một hàm băm (mapping) từ `preferred_hour`. Nếu giờ nằm trong [7, 8, 9, 17, 18, 19] thì giá trị = 1, ngược lại = 0.

## 3. Cấu trúc Biến Nhiễu (Confounder Injection)

Trong thực tế, Việc phát Voucher không bao giờ diễn ra ngẫu nhiên (Non-random Assignment). Hệ thống khuyến mãi luôn bị can thiệp bởi môi trường. Chúng tôi gài 2 biến nhiễu vào dữ liệu để tạo ra **Selection Bias (Thiên kiến lựa chọn)**:

1. **Nhiễu Cao điểm (`is_rush_hour`):** 
   - Giờ cao điểm -> Nhu cầu đặt xe tăng (+2 chuyến).
   - Giờ cao điểm -> App KHÔNG phát Voucher (Logit(Probability) giảm mạnh).
2. **Nhiễu Thời tiết (`is_rain_rider`):**
   - Trời mưa -> Nhu cầu tăng đột biến (+2 chuyến).
   - Trời mưa -> Hệ thống tắt khuyến mãi để bảo vệ margin.

> **Kết quả của Biến nhiễu:** Trong tập dữ liệu quan sát (`y_obs`), những người KHÔNG nhận Voucher lại có vẻ đi xe nhiều hơn người CÓ nhận. Nghịch lý này (Simpson's Paradox) là bài kiểm tra hoàn hảo cho các mô hình Causal Inference.

## 4. Gài Luật Nhân quả (Hardcoding the Uplift)

Đây là giá trị lớn nhất của bộ dữ liệu. Chúng tôi quy định trước (Ground Truth) ai là người nhạy cảm với khuyến mãi (Persuadables) và ai kháng khuyến mãi (Sure-things).

Phương trình toán học cốt lõi (Causal Equation):
```math
ITE = 2.0 (Base) + 2.0 * SuburbanLeisure + 0.5 * RainAgeInteraction - 1.5 * is_airport - 1.0 * is_rush_hour - 0.5 * is_cash + RecencyBoost
```

**Diễn giải logic kinh doanh chi tiết:**
- Tác động cơ bản của Voucher là tăng **2.0 chuyến/tháng**.
- **Ngoại ô & Cuối tuần (Suburban Leisure):** Khách đi chơi ngoại ô cuối tuần cực kỳ nhạy cảm giá -> Tăng thêm **+2.0 chuyến**. Đây chính là hạt nhân toán học tạo ra nhóm *Suburban Card* thành công ở Tuần 3 và 4.
- **Tương tác Mưa & Tuổi (Rain Age Interaction):** Khách hàng trẻ tuổi nhạy cảm hơn với khuyến mãi khi trời mưa -> Tăng thêm **+0.5 chuyến**.
- **Sân bay (Airport):** Khách ra sân bay bắt buộc phải đi -> Giảm **1.5 chuyến**. Voucher là vô nghĩa.
- **Giờ cao điểm (Rush Hour):** Khách đi làm -> Giảm **1.0 chuyến**.
- **Tiền mặt (Cash Penalty):** Khách dùng tiền mặt có sức mua/độ trung thành thấp hơn -> Giảm **0.5 chuyến**.
- **Hiệu ứng Win-back (Recency Boost):** Bỏ app càng lâu, Voucher càng có tác dụng đánh thức mạnh.

Ngoài ra, ITE còn bị suy giảm bởi **Quy luật Hiệu suất giảm dần (Diminishing Returns)**: Những người vốn dĩ đã đi quá nhiều chuyến trong tháng (Heavy Users) sẽ rất khó bị kích thích thêm bởi Voucher.

## 5. Kết luận
Nhờ có Data Generating Protocol chi tiết này, tập dữ liệu không chỉ là một bảng tính ngẫu nhiên, mà là một **phòng thí nghiệm (Laboratory)** chuẩn mực để chúng ta có thể kiểm thử, đo lường các thuật toán Clustering (Tuần 3) và Uplift Modeling (Tuần 7) một cách chính xác tuyệt đối.
