# Báo Cáo Kỹ Thuật Tuần 5: Uplift Modeling và Profit-Based Targeting

## 1. Câu Hỏi Kinh Doanh

Ở tuần 4, A/B testing trả lời câu hỏi:

```text
Trung bình voucher có làm tăng số chuyến đi không?
```

Nhưng quyết định kinh doanh thực tế cần trả lời câu hỏi cụ thể hơn:

```text
Nên phát voucher cho user nào để campaign tạo ra lợi nhuận tăng thêm?
```

Một user có nhiều chuyến sau campaign chưa chắc là user nên được nhận voucher. Họ có thể vốn đã là heavy user và vẫn sẽ đi nhiều chuyến dù không có voucher. Vì vậy, tuần 5 chuyển từ đo hiệu ứng trung bình sang đo phản ứng cá nhân:

```text
CATE_i = E[Y_i(1) - Y_i(0) | X_i]
```

Trong đó:

- `Y_i(1)` = số chuyến tiềm năng nếu user `i` nhận voucher
- `Y_i(0)` = số chuyến tiềm năng nếu user `i` không nhận voucher
- `X_i` = đặc điểm user trước khi phát voucher
- `CATE_i` = số chuyến tăng thêm do voucher gây ra

Mục tiêu cuối cùng không chỉ là tìm user có uplift cao, mà là:

```text
Tìm user có incremental margin lớn hơn promotion burn.
```

## 2. Vì Sao A/B Testing và Segmentation Chưa Đủ

### 2.1 Hạn chế của A/B Testing

A/B testing ước lượng:

```text
ATE = E[Y | T = 1] - E[Y | T = 0]
```

Chỉ số này hữu ích để kiểm tra voucher có tác dụng trung bình hay không. Tuy nhiên, nó không cho biết từng cá nhân nên hay không nên nhận voucher.

Nếu phát voucher cho toàn bộ user, công ty sẽ trợ giá cả cho những người vốn dĩ vẫn sẽ đi xe. Đây là vấn đề:

```text
Cannibalization = ăn lẹm doanh thu từ khách hàng không cần khuyến mãi.
```

### 2.2 Hạn chế của Segment Targeting

Các persona như `Suburban Cash`, `Suburban Card`, `Urban Regulars` hữu ích cho giải thích nghiệp vụ và truyền thông với marketing. Tuy nhiên, policy theo segment vẫn còn thô:

```text
Trong cùng một persona vẫn có user nhạy voucher và user không nhạy voucher.
```

Vì vậy, segmentation được giữ như một tầng giải thích, còn uplift modeling trở thành tầng ra quyết định ở cấp cá nhân.

## 3. Các Giả Định Trước Khi Xây Uplift Model

Các model uplift trong project dựa trên những giả định causal sau:

1. **Treatment assignment là randomized**

   Project dùng `treatment_rand`, tức treatment được chia ngẫu nhiên 50/50. Điều này giúp giảm selection bias.

2. **Feature phải là pre-treatment feature**

   Các biến đầu vào đều là thông tin có trước khi phát voucher:

   ```text
   age, is_urban, preferred_hour, is_rush_hour,
   is_airport_trip, is_rain_rider, is_weekend_rider,
   is_credit_card, passenger_count, monthly_rides_history,
   recency_days
   ```

   Không dùng các biến xảy ra sau treatment để tránh data leakage.

3. **Overlap**

   Với các nhóm user quan trọng, phải có cả treated và control. Thiết kế RCT 50/50 hỗ trợ giả định này.

4. **Không có spillover**

   Giả định việc một user nhận voucher không làm thay đổi outcome của user khác.

5. **Phạm vi synthetic sandbox**

   Dữ liệu có `Y0`, `Y1`, `cate_true`, nên có thể dùng để kiểm chứng methodology. Tuy nhiên, đây không phải bằng chứng production thật của GSM/Xanh SM.

## 4. Hành Trình Thử Các Uplift Learner

Tuần 5 không chọn R-Learner ngay từ đầu. Project đi qua nhiều hướng model để hiểu ưu/nhược điểm, rồi mới chọn champion.

### 4.1 T-Learner

T-Learner train hai model outcome riêng:

```text
mu_0(X) = E[Y | X, T = 0]
mu_1(X) = E[Y | X, T = 1]
```

