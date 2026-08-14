# GSM Promotion Experimentation — Review tổng thể và hướng tối ưu hóa dự án

> **Mục tiêu tài liệu:** Đóng gói toàn bộ các góp ý về repo `GSM-promotion-experimentation` theo hướng biến dự án từ một chuỗi notebook A/B Testing + Uplift Modeling thành một **Promotion Experimentation & Incremental Profit Optimization System** có logic gần với bài toán doanh nghiệp hơn.
>
> **Nguồn review chính trong repo:** `README.md`, `docs/Week2_Synthetic_Data_Comprehensive_Report.md`, `docs/Week3_Comprehensive_Report.md`, `docs/Week4_AA_AB_Testing_Report.md`, `docs/Week5_Uplift_Modeling_Report.md`, `docs/Week6_Stress_Test_Report.md`, `docs/Decision_Memo.md`, cùng cấu trúc `notebooks/` và `src/`.
>
> **Nguyên tắc xuyên suốt:** Phải phân biệt rõ giữa **kết quả đã được kiểm chứng trong mô phỏng** và **kết quả có thể khẳng định về GSM/Xanh SM ngoài thực tế**.

---

# 1. Kết luận tổng quát

Repo hiện tại đã vượt xa một project A/B Testing cơ bản. Pipeline hiện có đủ các mảnh ghép chính:

```text
NYC TLC EDA
    ↓
Synthetic user-level data
    ↓
Structural Causal Model
    ↓
Y0 / Y1 / true ITE
    ↓
K-Means segmentation
    ↓
Experiment design
    ↓
A/A Test + SRM + SMD + FPR
    ↓
A/B Test + ATE + Confidence Interval + Economics
    ↓
T-Learner XGBoost
    ↓
CATE / Qini / AUUC
    ↓
Break-even CATE
    ↓
Stress Test
    ↓
Decision Memo
```

Điểm cần nâng cấp không còn là “thêm thuật toán”. Project đã có đủ technical breadth. Phần cần làm sâu hơn là:

1. **Decision Science:** biến uplift score thành quyết định phát voucher dưới ràng buộc chi phí/ngân sách.
2. **Evidence Discipline:** không diễn giải kết quả synthetic như bằng chứng thật của GSM.
3. **Productization:** đóng gói thành một hệ thống hỗ trợ quyết định thay vì tập notebook rời rạc.

### Hướng chốt nên theo

> **Promotion Experimentation & Incremental Profit Optimization System**

Ba module chính:

```text
Module 1 — Experimentation
A/A → SRM → Balance → Power/MDE → A/B → ATE/CI

Module 2 — Heterogeneous Response
K-Means để giải thích persona
+
Uplift Model để ước lượng response khác biệt

Module 3 — Decision Policy
Predicted CATE
× contribution margin
− expected voucher cost
→ expected incremental profit
→ target policy dưới budget
```

---

# 2. Những gì project hiện đã làm tốt

## 2.1. Synthetic Data không phải random data đơn giản

Repo đã xây một SCM với:

- `Y0`: outcome khi không treatment
- `Y1`: outcome khi treatment
- `true_ite`: treatment effect thực được biết trong simulation
- `treatment_obs`: assignment có confounding
- `treatment_rand`: randomized assignment

Điểm này rất mạnh vì cho phép:

- unit-test A/B pipeline
- kiểm tra estimator có phục hồi đúng effect không
- so observational với randomized estimate
- kiểm tra uplift model có học được HTE hay không

Repo còn dùng Zero-Inflated Negative Binomial để tạo count outcome, hợp lý hơn Poisson thông thường khi có nhiều zero và overdispersion.

## 2.2. Có heterogeneous treatment effect rõ ràng

`true_ite` được tạo dựa trên các yếu tố như:

- urban/suburban leisure
- rain-age interaction
- airport
- rush hour
- cash
- recency
- diminishing returns

Điều này giúp project không chỉ có ATE chung mà còn có HTE/CATE.

## 2.3. Segmentation đã vượt mức “cluster cho có”

Repo có:

- K-Means
- PCA
- validation
- persona
- business labeling

Nó hữu ích cho phần giải thích nghiệp vụ.

