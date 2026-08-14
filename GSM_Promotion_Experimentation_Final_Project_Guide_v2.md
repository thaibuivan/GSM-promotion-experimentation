# GSM Promotion Experimentation — Final Project Guide v2

> **Mục tiêu:** Định vị lại toàn bộ project thực tập theo hướng gần bài toán doanh nghiệp GSM hơn nhưng không overclaim rằng project đang trực tiếp chạy trên production.
>
> **Framing đề xuất:** **Simulation-Based Promotion Experimentation & Uplift Modeling Sandbox for Ride-Hailing**
>
> Project sử dụng public mobility data + synthetic causal user-level data để kiểm chứng end-to-end pipeline từ **Experiment Design → A/A → A/B → HTE/Uplift → GMV/Burn Economics → Policy Evaluation → Stress Test → Decision Support**.

---

# 1. Bối cảnh và ranh giới

Theo bối cảnh được tìm hiểu trong kỳ thực tập:

- Business/Marketing đang vận hành promotion theo dạng rule-based/matrix và cập nhật định kỳ.
- Data/AI đang nghiên cứu hoặc bắt đầu ứng dụng Uplift Modeling để cá nhân hóa treatment tốt hơn.
- Historical treatment assignment chưa hoàn toàn randomized, nên treated/control trong dữ liệu lịch sử có thể chịu selection bias/confounding.
- Doanh nghiệp có pilot thật, nhưng project thực tập **không trực tiếp tham gia production, không dùng production data và không đưa recommendation triển khai thật**.

Do đó không nên nói:

> “Đây là hệ thống tối ưu voucher của GSM.”

Nên nói:

> **“Project lấy cảm hứng từ bài toán promotion thực tế và xây một controlled causal sandbox để kiểm chứng methodology có thể chuyển giao khi có randomized business data phù hợp.”**

---

# 2. Câu hỏi trung tâm

Thay vì chỉ hỏi:

> Voucher có tăng số chuyến không?

Nên nâng thành:

> **Làm thế nào để thiết kế một promotion experimentation sandbox có thể đo incremental rides/GMV, phát hiện heterogeneous treatment response, và so sánh các targeting policy dưới ràng buộc promotion burn và ngân sách?**

Ba lớp quyết định:

1. **Causal effectiveness:** promotion có thực sự tạo incremental behavior không?
2. **Heterogeneous response:** ai phản ứng nhiều hơn với promotion?
3. **Business efficiency:** policy nào tạo incremental GMV/profit tốt hơn với cùng mức burn?

---

# 3. Scope chính thức

## Core

- EDA & feature engineering
- Synthetic causal data generation
- Experiment design
- Randomization
- A/A testing
- SRM & covariate balance
- A/B effect estimation
- K-Means segmentation
- HTE analysis
- Uplift Modeling
- Economics layer
- Policy comparison
- Stress testing
- Decision-support dashboard

## Optional

- X-Learner benchmark
- Uplift calibration
- Randomized holdout
- Champion–Challenger simulation
- Policy frontier
- Analytics copilot

## Out of scope

- Driver Agent
- Multi-Agent Marketplace
- Matching
- Driver repositioning
- MARL
- Surge pricing
- Production-grade real-time serving
- Production MLOps
- Actual GSM campaign deployment

---

# 4. Current pipeline

```text
Public mobility data
        ↓
EDA + feature engineering
        ↓
Synthetic user-level data
        ↓
Y0 / Y1 / true ITE
        ↓
K-Means segmentation
        ↓
Experiment Design
        ↓
A/A + SRM + SMD
        ↓
A/B Test
        ↓
ATE + CI
        ↓
Uplift Model
        ↓
CATE / Qini / AUUC
        ↓
GMV / Burn Economics
        ↓
Policy Comparison
        ↓
Stress Test
        ↓
Decision Support
```

---

# 5. Vì sao synthetic sandbox có giá trị?

Một cách trình bày yếu:

> “Không có dữ liệu thật nên phải mô phỏng.”

Một cách trình bày mạnh hơn:

> **“Synthetic sandbox cung cấp known counterfactual để kiểm chứng correctness của toàn pipeline causal trước khi có randomized business data.”**

Trong synthetic:

```text
Y0 = outcome nếu không treatment
Y1 = outcome nếu có treatment
ITE = Y1 - Y0
```

Ta biết ground truth nên có thể đo:

- ATE recovery
- CI coverage
- CATE RMSE / MAE
- correlation với true ITE
- Qini / AUUC
- Oracle Policy
- Policy Regret

---

# 6. Hạn chế hiện tại của synthetic DGP

Nếu true ITE được sinh trực tiếp từ các feature mà model nhìn thấy, thì model đang giải một bài toán tương đối thuận lợi.

Ví dụ:

```text
Urban leisure    → uplift cao
Suburban leisure → uplift cao
Rush hour        → uplift thấp
Airport          → uplift thấp
Cash             → uplift thấp
Recency          → uplift cao
```

Điều này tốt để test **correctness**, nhưng chưa đủ để test **robustness**.

## Cải thiện thành hai tầng

### Tier A — Known-DGP

Giữ generator hiện tại để kiểm tra:

- estimator có recover effect không,
- uplift ranking có đúng không,
- CI có cover truth không.

### Tier B — Adversarial / Misspecified-DGP

Thêm:

- nonlinear HTE
- threshold effect
- negative uplift
- rare persuadables
- hidden effect modifier
- train-test DGP shift
- cluster không trùng treatment response
- segment proportion shift
- feature distribution shift

---

# 7. Vai trò đúng của K-Means

K-Means trả lời:

> User nào giống nhau về behavior?

Uplift trả lời:

> User nào thay đổi behavior do voucher?

Vì vậy:

```text
User Features
   ├──→ K-Means → Persona / Reporting / Explainability
   │
   └──→ Uplift Model → Predicted CATE → Economics → Target Policy
```

Segment Targeting vẫn nên giữ nhưng chỉ là **baseline** để so với:

- Mass Voucher
- Segment Targeting
- Uplift Targeting
- Profit/Burn-aware Targeting

---

# 8. Business metric architecture mới

> **Quan trọng:** Chưa có tài liệu nội bộ xác nhận chính xác công thức GMV/Burn của GSM. Vì vậy các metric dưới đây nên được gọi là **business-aligned proposed metrics**, chưa phải định nghĩa chính thức của GSM nếu mentor/business chưa xác nhận.

Ba lớp metric:

```text
Causal Effectiveness
→ Incremental Rides
→ Incremental GMV

Promotion Efficiency
→ Burn
→ Burn / GMV
→ Burn / Incremental GMV
→ Cost per Incremental Ride

Economic Decision
→ Incremental Contribution Margin − Burn
→ ROI / Policy Value
```

---

# 9. GMV

Trong sandbox nên hiểu GMV ở mức:

> Gross transaction value của các chuyến trong campaign population.

Phải tách:

```text
GMV ≠ Revenue ≠ Profit
```

Causal business effect:

```text
Incremental GMV
=
GMV(Treatment)
− Counterfactual GMV(Control)
```

Trong randomized A/B test, Control là proxy counterfactual.

---

# 10. Burn

Trong project có thể định nghĩa tổng quát:

> **Burn = promotion subsidy / incentive cost mà platform chịu.**

Nhưng không nên coi:

```text
Burn = Voucher Face Value
```

một cách mặc định.

Nên parameterize:

```text
voucher_face_value
redemption_rate
expected_burn
```

và ghi rõ công thức production cần được xác nhận với Business/Marketing.

---

# 11. Burn/GMV và Incremental GMV/Burn

## Burn / GMV

```text
Burn / GMV
```

trả lời:

> Promotion spend chiếm bao nhiêu phần gross transaction value?

Hữu ích như cost-intensity/guardrail.

Nhưng:

> Burn/GMV thấp chưa chứng minh causal incrementality.

## Incremental GMV / Burn

```text
Incremental GMV / Burn
```

trả lời:

> Mỗi 1 đồng burn tạo bao nhiêu đồng GMV tăng thêm?

Ngược lại:

```text
Burn / Incremental GMV
```

trả lời:

> Cần bao nhiêu đồng burn để tạo 1 đồng incremental GMV?

Đây là metric gần causal efficiency hơn GMV/Burn.

---

# 12. Cost per Incremental Ride

```text
CPIR
=
Burn / Incremental Rides
```

Ví dụ:

```text
Burn = 100m
Incremental Rides = 5,000

CPIR = 20,000 / incremental ride
```

Đây là metric business dễ hiểu và nên có trong dashboard.

---

# 13. Từ Uplift sang Economics

Không nên target user chỉ vì:

```text
Predicted CATE > 0
```

Nên tính:

```text
Expected Incremental Profit_i
=
Predicted Incremental Rides_i
× Contribution Margin_i
− Expected Burn_i
```