Sau đó:

```text
CATE(X) = mu_1(X) - mu_0(X)
```

**Ưu điểm**

- Dễ hiểu và dễ giải thích.
- Trực tiếp so sánh hai thế giới: có voucher và không voucher.
- Phù hợp làm baseline đầu tiên.

**Nhược điểm**

- Mỗi model chỉ học trên một phần dữ liệu.
- Nếu `mu_0` hoặc `mu_1` sai, CATE sẽ sai.
- Mục tiêu chính vẫn là dự đoán outcome, chưa trực tiếp tối ưu treatment effect.

**Đánh giá trong project**

Lưu ý: RMSE dưới đây chỉ là diagnostic cho hai outcome models `mu_0`, `mu_1`, không phải metric chính để chọn uplift model. RMSE đo sai số giữa số chuyến model dự đoán và số chuyến thực tế quan sát được:

```text
RMSE = sqrt(mean((Y_pred - Y_true)^2))
```

Vì vậy, RMSE trả lời câu hỏi:

```text
Model outcome dự đoán Y có lệch nhiều so với Y thực tế không?
```

Nó không trực tiếp trả lời:

```text
Model uplift có rank đúng user nhạy voucher không?
```

Metric chính của uplift model vẫn là Qini/AUUC, calibration và policy value.

Trong notebook exploratory, T-Learner được dùng như baseline đầu tiên trên một persona cụ thể (`Suburban Card`). Kết quả base model:

```text
Control model RMSE: 4.328
Treatment model RMSE: 4.936
```

Khi chuyển sang business policy:

```text
Phát voucher đại trà trong segment: 2,465.50
Chỉ target top 20% CATE: 4,620.22
Tăng lợi nhuận so với phát rộng: 87.4%
```

Notebook T-Learner cũng có vẽ Qini Curve để kiểm tra ranking uplift. Kết quả trong title biểu đồ:

```text
T-Learner Qini Coef: -0.320
```

Điểm này rất quan trọng: dù top 20% theo CATE tạo profit tốt hơn phát rộng trong riêng segment `Suburban Card`, đường Qini tổng thể lại nằm dưới random ở nhiều vùng nên Qini Coef âm. Vì vậy T-Learner chỉ nên được xem là baseline để minh họa cách tách treated/control, chưa đủ tốt để làm champion.

Diễn giải:

```text
T-Learner chứng minh được ý tưởng quan trọng: target theo uplift có thể tốt hơn phát đều trong một nhóm cụ thể.
Tuy nhiên, Qini Coef = -0.320 cho thấy ranking toàn đường chưa ổn định và kém hơn random baseline.
Vì nó chỉ được thử mạnh trên một persona và dùng hai outcome models riêng, nó phù hợp làm baseline hơn là champion toàn hệ thống.
```

### 4.2 S-Learner

S-Learner train một model duy nhất:

```text
Y = f(X, T)
```

Để tính CATE, cùng một user được dự đoán hai lần:

```text
CATE(X) = f(X, T = 1) - f(X, T = 0)
```

**Ưu điểm**

- Cấu trúc đơn giản.
- Dùng toàn bộ dữ liệu trong một model.

**Nhược điểm**

- Treatment signal có thể bị làm mờ nếu nhỏ hơn nhiều so với baseline behavior.
- Model có thể tối ưu dự đoán `Y` hơn là học heterogeneous uplift.

**Đánh giá trong project**

Lưu ý: RMSE ở đây đo khả năng dự đoán outcome `Y`, không trực tiếp đo CATE. Vì S-Learner chỉ có một outcome model `f(X, T)`, RMSE được dùng như sanity check xem model có học được pattern cơ bản của `Y` hay không.

S-Learner được thử trên toàn bộ population 20,000 users. Kết quả validation:

```text
Validation RMSE: 6.314
Qini Coef: 0.153
```

Khi chuyển sang profit:

```text
Phát voucher đại trà: -44,640.06
Top 30% user tốt nhất theo expected profit: 14,338.87
```

Top 30% profitable users chủ yếu thuộc:

```text
Suburban Cash: 54.6%
Suburban Card: 26.3%
Urban Regulars: 14.2%
```

Diễn giải:

```text
S-Learner cho thấy model một tầng có thể tìm được nhóm profitable tốt hơn mass voucher.
Qini Coef = 0.153 cho thấy ranking uplift tốt hơn random, nhưng vẫn thấp hơn R-Learner champion.
Tuy nhiên, vì treatment chỉ là một feature trong bài toán dự đoán Y, model có rủi ro làm mờ treatment effect.
Do đó S-Learner được giữ như benchmark đơn giản, không phải final champion.
```

### 4.3 X-Learner

X-Learner bắt đầu giống T-Learner, nhưng sau đó tạo pseudo-effect:

```text
Với treated user:
D_1 = Y - mu_0(X)

Với control user:
D_0 = mu_1(X) - Y
```

Sau đó model train tiếp trên `D_0`, `D_1` để học treatment effect.

**Ưu điểm**

- Học treatment effect trực tiếp hơn T-Learner.
- Có ích khi treatment/control mất cân bằng.

**Nhược điểm**

- Nhiều tầng model nên dễ tích lũy lỗi.
- Pseudo-effect có thể nhiễu.
- Calibration khó kiểm soát hơn.

**Đánh giá trong project**

Lưu ý: RMSE của `mu_0`, `mu_1` chỉ kiểm tra chất lượng hai outcome models tầng đầu. Để so sánh X-Learner với các uplift models khác, cần ưu tiên Qini/AUUC và business policy value.

X-Learner được thử trên toàn bộ population. Kết quả base outcome models:

```text
mu_0 RMSE: 6.328
mu_1 RMSE: 6.379
AUUC / Qini score: 0.038
```

Khi chuyển sang profit:

```text
Phát voucher đại trà: -33,138.55
Top 20% user tốt nhất: 10,023.58
Tăng lợi nhuận so với phát rộng: 130.2%
```

Diễn giải:

```text
X-Learner tốt hơn T-Learner ở chỗ nó học trực tiếp pseudo-effect thay vì chỉ lấy hiệu hai outcome models.
Kết quả cho thấy model có khả năng tránh mass voucher và tìm nhóm target tốt hơn.
Tuy nhiên, pipeline nhiều tầng khiến pseudo-effect và calibration dễ nhiễu, nên chưa được chọn làm champion.
```

### 4.4 Simplified R-Learner-style Residual Model

Mô hình residual theo phong cách R-Learner được chọn làm champion vì nó phù hợp với bài toán promotion: phải tách user vốn đi nhiều khỏi user đi thêm vì voucher.

Implementation hiện có hai model: model đầu học `m(X)`, sau đó residualization và model cuối học `τ(X)`. Vì chưa dùng cross-fitting, project không gọi implementation này là full Double Machine Learning.

R-Learner học baseline outcome trước:

```text
m(X) = E[Y | X]
```

Sau đó residualize outcome và treatment:

```text
Y_tilde = Y - m(X)
T_tilde = T - e(X)
```

Vì project dùng randomized 50/50:

```text
e(X) = P(T = 1 | X) = 0.5
```

Pseudo-label để học treatment effect:

```text
uplift_target = Y_tilde / T_tilde
```

Sau đó train model cuối:

```text
r_model(X) -> uplift_target
```

với trọng số:

```text
W = T_tilde^2
```

**Vì sao hợp với bài toán này**

Rủi ro lớn nhất khi phát voucher là nhầm lẫn:

```text
người vốn đi nhiều
```

với:

```text
người đi thêm vì voucher
```

R-Learner xử lý bằng cách trừ baseline behavior trước. Nó không hỏi:

```text
Ai đi nhiều nhất?
```

mà hỏi:

```text
So với mức bình thường của kiểu user này, outcome có tăng cùng chiều với treatment không?
```

**Ưu điểm**

- Phù hợp khi baseline behavior giữa user rất khác nhau.
- Tách được hành vi nền khỏi incremental response.
- Ổn định hơn trong synthetic DGP hiện tại.

**Nhược điểm**

- Phụ thuộc vào chất lượng model baseline `m(X)`.
- Pseudo-label từng user vẫn có nhiễu.
- Cần đánh giá thêm bằng Qini, calibration và policy value.

**Đánh giá trong project**

R-Learner được chọn làm champion vì kết quả cân bằng nhất giữa model quality và business value:

```text
Mean predicted CATE: 0.9551
Qini Coef: 0.188
Users targeted với EV > 0: 888 / 4,000
Predicted profit: 7,939
Synthetic benchmark profit: 7,060
ROI: 54.1%
```

So với các policy khác:

```text
Mass Voucher: -65,358 predicted profit
Segment Targeting: -4,286 predicted profit
Top 30% CATE: -10,187 predicted profit
Profit Targeting EV > 0: 7,939 predicted profit
```

Diễn giải:

```text
R-Learner không chỉ rank tốt hơn random qua Qini Curve, mà còn tạo ra policy có lợi nhuận dương khi chuyển CATE sang Expected Value.
Điểm mạnh chính là khả năng tách baseline ride behavior khỏi incremental response do voucher.
```

### 4.5 DR-Learner Challenger

DR-Learner được thêm như một challenger nâng cao.

Nó bắt đầu từ:

```text
mu_1(X) - mu_0(X)
```

rồi sửa bằng sai số quan sát thực tế:

```text
DR_target =
mu_1(X) - mu_0(X)
+ T / e(X) * [Y - mu_1(X)]
- (1 - T) / (1 - e(X)) * [Y - mu_0(X)]
```

Sau đó train model cuối:

```text
tau_model(X) -> DR_target
```

**Tại sao DR-Learner được gọi là "Doubly Robust"?**

Đây là tính chất nổi bật nhất của DR-Learner: phương trình correction term có 2 thành phần độc lập:

$$DR\_target_i = \underbrace{\mu_1(X_i) - \mu_0(X_i)}_{\text{Thành phần 1: Dự đoán từ Outcome Models}} + \underbrace{\frac{T_i}{e(X_i)}[Y_i - \mu_1(X_i)] - \frac{1-T_i}{1-e(X_i)}[Y_i - \mu_0(X_i)]}_{\text{Thành phần 2: Correction bằng Sai số quan sát thực tế}}$$

- **Thành phần 1** (T-Learner component): Ước lượng hiệu ứng nhân quả dựa hoàn toàn vào 2 outcome models $\mu_0, \mu_1$. Nếu cả 2 model này chính xác, Thành phần 1 đã đủ tốt.
- **Thành phần 2** (Augmented correction): Dùng sai số quan sát thực tế $[Y_i - \mu_1(X_i)]$ và $[Y_i - \mu_0(X_i)]$ để "sửa lỗi" cho Thành phần 1. Nếu outcome model sai, phần correction sẽ bù đắp lại — với điều kiện Propensity Score $e(X)$ phải chính xác.
- **Tính "Doubly Robust":** Thuật toán cho kết quả $\hat{\tau}$ **nhất quán (consistent)** khi:
  - *Hoặc* outcome models $\mu_0, \mu_1$ chính xác (dù $e(X)$ sai), *hoặc*
  - *Hoặc* propensity model $e(X)$ chính xác (dù $\mu_0, \mu_1$ sai).
  - Chỉ cần **1 trong 2 loại model** ước lượng đúng là đủ.

**Tại sao DR-Learner bị overestimate trong project này?**

Trong setting RCT 50/50, $e(X) = 0.5$ là hằng số nên không cần ước lượng — Propensity Score đã chính xác. Nhưng trong DGP phức tạp ZINB, các outcome models $\mu_0, \mu_1$ vẫn còn sai số đáng kể (RMSE > 6). Khi $Y_i - \mu_1(X_i)$ (sai số outcome) lớn, correction term bị khuếch đại và tạo ra pseudo-target nhiễu, làm DR-Learner overestimate CATE ở một số user, dẫn đến predicted profit ảo cao hơn thực tế (Oracle profit âm).

**Ưu điểm**

- Có cơ chế correction, hấp dẫn về mặt lý thuyết.
- Kết hợp outcome models và propensity.
- Là challenger hợp lý trong dữ liệu randomized.

**Nhược điểm quan sát trong project**

- Correction term có thể khuếch đại noise của outcome.
- Model chọn target aggressive hơn.
- Trong test hiện tại, DR-Learner overestimate business value.

**Đánh giá trong project**

DR-Learner được dùng để kiểm tra xem một learner có correction doubly robust có vượt R-Learner không. Kết quả model-level:

