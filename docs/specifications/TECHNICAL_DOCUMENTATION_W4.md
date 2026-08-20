# TECHNICAL DOCUMENTATION — WIP AFTER 4 WEEKS
## Growth & Experimentation Project for Ride-Hailing Promotions

> **Document status:** WIP Technical Documentation — Snapshot at the end of Week 4  
> **Current project week:** Week 5  
> **Repository:** `GSM-promotion-experimentation`  
> **Purpose:** Mô tả thành phẩm kỹ thuật đã hoàn thành trong 4 tuần đầu, cách các thành phần nối với nhau, các output đã có, cách demo, và giới hạn hiện tại.
>
> **Scope boundary:** Đây là một **simulation-based experimentation sandbox**. Dữ liệu treatment/outcome và các kết quả causal là dữ liệu mô phỏng, không phải kết quả production của GSM/Xanh SM.
> 
> **Methodology Update:** At the Week 4 snapshot, some artifacts used inconsistent analysis horizons. This was standardized to a 30-day primary outcome window in subsequent project iterations.

---

# 1. Executive Summary

Sau 4 tuần đầu, project đã hoàn thành một pipeline WIP end-to-end theo luồng:

```text
Public Mobility Data
        ↓
Data Quality & EDA
        ↓
Synthetic User-Level Causal Data
        ↓
Y0 / CATE / Y1 Ground Truth
        ↓
K-Means Segmentation
        ↓
Experiment Design
        ↓
A/A Testing
        ↓
SRM + Covariate Balance
        ↓
A/B Testing
        ↓
ATE + Confidence Interval
        ↓
Segment-Level Business Interpretation
```

Core deliverable đến hết Week 4 là:

1. Data foundation và preprocessing.
2. Synthetic causal data generation.
3. User segmentation.
4. Experiment specification.
5. A/A testing và trust checks.
6. A/B effect estimation.
7. Business interpretation bằng incremental rides / incremental revenue / voucher cost / ROI trong sandbox.

**Uplift Modeling không thuộc snapshot Week 4.** Đây là extension bắt đầu từ Week 5 để đi từ Average Treatment Effect sang Individual/Conditional Treatment Effect và targeting policy.

---

# 2. Business / Technical Problem

Bài toán tổng quát của project:

> Làm thế nào để đánh giá promotion theo góc nhìn **incremental effect**, thay vì chỉ quan sát correlation hoặc số chuyến/doanh thu sau khi phát voucher?

Một user có số chuyến cao sau khi nhận voucher chưa chắc tăng số chuyến **vì voucher**. Họ có thể vốn đã là heavy user.

Do đó project được xây theo causal experimentation flow:

```text
Behavioral Data
→ Counterfactual Simulation
→ Randomized Experiment
→ Treatment Effect Estimation
```

---

# 3. Vì sao cần Synthetic Causal Data?

Nguồn public mobility data chủ yếu ở mức **trip-level**.

Trong khi A/B Testing và treatment-effect analysis cần cấu trúc gần với:

```text
user_id
pre-treatment features
treatment assignment
potential outcome Y0
potential outcome Y1
observed outcome
```

Public trip data không cung cấp trực tiếp:

- treatment/control thật,
- voucher exposure,
- counterfactual outcome,
- true treatment effect,
- persistent user-level causal history phù hợp.

Vì vậy project sử dụng public/reference data để tạo **empirical inputs**, sau đó xây một synthetic causal population để có known ground truth.

Mục tiêu của synthetic data không phải:

> “Mô phỏng chính xác khách hàng GSM.”

Mà là:

> **Tạo một laboratory có known causal truth để kiểm tra pipeline experimentation.**

---

# 4. High-Level Architecture — W4 Snapshot

