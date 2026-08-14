# GSM Promotion Experimentation — Định vị dự án thực tập, lý do lựa chọn và hướng cải thiện

> **Mục tiêu tài liệu:** Đóng gói toàn bộ định hướng cho project thực tập liên quan đến bài toán promotion/voucher của GSM, trong bối cảnh **project thực tập không phải project production thật của GSM**, người thực tập **không trực tiếp tham gia vận hành dự án doanh nghiệp**, mà được giao một bài toán liên quan để nghiên cứu, mô phỏng và xây prototype.
>
> Tài liệu tập trung trả lời 4 câu hỏi:
>
> 1. Vì sao nên định vị project theo hướng **Experimentation → Uplift → Policy Evaluation**?
> 2. Project thực tập khác gì với project doanh nghiệp thật?
> 3. Những phần hiện có nên giữ, bỏ, hoặc nâng cấp như thế nào?
> 4. Làm thế nào để trình bày project sao cho doanh nghiệp đánh giá cao tính thực chiến và khả năng chuyển giao sang project thật sau này?

---

# 1. Bối cảnh doanh nghiệp và ranh giới của project thực tập

## 1.1. Bối cảnh bài toán doanh nghiệp

Theo bối cảnh được chia sẻ trong quá trình thực tập:

- GSM có bài toán tối ưu promotion/voucher cho khách hàng ride-hailing.
- Phía Business/Marketing hiện vẫn có logic khuyến mãi theo dạng rule-based/matrix và có chu kỳ cập nhật định kỳ.
- Phía Data/AI đang nghiên cứu hoặc ứng dụng hướng uplift modeling để cá nhân hóa treatment/promotion tốt hơn.
- Một khó khăn của dữ liệu lịch sử là treatment assignment không hoàn toàn randomized, nên việc học treatment effect trực tiếp từ historical data có thể chịu selection bias/confounding.
- Doanh nghiệp đã có pilot thực tế trên một phần user population, nhưng project thực tập **không trực tiếp sử dụng hay triển khai trên dữ liệu production này**.

Điểm này cần được phân biệt rõ trong mọi tài liệu và presentation.

## 1.2. Project thực tập không phải project production

Project thực tập nên được mô tả là:

> **Một simulation-based prototype mô phỏng bài toán promotion experimentation và uplift modeling trong ride-hailing, sử dụng public mobility data kết hợp synthetic causal data để nghiên cứu toàn bộ pipeline từ thiết kế thí nghiệm đến policy evaluation.**

Không nên mô tả là:

> “Hệ thống tối ưu voucher của GSM.”

Không nên tuyên bố:

> “Mô hình của em giải quyết trực tiếp bài toán đang chạy tại GSM.”

Đúng hơn phải là:

> “Project lấy cảm hứng từ bài toán thực tế tại doanh nghiệp và xây một controlled sandbox để nghiên cứu phương pháp có thể chuyển giao khi có randomized business data phù hợp.”

---

# 2. Vì sao framing này tốt hơn?

## 2.1. Không cạnh tranh trực tiếp với team Data/AI production

Nếu project thực tập chỉ cố:

- thêm model uplift,
- tối ưu hyperparameter,
- thử thêm Causal Forest,
- benchmark nhiều thuật toán,

thì rất dễ trở thành một bài benchmark thuật toán bên ngoài.

Trong khi đó, team Data/AI nội bộ:

- hiểu hệ thống production hơn,
- có access data thật,
- có infrastructure,
- có domain constraints,
- có deployment pipeline.

Intern khó tạo lợi thế nếu chỉ nói:

> “Em thử model X tốt hơn model Y.”

Hướng tốt hơn là xây **methodology layer**:

```text
Business Problem
      ↓
Experiment Design
      ↓
Trust Checks
      ↓
ATE / HTE
      ↓
Uplift
      ↓
Economics
      ↓
Policy Evaluation
```

Đây là phần vừa có tính causal, vừa có business, vừa có thể tái sử dụng.

---

# 3. Câu hỏi trung tâm nên được chốt lại