Target nếu:

```text
Expected Incremental Profit_i > 0
```

Nếu có budget:

```text
Maximize:
Σ target_i × Expected Incremental Profit_i

Subject to:
Σ target_i × Expected Burn_i ≤ Budget
```

Nếu chỉ một voucher type, baseline rất đơn giản:

1. tính expected value từng user,
2. loại EV <= 0,
3. rank giảm dần,
4. chọn đến khi hết budget.

Không cần solver phức tạp.

---

# 14. Không dùng Fare thay Profit

Fare không phải Contribution Margin.

Nếu không có economics thật:

```text
contribution_margin_per_ride
```

nên là parameter scenario, ví dụ:

```text
10k / 20k / 30k
```

Sau đó sensitivity analysis.

---

# 15. Policy comparison phải là output chính

Final report/dashboard nên so:

| Policy | Logic |
|---|---|
| No Voucher | Không treatment |
| Mass Voucher | Tất cả eligible |
| Segment Targeting | Target theo persona |
| Uplift Targeting | Top predicted CATE |
| Burn-Constrained Uplift | Top CATE dưới burn cap |
| Profit Targeting | Top expected incremental profit |
| Budget-Constrained Policy | Max policy value dưới budget |

KPI:

- Targeted Users
- Target Rate
- Total Rides
- Incremental Rides
- GMV
- Incremental GMV
- Burn
- Burn / GMV
- Burn / Incremental GMV
- Cost per Incremental Ride
- Incremental Contribution Margin
- Incremental Profit
- ROI
- Policy Value

---

# 16. Oracle Policy — lợi thế của synthetic

Vì biết true ITE:

```text
Oracle EV_i
=
True ITE_i × Margin_i
− Burn_i
```

Từ đó:

```text
Policy Regret
=
Oracle Profit
− Learned Policy Profit
```

Đây là metric rất mạnh để chứng minh learned policy còn cách optimal-under-DGP bao xa.

---

# 17. Uplift evaluation

## Ranking metrics

- Qini
- AUUC
- Uplift Curve

## Accuracy metrics trong synthetic

- CATE RMSE
- CATE MAE
- Correlation với true ITE

## Policy metrics

- Profit@Top10%
- Profit@Top20%
- Incremental GMV@Budget
- Burn@Budget
- Policy Value
- Policy Regret

---

# 18. Uplift calibration

Ranking tốt chưa chắc CATE scale đúng.

Nếu:

```text
Predicted CATE = +1.0
Observed/True Uplift = +0.2
```

thì economics sẽ bị thổi phồng.

Nên:

1. chia predicted CATE thành decile,
2. tính predicted uplift mean,
3. tính observed treatment-control uplift,
4. tính true ITE mean trong synthetic,
5. so sánh ba giá trị.

---

# 19. A/A trở thành Experiment Trust Gate

```text
Experiment
    ↓
SRM?
Fail → STOP
    ↓
Covariate Balance?
Major Fail → REVIEW
    ↓
Exposure Integrity?
Fail → STOP
    ↓
A/A Calibration?
Fail → REVIEW
    ↓
Primary Metric
    ↓
Business Decision
```

Output:

```text
EXPERIMENT HEALTH:
PASS / REVIEW / FAIL
```

A/A không chứng minh hệ thống hoàn hảo. Nó chỉ cho thấy trong các simulated settings đã thử, không phát hiện bất thường đáng kể về randomization/statistical calibration.

---

# 20. Power, MDE và uncertainty

Experiment design nên có:

```text
baseline metric
variance
MDE
alpha
power
treatment ratio
```

Output:

```text
required sample size
estimated duration
```

Không nên dừng ở:

```text
ATE ± CI
```

Mà nên propagate:

```text
ATE CI
  ↓
Incremental Rides CI
  ↓
Incremental GMV CI
  ↓
Incremental Profit CI
```

Decision rule minh họa:

```text
ROLL OUT
if Lower CI of Incremental Profit > 0

CONTINUE TEST
if Point Estimate > 0 nhưng CI cắt 0

STOP
if Upper CI <= 0
```

---

# 21. Experiment lifecycle thực chiến hơn

Không nên:

```text
A/B → Uplift → Recommendation → END
```

Nên:

```text
1. Define eligible population
2. Randomize
3. Validate experiment health
4. Estimate ATE / HTE
5. Train uplift
6. Build targeting policy
7. Keep randomized holdout
8. Champion–Challenger
9. Re-estimate
10. Update
```