```text
┌───────────────────────────────┐
│  NYC TLC / Reference Data     │
└───────────────┬───────────────┘
                ↓
┌───────────────────────────────┐
│ Week 1 — Data Quality & EDA   │
│ Clean / Audit / Patterns      │
└───────────────┬───────────────┘
                ↓
┌───────────────────────────────┐
│ Week 2 — Synthetic Causal DGP │
│ Covariates → Y0 → CATE → Y1  │
└───────────────┬───────────────┘
                ↓
┌───────────────────────────────┐
│ Week 3 — K-Means + Design     │
│ Persona + Experiment Spec     │
└───────────────┬───────────────┘
                ↓
┌───────────────────────────────┐
│ Week 4 — A/A + A/B Analysis   │
│ Trust Checks → ATE → ROI      │
└───────────────────────────────┘
```

---

# 5. WEEK 1 — Data Foundation

## 5.1. Data source

Nguồn chính:

- NYC TLC Yellow Taxi — January 2026.
- Taxi Zone Lookup.
- Community/reference ride-sharing data được dùng ở một số bước để tham khảo user-level structure.

Raw Yellow Taxi dataset trong Data Quality Report có:

```text
3,724,889 trip records
20 columns after geographic enrichment
```

## 5.2. Data Quality Audit

Các nhóm vấn đề được kiểm tra:

### Missing values

Một nhóm cột có missing rate lớn và có cấu trúc, thay vì missing ngẫu nhiên.

Project không dùng chiến lược:

```text
dropna() everything
```

mà cố phân biệt:

```text
Structural Missing
vs
Invalid Record
```

### Logical / physical validity

Kiểm tra các trường hợp như:

- negative fare,
- zero / invalid distance,
- pickup/dropoff timestamp inconsistency,
- extreme speed,
- cross-column monetary inconsistency,
- unknown geographic zones.

### Outlier philosophy

Nguyên tắc xử lý:

> **Outlier không mặc nhiên là Error.**

Extreme observations vẫn được giữ nếu không vi phạm business/physical logic rõ ràng.

---

# 6. Week 1 Output

Các artifact chính:

```text
docs/Week1_Data_Quality_Report.md
docs/Week1_Data_Preprocessing_Report.md
```

Vai trò của Week 1 không chỉ là cleaning.

EDA được dùng để lấy các empirical patterns phục vụ simulation, bao gồm:

- fare behavior,
- time-of-day demand,
- airport/non-airport characteristics,
- trip-level distributions.

---

# 7. WEEK 2 — Synthetic Causal Data Generation

Đây là một trong những technical components quan trọng nhất của project.

Synthetic population:

```text
N_USERS = 20,000
```

Pipeline chính:

```text
Pre-treatment Covariates
        ↓
Baseline Potential Outcome Y0
        ↓
Expected Treatment Effect / CATE
        ↓
Potential Outcome Y1
        ↓
Randomized Treatment
        ↓
Observed RCT Outcome
```

---

# 8. Pre-Treatment Features

Synthetic population bao gồm các nhóm feature như:

### Behavioral

- `monthly_rides_history`
- `recency_days`
- `preferred_hour`
- weekend / rush-hour behavior

### Spatial / usage context

- `is_urban`
- `is_airport_trip`

### Payment / monetary

- payment behavior
- `avg_fare_per_trip`

### Synthetic demographics

- age
- income-related variables

> Age/income là **simulation assumptions** để tạo heterogeneity; không được calibrated trực tiếp từ NYC TLC.

---

# 9. Baseline Potential Outcome — Y0

`Y0` đại diện:

> Số chuyến user sẽ thực hiện nếu **không nhận voucher**.

Project dùng:

> **Zero-Inflated Negative Binomial (ZINB)**

thay vì Poisson đơn giản.

Lý do:

```text
Ride count data
├── nhiều zero
└── overdispersion / heavy-user tail
```

ZINB cho phép mô phỏng đồng thời:

1. user có activity count theo Negative Binomial;
2. nhóm inactive/zero-heavy qua zero-inflation.

---

# 10. Treatment Effect Ground Truth