Thay vì:

> “Model uplift nào dự đoán tốt nhất?”

Nên dùng:

> **Làm thế nào để từ một promotion experiment đáng tin cậy đo được incremental effect, phát hiện treatment heterogeneity và chuyển kết quả đó thành một policy target voucher hiệu quả về mặt kinh tế?**

Câu hỏi này mạnh hơn vì bao trùm:

- experimental design,
- causal inference,
- uplift modeling,
- targeting,
- economics,
- decision support.

---

# 4. Phạm vi project nên chốt

## 4.1. Core scope

1. **Experiment Design**
2. **A/A Testing**
3. **Experiment Trust Checks**
4. **A/B Effect Estimation**
5. **Segmentation for Business Understanding**
6. **Uplift Modeling**
7. **Profit-aware Targeting**
8. **Stress Testing**
9. **Policy Comparison**
10. **Decision-support Prototype**

## 4.2. Optional scope

- X-Learner benchmark
- Uplift calibration
- Champion–Challenger simulation
- Randomized holdout design
- Agentic analytics assistant

## 4.3. Out of scope

Không nên mở rộng sang:

- Driver Agent
- Multi-Agent Marketplace
- Matching
- Driver repositioning
- Surge pricing
- MARL
- Real-time production serving
- Full production MLOps
- Marketplace interference modeling

Những hướng này thú vị nhưng sẽ biến project thành một bài toán khác.

---

# 5. Giá trị thật sự của synthetic sandbox

Một cách trình bày yếu:

> “Vì không có data thật nên em phải mô phỏng.”

Một cách trình bày tốt hơn:

> **“Em sử dụng synthetic causal sandbox để tạo môi trường có known counterfactual, từ đó có thể kiểm chứng correctness của A/B, uplift và policy evaluation trước khi áp dụng trên dữ liệu doanh nghiệp thật.”**

## 5.1. Vì sao synthetic có giá trị?

Trong dữ liệu thực:

- không biết true ITE,
- không quan sát trực tiếp counterfactual,
- khó biết model có học đúng treatment effect không.

Trong synthetic:

```text
Y0 = outcome nếu không treatment
Y1 = outcome nếu có treatment

ITE = Y1 - Y0
```

Ta biết ground truth.

Do đó có thể kiểm tra:

- estimated ATE có gần true ATE không?
- CI có cover true effect không?
- uplift model có rank đúng không?
- policy learned có gần oracle policy không?
- profit estimate có ổn định không?

---

# 6. Nhưng synthetic hiện tại có một hạn chế lớn

Synthetic generator hiện tại có thể đang “biết trước đáp án” tương đối nhiều.

Ví dụ:

```text
Urban leisure    → uplift cao
Suburban leisure → uplift cao
Airport          → uplift thấp
Rush hour        → uplift thấp
Cash             → uplift thấp
Recency          → uplift cao
```

Sau đó uplift model được train trên chính hoặc gần các feature tạo ra treatment effect.

Điều này phù hợp để kiểm tra:

> “Pipeline có recover known DGP không?”

Nhưng chưa đủ để chứng minh:

> “Pipeline robust khi DGP không giống assumptions.”

## Cải thiện

Chia synthetic evaluation thành 2 tầng.

### Tier A — Known-DGP

Giữ generator hiện tại.

Mục tiêu:

> correctness test.

### Tier B — Adversarial / Misspecified-DGP

Tạo thêm các scenario:

- nonlinear HTE,
- threshold effect,
- negative uplift,
- rare persuadables,
- hidden effect modifier,
- train-test shift,
- cluster không trùng treatment response.

Mục tiêu:

> robustness test.

---

# 7. Vai trò đúng của K-Means

K-Means không nên là decision engine cuối.

## 7.1. K-Means trả lời

> User nào giống nhau về behavior profile?

## 7.2. Uplift trả lời

> User nào thay đổi hành vi do voucher?

Hai câu hỏi khác nhau.

## 7.3. Architecture đúng