```text
Mean predicted CATE: 0.8283
Qini Coef: 0.138
Users targeted với EV > 0: 1,266 / 4,000
```

Kết quả policy-level:

| Model | Mean CATE | Users Targeted (EV > 0) | Predicted Profit | Oracle Profit |
|---|---:|---:|---:|---:|
| R-Learner | 0.9551 | 888 | 7,939 | 7,060 |
| DR-Learner | 0.8283 | 1,266 | 23,288 | -2,033 |

Diễn giải:

```text
DR-Learner dự đoán profit cao hơn nhưng oracle profit lại âm.
Điều này cho thấy model overestimate treatment effect và calibration kém hơn.
R-Learner thận trọng hơn nhưng đáng tin hơn trong setting hiện tại.
```

## 5. Chỉ Số Đánh Giá Model

RMSE/MAE có thể xuất hiện trong các notebook exploratory, nhưng chúng chỉ đo khả năng dự đoán outcome `Y` của các nuisance/outcome models. Với uplift modeling, mục tiêu chính không phải dự đoán số chuyến chính xác nhất, mà là rank đúng user có treatment effect cao và tạo policy có lợi nhuận.

Vì vậy, tiêu chí chính để chọn champion model trong project là:

```text
1. Qini Curve / Qini Coef / AUUC
2. Calibration theo decile
3. Profit Targeting / Policy Value
4. Oracle Regret nếu có cate_true trong synthetic data
```

### 5.1 Qini Curve

User được sắp xếp theo `CATE_pred` từ cao xuống thấp. Tại mỗi mức top-k:

```text
N_T(k) = số treated users trong top k
N_C(k) = số control users trong top k
Y_T(k) = tổng outcome của treated users trong top k
Y_C(k) = tổng outcome của control users trong top k
```

Qini uplift:

```text
Qini(k) = Y_T(k) - Y_C(k) * N_T(k) / N_C(k)
```

Ý nghĩa:

```text
Qini(k) ước lượng cumulative incremental rides nếu target top-k users.
```

### 5.2 Qini Coefficient

Random baseline:

```text
Random_Qini(k) = k / N * Qini(N)
```

Diện tích dưới đường:

```text
AUUC_model = Area under Qini curve
AUUC_random = Area under Random_Qini curve
```

Qini coefficient trong notebook:

```text
Qini Coef = (AUUC_model - AUUC_random) / AUUC_random
```

**Công thức tính AUUC bằng Trapezoidal Rule (Tích phân số):**

$$AUUC = \sum_{k=1}^{N-1} \frac{Qini(k) + Qini(k+1)}{2} \cdot \Delta k$$

Trong đó: $\Delta k = \frac{1}{N}$ (mỗi bước tương ứng thêm 1 user vào danh sách target). Đây là phương pháp tính diện tích dưới đường cong bằng cách chia thành các hình thang nhỏ — cách làm chuẩn mực trong Uplift Model evaluation. **AUUC_random** được tính bằng diện tích tam giác dưới đường thẳng tuyến tính từ $(0, 0)$ đến $(N, Qini(N))$, tức là:
$$AUUC_{\text{random}} = \frac{1}{2} \cdot Qini(N)$$

Vì vậy, **Qini Coefficient** đo lường *phần diện tích vượt trội của model so với chiến lược target ngẫu nhiên*, được chuẩn hóa theo diện tích của đường random:
$$\text{Qini Coef} = \frac{AUUC_{\text{model}} - AUUC_{\text{random}}}{|AUUC_{\text{random}}|}$$

Diễn giải:

```text
Qini Coef > 0 nghĩa là model rank user tốt hơn random targeting.
Qini Coef = 1 là model hoàn hảo (target đúng toàn bộ người nhạy cảm trước).
Qini Coef < 0 nghĩa là model xếp hạng sai — target ngẫu nhiên còn tốt hơn.
```

Kết quả:

```text
T-Learner Qini Coef: -0.320
X-Learner Qini Coef: 0.038
S-Learner Qini Coef: 0.153
R-Learner Qini Coef: 0.188
DR-Learner Qini Coef: 0.138
```