## 2.4. A/A Testing khá đầy đủ

Repo hiện có:

- Monte Carlo repeated randomization
- Sample Ratio Mismatch
- Standardized Mean Difference
- false positive rate
- p-value distribution

Đây là điểm mạnh thực tế vì một experimentation pipeline phải được kiểm tra trước khi tin kết quả A/B.

## 2.5. A/B Testing đã có economics

Không chỉ dừng ở p-value. Repo có:

- ATE
- CI
- robust inference
- segment effect
- voucher economics
- ROI

Đây là hướng phù hợp bài toán promotion.

## 2.6. Uplift Modeling đã đi tới business threshold

Repo có:

- T-Learner + XGBoost
- train/validation/test
- early stopping
- Qini
- AUUC
- CATE
- break-even threshold

Công thức hiện tại:

```text
Break-even CATE
=
Voucher Cost / Margin per Incremental Ride
```

Đây là bước đúng vì business không ra quyết định chỉ dựa trên uplift score.

## 2.7. Có stress test

Repo đã thử:

- sample size
- true effect = 0
- treatment ratio 90/10
- Gaussian noise

Đây là baseline robustness tốt.

## 2.8. Đã bắt đầu productization

Repo có:

```text
src/
├── dashboard/
└── pipeline/
```

Nên tận dụng để xây **Policy Simulator** thay vì thêm thuật toán mới.

---

# 3. Vấn đề lớn nhất: business conclusion đang mạnh hơn bằng chứng

## 3.1. Vì sao?

Treatment effect hiện tại do chính project thiết kế.

Nếu synthetic generator quy định:

- nhóm A nhạy voucher
- nhóm B ít nhạy
- airport penalty
- cash penalty
- recency boost

thì các kết luận sau A/B/Uplift đang chứng minh:

> Pipeline hoạt động đúng dưới assumptions đã cài.

Nó chưa chứng minh:

> Khách hàng thật của GSM có treatment response như vậy.

## 3.2. Cần sửa wording

Nên tránh:

- “chính xác tuyệt đối”
- “hoàn hảo”
- “công bằng tuyệt đối”
- “sẵn sàng deploy diện rộng”
- “triển khai ngay”
- “lợi thế cạnh tranh tuyệt đối”

Nên dùng:

- “phù hợp với kỳ vọng dưới simulation”
- “không phát hiện vi phạm trong các checks đã thực hiện”
- “ổn định trong các scenario được stress-test”
- “recommendation trong synthetic sandbox”
- “cần validation trên randomized GSM data trước production use”

## 3.3. Cách kết luận đúng hơn

Không nên:

> Segment Targeting tạo lợi nhuận dương nên GSM nên triển khai.

Nên:

> Trong synthetic sandbox với assumptions hiện tại về treatment effect, voucher cost và contribution margin, segment-targeting cho policy value tốt hơn mass-targeting. Kết quả chứng minh pipeline ra quyết định hoạt động đúng trong môi trường kiểm soát; policy thực tế cần được kiểm chứng bằng randomized experiment trên dữ liệu GSM.

---

# 4. Vấn đề thứ hai: Synthetic DGP đang hơi “biết trước đáp án”

## 4.1. Cơ chế hiện tại

`true_ite` được tạo trực tiếp từ các feature mà model sau đó có thể nhìn thấy hoặc nhìn thấy proxy rất gần.

Do đó uplift model đang giải bài toán:

> Recover một ground truth được tạo từ đúng feature space mà model học.

Đây là **known-DGP validation**.

Nó rất tốt cho correctness, nhưng chưa đủ cho robustness.

## 4.2. Nên chia synthetic evaluation thành hai tầng

### Tier A — Known-DGP Validation

Giữ dataset hiện tại.

Mục tiêu:

> Kiểm tra method correctness.

Nên đo:

- ATE error
- CATE RMSE vs true ITE
- MAE
- correlation
- Qini/AUUC
- policy value
- CI coverage

### Tier B — Misspecified / Adversarial DGP

Tạo một generator thứ hai khó hơn.

Các scenario nên thêm:

1. **Nonlinear HTE**  
   Uplift chỉ tăng khi nhiều điều kiện cùng xảy ra.