```text
User Features
   ├──→ K-Means
   │      ↓
   │    Persona
   │    Explainability
   │    Monitoring
   │
   └──→ Uplift Model
          ↓
       Predicted CATE
          ↓
       Economics
          ↓
       Target Policy
```

## 7.4. Segment targeting vẫn nên giữ

Nhưng chỉ với vai trò baseline.

So sánh:

- Mass Voucher
- Segment Targeting
- Uplift Targeting
- Profit Targeting

Như vậy mới chứng minh uplift có mang thêm giá trị so với segmentation không.

---

# 8. Từ Uplift sang Profit

Không nên target user chỉ vì:

```text
CATE > 0
```

Nên target nếu:

```text
Expected Incremental Profit > 0
```

Công thức:

```text
Expected Value_i
=
Predicted CATE_i × Contribution Margin_i
− Expected Voucher Cost_i
```

Target nếu:

```text
Expected Value_i > 0
```

Nếu có budget B:

```text
Maximize:
Σ target_i × Expected Value_i

Subject to:
Σ target_i × VoucherCost_i ≤ B
```

Nếu chỉ có một voucher type, baseline đơn giản:

```text
1. Tính EV từng user
2. Loại EV <= 0
3. Sort EV giảm dần
4. Chọn đến khi hết budget
```

Không cần solver phức tạp.

---

# 9. Vì sao phải dùng Contribution Margin thay vì Fare?

Fare không phải profit.

Để đánh giá promotion cần gần với:

```text
Contribution Margin
=
Revenue
− variable operating cost
```

Nếu project không có số thật, không được coi assumptions là truth.

Nên parameterize:

```text
voucher_cost
contribution_margin_per_ride
redemption_rate
budget
```

Sau đó chạy sensitivity.

---

# 10. Policy Comparison nên là output chính

Final dashboard/report không nên chỉ khoe:

- Qini Curve
- AUUC
- RMSE
- feature importance

Business cần thấy:

| Policy | Logic |
|---|---|
| No Voucher | Không treatment |
| Mass Voucher | Tất cả eligible |
| Segment Targeting | Target theo persona |
| Uplift Targeting | Top predicted CATE |
| Profit Targeting | Top expected profit |
| Budget-Constrained Policy | Max profit dưới budget |

KPI:

- target rate
- voucher spend
- incremental rides
- cost per incremental ride
- incremental profit
- ROI
- policy value

---

# 11. Oracle Policy — lợi thế lớn của synthetic data

Vì synthetic có true ITE, có thể tính:

```text
Oracle EV_i
=
True ITE_i × Margin_i
− Voucher Cost_i
```

Oracle policy target các user có EV thật cao nhất.

Sau đó:

```text
Policy Regret
=
Oracle Profit
− Learned Policy Profit
```

Đây là metric mạnh vì trực tiếp đo:

> Policy học được còn cách optimal-under-DGP bao xa?

---

# 12. Uplift Model nên đánh giá thế nào?

Không dùng Accuracy.

## Model-level metrics

- Qini
- AUUC
- CATE RMSE
- MAE
- Correlation với true ITE
- Uplift by decile

## Policy-level metrics

- Profit@Top10%
- Profit@Top20%
- Profit@Budget
- Incremental Rides@Budget
- Policy Value
- Policy Regret

---

# 13. Thêm Uplift Calibration

Ranking tốt chưa đủ.

Ví dụ:

```text
Predicted CATE = +1.0
Actual uplift = +0.2
```

Nếu dùng predicted CATE để tính profit, economics sẽ bị thổi phồng.

Cách kiểm tra:

1. Chia predicted CATE thành decile.
2. Với mỗi decile tính:
   - predicted uplift mean,
   - observed treatment-control uplift,
   - true ITE mean (synthetic).
3. So predicted vs observed/true.

---

# 14. A/A không chỉ là một notebook phụ

A/A nên trở thành một phần của **Experiment Trust Gate**.

