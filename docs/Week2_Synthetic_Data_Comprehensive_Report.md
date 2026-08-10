# Báo cáo Toàn diện: Phân tích Cấu trúc Nhân quả & Sinh dữ liệu mô phỏng (Tuần 2)

## Phần I: Báo cáo Kỹ thuật Tổng quan

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


---

## Phần II: Cơ chế Mô phỏng Data Sinh học (Data Generating Protocol)

Tài liệu này giải thích cơ chế Toán học và Logic đằng sau việc tạo ra tập dữ liệu 20,000 khách hàng. Báo cáo này đặc biệt hữu ích để chứng minh độ tin cậy của tập dữ liệu trước khi đưa vào mô hình học máy.

### 1. Phương pháp luận
Thay vì sinh ngẫu nhiên toàn bộ các cột dữ liệu (Random Generation), chúng tôi áp dụng **Mô hình Nhân quả Cấu trúc (Structural Causal Models - SCM)**. Phương pháp này đảm bảo rằng các biến số trong tập dữ liệu có mối quan hệ tương quan logic với nhau, hệt như trong thế giới thực.

### 2. Quy trình Sinh Đặc điểm (Raw Features Generation)

#### 2.1. Cụm Biến Địa lý & Giá trị cước (Spatial & Monetary)
- `is_urban`: Sinh bằng Bernoulli (p=0.7). Phần lớn khách hàng của hãng xe tập trung ở nội thành.
- `fare_obs`: Mức cước phí được sinh dựa trên `is_urban`. Khách nội thành thường đi chuyến ngắn (cước trung bình thấp hơn), khách ngoại thành đi chuyến xa (cước trung bình cao hơn). Được phân phối theo dải **Log-normal** để có chiếc đuôi dài (Long-tail) y hệt dữ liệu cước phí thực tế.
- **Quy tắc Ngoại lệ (Airport Multiplier):** Nếu `is_airport_trip = 1` (khoảng 5% khách hàng), mức cước `fare_obs` lập tức được nhân 4 (x4). 

#### 2.2. Cụm Biến Thời gian (Temporal)
- `preferred_hour`: Phân phối **Có trọng số (Weighted Probability)** dựa trên `HOUR_DEMAND_MULTIPLIER`. Lấy cảm hứng từ EDA Tuần 1, xác suất rơi vào các khung giờ 7h-9h sáng và 17h-19h tối được ép đẩy lên rất cao (Rush Hours), trong khi các giờ rạng sáng bị ép xuống thấp.
- `is_rush_hour`: Một hàm băm (mapping) từ `preferred_hour`. Nếu giờ nằm trong [7, 8, 9, 17, 18, 19] thì giá trị = 1, ngược lại = 0.

### 3. Cấu trúc Biến Nhiễu (Confounder Injection)

Trong thực tế, Việc phát Voucher không bao giờ diễn ra ngẫu nhiên (Non-random Assignment). Hệ thống khuyến mãi luôn bị can thiệp bởi môi trường. Chúng tôi gài 2 biến nhiễu vào dữ liệu để tạo ra **Selection Bias (Thiên kiến lựa chọn)**:

1. **Nhiễu Cao điểm (`is_rush_hour`):** 
   - Giờ cao điểm -> Nhu cầu đặt xe tăng (+2 chuyến).
   - Giờ cao điểm -> App KHÔNG phát Voucher (Logit(Probability) giảm mạnh).
2. **Nhiễu Thời tiết (`is_rain_rider`):**
   - Trời mưa -> Nhu cầu tăng đột biến (+2 chuyến).
   - Trời mưa -> Hệ thống tắt khuyến mãi để bảo vệ margin.

> **Kết quả của Biến nhiễu:** Trong tập dữ liệu quan sát (`y_obs`), những người KHÔNG nhận Voucher lại có vẻ đi xe nhiều hơn người CÓ nhận. Nghịch lý này (Simpson's Paradox) là bài kiểm tra hoàn hảo cho các mô hình Causal Inference.

### 4. Gài Luật Nhân quả (Hardcoding the Uplift)

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

### 5. Kết luận
Nhờ có Data Generating Protocol chi tiết này, tập dữ liệu không chỉ là một bảng tính ngẫu nhiên, mà là một **phòng thí nghiệm (Laboratory)** chuẩn mực để chúng ta có thể kiểm thử, đo lường các thuật toán Clustering (Tuần 3) và Uplift Modeling (Tuần 7) một cách chính xác tuyệt đối.


---

## Phần III: Từ điển Dữ liệu Giả lập (Synthetic Data Dictionary)

Tài liệu này định nghĩa chi tiết các biến số (features) được mô phỏng trong tập dữ liệu `complex_simulation_data.csv` (20,000 khách hàng), phục vụ trực tiếp cho bài toán Phân cụm (K-Means) và Suy luận Nhân quả (Uplift Modeling).

### 1. Biến Định danh (Identifier)
| Tên biến | Kiểu dữ liệu | Mô tả chi tiết |
|---|---|---|
| `user_id` | String | Mã định danh duy nhất của mỗi khách hàng. |

### 2. Biến Nhân khẩu học & Hành vi (Covariates)
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
| `monthly_rides_history` | Integer | Phụ thuộc Khu vực (is_urban) & Thanh toán (payment_type) | Tần suất đi xe trong tháng trước đó. Khách nội thành và dùng Thẻ tín dụng đi nhiều hơn. |
| `recency_days` | Integer | Phân phối Poisson nghịch đảo | Số ngày kể từ lần cuối cùng khách hàng mở app đặt xe (0-30 ngày). |

### 3. Biến Can thiệp (Treatment Variables)
Mô phỏng 2 môi trường: Môi trường Quan sát (có thiên kiến) và Môi trường Thí nghiệm (ngẫu nhiên).

| Tên biến | Kiểu dữ liệu | Mô tả chi tiết |
|---|---|---|
| `treatment_obs` | Binary (0/1) | **Dữ liệu Quan sát (Observational):** Khách hàng có nhận được Voucher trong thực tế hay không. Bị nhiễu bởi `is_rush_hour` (giờ cao điểm ít phát mã) và `is_rain_rider` (trời mưa ít phát mã). |
| `treatment_rand`| Binary (0/1) | **Dữ liệu Thí nghiệm (RCT - A/B Test):** Khách hàng có nhận Voucher không (Tung đồng xu ngẫu nhiên 50/50). **Không bị nhiễu.** |

### 4. Biến Kết quả (Outcome Variables)
Biến mục tiêu (Target Variables) đại diện cho số chuyến đi khách hàng thực hiện trong 14 ngày theo dõi.

| Tên biến | Kiểu dữ liệu | Mô tả chi tiết |
|---|---|---|
| `y_obs` | Float | **Số chuyến đi ở Môi trường Tự nhiên:** Số chuyến đi khi bị thiên kiến bởi `treatment_obs`. Dùng để demo Simpson's Paradox. |
| `y_rand` | Float | **Số chuyến đi ở Môi trường Thử nghiệm:** Số chuyến đi khi áp dụng `treatment_rand`. Đây là thước đo chuẩn xác để đánh giá **Uplift Model** sau này. |
| `true_ite` | Float | **Tác động Nhân quả Thực sự (Ground Truth):** Tác động chính xác của Voucher lên số chuyến đi của một cá nhân, được mô phỏng bởi hệ thống SCM. Dữ liệu thực tế không bao giờ có cột này. Ta dùng nó để chấm điểm mô hình. |