2. **Threshold Effect**  
   Voucher chỉ có tác dụng khi recency/fare vượt một threshold.

3. **Negative Uplift**  
   Một số nhóm có effect âm.

4. **Rare Persuadables**  
   Chỉ 5–10% population có uplift cao.

5. **Hidden Modifier**  
   Một latent variable tác động treatment effect nhưng model không quan sát được.

6. **Train/Test DGP Shift**  
   Quy luật effect khác giữa train và test.

7. **Persona không trùng HTE**  
   Cluster vẫn rõ về hành vi nhưng treatment response khác nhau bên trong cùng cluster.

Scenario 7 đặc biệt quan trọng để chứng minh:

> **Segmentation ≠ Uplift Targeting**

---

# 5. Đổi vai trò K-Means

## 5.1. Không nên để K-Means là targeting engine cuối cùng

Logic:

```text
K-Means
→ chọn cluster tốt
→ phát voucher
```

chỉ nên là baseline.

Segmentation trả lời:

> Ai giống ai về hành vi?

Uplift trả lời:

> Ai thay đổi hành vi do voucher?

Hai câu hỏi khác nhau.

## 5.2. Vai trò đúng của K-Means

Nên dùng cho:

- business understanding
- persona
- reporting
- campaign communication
- explainability
- monitoring
- HTE exploration

Ví dụ:

> Top 20% uplift target gồm 48% Suburban Card, 25% Urban Leisure...

## 5.3. Architecture mới

```text
User features
      ↓
Uplift Model
      ↓
Predicted CATE
      ↓
Economics Policy
      ↓
Target / Holdout

User features
      ↓
K-Means
      ↓
Persona / Explain / Monitor
```

K-Means giải thích.

Uplift + economics quyết định.

---

# 6. Chuyển từ uplift sang expected incremental profit

Đây nên là core business layer.

Với user i:

```text
Expected Value_i
=
Predicted CATE_i × Expected Margin_i
− Expected Voucher Cost_i
```

Target nếu:

```text
Expected Value_i > 0
```

Nếu có ngân sách B:

```text
Maximize:
Σ target_i × Expected Value_i

Subject to:
Σ target_i × Expected Voucher Cost_i ≤ B
```

Nếu chỉ có một voucher type tương đối đồng nhất, baseline có thể là:

```text
1. Tính EV
2. Loại EV <= 0
3. Rank EV giảm dần
4. Chọn đến khi hết budget
```

Không cần metaheuristic hay solver phức tạp.

---

# 7. So sánh Policy chứ không chỉ Model

Final evaluation nên có ít nhất:

| Policy | Logic |
|---|---|
| No Voucher | Không phát |
| Mass Voucher | Phát tất cả eligible |
| Segment Targeting | Phát theo cluster |
| Uplift Targeting | Top-k predicted CATE |
| Profit Targeting | Rank theo expected incremental profit |
| Budget-Constrained Profit | Tối đa profit dưới budget |

Điểm quan trọng:

> Business không mua một Qini curve. Business cần một policy.

---

# 8. Uplift Model nên train trên toàn eligible population

Repo hiện tập trung nhiều vào `Urban Cash`.

Đó là bài test hay:

> Có cứu được một segment đang lỗ không?

Nhưng final business question nên là:

> Trong toàn bộ eligible population, nên phát cho ai?

Pipeline nên là:

```text
All eligible users
        ↓
CATE prediction
        ↓
Expected incremental profit
        ↓
Rank
        ↓
Budget allocation
        ↓
Target list
```

Sau đó mới phân tích target list theo persona.

---

# 9. Không cần model zoo

T-Learner hiện đã hợp lý.

Nếu còn thời gian, benchmark tối đa:

1. S-Learner
2. T-Learner
3. X-Learner

Không nên mở rộng sang quá nhiều model chỉ để tăng breadth.

Quan trọng hơn là:

- out-of-sample Qini
- AUUC
- calibration
- true-ITE error trong synthetic
- profit@k
- policy value
- robustness under shift

---

# 10. Evaluation nên nâng cấp từ model metric sang policy metric

## Model metrics

- CATE RMSE
- CATE MAE
- correlation with true ITE
- Qini
- AUUC
- uplift by decile