Randomized holdout giúp duy trì counterfactual data, monitor model decay và recalibrate uplift.

---

# 22. Stress test cần mở rộng

## Statistical

- sample size
- treatment ratio
- true effect = 0
- noisy outcome

## DGP

- nonlinear HTE
- sign flip
- rare responders
- hidden modifier

## Economics

- burn tăng
- margin giảm
- redemption thay đổi
- budget thay đổi

## Data

- missingness
- covariate shift
- segment drift

## Experiment Integrity

- SRM
- exposure mismatch
- logging loss
- contamination

Quan trọng nhất:

> Không chỉ hỏi model score có ổn không; phải hỏi **policy recommendation có đổi không khi assumptions thay đổi**.

---

# 23. Product cuối — Promotion Experimentation & Policy Simulator

## Tab 1 — Experiment Setup

```text
Population
Treatment Ratio
Primary Metric
MDE
Power
Duration
```

## Tab 2 — Experiment Health

```text
SRM
Balance
Exposure
A/A Calibration
```

## Tab 3 — A/B Results

```text
ATE Rides
ATE GMV
95% CI
p-value
```

## Tab 4 — Heterogeneity

```text
Persona
Segment ATE
Predicted CATE
Observed Uplift
```

## Tab 5 — Business Metrics

```text
GMV
Incremental GMV
Burn
Burn / GMV
Burn / Incremental GMV
Cost / Incremental Ride
```

## Tab 6 — Policy Simulator

Input:

```text
Budget
Voucher Value
Expected Burn
Contribution Margin
Max Burn / GMV
Target Rate
```

Output:

```text
Recommended Policy
Target Users
Incremental Rides
Incremental GMV
Burn
Burn Efficiency
Incremental Profit
ROI
```

Định vị dashboard là:

> **Interactive Simulation & Decision-Support Prototype**

không phải production engine.

---

# 24. Reusable engineering structure

```text
src/
├── synthetic_generator.py
├── experiment_design.py
├── experiment_health.py
├── ab_analysis.py
├── segmentation.py
├── uplift_model.py
├── uplift_evaluation.py
├── economics.py
├── policy_evaluation.py
├── stress_test.py
└── dashboard/
```

Config:

```text
config/
├── experiment.yaml
├── economics.yaml
└── synthetic_dgp.yaml
```

Ví dụ:

```yaml
experiment:
  treatment_ratio: 0.5
  alpha: 0.05
  power: 0.8

economics:
  voucher_value: 20000
  redemption_rate: 0.7
  expected_burn: 14000
  margin_per_ride: 25000
  budget: 500000000
```

Data contract tối thiểu:

```text
user_id
experiment_id
assignment_time
pre_treatment_features
treatment
exposure
outcome_rides
outcome_gmv
segment
voucher_value
burn
```

Feature cutoff:

```text
Historical Window [-90d, 0)
        ↓
Assignment t=0
        ↓
Outcome Window [0, +14d]
```

Không dùng post-treatment leakage.

---

# 25. Hai lớp bằng chứng

Final report nên luôn tách:

| Validated in Simulation | Requires Real Business Data |
|---|---|
| A/A calibration | Real randomization integrity |
| Recover true ATE | Actual GSM ATE |
| CATE vs true ITE | Real CATE |
| Burn sensitivity | Actual promotion burn |
| Policy value under assumptions | Actual policy value |
| Robustness under simulated shift | Production drift |

---

# 26. Cách nói về metric GSM

Nếu chưa có định nghĩa chính thức:

Không nói:

> “Burn của GSM được tính như này.”

Nên nói:

> “Project sử dụng business-aligned definitions của GMV/Burn để mô phỏng promotion economics; production definitions cần được xác nhận với Business/Marketing.”

Nên hỏi mentor/business 5 câu:

1. GMV nội bộ được định nghĩa chính xác thế nào?
2. Burn gồm những khoản nào?
3. Burn/GMV là optimization metric hay guardrail?
4. Team tối ưu Rides, GMV, Net Revenue hay Contribution Margin?
5. Có metric nội bộ tương tự Incremental GMV/Burn hoặc Cost per Incremental Ride không?

---

# 27. Storyline thuyết trình cuối