```text
Experiment
    ↓
SRM?
Fail → STOP
    ↓
Balance?
Fail lớn → REVIEW
    ↓
Exposure/Logging?
Fail → STOP
    ↓
Invariant Metrics?
Fail → REVIEW
    ↓
Primary Metric
    ↓
Decision
```

Output:

```text
EXPERIMENT HEALTH:
PASS / REVIEW / FAIL
```

---

# 15. Cách diễn giải A/A đúng

Không nên:

> “A/A chứng minh hệ thống hoàn toàn chính xác.”

Nên:

> “Trong các simulated settings đã kiểm tra, hệ thống không cho thấy vấn đề đáng kể về sample ratio, covariate balance và Type-I error calibration.”

A/A không đảm bảo production correctness.

---

# 16. SRM, Balance và Logging Integrity

## SRM

Kiểm tra:

```text
Observed Treatment/Control Ratio
vs
Expected Ratio
```

Nếu lệch đáng kể:

- assignment bug,
- logging bug,
- eligibility issue,
- experiment contamination.

## Covariate Balance

Dùng SMD với các pre-treatment variables.

## Exposure Integrity

Không chỉ assignment.

Cần phân biệt:

```text
Assigned Treatment
vs
Actually Exposed
```

Trong sandbox có thể mô phỏng exposure failure để stress-test pipeline.

---

# 17. Power và MDE nên thành một module riêng

Business question:

> “Campaign này cần bao nhiêu user để detect uplift tối thiểu có ý nghĩa?”

Input:

```text
baseline_mean
variance
MDE
alpha
power
treatment_ratio
```

Output:

```text
required_sample_size
estimated_duration
```

Đây là phần rất thực chiến.

---

# 18. Statistical Significance ≠ Business Significance

Scenario:

```text
p < 0.05
nhưng
incremental_profit < 0
```

→ không rollout.

Scenario:

```text
profit > 0
nhưng CI rộng và cắt 0
```

→ tiếp tục test / không rollout toàn phần.

Decision rule có thể:

```text
ROLL OUT
if lower bound of incremental profit > 0

CONTINUE TEST
if point estimate > 0 nhưng CI cắt 0

STOP
if upper bound <= 0
```

---

# 19. Uncertainty cần đi xuyên sang Economics

Không chỉ:

```text
ATE + CI
```

mà cần:

```text
ATE CI
  ↓
Incremental Rides CI
  ↓
Incremental Profit CI
```

Đây là điểm làm project khác một bài dashboard thông thường.

---

# 20. Experiment → Learn → Policy → Re-test

Không nên:

```text
A/B
→ Uplift
→ Recommendation
→ END
```

Nên:

```text
1. Define population
2. Randomize
3. Validate experiment health
4. Estimate ATE/HTE
5. Train uplift
6. Build targeting policy
7. Keep randomized holdout
8. Champion–Challenger
9. Re-estimate
10. Update policy
```

Đây là lifecycle thực tế hơn.

---

# 21. Randomized Holdout

Nếu high-CATE users luôn treatment:

- mất counterfactual,
- khó estimate decay,
- khó recalibrate model.

Nên giữ một randomized holdout nhỏ.

Trong project thực tập, có thể mô phỏng design này.

---

# 22. Champion–Challenger

Ví dụ:

```text
Champion:
Segment Targeting

Challenger:
Profit-Based Uplift Targeting
```

Randomize user giữa hai policy.

So sánh:

- incremental rides,
- incremental profit,
- cost/incremental ride,
- guardrails.

Đây là cách validate policy mới trước khi thay policy cũ.

---

# 23. Product cuối nên là Promotion Policy Simulator

Không chỉ là notebook.

## Tab 1 — Experiment Setup

Input:

```text
Population
Treatment Ratio
Primary Metric
MDE
Alpha
Power
Campaign Duration
```

## Tab 2 — Experiment Health

```text
SRM               PASS
Balance           PASS
Exposure          PASS
A/A Calibration   PASS
```

## Tab 3 — A/B Result