## Policy metrics

- Incremental Rides
- Incremental Revenue
- Incremental Profit
- ROI
- Cost per Incremental Ride
- Profit @ Top-k
- Profit @ Budget
- Policy Value

## Oracle Policy

Vì synthetic data có true ITE, có thể tính:

```text
Oracle EV_i
=
true_ite_i × margin_i
− voucher_cost_i
```

Từ đó:

```text
Regret
=
Profit_oracle − Profit_learned_policy
```

Đây là một metric rất mạnh cho sandbox.

---

# 11. Thêm uplift calibration

Ranking tốt chưa chắc predicted CATE đúng scale.

Nên chia user thành decile:

```text
D1 ... D10
```

Với mỗi decile tính:

- predicted uplift mean
- observed treatment-control uplift
- true ITE mean (chỉ synthetic)

Nếu predicted CATE = +1.2 rides nhưng observed chỉ +0.3 thì profit policy có thể sai.

---

# 12. Economics cần trở thành tham số

Không nên coi một bộ economics cố định là business truth.

Nên parameterize:

```text
voucher_face_value
expected_redemption_rate
expected_voucher_cost
contribution_margin_per_ride
campaign_budget
eligible_population
max_target_rate
```

Ví dụ sensitivity:

```text
Voucher:
10k / 15k / 20k / 30k

Margin:
10k / 20k / 30k

Budget:
100m / 500m / 1b
```

Mục tiêu:

> Recommendation có đổi khi economics assumptions đổi không?

---

# 13. Policy Frontier

Có thể tạo bảng:

| Voucher Cost | Margin | Best Policy |
|---:|---:|---|
| 10k | 30k | Uplift targeting |
| 20k | 30k | Profit targeting |
| 30k | 20k | Very selective / no promotion |

Hoặc curve:

```text
Campaign Spend
        ↓
Expected Incremental Profit
```

Từ đó tìm:

- budget tối ưu
- diminishing returns
- break-even frontier

---

# 14. A/B pipeline nên trở thành Experiment Trust Gate

Không nên coi A/A là notebook riêng rồi kết thúc.

Nên thiết kế:

```text
Experiment arrives
        ↓
SRM?
   Fail → STOP
        ↓
Covariate balance?
   Major fail → REVIEW
        ↓
Exposure/logging valid?
   Fail → STOP
        ↓
Invariant metrics?
   Fail → REVIEW
        ↓
Primary metric
        ↓
Guardrails
        ↓
Decision
```

Output:

```text
EXPERIMENT HEALTH:
PASS / REVIEW / FAIL
```

---

# 15. A/A Test cần diễn giải đúng

A/A không chứng minh:

> Hệ thống hoàn hảo.

Nó chỉ cho thấy dưới simulation/settings đã thử:

- Type I error gần kỳ vọng
- assignment không có mismatch đáng kể
- balance phù hợp

Nên viết:

> Không phát hiện randomization/statistical calibration issue đáng kể dưới các thiết lập mô phỏng đã kiểm tra.

---

# 16. HC1 và covariate adjustment cần diễn giải thận trọng

Robust Standard Errors giúp inference ít nhạy với heteroskedasticity.

Nó không đảm bảo:

- p-value đúng trong mọi setting
- estimator không bias
- model specification luôn đúng

Nếu thêm `monthly_rides_history` để giảm residual variance, nên gọi đúng:

> pre-treatment covariate adjustment

Không nên đồng nhất hoàn toàn với CUPED nếu chưa triển khai đúng CUPED formulation.

---

# 17. Stress Test hiện tại nên mở rộng

Hiện đã có:

- sample size
- A/A
- imbalanced treatment ratio
- Gaussian noise

Nên thêm:

## Data Shift

- feature distribution shift
- recency shift
- segment proportion shift

## Treatment Effect Shift

- uplift giảm 30%
- uplift đổi nhóm
- một nhóm đổi dấu

## Economic Shift

- voucher cost tăng
- margin giảm
- redemption thay đổi

## Missingness

- missing covariates
- missing treatment logs
- missing outcome

## Segment Drift

- centroid shift
- cluster size shift

## Null World repeated trials

Nhiều simulation để kiểm tra:

- Type I error
- CI coverage
- policy false discovery

---

# 18. Experiment → Learn → Policy → Re-test

Không nên pipeline một chiều:

```text
A/B
→ Uplift
→ Recommendation
→ END
```

Nên là:

```text
1. Define eligible population
        ↓
2. Randomized experiment
        ↓
3. Trust checks
        ↓
4. Estimate ATE / HTE
        ↓
5. Train uplift model
        ↓
6. Build targeting policy
        ↓
7. Keep randomized holdout
        ↓
8. Champion vs Challenger
        ↓
9. Update model / policy
```

Đây là logic thực chiến hơn.

---

# 19. Randomized Holdout

Nếu tất cả high-CATE user đều luôn treatment, hệ thống mất counterfactual data.

Nên duy trì một randomized holdout.

Vai trò:

- monitor causal lift
- detect model decay
- retrain
- calibration
- tránh pure exploitation

---

# 20. Champion–Challenger

Ví dụ:

```text
Champion:
Segment-based targeting

Challenger:
Profit-based uplift targeting
```

Randomize eligible users vào hai policy.

So:

- incremental rides
- incremental profit
- cost/incremental ride
- guardrails

Đây mới là bước xác minh policy.

---

# 21. Product cuối nên là Promotion Policy Simulator

Dashboard nên cho business user nhập:

```text
Campaign Budget
Voucher Cost
Margin per Incremental Ride
Eligible Population
Max Target %
CATE Threshold
Campaign Horizon
```

Tool trả:

```text
Recommended Policy
Users Targeted
Expected Spend
Expected Incremental Rides
Expected Incremental Profit
ROI
Cost per Incremental Ride
Expected Coverage
Uncertainty
```

Và so sánh:

```text
No Promotion
Mass Voucher
Segment Targeting
Uplift Targeting
Profit Targeting
Budget-Constrained Policy
```

Đây là demo có giá trị doanh nghiệp hơn việc chỉ hiển thị Qini Curve.

---

# 22. Dashboard không phải production deployment

Nên định vị là:

> Interactive simulation / decision-support prototype

Không phải:

> Production voucher allocation engine

---

# 23. Mọi report cuối nên có hai lớp bằng chứng

| Validated in Simulation | Requires GSM Real Data |
|---|---|
| Randomization calibration | Real GSM treatment response |
| Recover known ATE | Actual GSM ATE |
| Rank known synthetic ITE | Real uplift ranking |
| Profit policy under assumptions | Actual contribution margin |
| Robustness under simulated shifts | Real operational drift |

Điều này làm project chuyên nghiệp hơn.

---

# 24. Decision Memo nên viết lại

Cấu trúc khuyến nghị:

## A. Decision Question

> Với budget B và voucher economics giả định, policy nào tối đa hóa incremental profit?

## B. Evidence

- randomized simulation
- A/A checks
- uplift evaluation
- policy value

## C. Recommendation in Sandbox

Ví dụ:

> Profit-based targeting dominates mass voucher under tested assumptions.

## D. Conditions Required

- margin
- voucher cost
- calibration
- sample size

## E. What We Cannot Claim

- không phải GSM observed causal effect
- không chứng minh production profitability
- chưa có real treatment data

## F. Next Real Experiment

- eligibility
- holdout
- MDE
- duration
- primary outcome
- guardrails

---

# 25. README cần chỉnh framing

## Timeline

Nếu mentor roadmap là 6 tuần nhưng README ghi 8 tuần, cần thống nhất hoặc giải thích rõ actual project evolution.

## Data source wording

Không nên gọi một nguồn Kaggle là “thực tế” nếu provenance chưa được xác minh.

Nên chia:

```text
Official public mobility data
Community/public ride-sharing reference
Synthetic causal user-level data
```

## Business wording

Không nên:

> Hệ thống giúp công ty tránh thất thoát hàng chục phần trăm.

Nên:

> Prototype demonstrates how uplift-informed policies can be evaluated against mass promotion under controlled assumptions.

---

# 26. Thêm Experiment Configuration

Không hard-code parameters trong notebook.

Nên có:

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
  horizon_days: 14

economics:
  voucher_cost: 15000
  margin_per_incremental_ride: 20000
  campaign_budget: 500000000