Pipeline hiện phân biệt hai khái niệm:

```text
cate_true
=
Expected treatment effect conditional on X

ite_realized
=
Y1 - Y0 after stochastic draws
```

`cate_true` được thiết kế từ heterogeneous causal rules dựa trên behavioral context.

Ví dụ treatment response có thể thay đổi theo:

- urban/suburban context,
- leisure/weekend behavior,
- airport trip,
- rush-hour behavior,
- payment behavior,
- recency.

Điểm quan trọng:

> Treatment effect được tạo trong causal DGP **trước K-Means**.

K-Means không tạo ra ground-truth effect.

---

# 11. Potential Outcome — Y1

Sau khi có baseline process và treatment-effect mechanism:

```text
Expected Y1
=
Expected Y0 + treatment effect
```

Sau đó potential outcome thực tế được sample từ count process.

Synthetic setup vì vậy có:

```text
Y0
Y1
cate_true
ite_realized
```

để phục vụ validation.

---

# 12. Hai Treatment Assignment Mechanisms

Project tạo hai thế giới khác nhau.

## 12.1. Observational Assignment

Treatment probability phụ thuộc vào các feature/confounder.

Mục đích:

> Minh họa vì sao observational comparison có thể bias.

## 12.2. Randomized Assignment

Treatment được randomize theo user/block.

Mục đích:

- A/A Testing
- A/B Testing
- unbiased effect estimation trong sandbox.

Observed randomized outcome:

```text
Y_rand =
Y1 if Treatment = 1
Y0 if Treatment = 0
```

---

# 13. Week 2 Output

Artifact kỹ thuật:

```text
notebooks/week2_synthetic_data/
docs/Week2_Synthetic_Data_Comprehensive_Report.md
src/pipeline/main_pipeline.py
data/processed/...
```

Week 2 tạo nền tảng để các tuần sau có thể so:

```text
Estimated Effect
vs
Known Ground Truth
```

---

# 14. WEEK 3 — User Segmentation

> **Historical note:** Week 3 explored PCA + K-Means for behavioral structure discovery. The current final dashboard uses stable rule-based behavioral persona labels for reporting consistency.

K-Means được dùng để tạo behavioral personas phục vụ:

- business interpretation,
- experiment slicing,
- heterogeneity analysis.

Pipeline:

```text
Behavioral Features
        ↓
Standardization
        ↓
PCA
        ↓
K-Means
        ↓
5 Personas
```

Current Week 3 report mô tả:

```text
11 behavioral features
→ PCA giữ ~90% variance
→ 9 principal components
→ K = 5
```

5 persona:

1. Urban Regulars
2. Rain Riders
3. Airport Business
4. Suburban Cash
5. Suburban Card

---

# 15. Vai trò đúng của K-Means

K-Means trả lời:

> Những user nào có behavioral profile tương tự nhau?

K-Means **không** trả lời:

> User nào thực sự thay đổi vì voucher?

Vì vậy ở snapshot Week 4:

```text
K-Means
=
Segmentation / Reporting Layer
```

chứ chưa phải individualized targeting engine.

---

# 16. WEEK 3 — Experiment Design

Experiment design được xây ở mức user.

## Randomization unit

```text
User
```

Lý do:

- mỗi user chỉ thuộc Treatment hoặc Control;
- tránh cùng user bị cả hai trạng thái treatment trong cùng experiment.

## Core estimand

```text
ATE
=
E[Y(1) - Y(0)]
```

Primary outcome:

```text
Incremental Rides per User
```

---

# 17. Experiment Design Components

Experiment spec bao gồm:

- population / eligibility,
- treatment,
- control,
- randomization unit,
- treatment ratio,
- pre-treatment window,
- outcome window,
- primary metric,
- economics guardrails,
- power / MDE,
- decision logic.

> Một số voucher value, business threshold và campaign mechanics trong Week 3 docs là **illustrative simulation assumptions**, không phải confirmed GSM production parameters.