```text
Control Mean
Treatment Mean
ATE
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

## Tab 5 — Policy Simulator

Input:

```text
Budget
Voucher Cost
Contribution Margin
Max Target %
CATE Threshold
```

Output:

```text
Policy
Targeted Users
Spend
Incremental Rides
Incremental Profit
ROI
Uncertainty
```

---

# 24. Không gọi dashboard là production system

Nên gọi:

> **Interactive Simulation & Decision-Support Prototype**

Không gọi:

> “Production promotion engine.”

---

# 25. Reusable Code mới là điểm cộng lớn

Project nên giảm notebook-only logic.

Gợi ý:

```text
src/
├── synthetic_generator.py
├── experiment_design.py
├── experiment_health.py
├── ab_analysis.py
├── segmentation.py
├── uplift_model.py
├── uplift_evaluation.py
├── policy_evaluation.py
├── stress_test.py
└── dashboard/
```

---

# 26. Config-driven Design

Không hard-code:

- treatment ratio,
- voucher cost,
- margin,
- DGP assumptions.

Nên:

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
```

---

# 27. Data Contract

Tạo:

```text
docs/data_contract.md
```

Schema tối thiểu:

```text
user_id
experiment_id
assignment_time
pre_treatment_features
treatment
exposure
outcome
segment
```

Khi sau này thay data thật:

- giữ schema,
- thay input source.

Đây chính là tính transferability.

---

# 28. Feature Cutoff

Phải tách:

```text
Historical Feature Window
[-90d, 0)
       ↓
Randomization
t = 0
       ↓
Outcome Window
[0, +14d]
```

Không dùng post-treatment feature để dự đoán uplift.

---

# 29. Stress Test cần mở rộng

Hiện stress test không nên chỉ có:

- sample size,
- Gaussian noise,
- treatment ratio.

Nên thêm:

## DGP Shift

- HTE thay đổi
- cluster composition shift
- nonlinear response

## Economics Shift

- voucher cost tăng
- margin giảm
- budget thay đổi

## Data Shift

- user behavior distribution thay đổi
- missingness tăng
- recency shift

## Experiment Failure

- SRM
- exposure failure
- logging missing
- contamination

---

# 30. Policy Robustness

Không chỉ hỏi:

> “Model score có ổn không?”

Hỏi:

> “Recommendation có đổi khi assumptions thay đổi không?”

Ví dụ:

```text
Voucher Cost 10k → Profit Targeting
Voucher Cost 30k → Only top 5%
Voucher Cost 50k → No Campaign
```

Đây là business insight mạnh.

---

# 31. Policy Frontier

Tạo grid:

```text
Voucher Cost × Margin
```

Mỗi cell:

```text
Best Policy
```

Ví dụ:

| Voucher | Margin | Best Policy |
|---:|---:|---|
| 10k | 30k | Uplift Targeting |
| 20k | 30k | Profit Targeting |
| 30k | 20k | Very Selective |
| 40k | 15k | No Promotion |

---

# 32. Cách nói về project thật của GSM

Không nên:

> “Em đang giải quyết vấn đề data của uplift model GSM.”

Nên:

> “Bối cảnh bài toán doanh nghiệp cho thấy promotion optimization đang chuyển từ rule-based sang data/AI và uplift modeling, trong khi causal treatment data vẫn là một challenge. Project thực tập của em mô phỏng một experimentation foundation có known ground truth để nghiên cứu các phương pháp cần thiết cho bài toán này.”

---

# 33. Cách nói về dữ liệu production

Không được ngụ ý:

> “Kết quả synthetic là GSM effect.”

Phải nói:

> “Synthetic treatment effect chỉ là assumptions dùng để kiểm chứng pipeline.”

---

# 34. Hai lớp bằng chứng

Final report nên có:

| Validated in Simulation | Requires Real Business Data |
|---|---|
| A/A calibration | Real assignment integrity |
| Recover known ATE | Real GSM ATE |
| Uplift ranking vs true ITE | Real CATE |
| Policy value under assumptions | Real economics |
| Robustness in simulated shift | Production drift |

---

# 35. Vì sao cách này giúp được đánh giá cao?