synthetic:
  n_users: 20000
  urban_share: 0.7
  rain_share: 0.2
  airport_share: 0.05
```

Lợi ích:

- reproducible
- stress-test dễ
- tránh magic numbers
- dashboard chỉnh scenario dễ

---

# 27. Thêm Data Contract

Tạo:

```text
docs/data_contract.md
```

Schema tối thiểu:

```text
user_id
experiment_id
assignment_timestamp
pre-treatment features
treatment
exposure_flag
outcome
segment_id
```

Nếu có real data:

```text
voucher_cost
redemption
incremental_margin_proxy
```

Quy tắc:

> Uplift feature chỉ được lấy trước treatment.

Không dùng post-treatment behavior làm input.

---

# 28. Experiment Specification chuẩn

Mỗi experiment nên có:

```text
Experiment Name
Business Question
Hypothesis
Population
Eligibility
Randomization Unit
Treatment
Control
Treatment Ratio
Exposure Window
Outcome Window
Primary Metric
Secondary Metrics
Guardrails
MDE
Power
Decision Rule
Stop Conditions
```

Đây là artifact rất thực chiến.

---

# 29. Metric Specification

Ví dụ:

```text
Primary:
rides_per_eligible_user_14d

Guardrails:
voucher_cost_per_user
cancellation_rate
completion_rate
revenue_per_user
```

Mỗi metric cần:

- definition
- numerator
- denominator
- aggregation
- time window
- missing rule
- outlier rule

---

# 30. Uncertainty trong Economics

Không chỉ tính point estimate.

Nên propagate uncertainty:

```text
ATE CI
→ Incremental Trips CI
→ Incremental Profit CI
```

Decision rule ví dụ:

```text
Rollout:
lower bound of incremental profit > 0

Continue Test:
point estimate > 0 nhưng CI cắt 0

Stop:
upper bound <= 0
```

---

# 31. Statistical Significance ≠ Business Significance

Có thể:

```text
p < 0.05
nhưng
profit < 0
```

→ không rollout.

Hoặc:

```text
profit point estimate > 0
nhưng CI rộng
```

→ test thêm.

---

# 32. MDE / Power nên được đưa vào product

Business nhập:

```text
baseline rides
desired uplift
variance
alpha
power
treatment ratio
```

Tool trả:

```text
required sample size
estimated experiment duration
```

Điều này thực chiến hơn thêm model phức tạp.

---

# 33. Feature Store cần rõ time cutoff

Pipeline:

```text
Historical window
[-90d, 0)
       ↓
features
       ↓
randomization at t=0
       ↓
outcome window
[0, +14d]
```

Phần này nên được ghi rõ trong methodology.

---

# 34. Explainability nên giải thích treatment response

Không nên chỉ nhìn feature importance của outcome prediction.

Câu hỏi cần trả lời:

> Feature nào liên quan đến treatment effect heterogeneity?

Có thể dùng:

- CATE slice analysis
- permutation trên uplift metric
- uplift by feature bins
- calibration theo feature

---

# 35. Agent chỉ nên là optional analytics layer

Nếu muốn tận dụng teammate chuyên agent, hướng phù hợp nhất là **Analytics Copilot**, không phải Driver Agent.

Ví dụ:

```text
User:
"Why did policy profit drop?"

Agent gọi:
- get_experiment_health()
- get_segment_uplift()
- get_policy_value()
- get_drift_summary()