---

# 18. Power / Sample Size

Week 3 experiment design có Power Analysis với:

```text
alpha = 0.05
power = 0.80
```

và một MDE assumption để estimate required sample size.

Vai trò:

> Xác định experiment có đủ sample để phát hiện business-relevant effect hay không.

---

# 19. WEEK 4 — A/A Testing

Trước khi phân tích A/B effect, pipeline kiểm tra randomization/statistical behavior bằng A/A Testing.

Setup được report:

```text
Target sample:
Suburban Card
N = 2,792

Monte Carlo repetitions:
5,000
```

---

# 20. Sample Ratio Mismatch — SRM

SRM dùng để kiểm tra:

```text
Observed assignment
vs
Expected assignment
```

Week 4 report ghi nhận:

```text
SRM alerts:
263 / 5,000
= 5.26%

Binomial p-value:
0.3988
```

Diễn giải WIP:

> Không phát hiện dấu hiệu bất thường đáng kể so với random variation trong simulation setting đã kiểm tra.

---

# 21. Covariate Balance

Balance được kiểm bằng:

> **Standardized Mean Difference — SMD**

Các pre-treatment covariates được kiểm tra gồm những feature như:

- age,
- ride history,
- recency,
- average fare / usage-related features.

Diagnostic threshold:

```text
|SMD| < 0.1
```

Mục tiêu:

> Kiểm tra Treatment và Control có comparable về các observed pre-treatment features hay không.

---

# 22. False Positive Rate Calibration

A/A Monte Carlo dùng để kiểm tra Type-I Error behavior.

Week 4 report ghi:

```text
False Positive Rate:
5.08%

KS-test p-value:
0.5691
```

Diễn giải:

> FPR quan sát được gần mức alpha = 5% trong simulated A/A runs; không phát hiện calibration issue đáng kể trong các settings đã kiểm tra.

---

# 23. WEEK 4 — A/B Effect Estimation

A/B analysis sử dụng:

> **OLS Regression with HC1 robust standard errors**

với pre-treatment covariate adjustment.

Mô hình khái niệm:

```text
Outcome
=
β0
+ β1 × Treatment
+ β2 × PreTreatmentHistory
+ error
```

Trong đó:

```text
β1
≈
Estimated ATE
```

HC1 được dùng để có heteroskedasticity-robust standard errors.

---

# 24. Statistical Outputs

Core outputs:

- Treatment mean
- Control mean
- ATE
- Confidence Interval
- p-value

Bên cạnh statistical significance, project bổ sung sandbox economics:

- Incremental revenue / GMV proxy
- Voucher cost
- Net incremental value
- ROI

Mục đích:

> Không chỉ hỏi effect có statistical significance hay không, mà còn xem effect có đủ lớn để bù promotion cost dưới assumptions hiện tại hay không.

---

# 25. Segment-Level W4 Results

Week 4 report hiện ghi các kết quả synthetic theo persona:

| Persona | N | ATE (incremental rides) | ROI |
|---|---:|---:|---:|
| Urban Regulars | 8,424 | +1.00 | -40.7% |
| Rain Riders | 2,592 | +0.86 | -38.9% |
| Airport Business | 1,131 | +1.21 | -18.0% |
| Suburban Card | 2,792 | +1.04 | +20.7% |
| Suburban Cash | 5,061 | +0.79 | +24.7% |

> **Important:** Đây là kết quả từ **synthetic DGP và economics assumptions**. Chúng minh họa pipeline có thể phát hiện treatment heterogeneity và khác biệt economics giữa segment; không phải bằng chứng về segment thật của GSM.

---

# 26. W4 Interpretation

Từ sandbox:

```text
Average Treatment Effect
≠
Uniform Business Value
```

Một segment có ATE dương vẫn có thể có ROI âm nếu:

```text
incremental value
<
voucher cost
```

Đây là lý do Week 4 không chỉ dừng ở p-value.