R-Learner có ranking quality tốt nhất trong các model đã thử. S-Learner đứng sau R-Learner theo Qini, DR-Learner thấp hơn R-Learner và còn bị lệch mạnh khi quy đổi sang profit. X-Learner chỉ nhỉnh hơn random nhẹ, còn T-Learner âm nên không phù hợp làm model cuối.

### 5.3 Calibration theo Decile

User được chia thành 10 decile theo predicted CATE. Với mỗi decile:

```text
Predicted_CATE = trung bình CATE dự đoán
Observed_Uplift = mean(Y | T=1) - mean(Y | T=0)
Ground_Truth_CATE = trung bình cate_true
```

Mục tiêu là kiểm tra:

```text
Nhóm được model dự đoán CATE cao có thật sự có uplift cao không?
```

Kết luận:

```text
R-Learner có ranking signal hữu ích, nhưng calibration ở scale CATE vẫn chưa hoàn hảo.
```

Vì vậy, không nên chỉ nhìn predicted CATE, mà cần đánh giá thêm policy value.

## 6. Business Translation: Từ CATE Sang Expected Value

Model CATE chỉ dự đoán số chuyến tăng thêm. Business cần biết phát voucher có lời không.

Expected value của từng user:

```text
EV_i =
CATE_i * margin_per_ride_i
- pred_rides_treated_i * voucher_cost_i
```

Trong đó:

```text
margin_per_ride_i = avg_fare_i * margin_rate
voucher_cost_i = avg_fare_i * voucher_rate
pred_rides_treated_i = số chuyến dự đoán nếu user nhận voucher
```

Giả định hiện tại:

```text
voucher_rate = 15%
margin_rate = 70%
budget_limit = 50,000
```

Luật target cuối:

```text
Chỉ phát voucher nếu EV_i > 0.
```

Insight quan trọng:

```text
CATE cao không tự động đồng nghĩa với có lời.
Top-CATE users vẫn có thể lỗ nếu promotion burn lớn hơn incremental margin.
```

Vì vậy policy deployable là:

```text
Profit Targeting, không phải pure Uplift Targeting.
```

## 7. Công Thức Các Business Metrics

Với tập user được chọn là `S`:

### 7.1 Expected Incremental Rides

```text
Expected_Incremental_Rides = sum(CATE_i) với i thuộc S
```

### 7.2 Expected GMV

```text
Expected_GMV = sum(pred_rides_treated_i * avg_fare_i) với i thuộc S
```

### 7.3 Incremental GMV

```text
Incremental_GMV = sum(CATE_i * avg_fare_i) với i thuộc S
```

### 7.4 Promotion Burn

```text
Burn = sum(pred_rides_treated_i * voucher_cost_i) với i thuộc S
```

### 7.5 Predicted Incremental Profit

```text
Predicted_Incremental_Profit = sum(EV_i) với i thuộc S
```

Tương đương:

```text
Predicted_Incremental_Profit =
sum(CATE_i * margin_per_ride_i)
- sum(pred_rides_treated_i * voucher_cost_i)
```

### 7.6 CPIR: Cost Per Incremental Ride

```text
CPIR = Burn / Expected_Incremental_Rides
```

CPIR càng thấp càng tốt.

### 7.7 Burn per GMV

```text
Burn_per_GMV_pct = Burn / Expected_GMV * 100
```

### 7.8 Burn per Incremental GMV

```text
Burn_per_Inc_GMV_pct = Burn / Incremental_GMV * 100
```

### 7.9 Estimated ROI

```text
Est_ROI_pct = Predicted_Incremental_Profit / Burn * 100
```

### 7.10 Oracle Regret

Vì đây là synthetic data, ta có thể so policy học được với oracle policy:

```text
Oracle_Regret = Oracle_Profit - Model_Policy_Profit
```

và:

```text
Oracle_Regret_pct = Oracle_Regret / Oracle_Profit * 100
```

Kết quả:

```text
Oracle Profit = 10,818
R-Learner Profit Targeting oracle profit = 7,060
Oracle Regret = 3,758
Oracle Regret pct = 34.7%
```

## 8. So Sánh Các Policy

R-Learner champion được đưa vào policy simulator để so với các chiến lược khác.

### 8.1 No Voucher

Không phát voucher cho ai.

```text
Incremental profit = 0
```