Agent trả:
- diagnostics
- evidence
- recommendation
```

Agent không tự:

- phát voucher
- đổi budget production
- tự randomize
- tự rollout

Nếu thời gian ngắn, có thể bỏ hoàn toàn.

---

# 36. Không nên mở rộng Driver Agent trong scope chính

Driver Agent kéo theo:

- supply data
- matching
- waiting time
- interference
- marketplace simulation
- cross-side effects

Đó gần như là một project khác.

Chỉ nên ghi limitation:

> Current prototype assumes no material marketplace interference or supply constraint. Future work may extend to marketplace-level experimentation when driver-supply data become available.

---

# 37. Scope cuối khuyến nghị

## Tên project

**GSM Promotion Experimentation & Incremental Profit Optimization**

Hoặc:

**A/B Testing and Uplift-Based Voucher Targeting for Ride-Hailing Promotions**

## Business Question

> Voucher có tạo thêm chuyến đi hay chỉ trợ giá cho những khách vốn đã sử dụng dịch vụ, và với ngân sách giới hạn nên phát voucher cho ai để tối đa hóa incremental profit?

## Core Scope

1. Experiment Design
2. A/A & Trust Checks
3. A/B Effect Estimation
4. Segmentation for Interpretation
5. Uplift Modeling
6. Profit-based Targeting
7. Stress Testing
8. Decision Support Dashboard

## Optional

- X-Learner
- Calibration
- Agentic Analytics Copilot

## Out of Scope

- Driver ABM
- Multi-agent marketplace
- real-time matching
- surge pricing
- MARL
- production deployment
- model zoo quá lớn

---

# 38. Target Architecture

```text
Historical User Features
        ↓
Eligibility Filter
        ↓
Experiment Assignment
        ↓
Outcome Collection
        ↓
Experiment Trust Gate
SRM / SMD / A/A
        ↓
ATE / HTE Estimation
        ↓
┌─────────────────────┐
│                     │
K-Means           Uplift Model
Persona           CATE
│                     │
└──────────┬──────────┘
           ↓
Economics Layer
Margin − Voucher Cost
           ↓
Policy Optimization
Budget Constraint
           ↓
Recommendation
+ Uncertainty
```

---

# 39. Deliverable cuối nên có

## Technical

- reproducible repo
- synthetic generator
- experiment design module
- A/A / trust checks
- A/B analysis
- uplift model
- policy evaluator
- stress test
- config files

## Business

- Promotion Policy Simulator
- Decision Memo
- Experiment Health Report
- Policy Comparison
- Economics Sensitivity
- Final Presentation

---

# 40. Acceptance Criteria

## Simulation

- DGP documented
- assumptions configurable
- known-DGP + adversarial-DGP

## Experiment

- SRM
- balance
- A/A Type-I behavior
- ATE + CI
- power/MDE
- decision rule

## Uplift

- out-of-sample evaluation
- Qini/AUUC
- true-ITE validation
- calibration
- policy value

## Economics

- configurable voucher cost
- configurable margin
- configurable budget
- profit targeting
- uncertainty

## Robustness

- sample size
- assignment ratio
- noise
- DGP shift
- economics shift
- segment drift

## Product

- dashboard chạy được
- compare policy được
- synthetic assumptions hiển thị rõ
- limitations hiển thị rõ

---

# 41. Ưu tiên 1–2 tuần tới

Nếu thời gian còn ngắn, thứ tự ưu tiên:

## Priority 1 — Sửa framing

Sửa:

- README
- Decision Memo
- A/A wording
- Stress Test wording

Mục tiêu: không overclaim.

## Priority 2 — Refactor economics thành config

Đưa:

```text
voucher_cost
margin
budget
```

thành parameters.

## Priority 3 — Train uplift toàn eligible population

Không chỉ Urban Cash.

## Priority 4 — Xây 5-policy comparison

```text
No Voucher
Mass Voucher
Segment
Uplift
Profit
```

## Priority 5 — Policy Value + Oracle Regret

Tận dụng `true_ite`.

## Priority 6 — Policy Simulator

Đây là phần tạo cảm giác sản phẩm doanh nghiệp mạnh nhất.

---

# 42. Nếu còn thời gian

Thêm:

- X-Learner
- uplift calibration
- adversarial DGP
- champion–challenger simulation
- randomized holdout
- experiment duration calculator

---

# 43. Không nên ưu tiên

- Driver dataset
- Agent-Based Modeling
- marketplace simulation
- MARL
- matching
- quá nhiều uplift model
- causal forest chỉ để tăng breadth
- production API phức tạp

---

# 44. Cách trình bày với PM/Mentor

Không nên nói:

> Em đã làm K-Means, PCA, OLS, A/A, XGBoost, Qini...

Nên nói:

> Nhóm em xây một pipeline trả lời ba quyết định:
>
> 1. Voucher có thực sự tạo incremental rides không?
> 2. User nào có treatment response cao hơn?
> 3. Với voucher economics và ngân sách cụ thể, policy nào tối đa hóa incremental profit?

Map kỹ thuật:

```text
A/B Testing
→ causal effect