Doanh nghiệp không chỉ đánh giá:

- code có chạy không,
- model score cao không.

Họ còn đánh giá:

## Business Understanding

Bạn hiểu:

- campaign objective,
- cannibalization,
- incremental behavior,
- voucher economics.

## Causal Understanding

Bạn hiểu:

- randomization,
- confounding,
- ATE,
- HTE,
- counterfactual.

## Engineering Discipline

Bạn có:

- reusable pipeline,
- config,
- data contract,
- validation gate.

## Evidence Discipline

Bạn biết:

- đâu là simulation,
- đâu là production evidence,
- đâu là limitation.

Đây là profile mạnh hơn “intern biết nhiều thuật toán”.

---

# 36. Điều doanh nghiệp có thể reuse từ project

Không phải synthetic data.

Mà là:

```text
Experiment Specification
Experiment Health Checks
A/B Estimator
Uplift Evaluation
Policy Comparison
Economics Layer
Stress-Test Framework
Decision-Support UI
```

Synthetic chỉ là môi trường test.

---

# 37. Định vị khả năng chuyển giao

Câu nên dùng:

> “Em cố gắng thiết kế pipeline sao cho synthetic data generator chỉ là một data source. Khi có randomized business data, phần experiment health, A/B estimation, uplift evaluation và policy comparison có thể giữ nguyên logic.”

---

# 38. Final Architecture

```text
Public Mobility Data
        +
Synthetic User Generator
        ↓
Known Causal Ground Truth
        ↓
Experiment Design
        ↓
Randomization
        ↓
Trust Gate
SRM / Balance / A/A / Exposure
        ↓
ATE + HTE
        ↓
┌─────────────────────┐
│                     │
K-Means             Uplift
Persona             CATE
│                     │
└──────────┬──────────┘
           ↓
Economics Layer
           ↓
Policy Comparison
           ↓
Budget-Constrained Targeting
           ↓
Decision-Support Dashboard
           ↓
Stress Test / Sensitivity
```

---

# 39. Storyline thuyết trình

## Slide 1 — Business Context

> Promotion có thể tăng usage nhưng cũng có cannibalization/subsidy waste.

## Slide 2 — Why Prediction Is Not Enough

> High propensity ≠ high incremental response.

## Slide 3 — Internship Scope

> Simulation-based experimentation sandbox, không phải production GSM project.

## Slide 4 — Causal Data Generation

> Y0/Y1/true ITE.

## Slide 5 — Experiment Design

> Randomization, A/A, SRM, balance.

## Slide 6 — A/B Result

> ATE + CI + economics.

## Slide 7 — Heterogeneous Treatment Response

> segment ATE + uplift model.

## Slide 8 — From CATE to Profit

> expected incremental profit.

## Slide 9 — Policy Comparison

> mass vs segment vs uplift vs profit.

## Slide 10 — Stress Test

> robustness under DGP/economic shift.

## Slide 11 — What Is Validated

> simulation vs real business evidence.

## Slide 12 — Transferability

> same methodology can consume randomized real data.

---

# 40. Cách nói trong presentation

Một câu mở đầu tốt:

> “Project này không nhằm thay thế hệ thống promotion hiện tại của GSM hay khẳng định policy nào đang tối ưu trên production. Em xây một simulation-based experimentation sandbox lấy cảm hứng từ bài toán thực tế, với mục tiêu kiểm chứng end-to-end logic từ randomization, A/B testing, uplift modeling đến profit-aware targeting trong môi trường có known ground truth.”

---

# 41. Câu mô tả giá trị

> “Giá trị chính của project không nằm ở synthetic effect cụ thể, mà nằm ở methodology và reusable pipeline: nếu sau này có randomized business data, cùng framework có thể được dùng để kiểm tra experiment health, estimate treatment effect, evaluate uplift và so sánh promotion policy.”

---

# 42. Những điều không nên nói

Không nói:

- “Model này tốt hơn hệ thống GSM.”
- “Policy này nên deploy.”
- “Uplift thực tế của nhóm A là X.”
- “ROI của GSM sẽ là Y.”
- “Em đã xử lý trực tiếp pilot TP.HCM.”
- “Synthetic data đại diện cho customer behavior thật.”

---

# 43. Những điều nên nói

- “Validated in simulation.”
- “Assumption-driven economics.”
- “Synthetic causal ground truth.”
- “Reusable experimentation framework.”
- “Policy evaluation sandbox.”
- “Transferable methodology.”
- “Requires validation on randomized business data.”

---

# 44. Hướng cải thiện ưu tiên

## Priority 1 — Sửa framing

- README
- Decision Memo
- Final deck
- Dashboard labels

## Priority 2 — Refactor code

- module hóa,
- config-driven,
- data contract.

## Priority 3 — Policy Evaluation

- no voucher,
- mass,
- segment,
- uplift,
- profit.

## Priority 4 — Oracle Benchmark

- true ITE policy,
- regret.

## Priority 5 — Calibration

- predicted vs observed vs true uplift.

## Priority 6 — Adversarial DGP

- shift,
- nonlinear,
- hidden modifier.

## Priority 7 — Dashboard

- Experiment Health
- A/B
- HTE
- Policy Simulator

---

# 45. Nếu chỉ còn 1 tuần

Làm:

1. sửa README,
2. sửa Decision Memo,
3. train uplift toàn eligible population,
4. 5-policy comparison,
5. profit layer,
6. oracle regret,
7. dashboard policy simulator.

---

# 46. Nếu còn 2 tuần

Thêm:

8. uplift calibration,
9. adversarial DGP,
10. economics sensitivity,
11. experiment health gate,
12. champion–challenger simulation.

---

# 47. Không ưu tiên trong thời gian còn lại

- Driver Agent
- TDC/Taxi GPS dataset
- MARL
- matching simulator
- model zoo
- production API phức tạp
- thêm quá nhiều causal learner

---

# 48. Acceptance Criteria cuối

## Experiment

- [ ] Randomization rõ
- [ ] SRM check
- [ ] Balance check
- [ ] A/A repeated simulation
- [ ] ATE + CI
- [ ] MDE/Power
- [ ] Decision rule

## Uplift

- [ ] Out-of-sample evaluation
- [ ] Qini/AUUC
- [ ] true ITE comparison
- [ ] calibration
- [ ] segment vs uplift comparison

## Economics

- [ ] voucher cost config
- [ ] margin config
- [ ] budget config
- [ ] profit policy
- [ ] uncertainty

## Robustness

- [ ] DGP shift
- [ ] economics shift
- [ ] null effect
- [ ] treatment imbalance
- [ ] sample size

## Product

- [ ] reusable modules
- [ ] dashboard
- [ ] policy comparison
- [ ] limitation section
- [ ] simulation vs production evidence separation

---

# 49. Một câu chốt cho toàn project

> **Project thực tập nên được định vị như một experimentation-driven promotion decision sandbox: dùng synthetic causal ground truth để kiểm chứng toàn bộ chuỗi A/B Testing → Heterogeneous Treatment Effect → Uplift Modeling → Profit-Aware Targeting, với mục tiêu xây một methodology và reusable pipeline có thể chuyển giao khi doanh nghiệp có randomized real-world data phù hợp.**

---

# 50. Thông điệp cuối dành cho doanh nghiệp

Nếu muốn được đánh giá cao và có cơ hội tham gia project thật sau internship, điều cần chứng minh không phải:

> “Em đã thử nhiều thuật toán.”

Mà là:

> **“Em hiểu bài toán business, hiểu vì sao causal data quan trọng, xây được một pipeline có thể kiểm chứng bằng ground truth, biết cách chuyển uplift thành quyết định kinh tế, và biết rõ giới hạn của synthetic evidence. Khi có dữ liệu randomized thật, em có thể chuyển từ sandbox sang empirical validation thay vì phải bắt đầu lại từ đầu.”**

Đó mới là tín hiệu mạnh rằng intern có khả năng bước vào project doanh nghiệp thực tế.