---

# 27. W4 Deliverables — Completed

Đến cuối Week 4, các khối đã có:

```text
[✓] Data Quality & Preprocessing
[✓] EDA foundation
[✓] Synthetic user-level causal data
[✓] Y0 / Y1 / treatment-effect ground truth
[✓] K-Means segmentation
[✓] Experiment design
[✓] Power / MDE logic
[✓] A/A Monte Carlo
[✓] SRM check
[✓] Covariate balance
[✓] A/B effect estimation
[✓] Segment-level treatment analysis
[✓] Sandbox economics / ROI interpretation
[✓] Reusable analysis pipeline
```

---

# 28. W4 Deliverables — Not Yet Core / Next Week

Không thuộc W4 completion snapshot:

```text
[→] Uplift Modeling
[→] Individual CATE prediction
[→] Qini / AUUC
[→] Profit-aware targeting policy
[→] GMV/Burn policy optimization
[→] Oracle policy / policy regret
[→] Extended stress testing
```

Các phần này thuộc Week 5+ extension.

---

# 29. Repository Structure Relevant to W4

```text
GSM-promotion-experimentation/
│
├── docs/
│   ├── Week1_Data_Quality_Report.md
│   ├── Week1_Data_Preprocessing_Report.md
│   ├── Week2_Synthetic_Data_Comprehensive_Report.md
│   ├── Week3_Comprehensive_Report.md
│   └── Week4_AA_AB_Testing_Report.md
│
├── notebooks/
│   ├── week1_...
│   ├── week2_synthetic_data/
│   ├── week3_...
│   └── week4_...
│
├── src/
│   ├── pipeline/
│   │   └── main_pipeline.py
│   └── dashboard/
│       └── app.py
│
├── data/
│   └── processed/
│
├── requirements.txt
└── README.md
```

---

# 30. Technical Stack

Main stack visible in the project:

```text
Python
Pandas
NumPy
SciPy
scikit-learn
XGBoost
Statsmodels / statistical tooling
Plotly
Streamlit
```

Core techniques through Week 4:

```text
EDA
Data Validation
Zero-Inflated Negative Binomial
Structural Causal Simulation
PCA
K-Means
Power Analysis
Monte Carlo A/A
Chi-Square / SRM
SMD
OLS
HC1 Robust SE
A/B Testing
```

---

# 31. How to Run the WIP Demo

From repository root:

```bash
pip install -r requirements.txt
streamlit run src/dashboard/app.py
```

The current Streamlit application may contain features added after Week 4.

For a **W4 demo**, the recommended story is:

```text
Data Foundation
→ Experiment Setup
→ Experiment Health
→ A/B Result
→ Segment / Heterogeneity Interpretation
```

Nếu dashboard hiện hiển thị Uplift/Policy tabs:

> Giới thiệu rõ đây là **Week 5 WIP extension**, không phải deliverable đã hoàn thành ở cuối Week 4.

---

# 32. Recommended Demo Flow — 7 Minutes

## 0:00–0:40 — Problem

> Mục tiêu là đo incremental effect của promotion chứ không chỉ correlation.

## 0:40–1:40 — Data Foundation

Show:

```text
Public trip data
→ EDA
→ synthetic user-level population
```

Nhấn mạnh data challenge:

> Trip-level data không có treatment/counterfactual.

## 1:40–2:30 — Causal Simulation

Show:

```text
Y0
CATE / treatment effect
Y1
Randomized treatment
```

Key point:

> Synthetic sandbox cho phép biết ground truth.

## 2:30–3:15 — K-Means

Show 5 personas.

Key point:

> K-Means dùng để segmentation/reporting.

## 3:15–4:15 — Experiment Setup

Show:

- treatment/control
- MDE
- power
- sample size.

## 4:15–5:15 — Experiment Health

Show:

- SRM
- SMD
- A/A result.

Key point:

> Không đọc A/B result trước khi kiểm tra experiment health.

