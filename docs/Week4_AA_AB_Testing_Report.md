# Nền tảng Thống kê cho A/B Testing (Tuần 4)

# Đánh giá Độ tin cậy Hệ thống & A/A Testing

## 1. Mục tiêu Đánh giá (Objective)
Trước khi đưa vào triển khai bất kỳ thí nghiệm A/B Testing nào, việc kiểm định tính ổn định của hệ thống phân bổ ngẫu nhiên (Randomization Pipeline) và công cụ phân tích thống kê là yêu cầu bắt buộc. Quá trình này được thực hiện thông qua A/A Testing — một thí nghiệm giả lập nơi không có bất kỳ sự can thiệp (Voucher) nào được áp dụng cho cả hai nhóm. 

Mục tiêu cốt lõi là xác minh Tỷ lệ Dương tính giả (False Positive Rate - Type I Error) của hệ thống hội tụ chính xác về mức lý thuyết ($\alpha = 0.05$), đồng thời đảm bảo không có sự thiên vị trong việc phân bổ mẫu.

## 2. Phương pháp Thực hiện (Methodology)
Dự án áp dụng phương pháp Mô phỏng Monte Carlo. Tập khách hàng mục tiêu (`Suburban Card`, N=2,792) được phân bổ ngẫu nhiên thành hai nhóm (A và A') qua **5.000 vòng lặp** độc lập. Các chỉ số thống kê được ghi nhận ở mỗi vòng lặp để phân tích hành vi của hệ thống.

## 3. Các Chỉ số Đánh giá & Kết quả

### 3.1. Kiểm tra Lỗi Cân bằng Mẫu (Sample Ratio Mismatch - SRM)
- **Phương pháp:** Sử dụng Kiểm định Chi-Square ($X^2$) qua 5000 vòng lặp, kết hợp **Kiểm định Nhị phân (Binomial Test)** để đánh giá tỷ lệ lỗi.
- **Ngưỡng tiêu chuẩn:** Số lần P-value < 0.05 phải tương đồng với mức kỳ vọng ngẫu nhiên (5%). Binomial P-value > 0.05.
- **Kết quả đo lường:** Số lần cảnh báo SRM là **263/5000 (5.26%)**. Khoảng tin cậy hoàn toàn phù hợp với phương sai ngẫu nhiên (Binomial P-value = **0.3988**).
- **Kết luận:** ĐẠT (PASS). Không phát hiện dấu hiệu bất thường đáng kể về randomization trong các simulation settings đã kiểm tra. Tỷ lệ phân bổ user 50/50 là tương đối chính xác.

### 3.2. Kiểm tra Độ Cân bằng Đặc trưng (Covariate Balance — SMD)
- **Phương pháp:** Được thực hiện trong bước Sanity Check của A/B Test Analysis. Thay vì dùng T-Test thông thường dễ báo lỗi khi cỡ mẫu lớn, dự án sử dụng chỉ số **SMD (Standardized Mean Difference)** để kiểm tra độ cân bằng của các biến hiệp phương sai (Tuổi, Lịch sử chuyến đi, Số ngày ngủ đông, Giá vé trung bình) trước thí nghiệm.

- **Công thức SMD:**
$$SMD = \frac{\bar{X}_{T} - \bar{X}_{C}}{\sqrt{\dfrac{s^2_T + s^2_C}{2}}}$$

  Trong đó: $\bar{X}_T$, $\bar{X}_C$ là giá trị trung bình của biến trong nhóm Treatment và Control; $s^2_T$, $s^2_C$ là phương sai tương ứng. SMD chuẩn hóa sự chênh lệch theo đơn vị độ lệch chuẩn gộp, giúp so sánh được trên nhiều biến có đơn vị đo khác nhau. Ngưỡng $|SMD| < 0.1$ tương đương "chênh lệch dưới 10% độ lệch chuẩn" — mức được coi là không đáng kể về mặt thực tiễn (Cohen, 1988).

- **Ngưỡng tiêu chuẩn:** Giá trị $|SMD| < 0.1$ cho tất cả các biến.
- **Kết quả đo lường:** Hệ thống duy trì sự cân bằng đặc trưng đáng tin cậy, toàn bộ các biến quan trọng đều có $|SMD| < 0.1$.
- **Kết luận:** ĐẠT (PASS). |SMD| < 0.1 cho thấy không phát hiện material imbalance đáng kể trên các observed covariates được kiểm tra.

### 3.3. Kiểm tra Tỷ lệ Dương tính giả (False Positive Rate - FPR)
- **Phương pháp:** Đo lường tỷ lệ các vòng lặp A/A Test trả về P-value < 0.05 (FPR) và kiểm chứng bằng **KS-Test (Kolmogorov-Smirnov)** để xác nhận phân phối P-value là Uniform. *(Lưu ý: Bỏ qua Binomial Test thuần túy do đặc tính biến rời rạc của số chuyến đi).*
- **Ngưỡng tiêu chuẩn:** FPR không có sự khác biệt ý nghĩa thống kê so với 5.0%. KS-Test P-value > 0.05.
- **Kết quả đo lường:** Tỷ lệ False Positive thực tế đạt **5.08%** (254 lỗi / 5000 lần). KS-Test P-value = **0.5691**.
- **Kết luận:** ĐẠT (PASS). FPR quan sát được phù hợp với mức alpha 5% trong các simulation settings đã kiểm tra.

## 4. Kết luận Tổng thể
Không phát hiện randomization/statistical calibration issue đáng kể dưới các thiết lập mô phỏng đã kiểm tra. Pipeline có đủ độ tin cậy để chạy A/B Test trong môi trường synthetic. Để áp dụng vào dữ liệu GSM thật, cần thêm: kiểm tra exposure/logging, invariant metrics và guardrails thực tế vận hành.



---


## 1. Phương pháp Kiểm định Giả thuyết Nâng cao (OLS Regression with HC1)
Thay vì sử dụng phương pháp T-Test truyền thống (có phương sai lớn, dễ dẫn đến khoảng tin cậy rộng và khó phát hiện sự khác biệt), dự án đã nâng cấp thuật toán đo lường ATE bằng **Mô hình Hồi quy OLS với Robust Standard Errors (HC1)**.

**Công thức hồi quy đầy đủ:**
$$Y_i = \beta_0 + \hat{\tau} \cdot T_i + \gamma \cdot X_{\text{history}, i} + \varepsilon_i$$

Trong đó:
- $Y_i$: Số chuyến đi sau thí nghiệm của user $i$ (biến mục tiêu).
- $T_i \in \{0, 1\}$: Biến nhị phân chỉ định user $i$ thuộc nhóm Control ($0$) hay Treatment ($1$).
- $\hat{\tau}$: **Ước lượng ATE** — hệ số quan tâm chính, đo lường số chuyến đi tăng thêm do Voucher gây ra trung bình trên toàn bộ mẫu.
- $X_{\text{history}, i}$: Biến điều kiện (Covariate) — lịch sử chuyến đi trước thí nghiệm của user $i$, thu thập trước khi phát Voucher để không bị ô nhiễm bởi treatment.
- $\gamma$: Hệ số của Covariate. Việc đưa biến lịch sử vào giúp giải thích một phần biến thiên tự nhiên của $Y_i$, từ đó giảm phương sai của số dư $\varepsilon_i$ và thu hẹp khoảng tin cậy của $\hat{\tau}$ (tương tự mục đích CUPED của Microsoft/Netflix nhưng dưới dạng OLS covariate adjustment).
- $\varepsilon_i$: Sai số của mô hình.

**Ước lượng ma trận phương sai Robust (HC1 — White/Huber-White Estimator):**
$$\widehat{\text{Var}}_{HC1}(\hat{\beta}) = \frac{n}{n-k} (X^\top X)^{-1} \left(\sum_{i=1}^{n} \hat{\varepsilon}_i^2 x_i x_i^\top \right) (X^\top X)^{-1}$$

Trong đó: $n$ là cỡ mẫu, $k$ là số tham số, $\hat{\varepsilon}_i$ là phần dư của từng quan sát. Hiệu chỉnh $\frac{n}{n-k}$ của HC1 giúp chuẩn sai không bị ước lượng thấp hơn thực tế (downward bias) so với HC0. Nhờ đó, Khoảng tin cậy 95% và P-value đảm bảo tính chính xác kể cả khi phương sai sai số không đồng nhất (Heteroskedasticity) — điều gần như chắc chắn xảy ra khi nhóm Treatment và Control có hành vi khác nhau.

- **Pre-treatment Covariate Adjustment:** Mô hình Hồi quy đưa thêm biến lịch sử chuyến đi (`monthly_rides_history`) vào làm Covariate (biến đã có trước treatment). Kỹ thuật này giúp giảm phương sai của số dư, tương tự về mục đích với CUPED — nhưng không triển khai đầy đủ CUPED formulation của Microsoft/Netflix.
- **Robust Standard Errors (HC1):** HC1 cung cấp heteroskedasticity-robust standard errors, giúp inference bền vững hơn khi phương sai sai số không đồng nhất dưới các giả định hồi quy thông thường.

- **Giả thuyết Không ($H_0$):** Hệ số của biến Treatment trong phương trình hồi quy bằng 0 (Voucher không có tác dụng).
- **Giả thuyết Đối ($H_1$):** Hệ số của biến Treatment khác 0 (Voucher có tác động).
Việc bác bỏ Giả thuyết $H_0$ dựa trên P-value < $\alpha = 0.05$.

## 2. Tiêu chí Đánh giá trong A/B Testing
Hệ thống phân tích thực hiện hai phép đo lường thống kê độc lập tùy thuộc vào mục tiêu đánh giá:

### 2.1. Sanity Checks (Kiểm tra Cân bằng Hệ thống)
- **Mục tiêu:** Kiểm chứng thuật toán phân bổ ngẫu nhiên đã chia đều khách hàng vào các nhóm, đảm bảo tính đồng nhất (Comparability) trước khi phân tích kết quả.
- **Giả thuyết Không ($H_0$):** Hai nhóm hoàn toàn cân bằng về các đặc tính (Độ chênh lệch = 0).
- **Kết quả Kỳ vọng:** Mục tiêu ở bước này là **không thể bác bỏ $H_0$**. Covariate balance được đánh giá chủ yếu bằng SMD. Không reject null hypothesis (P-value > 0.05) không đồng nghĩa với chứng minh hai nhóm tương đương hoàn toàn, mà chỉ cho thấy không có bằng chứng thống kê để kết luận có lỗi SRM hoặc Covariate Imbalance.

### 2.2. Chỉ số Đánh giá Cốt lõi (Overall Evaluation Criterion - OEC)
- **Mục tiêu:** Đo lường tác động nhân quả thực sự của sự can thiệp (Voucher) lên chỉ số mục tiêu (Số chuyến đi tăng thêm).
- **Giả thuyết Không ($H_0$):** Sự can thiệp không mang lại tác động nào (Độ chênh lệch = 0).
- **Kết quả Kỳ vọng:** Mục tiêu ở bước này là **bác bỏ $H_0$** nhằm chứng minh hiệu quả của Voucher. Do đó, yêu cầu **P-value < 0.05** để kết luận mức độ tăng trưởng quan sát được có ý nghĩa thống kê và không xuất phát từ phương sai ngẫu nhiên.

## 3. Chỉ số An toàn Tài chính & Monte Carlo Stress Test
Bên cạnh ý nghĩa thống kê, ý nghĩa thực tiễn của chiến dịch được đánh giá thông qua chỉ số **Tỷ suất Hoàn vốn (ROI)**. ROI dương chứng minh chiến dịch sinh lời.

**Vũ khí Hạng nặng: Monte Carlo Stress Test**
Để bảo vệ mô hình thống kê trước mọi sự chất vấn, dự án đã cấy một hệ thống Stress Test giả lập vòng lặp 1.000 lần Monte Carlo với các kịch bản Effect Size (0, 0.1, 0.5, 1.0).
- **Kết quả:** Khi Voucher không có tác dụng (Scale = 0), qua 5,000 simulations, tỷ lệ báo động giả luôn kiểm soát chặt ở mức ~5% (FPR ≈ 5.08%, SRM alert rate ≈ 5.26%). Khi Voucher có tác dụng, độ chệch (Bias) của thuật toán OLS HC1 cực kỳ thấp (Bias < 0.002 ở mọi mức Scale). Randomization giúp cân bằng exogenous noise theo kỳ vọng, nhưng noise vẫn làm tăng uncertainty của estimator.

---

## 4. Kết quả Thực thi A/B Test (Empirical Results)

Dưới đây là kết quả A/B Testing thực tế được bóc tách theo các Behavioral Personas. Kết quả minh họa treatment heterogeneity được thiết kế trong synthetic DGP.

| Phân khúc Khách hàng (Persona) | N Users | ATE (Chuyến tăng thêm) | P-value | Promotion Burn ($) | CPIR ($/chuyến) | ROI | Kết luận Hành động |
|---|---|---|---|---|---|---|---|
| **Urban Regulars** | 8,424 | +1.00 | 3.18e-8 | ~$126,360 | ~$15.0 | **-40.7%** | ❌ Negative economics. Voucher bị cannibalized bởi nhóm đi bắt buộc. |
| **Rain Riders** | 2,592 | +0.86 | 0.010 | ~$38,880 | ~$17.4 | **-38.9%** | ❌ Negative economics. Hành vi phụ thuộc thời tiết, không phụ thuộc Voucher. |
| **Airport Business** | 1,131 | +1.21 | 0.008 | ~$56,550 | ~$41.3 | **-18.0%** | ❌ Negative economics. Giá vé cao nhưng nhóm kháng giá cực mạnh. |
| **Suburban Card** | 2,792 | +1.04 | **6.57e-7** | ~$27,920 | ~$9.6 | **+20.7%** | ✅ Positive economics. CPIR thấp nhất nhóm có lời. Candidate for validation. |
| **Suburban Cash** | 5,061 | +0.79 | **≈0** | ~$50,610 | ~$12.7 | **+24.7%** | 💡 Positive economics. ROI cao nhất. Candidate for validation. |




**Diễn giải các chỉ số bổ sung:**
- **Promotion Burn ($):** Tổng chi phí phát Voucher cho toàn bộ người dùng trong phân khúc — ước tính theo giá vé trung bình và Voucher Rate 15%.
- **CPIR (Cost Per Incremental Ride):** Chi phí để tạo ra 1 chuyến đi tăng thêm do Voucher gây ra:
  $$CPIR = \frac{\text{Promotion Burn}}{\text{ATE} \times N_{\text{nhóm}}}$$
  Giá trị CPIR thấp ($<10\$/chuyến) cho thấy chiến dịch đang khai thác đúng nhóm nhạy cảm với Voucher; giá trị cao cho thấy chi phí đang rơi vào nhóm sẽ đặt xe dù không có Voucher (Cannibalization).
- **ROI:** Lợi nhuận tăng thêm trên tổng chi phí Voucher đã chi ra:
  $$ROI = \frac{\text{Incremental Margin} - \text{Promotion Burn}}{\text{Promotion Burn}} \times 100\%$$
  Trong đó: $\text{Incremental Margin} = ATE \times N_{\text{nhóm}} \times \text{AvgFare} \times \text{MarginRate}$.


> **💡 Bài học Kinh doanh Cốt lõi:**
> Nếu ta chỉ chạy A/B Test đại trà (Mass Voucher) trên toàn bộ 20,000 user mà không phân cụm, **chiến dịch sẽ lỗ ròng -$116,338**.
> 
> Behavioral personas hỗ trợ segment-level interpretation, giúp hệ thống phát hiện được 2 nhóm sinh lời:
> - **Suburban Card**: ROI +20.7%, Candidate for further validation, lợi nhuận +$13,993 từ 2,792 users.
> - **Suburban Cash**: ROI +24.7%, Candidate for further validation.


---