1. **Business Context** — promotion có thể tăng usage nhưng cũng có cannibalization/subsidy waste.
2. **Why Causal?** — high GMV user chưa chắc cần voucher.
3. **Internship Scope** — simulation sandbox, không phải production GSM project.
4. **Synthetic Ground Truth** — Y0/Y1/ITE.
5. **Experiment Design** — Randomization, A/A, SRM, Balance.
6. **A/B Effect** — Incremental Rides + Incremental GMV.
7. **Heterogeneity** — K-Means + Uplift.
8. **Business Metrics** — GMV / Incremental GMV / Burn.
9. **Policy Comparison** — Mass vs Segment vs Uplift vs Profit.
10. **Stress Test** — Statistical + DGP + Economics.
11. **Decision Support** — Policy Simulator.
12. **Transferability** — Synthetic → randomized real-world data.

Câu mở đầu:

> “Project này không nhằm thay thế policy promotion hiện tại của GSM hay khẳng định một production policy cụ thể là tối ưu. Em xây một simulation-based experimentation sandbox lấy cảm hứng từ bài toán thực tế, với mục tiêu kiểm chứng toàn bộ chuỗi randomization → A/B Testing → Uplift Modeling → Burn-aware Policy Evaluation trong môi trường có known causal ground truth.”

---

# 28. Những gì nên sửa ngay trong repo

- [ ] README: giảm overclaim, nêu rõ simulation-based prototype
- [ ] Decision Memo: tách simulation recommendation và real-world implication
- [ ] Economics: thêm GMV/Burn layer
- [ ] Policy Evaluation: thêm Incremental GMV/Burn và CPIR
- [ ] Dashboard: thêm Business Metrics + Policy Simulator
- [ ] Uplift: train toàn eligible population
- [ ] K-Means: chuyển thành explainability layer
- [ ] Stress Test: thêm DGP/economics shift
- [ ] Oracle Policy + Regret
- [ ] Uplift Calibration
- [ ] Config-driven economics
- [ ] Data Contract
- [ ] Feature cutoff
- [ ] Experiment Health Gate
- [ ] Power/MDE module

---

# 29. Ưu tiên nếu còn 1 tuần

1. Sửa framing README/Decision Memo.
2. Thêm GMV/Burn metric architecture.
3. Train uplift toàn eligible population.
4. So sánh No/Mass/Segment/Uplift/Profit policies.
5. Thêm Oracle Regret.
6. Thêm Burn sensitivity.
7. Hoàn thiện Policy Simulator.

Nếu còn thêm thời gian:

- uplift calibration,
- adversarial DGP,
- champion–challenger,
- randomized holdout,
- CI cho incremental economics.

Không ưu tiên:

- Driver Agent
- Taxi GPS data
- MARL
- Marketplace simulation
- model zoo
- production deployment

---

# 30. Final Project Positioning

**English**

> **Simulation-Based Promotion Experimentation & Uplift Modeling for Burn-Efficient Ride-Hailing Targeting**

**Vietnamese**

> **Xây dựng hệ thống mô phỏng A/B Testing và Uplift Modeling cho bài toán phân bổ khuyến mãi hiệu quả theo Incremental Rides, Incremental GMV và Promotion Burn**

**Final Objective**

> **Xây dựng một experimentation-driven promotion decision sandbox có thể kiểm chứng treatment effect trong môi trường known ground truth, phát hiện heterogeneous treatment response bằng uplift modeling, và so sánh các promotion policy dựa trên incremental rides, incremental GMV, burn efficiency và expected incremental profit.**

---

# 31. Thông điệp cuối dành cho doanh nghiệp

> **Project thực tập không chứng minh policy thật của GSM nên thay đổi như thế nào. Project chứng minh người thực tập hiểu đúng bài toán promotion theo causal lens, biết cách thiết kế và kiểm tra experiment, hiểu vì sao uplift cần treatment data tốt, biết chuyển treatment response sang các metric business như Incremental GMV và Burn Efficiency, và biết đóng gói thành một reusable decision-support framework.**
>
> Khi có randomized production data phù hợp, phần synthetic generator có thể được thay bằng dữ liệu thật trong khi các layer experiment health, A/B estimation, uplift evaluation và policy comparison vẫn giữ nguyên logic cốt lõi.

---

# 32. Một câu chốt toàn bộ dự án

> **Từ “A/B Test + Uplift Model” chuyển thành “Experimentation-Driven Promotion Decision Sandbox”: đo causal incrementality, học heterogeneous response, quy đổi sang Incremental GMV/Burn, rồi lựa chọn targeting policy dưới ràng buộc ngân sách và uncertainty.**