## 5:15–6:30 — A/B Result

Show:

- ATE
- CI
- p-value
- segment differences
- sandbox ROI.

## 6:30–7:00 — Current Week 5

Conclude:

> “Core pipeline đến cuối Week 4 dừng ở A/B + business interpretation. Week 5 em đang mở rộng sang Uplift Modeling để đi từ average treatment effect sang individual treatment response.”

---

# 33. Current Limitations

## 33.1. Synthetic Ground Truth

Treatment effects được thiết kế trong DGP.

Do đó:

> W4 validates methodology under controlled assumptions, không estimate GSM production causal effect.

## 33.2. Demographic assumptions

Một số synthetic features như age/income không đến trực tiếp từ TLC.

## 33.3. Business economics

Voucher cost / margin / ROI assumptions là sandbox parameters.

## 33.4. Exposure / logging

Synthetic environment chưa phản ánh đầy đủ:

- failed exposure,
- production logging loss,
- campaign collision,
- interference,
- operational constraints.

## 33.5. Analysis-window consistency

At the Week 4 snapshot, some artifacts used inconsistent analysis horizons. This was standardized to a 30-day primary outcome window in subsequent project iterations.

Trước final delivery cần chuẩn hóa hoặc label rõ từng horizon.

---

# 34. Evidence Boundary

| Validated in W4 Sandbox | Chưa thể kết luận cho Production |
|---|---|
| Synthetic randomization behavior | GSM assignment integrity |
| A/A FPR behavior | Production tracking quality |
| ATE recovery in simulation | Real promotion ATE |
| Segment heterogeneity in DGP | Real GSM segment response |
| ROI under assumed economics | Real GSM campaign ROI |

---

# 35. W5 Next Step

Sau W4, extension tự nhiên là:

```text
A/B
→ Average Treatment Effect

then

Uplift Modeling
→ Conditional / Individual Treatment Response
```

Mục tiêu Week 5:

- benchmark uplift learners,
- evaluate ranking quality,
- compare predicted CATE with synthetic ground truth,
- move from segment targeting toward individualized targeting,
- connect treatment response with business policy metrics.

---

# 36. WIP Completion Statement

Có thể mô tả trạng thái sau 4 tuần như sau:

> **After four weeks, the project has a working causal experimentation pipeline from data preparation and synthetic ground-truth generation to segmentation, experiment design, A/A validation and A/B effect estimation. The current WIP is sufficient for an end-to-end technical demo in a controlled sandbox. Uplift-based individualized targeting is being developed as the Week 5 extension.**

---

# 37. Notes on Source Artifacts

Tài liệu này được tổng hợp từ trạng thái repo hiện tại nhưng **đóng băng scope ở cuối Week 4**.

Một số báo cáo cũ trong repo đã được cập nhật thêm kết quả ở các tuần sau hoặc dùng wording quá mạnh như “tương đối chính xác”, “đáng tin cậy”, “xem xét thử nghiệm thực tế”.

Tech doc này sử dụng wording thận trọng hơn:

```text
validated in simulation
no material issue detected
under current assumptions
requires real-world validation
```

để phản ánh đúng evidence boundary của project.

---

# 38. Source Files in Repository

```text
README.md

docs/Week1_Data_Quality_Report.md
docs/Week1_Data_Preprocessing_Report.md
docs/Week2_Synthetic_Data_Comprehensive_Report.md
docs/Week3_Comprehensive_Report.md
docs/Week4_AA_AB_Testing_Report.md

src/pipeline/main_pipeline.py
src/dashboard/app.py

requirements.txt
```

---

# 39. Recommended Submission Artifact

File này nên được lưu trong repo tại:

```text
docs/TECHNICAL_DOCUMENTATION_W4.md
```

Cùng với:

```text
README.md
Streamlit Demo
GitHub Repository
```

Đây là bộ WIP package phù hợp để PM review tiến độ sau 4 tuần.