Uplift Modeling
→ heterogeneous response

Economics Policy
→ business allocation
```

---

# 45. Storyline thuyết trình đề xuất

1. Business Problem — cannibalization và subsidy waste
2. Why Prediction Is Not Enough
3. Experimentation Foundation
4. Heterogeneous Response
5. From Uplift to Money
6. Policy Comparison
7. Stress Test
8. Validated in Simulation vs Requires GSM Data
9. Policy Simulator Demo
10. Next Real Experiment

---

# 46. Câu hỏi phản biện cần trả lời trước final review

1. Tại sao cần uplift nếu đã có segmentation?
2. Tại sao cluster tốt không đồng nghĩa target tốt?
3. High-propensity user khác Persuadable thế nào?
4. Tại sao A/A không chứng minh production correctness?
5. Tại sao true ITE chỉ tồn tại trong synthetic?
6. Nếu Qini tốt nhưng calibration tệ thì sao?
7. Voucher cost tăng 50% thì policy có đổi không?
8. Treatment effect drift thì sao?
9. Vì sao contribution margin quan trọng hơn fare?
10. Nếu CI profit cắt 0 thì decision là gì?
11. Tại sao phải giữ randomized holdout?
12. Khi nào segment targeting tốt hơn uplift?
13. Khi nào tốt nhất là không chạy campaign?
14. Nếu sample không đủ power thì sao?
15. Điểm nào được validate thật, điểm nào chỉ validate trong simulation?

---

# 47. Final Recommendation

Project hiện tại đã đủ technical breadth.

Bước tiếp theo không phải:

> “Thêm một mô hình nữa.”

Mà là:

> **Biến pipeline hiện tại thành một hệ thống ra quyết định voucher có causal ground truth từ A/B Testing, heterogeneous response từ Uplift Modeling và business allocation từ Incremental Profit Optimization.**

Architecture cuối:

```text
Experiment
→ Learn Causal Effect
→ Personalize Response
→ Optimize Policy
→ Retain Holdout
→ Re-test
```

Thông điệp cuối nên là:

> Đây không phải hệ thống chứng minh policy voucher thực tế của GSM đã tối ưu. Đây là một prototype có thể tái lập, dùng mobility data công khai và synthetic causal outcomes để minh họa cách một doanh nghiệp ride-hailing có thể chuyển từ mass promotion sang experimentation-driven, uplift-informed và profit-aware targeting. Khi có randomized GSM data thật, cùng pipeline có thể được dùng để estimate treatment response thực tế và benchmark policy mới trong champion–challenger experiments.

---

# 48. Checklist hành động

- [ ] Sửa README để giảm overclaim và thống nhất timeline
- [ ] Ghi rõ hybrid data + synthetic causal outcomes
- [ ] Refactor economics thành config
- [ ] Train uplift trên toàn eligible population
- [ ] Đưa K-Means về explainability layer
- [ ] Thêm No/Mass/Segment/Uplift/Profit policy comparison
- [ ] Thêm policy value
- [ ] Thêm oracle policy và regret
- [ ] Thêm uplift calibration
- [ ] Thêm adversarial DGP
- [ ] Mở rộng stress test sang DGP/economics shift
- [ ] Sửa wording A/A và Stress Test
- [ ] Viết lại Decision Memo theo assumption-based recommendation
- [ ] Thêm uncertainty vào economics
- [ ] Thiết kế randomized holdout
- [ ] Thêm champion–challenger simulation
- [ ] Hoàn thiện Promotion Policy Simulator
- [ ] Ghi rõ validated-in-simulation vs requires-GSM-data
- [ ] Không mở rộng Driver Agent/MARL trong scope chính

---

# 49. Một câu chốt cho toàn dự án

> **Từ “A/B Testing + Uplift Model” chuyển thành “Experimentation-Driven Promotion Decision System”: đo incremental effect, dự đoán heterogeneous response, chuyển response thành expected profit, rồi chọn targeting policy tối ưu dưới ràng buộc ngân sách và uncertainty.**