Đây là baseline.

### 8.2 Mass Voucher

Phát voucher cho toàn bộ user.

Kết quả:

```text
Users targeted: 4,000
Predicted profit: -65,358
Synthetic benchmark profit: -76,313
ROI: -49.5%
```

Diễn giải:

```text
Mass Voucher lỗ nặng do cannibalization và promotion burn quá lớn.
```

### 8.3 Segment Targeting

Phát voucher cho user thuộc segment `Suburban`.

Kết quả:

```text
Users targeted: 1,660
Predicted profit: -4,286
Synthetic benchmark profit: -996
ROI: -12.1%
```

Diễn giải:

```text
Segment targeting tốt hơn mass voucher, nhưng vẫn quá thô và chưa có lời.
```

### 8.4 Uplift Targeting: Top 30% CATE

Phát voucher cho top 30% user có predicted CATE cao nhất.

Kết quả:

```text
Users targeted: 1,200
Predicted profit: -10,187
Synthetic benchmark profit: -25,360
ROI: -23.6%
```

Diễn giải:

```text
Target theo uplift thuần chưa đủ. Một số user uplift cao vẫn không profitable sau khi trừ voucher cost.
```

Mốc top 30% chỉ là benchmark, không phải ngưỡng tối ưu.

### 8.5 Profit Targeting: EV > 0

Chỉ phát voucher nếu:

```text
EV_i > 0
```

Kết quả:

```text
Users targeted: 888 / 4,000
Targeted share: 22.2%
Expected incremental rides: 1,112
Incremental GMV: 32,293
Burn: 14,666
CPIR: 13
Predicted profit: 7,939
Synthetic benchmark profit: 7,060
ROI: 54.1%
```

Diễn giải:

```text
Đây là policy triển khai tốt nhất trong synthetic sandbox hiện tại.
```

### 8.6 Budget-Constrained Policy

Sắp xếp user theo expected value và chọn đến khi chạm budget.

Trong kết quả hiện tại, policy này trùng với Profit Targeting:

```text
Users targeted: 888
Predicted profit: 7,939
Synthetic benchmark profit: 7,060
```

Lý do:

```text
Tổng burn của nhóm EV > 0 vẫn thấp hơn budget 50,000.
```

### 8.7 Oracle Policy

Oracle dùng `cate_true`, nên không deploy được ngoài đời thật. Nó chỉ là upper-bound benchmark.

Kết quả:

```text
Users targeted: 1,002
Synthetic benchmark profit: 10,818
```

Diễn giải:

```text
Oracle cho biết trần lý tưởng và khoảng còn có thể cải thiện của model.
```

## 9. Quyết Định Champion Model

R-Learner được chọn làm champion vì:

1. Qini ranking tốt nhất trong các model đã thử: `0.188`, cao hơn S-Learner `0.153`, DR-Learner `0.138`, X-Learner `0.038` và T-Learner `-0.320`.
2. Tạo predicted profit dương và synthetic benchmark profit dương.
3. Predicted profit gần với oracle-evaluated profit hơn DR-Learner, cho thấy đáng tin hơn.
4. Phù hợp với cấu trúc causal của bài toán: tách baseline ride behavior khỏi voucher-induced incremental response.

Khuyến nghị cuối:

```text
Dùng R-Learner để dự đoán CATE.
Dùng EV > 0 làm rule target deployable.
Dùng Qini, calibration, profit, ROI, CPIR và oracle regret để đánh giá.
```

## 10. Hạn Chế và Bước Tiếp Theo

1. **Bằng chứng chỉ nằm trong synthetic sandbox**

   Kết quả chứng minh methodology, không phải production impact thật.

2. **Calibration chưa hoàn hảo**

   Model có ranking signal hữu ích, nhưng scale CATE vẫn cần theo dõi.

3. **Top-k threshold chỉ là benchmark**

   Top 30% CATE không nên được hiểu là policy cuối.

4. **DR-Learner chưa nên bị loại vĩnh viễn**

   Một bản DR-Learner mạnh hơn có thể dùng full cross-fitting, clipping target và tuning hyperparameter.

5. **Triển khai thật cần champion/challenger experiment**

   Policy cuối phải được xác nhận bằng randomized experiment thật trước khi rollout.
