# GSM Promotion Experimentation — MASTER FINAL DOCUMENT
## Data Foundation → Causal Experimentation → Uplift & Business Policy

> **Trạng thái tài liệu:** FINAL — dùng thay thế toàn bộ các bản góp ý/roadmap trước.  
> **Mục đích:** Master document để (1) ghi lại hiện trạng đã làm, (2) giải thích vì sao từng bước tồn tại, (3) chỉ ra điểm mạnh/yếu hiện tại, (4) định hướng cải thiện cuối cùng, và (5) làm khung trình bày project với mentor/doanh nghiệp.
>
> **Project:** GSM Promotion Experimentation  
> **Repo:** https://github.com/thaibuivan/GSM-promotion-experimentation
>
> **Nguyên tắc quan trọng nhất:** Project thực tập **không phải production project của GSM**. Đây là một bài toán liên quan đến project thực tế, được xây như một **simulation-based experimentation sandbox** để nghiên cứu và kiểm chứng methodology trước khi có randomized business data phù hợp.

---

# 0. Executive Summary

Project nên được định vị bằng 3 trụ cột:

```text
PILLAR 1 — DATA FOUNDATION & CAUSAL SIMULATION
Real mobility data
→ Data quality
→ EDA
→ Empirical calibration
→ Synthetic user population
→ Y0 / ITE / Y1
→ Synthetic validation

                ↓

PILLAR 2 — EXPERIMENTATION & CAUSAL ESTIMATION
Segmentation
→ Experiment design
→ Randomization
→ A/A
→ SRM / Balance
→ A/B
→ ATE / HTE
→ Power / Uncertainty

                ↓

PILLAR 3 — UPLIFT & BUSINESS POLICY
Uplift model
→ Individual CATE
→ Incremental Rides / GMV
→ Burn / Economics
→ Policy comparison
→ Decision-support prototype
```

Đây là cấu trúc cuối cùng phù hợp nhất vì:

1. Nó **nêu bật phần EDA + mô phỏng dữ liệu**, vốn là phần nặng và có giá trị lớn của project.
2. Nó giữ đúng **core scope mentor giao là A/B Testing**.
3. Nó đặt **Uplift Modeling là strategic extension** — không phải yêu cầu bắt buộc ban đầu, nhưng là bước mở rộng tự nhiên và rất sát hướng team Data/AI thực tế đang nghiên cứu.
4. Nó kết nối technical result với business metric như **Incremental Rides, Incremental GMV, Burn, Burn/GMV, Cost per Incremental Ride, Expected Incremental Profit** mà không giả vờ rằng project đã biết công thức nội bộ GSM chính xác.
5. Nó biến project từ “chuỗi notebook” thành một **reusable experimentation & policy evaluation framework**.

---

# 1. Bối cảnh doanh nghiệp

Theo bối cảnh được tìm hiểu trong kỳ thực tập:

- Business/Marketing đang vận hành promotion theo dạng rule-based/matrix.
- Rule được cập nhật định kỳ theo nhu cầu business.
- Phía Data/AI đang nghiên cứu/ứng dụng Uplift Modeling để cá nhân hóa treatment tốt hơn.
- Historical treatment assignment chưa hoàn toàn randomized, vì vậy treatment/control trong dữ liệu lịch sử có thể chịu selection bias/confounding.
- Doanh nghiệp có pilot thật trên một phần user population, nhưng project thực tập **không trực tiếp tham gia triển khai, không sử dụng production data và không có quyền kết luận production policy**.

## 1.1. Vì sao non-randomized historical data là vấn đề?

Nếu treatment assignment trước đây phụ thuộc vào:

- activity level,
- customer segment,
- recency,
- location,
- campaign rule,
- business priority,
- channel,

thì:

```text
E[Y | T=1] - E[Y | T=0]
```

không mặc nhiên là causal treatment effect.

Treated và Control có thể khác nhau **trước treatment**.

Đây chính là lý do Experimentation và Randomization là nền tảng quan trọng trước khi Uplift Modeling được dùng như một causal targeting tool.

---

# 2. Ranh giới của project thực tập

## 2.1. Không nên nói

- “Đây là hệ thống tối ưu voucher của GSM.”
- “Model này tốt hơn hệ thống hiện tại của GSM.”
- “Policy này nên deploy vào production.”
- “ROI synthetic này là ROI thật của GSM.”
- “Uplift của segment X trong GSM là Y.”
- “Project đã xử lý trực tiếp pilot thực tế.”

## 2.2. Nên nói

> **Project xây một simulation-based experimentation sandbox, sử dụng public mobility data kết hợp synthetic causal user-level data để kiểm chứng end-to-end methodology từ Data Foundation → A/B Testing → Uplift Modeling → Business Policy Evaluation.**

Giá trị của project nằm ở:

- data reasoning,
- causal simulation,
- experiment design,
- statistical validation,
- uplift methodology,
- economics/policy layer,
- robustness,
- reusable pipeline.

---

# 3. Câu hỏi trung tâm của project

Câu hỏi ban đầu:

> Voucher có làm tăng số chuyến không?

Câu hỏi cuối nên là:

> **Làm thế nào để từ dữ liệu mobility công khai xây một causal experimentation sandbox đủ hợp lý, sau đó dùng randomized A/B Testing để đo incremental effect, mở rộng sang Uplift Modeling để phát hiện heterogeneous response, và đánh giá các promotion policy theo Incremental Rides/GMV và Promotion Burn?**

Ba tầng:

### Causal Effectiveness
> Voucher có thực sự tạo thêm hành vi không?

### Heterogeneous Response
> Ai phản ứng mạnh hơn với voucher?

### Business Efficiency
> Với cùng mức burn/budget, policy nào tạo nhiều incremental value hơn?

---

# 4. Vì sao cấu trúc 3 Pillar này khác bản v2 trước?

Bản v2 trước đó đặt trọng tâm khá mạnh vào:

```text
Experimentation
→ Uplift
→ Economics
→ Policy
```

EDA và synthetic data vẫn có mặt, nhưng chủ yếu được trình bày như **input preparation**.

Cấu trúc FINAL thay đổi ở 4 điểm:

## 4.1. Data Foundation được nâng thành một trụ cột độc lập

Không còn:

```text
EDA → preprocessing step
```

mà thành:

```text
EDA
→ empirical understanding
→ simulation design
→ causal data generation
→ validation
```

Tức là **EDA và synthetic generation là technical contribution**, không phải bước phụ.

## 4.2. Y0 / ITE / Y1 được đặt đúng trước K-Means

Thứ tự chính xác theo Week 2:

```text
EDA
→ Synthetic covariates
→ Y0
→ ITE
→ Y1
→ Observational / Randomized treatment
→ K-Means
→ Experiment
```

K-Means **không sinh ra treatment effect**.

Treatment effect đã tồn tại trong causal DGP trước khi segmentation được chạy.

## 4.3. A/B là core mentor scope

Mentor giới hạn yêu cầu chính đến A/B Testing.

Vì vậy:

```text
Pillar 2 = Core internship deliverable
```

Trong khi:

```text
Pillar 3 / Uplift = Strategic extension
```

Uplift vẫn được giữ rất mạnh vì sau khi xây, nó trở thành một phần logic quan trọng của pipeline và sát với hướng Data/AI thực tế.

## 4.4. Business metrics được đưa xuống sau causal evidence

Không bắt đầu từ Profit/GMV/Burn.

Thứ tự đúng:

```text
Causal Effect
→ Incremental Rides
→ Incremental GMV
→ Burn Efficiency
→ Policy Decision
```

Điều này tránh việc business metric “đè” lên causal reasoning.

---

# 5. Hiện trạng project theo repo

Repo hiện có các nhóm chính:

```text
notebooks/
├── week1_eda
├── week2_synthetic_data
├── week3_segmentation
├── week4_ab_testing
├── week5_uplift_modeling
└── week6_stress_test
```

Các báo cáo trong `docs/` cũng phản ánh pipeline tương ứng:

- Week 1: Data Quality, Preprocessing, Causal Thinking
- Week 2: Synthetic Data / SCM
- Week 3: Segmentation + Experiment Design
- Week 4: A/A + A/B
- Week 5: Uplift Modeling
- Week 6: Stress Test

Như vậy project đã có technical breadth đủ lớn. Việc cần làm không phải là thêm nhiều thuật toán hơn, mà là **làm rõ logic, validation và business transferability**.

---

# 6. PILLAR 1 — DATA FOUNDATION & CAUSAL SIMULATION

Đây nên được coi là phần nặng và quan trọng ngang Experimentation.

---

# 7. Data Challenge: dữ liệu ban đầu không có cấu trúc phù hợp trực tiếp cho Uplift/A-B

NYC TLC là trip-level data.

Trong khi bài toán promotion experimentation cần gần với:

```text
user_id
pre-treatment behavior
treatment
exposure
post-treatment outcome
```

TLC không cung cấp trực tiếp:

- persistent customer ID,
- voucher assignment,
- treatment/control,
- true counterfactual,
- true treatment effect,
- customer demographics.

Do đó không thể:

```text
Load TLC
→ train uplift
```

một cách trực tiếp.

Project bắt buộc phải giải bài toán:

> **Làm thế nào chuyển empirical trip-level information thành một user-level causal simulation environment?**

Đây chính là lý do phần EDA + simulation có giá trị lớn.

---

# 8. Data Quality không phải bước làm sạch cơ học

Week 1 bắt đầu với Yellow Taxi January 2026.

Báo cáo Data Quality ghi nhận:

- 3,724,889 raw trip records.
- Missing có cấu trúc ở một nhóm biến.
- Nhiều lỗi cần phân biệt giữa logical error và long-tail observation.
- Geographic lookup có unmatched records.

Điểm quan trọng về tư duy:

> Không được đồng nhất outlier với error.

Project đã cố giữ các extreme observations nếu vẫn hợp lý về mặt nghiệp vụ/vật lý, thay vì áp hard cutoff tùy ý.

## 8.1. Điều nên nhấn khi present

Phần preprocessing không chỉ là:

> “Xóa null và outlier.”

Mà là:

> **Phân biệt Data Error, Structural Missing và Valid Long-Tail Behavior.**

Đây là tư duy data science thực tế.

---

# 9. EDA nên được gọi là Empirical Calibration Layer

EDA không nên được trình bày như gallery biểu đồ.

Vai trò cuối của EDA là:

> **Rút ra empirical patterns để định nghĩa simulation assumptions.**

Các nhóm pattern:

## 9.1. Temporal

- Hour-of-day
- Peak / off-peak
- Weekday / weekend
- Daily variation

## 9.2. Spatial

- Pickup/drop-off concentration
- Borough/zone behavior
- Airport vs non-airport

## 9.3. Trip economics

- Fare distribution
- Fare long tail
- Fare/distance relationship
- Revenue proxies

## 9.4. Trip behavior

- Distance
- Duration
- Speed
- Short/long trips

---

# 10. Bắt buộc tạo EDA → Simulation Mapping

Một artifact nên có trong final report:

| EDA / External Observation | Simulation Decision | Source Type |
|---|---|---|
| Fare distribution lệch phải | `fare_obs` dùng log-normal / skewed distribution | TLC empirical |
| Peak demand theo hour | `preferred_hour` dùng weighted probability | TLC empirical |
| Airport trips có economics khác | airport indicator + fare multiplier | TLC-inspired |
| Distance/duration/fare có dependency | không sinh độc lập hoàn toàn | TLC empirical |
| User trip frequency | user-level synthetic/reference calibration | External / synthetic |
| Age | synthetic distribution | Assumption / external source |
| Income | synthetic log-normal | Assumption / external source |
| Treatment effect | SCM causal equation | Explicit causal assumption |
| Rain response | confounding scenario | Assumption |
| Voucher assignment bias | observational assignment mechanism | Assumption |

Bảng này rất quan trọng vì nó cho thấy:

> **Không phải mọi biến synthetic đều đến từ NYC TLC.**

---

# 11. Một điểm cần sửa về cách diễn giải Week 2

Week 2 report hiện mô tả một số biến như age/income là “sát thực tế nhân khẩu học”.

Cần cẩn thận:

NYC TLC không có user age/income.

Do đó final documentation nên tách:

### Empirically calibrated
- fare
- hour pattern
- trip-related distributions
- geographic/trip structure

### Reference-calibrated
- user-level usage distribution nếu lấy từ nguồn ride-sharing khác

### Assumption-driven
- age
- income
- rain propensity
- treatment response
- causal ITE coefficients
- some persona proportions

Đây là cách tăng credibility.

---

# 12. Synthetic Data Architecture — thứ tự đúng

Phần Week 2 cần được trình bày theo đúng logic:

```text
STEP 1 — Generate pre-treatment covariates

STEP 2 — Generate baseline potential outcome Y0

STEP 3 — Generate individual treatment effect ITE

STEP 4 — Construct Y1 from Y0 + ITE

STEP 5 — Generate observational treatment assignment
         có confounding

STEP 6 — Generate randomized treatment assignment
         cho RCT/A-B sandbox

STEP 7 — Materialize observed outcomes

STEP 8 — K-Means segmentation
         chạy sau khi causal dataset đã tồn tại
```

Đây là thứ tự đúng cần giữ trong final presentation.

---

# 13. Y0 — Baseline Potential Outcome

Week 2 sử dụng Zero-Inflated Negative Binomial để mô phỏng số chuyến nền.

Điểm này nên được nhấn mạnh vì count outcome thường có:

- nhiều zero,
- overdispersion,
- heavy users.

Cấu trúc:

```text
Zero inflation
+
Negative Binomial count process
→ Y0
```

Ý nghĩa:

> Y0 đại diện số chuyến user sẽ đi nếu **không nhận voucher**.

Đây là counterfactual baseline của causal sandbox.

---

# 14. ITE — Ground Truth Treatment Effect

Week 2 định nghĩa explicit ITE equation dựa trên các business/behavioral assumptions.

Ý nghĩa quan trọng:

> **True ITE không được “học” từ K-Means.**

Nó được cài trước trong SCM.

Do đó K-Means sau này chỉ:

- phân nhóm behavior,
- tạo personas,
- dùng để phân tích heterogeneity ở mức segment.

## 14.1. Đây là điểm mạnh

Vì simulator có known ITE nên có thể:

```text
Predicted CATE
vs
True ITE
```

Điều mà real-world dataset thường không làm được.

## 14.2. Đây cũng là giới hạn

ITE coefficients là **assumption-driven**, không phải GSM causal truth.

Không được nói:

> “Voucher thật sẽ tăng 1.5 chuyến.”

Nên nói:

> “Simulator định nghĩa ground truth để kiểm chứng estimator.”

---

# 15. Y1 — Potential Outcome under Treatment

Logic:

```text
Y1 ≈ Y0 + ITE
```

sau đó có resampling/constraints để giữ outcome hợp lệ.

Ý nghĩa:

> Y1 là số chuyến lý thuyết nếu cùng user nhận treatment.

Ta có:

```text
ITE = Y1 - Y0
```

theo causal setup.

---

# 16. Hai thế giới treatment nên được giữ rõ ràng

## 16.1. Observational Assignment

Treatment phụ thuộc confounders.

Dùng để minh họa:

- selection bias,
- Simpson's paradox,
- naive comparison failure.

## 16.2. Randomized Assignment

Treatment random.

Dùng cho:

- A/A,
- A/B,
- ATE estimation,
- uplift training/evaluation.

Đây là một điểm rất hay của sandbox.

---

# 17. Synthetic Validation phải được nâng thành deliverable riêng

Không chỉ generate xong rồi dùng.

Cần có:

> **Synthetic Data Validation Report**

4 lớp.

## 17.1. Marginal Validation

Real/reference vs synthetic:

- fare
- trip frequency
- hour
- geography
- recency
- zero rate

## 17.2. Dependency Validation

So:

- correlation matrix
- fare vs distance
- duration vs distance
- demand vs hour
- behavior conditional on geography

## 17.3. User-level Validation

- rides/user
- recency
- spend/user
- persona size
- long-tail behavior

## 17.4. Causal Validation

- true ATE
- estimated ATE
- CI coverage
- true ITE vs predicted CATE

---

# 18. Calibration Scorecard đề xuất

Mỗi synthetic variable nên có:

| Variable | Source | Target Statistic | Synthetic Statistic | Gap | Status |
|---|---|---:|---:|---:|---|
| fare | TLC | ... | ... | ... | PASS/REVIEW |
| preferred_hour | TLC | ... | ... | ... | PASS |
| zero rides rate | reference/assumption | ... | ... | ... | REVIEW |
| airport share | TLC/assumption | ... | ... | ... | PASS |
| age | assumption | N/A | ... | N/A | ASSUMPTION |
| income | assumption | N/A | ... | N/A | ASSUMPTION |

Điểm mạnh:

> Người review nhìn ngay được cái gì được calibrated và cái gì chỉ là assumption.

---

# 19. Known-DGP vs Adversarial-DGP

Synthetic v1 hiện có vai trò:

> **Known-DGP correctness test**

Đây không phải điểm yếu.

Câu hỏi:

> Nếu biết truth, pipeline có recover được truth không?

Nhưng nên thêm synthetic v2:

> **Adversarial/Misspecified robustness test**

Các scenario:

- nonlinear ITE
- threshold effect
- negative uplift
- rare persuadables
- hidden modifier
- train/test shift
- persona không trùng HTE
- economics shift

Câu chuyện:

```text
V1 — Can we recover known truth?
V2 — Can we survive a harder world?
```

---

# 20. PILLAR 2 — EXPERIMENTATION & CAUSAL ESTIMATION

Đây là **core internship deliverable theo mentor**.

Uplift là extension.

---

# 21. Segmentation đứng ở đâu?

K-Means chạy sau causal dataset.

Vai trò:

```text
Synthetic user behavior
→ PCA
→ K-Means
→ Personas
```

K-Means không nên được coi là causal model.

Nó trả lời:

> Ai giống ai?

A/B/Uplift trả lời:

> Ai thay đổi vì treatment?

---

# 22. Vai trò đúng của K-Means

Nên dùng cho:

- business understanding,
- marketing persona,
- descriptive reporting,
- heterogeneity slicing,
- baseline targeting.

Không nên dùng làm final targeting engine.

Architecture cuối:

```text
                    ┌→ K-Means → Persona / Explain
User features ──────┤
                    └→ Uplift → CATE → Policy
```

---

# 23. Experiment Design

Mentor scope chính là A/B.

Experiment specification nên có:

- Business question
- Hypothesis
- Population
- Eligibility
- Randomization unit
- Treatment
- Control
- Treatment ratio
- Pre-treatment window
- Exposure window
- Outcome window
- Primary metric
- Guardrails
- MDE
- Power
- Decision rule

---

# 24. A/A Testing

Repo hiện chạy Monte Carlo A/A nhiều vòng để kiểm tra:

- SRM behavior,
- SMD balance,
- false positive rate.

Đây là phần mạnh.

Nhưng wording cần sửa.

Không nói:

> “Randomization công bằng tuyệt đối.”

Nên:

> “Không phát hiện bất thường đáng kể trong các simulated randomization checks đã thực hiện.”

Không nói:

> “Đủ tin cậy cho quyết định vận hành thực tế.”

Nên:

> “Pipeline có statistical behavior phù hợp với expectation trong simulation.”

---

# 25. Experiment Trust Gate

A/A không nên chỉ là notebook.

Nên đóng gói thành:

```text
EXPERIMENT HEALTH GATE

1. SRM
2. Covariate Balance
3. Missing Assignment
4. Exposure Integrity
5. Invariant Metrics
6. A/A Calibration

→ PASS / REVIEW / FAIL
```

Chỉ khi PASS mới phân tích A/B outcome.

---

# 26. SRM

Check:

```text
Observed assignment ratio
vs
Designed assignment ratio
```

SRM failure có thể chỉ ra:

- randomization bug,
- eligibility issue,
- logging loss,
- treatment delivery issue.

---

# 27. Covariate Balance

Nên ưu tiên SMD cho pre-treatment covariates.

Rule phổ biến:

```text
|SMD| < 0.1
```

nhưng nên diễn giải như diagnostic threshold, không phải “chứng minh tuyệt đối”.

---

# 28. A/B Estimation

Primary causal estimand:

```text
ATE
=
E[Y(1) - Y(0)]
```

Trong randomized experiment có thể estimate bằng treatment-control difference hoặc regression adjustment.

Repo hiện sử dụng OLS + HC1 và pre-treatment covariate adjustment.

Cần diễn giải chính xác:

- HC1 giúp robust hơn với heteroskedasticity.
- Covariate adjustment có thể giảm residual variance.
- Nó **không đảm bảo p-value “hoàn toàn chính xác” trong mọi setting**.
- Không nên gọi toàn bộ adjustment là CUPED nếu chưa triển khai đúng CUPED formulation.

---

# 29. Power & MDE

Nên giữ thành module riêng.

Input:

```text
baseline mean
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

Đây là phần rất gần workflow doanh nghiệp.

---

# 30. Statistical vs Business Significance

Có thể:

```text
p < 0.05
```

nhưng campaign vẫn lỗ.

Do đó decision cần 2 tầng:

### Statistical
- ATE
- CI
- p-value

### Business
- Incremental Rides
- Incremental GMV
- Burn
- Economics

---

# 31. HTE

Trước Uplift, nên có segment-level HTE:

```text
ATE by persona
ATE by recency band
ATE by payment behavior
ATE by geography
```

Đây là bridge từ A/B chung sang individualized uplift.

---

# 32. PILLAR 3 — UPLIFT & BUSINESS POLICY

Đây là **strategic extension**, không phải scope mentor bắt buộc ban đầu.

Nhưng nên giữ vì:

1. Sau A/B, ATE chỉ cho biết average response.
2. Promotion targeting cần heterogeneity.
3. Uplift Modeling gần với bài toán Data/AI thực tế.
4. Nó biến project từ “đo campaign” sang “học ai nên nhận campaign”.

---

# 33. Uplift nên được framing như phần mở rộng tự nhiên

Câu nói tốt:

> “Mentor giao core scope đến A/B Testing. Sau khi có randomized causal sandbox và ATE/HTE, project mở rộng sang Uplift Modeling để nghiên cứu bước tiếp theo: từ average treatment effect sang individual-level treatment response.”

Như vậy không làm sai scope.

---

# 34. T-Learner hiện tại

Repo dùng:

- T-Learner
- XGBoost regressors
- train/validation/test
- early stopping
- Qini/AUUC

Đây là baseline hợp lý.

Không cần model zoo lớn.

Nếu mở rộng, chỉ cần:

- S-Learner baseline
- T-Learner
- X-Learner comparator

Quan trọng hơn là policy evaluation.

---

# 35. Không chỉ train trên một segment

Current Uplift report tập trung nhiều vào Urban Cash.

Điều này hợp như case study.

Nhưng final extension nên train/evaluate trên:

```text
All eligible users
```

rồi mới hỏi:

> Policy target ai dưới budget?

---

# 36. Uplift Evaluation

## Ranking
- Qini
- AUUC
- Uplift curve

## Ground-truth accuracy trong synthetic
- CATE RMSE
- CATE MAE
- Correlation with true ITE

## Calibration
- predicted uplift deciles
- observed uplift
- true ITE mean

## Business
- Incremental Rides@TopK
- Incremental GMV@Budget
- Policy Value
- Policy Regret

---

# 37. Oracle Policy

Synthetic data có true ITE.

Do đó có thể tạo:

```text
Oracle EV_i
=
True ITE_i × Value per Incremental Ride_i
− Burn_i
```

Learned policy:

```text
Predicted EV_i
=
Predicted CATE_i × Value per Incremental Ride_i
− Expected Burn_i
```

Policy Regret:

```text
Regret
=
Oracle Policy Value
− Learned Policy Value
```

Đây là một trong những metric mạnh nhất của sandbox.

---

# 38. BUSINESS METRICS — GMV & BURN

> **Cảnh báo quan trọng:** Project hiện chỉ biết qua trao đổi rằng doanh nghiệp có dùng các metric như GMV/Burn. Chưa có tài liệu nội bộ xác nhận công thức chính xác. Vì vậy mọi công thức dưới đây là **business-aligned proposed metrics**, không được gọi là official GSM definitions.

---

# 39. GMV

Dùng trong sandbox như:

> Gross transaction value của trips trong campaign population.

Không đồng nhất:

```text
GMV ≠ Revenue ≠ Profit
```

---

# 40. Incremental GMV

Causal business metric:

```text
Incremental GMV
=
GMV Treatment
− Counterfactual GMV
```

Trong RCT:

```text
Control
```

là estimator cho counterfactual expectation.

---

# 41. Burn

Định nghĩa sandbox:

> Promotion subsidy/incentive cost mà platform chịu.

Không nên mặc định:

```text
Burn = Voucher Face Value
```

Nên parameterize:

```text
voucher_face_value
redemption_rate
expected_burn
```

---

# 42. Burn / GMV

```text
Burn / GMV
```

trả lời:

> Promotion spend chiếm bao nhiêu phần gross transaction value?

Hữu ích như:

- cost intensity,
- guardrail,
- efficiency signal.

Nhưng:

> Burn/GMV thấp chưa chứng minh causal incrementality.

---

# 43. Incremental GMV / Burn

```text
Incremental GMV / Burn
```

trả lời:

> 1 đồng burn tạo bao nhiêu đồng incremental GMV?

Ngược lại:

```text
Burn / Incremental GMV
```

trả lời:

> Cần bao nhiêu burn để tạo 1 đồng incremental GMV?

Đây là causal efficiency metric phù hợp với framing A/B hơn.

---

# 44. Cost per Incremental Ride

```text
CPIR
=
Burn / Incremental Rides
```

Rất dễ dùng trong business review.

---

# 45. Contribution Margin

Fare/GMV không phải profit.

Nếu chưa có business margin thật:

```text
contribution_margin_per_ride
```

phải là configurable assumption.

Không hard-code rồi gọi là GSM economics.

---

# 46. Expected Incremental Profit

```text
EV_i
=
Predicted CATE_i
× Contribution Margin_i
− Expected Burn_i
```

Target nếu:

```text
EV_i > 0
```

Nếu có budget:

```text
maximize Σ target_i × EV_i

subject to

Σ target_i × ExpectedBurn_i ≤ Budget
```

---

# 47. Policy Comparison

Final evaluation nên có:

| Policy | Logic |
|---|---|
| No Voucher | Baseline |
| Mass Voucher | All eligible |
| Segment Targeting | K-Means persona |
| Uplift Targeting | Top predicted CATE |
| Burn-Constrained Uplift | Uplift dưới burn cap |
| Profit Targeting | Top expected incremental profit |
| Budget-Constrained Policy | Max value dưới budget |

---

# 48. KPI cho policy

- Target users
- Target rate
- Total rides
- Incremental rides
- GMV
- Incremental GMV
- Burn
- Burn / GMV
- Burn / Incremental GMV
- CPIR
- Incremental Contribution Margin
- Incremental Profit
- ROI
- Policy Value
- Regret vs Oracle

---

# 49. Stress Test — hiện tại và cần mở rộng

Repo hiện đã có:

- sample size
- null effect
- 90/10 treatment split
- Gaussian noise

Đây là baseline tốt.

Nhưng final robustness framework nên có 5 nhóm.

## Statistical
- sample size
- assignment ratio
- null effect
- noise

## DGP
- nonlinear ITE
- negative uplift
- rare responders
- hidden modifier

## Data
- missingness
- feature shift
- segment drift

## Experiment Integrity
- SRM
- exposure mismatch
- logging loss
- contamination

## Economics
- burn tăng
- margin giảm
- redemption thay đổi
- budget thay đổi

---

# 50. Policy Robustness

Không chỉ hỏi:

> Model score còn tốt không?

Mà hỏi:

> Recommendation có đổi không?

Ví dụ:

```text
Low burn
→ Uplift targeting

Medium burn
→ Profit targeting

High burn
→ Very selective

Extreme burn
→ No promotion
```

---

# 51. Engineering — từ notebooks thành reusable pipeline

Final structure đề xuất:

```text
src/
├── data_quality.py
├── empirical_calibration.py
├── synthetic_generator.py
├── synthetic_validation.py
├── segmentation.py
├── experiment_design.py
├── experiment_health.py
├── ab_analysis.py
├── uplift_model.py
├── uplift_evaluation.py
├── economics.py
├── policy_evaluation.py
├── stress_test.py
└── dashboard/
```

---

# 52. Config-driven design

```text
config/
├── calibration.yaml
├── synthetic_dgp.yaml
├── experiment.yaml
└── economics.yaml
```

Ví dụ:

```yaml
experiment:
  treatment_ratio: 0.5
  alpha: 0.05
  power: 0.8
  outcome_window_days: 14

economics:
  voucher_face_value: 20000
  redemption_rate: 0.7
  contribution_margin_per_ride: 25000
  campaign_budget: 500000000
```

---

# 53. Data Contract

```text
user_id
experiment_id

# Pre-treatment
age
income
recency
historical_rides
historical_spend
location_features
payment_features

# Causal ground truth — synthetic only
y0
true_ite
y1

# Experiment
treatment
exposure
outcome_rides
outcome_gmv

# Descriptive
segment_id
persona
```

---

# 54. Feature cutoff

```text
Historical Window
[-90d, 0)
        ↓
Treatment Assignment
t=0
        ↓
Outcome Window
[0, +14d]
```

Không dùng post-treatment feature làm uplift input.

---

# 55. Product cuối — Promotion Experimentation & Policy Simulator

Không cần production-grade.

Định vị:

> **Interactive Simulation & Decision-Support Prototype**

Các tab:

## Tab 1 — Data Foundation
- real vs synthetic distributions
- calibration scorecard
- assumption registry

## Tab 2 — Experiment Setup
- population
- treatment ratio
- MDE
- power
- window

## Tab 3 — Experiment Health
- SRM
- SMD
- A/A
- exposure

## Tab 4 — A/B Result
- ATE rides
- ATE GMV
- CI
- p-value

## Tab 5 — Heterogeneity
- persona ATE
- CATE
- uplift deciles

## Tab 6 — Business Metrics
- GMV
- incremental GMV
- burn
- burn/GMV
- burn/incremental GMV
- CPIR

## Tab 7 — Policy Simulator
- Mass
- Segment
- Uplift
- Profit
- Budget-constrained

---

# 56. Hai lớp bằng chứng

Final report phải tách:

| Validated in Simulation | Requires Real Business Data |
|---|---|
| Data generator logic | True customer behavior |
| A/A calibration | Production randomization integrity |
| Recover synthetic ATE | Actual GSM ATE |
| CATE vs true ITE | Actual GSM CATE |
| Burn sensitivity | Actual GSM burn formula |
| Policy comparison | Production policy value |
| Simulated robustness | Real-world drift |

---

# 57. Các wording cần sửa trong repo

Một số report hiện dùng từ quá mạnh:

- “công bằng tuyệt đối”
- “chuẩn xác tuyệt đối”
- “độ tin cậy tuyệt đối”
- “sẵn sàng deploy diện rộng”
- “lợi thế cạnh tranh tuyệt đối”

Nên đổi thành:

- “consistent with expected randomization behavior”
- “no material issue detected in tested simulations”
- “robust within evaluated scenarios”
- “validated in simulation”
- “requires real-world randomized validation”

Đây không làm project yếu đi.

Nó làm project đáng tin hơn.

---

# 58. README nên framing lại

README hiện đặt mục tiêu rất mạnh về tối ưu ROI và tránh cannibalization.

Final README nên mở bằng:

> **A simulation-based experimentation sandbox for ride-hailing promotions, combining real mobility patterns with synthetic causal outcomes to validate A/B testing, uplift modeling, and policy evaluation under controlled assumptions.**

Data source nên chia:

### Official/Public Mobility Data
NYC TLC

### User-level Reference Data
nếu có nguồn public khác

### Synthetic Causal Data
Y0 / ITE / Y1 / treatment

---

# 59. Storyline thuyết trình cuối

Nếu khoảng 12–14 slide:

## Slide 1 — Business Context
Promotion, cannibalization, burn.

## Slide 2 — Data Challenge
Trip-level public data ≠ user-level causal data.

## Slide 3 — Data Quality & EDA
Những vấn đề thực tế đã xử lý.

## Slide 4 — EDA → Simulation Mapping
Empirical pattern nào đi vào generator.

## Slide 5 — Causal Synthetic Data
Covariates → Y0 → ITE → Y1.

## Slide 6 — Synthetic Validation
Real/reference vs synthetic + assumptions.

## Slide 7 — Segmentation
K-Means persona as descriptive layer.

## Slide 8 — Experiment Design
Randomization + power + metrics.

## Slide 9 — A/A & Trust Gate
SRM + balance + FPR.

## Slide 10 — A/B Results
ATE + CI + HTE.

## Slide 11 — Uplift Extension
T-Learner + CATE + Qini/AUUC.

## Slide 12 — Business Metrics
Incremental rides/GMV + Burn.

## Slide 13 — Policy Comparison & Stress Test
Mass vs Segment vs Uplift vs Profit.

## Slide 14 — Transferability
Synthetic sandbox → real randomized data.

---

# 60. Nếu PM hỏi “phần khó nhất là gì?”

Câu trả lời nên là:

> **“Phần khó nhất không phải fitting model mà là xây được một experimental world đủ hợp lý. Dữ liệu public ban đầu là trip-level, trong khi A/B và uplift cần user-level pre-treatment features, treatment assignment, outcome và counterfactual. Vì vậy em phải đi từ data quality/EDA để hiểu empirical patterns, thiết kế synthetic user population, xây Y0/ITE/Y1 để có causal ground truth, rồi mới có thể kiểm chứng A/B và uplift.”**

Đây là điểm nên nhấn mạnh.

---

# 61. Nếu hỏi “tại sao phải K-Means nếu có Uplift?”

Trả lời:

> K-Means và Uplift giải hai bài toán khác nhau. K-Means tạo behavioral personas để Business/Marketing hiểu và vận hành theo nhóm. Uplift ước lượng treatment response ở cấp cá nhân. Vì vậy K-Means là descriptive/explainability layer, còn Uplift là targeting extension.

---

# 62. Nếu hỏi “tại sao Uplift ngoài scope mentor mà vẫn làm?”

Trả lời:

> Core scope của mentor dừng ở A/B Testing. Sau khi đã có randomized causal sandbox và ATE/HTE, em mở rộng Uplift Modeling để nghiên cứu bước tiếp theo của cùng pipeline: từ average treatment effect sang individual treatment response. Hướng này cũng gần với bài toán Data/AI thực tế mà em được tìm hiểu trong doanh nghiệp.

---

# 63. Nếu hỏi “synthetic data có đại diện GSM không?”

Trả lời:

> Không. Synthetic data là controlled causal environment. Một phần distribution được calibrated từ public/reference data, còn demographics và treatment-effect mechanism có assumption-driven components. Mục đích chính là validate methodology, không phải estimate GSM production effect.

---

# 64. Nếu hỏi “GMV/Burn có phải công thức GSM không?”

Trả lời:

> Em chỉ được biết qua trao đổi rằng các metric như GMV/Burn được sử dụng trong project thực tế. Project hiện dùng business-aligned definitions để mô phỏng economics. Exact internal definitions cần được xác nhận với Business/Marketing trước khi áp dụng thật.

---

# 65. Ưu tiên cải thiện cuối

## Priority 1 — Làm nổi bật Data Foundation
- EDA → simulation mapping
- calibration scorecard
- assumption registry
- synthetic validation report

## Priority 2 — Correct causal order
- Y0/ITE/Y1 trước K-Means
- observational vs randomized assignment rõ ràng

## Priority 3 — Experiment Trust Gate
- A/A
- SRM
- SMD
- exposure integrity

## Priority 4 — Uplift extension
- all eligible users
- true ITE benchmark
- calibration
- oracle regret

## Priority 5 — Business layer
- incremental GMV
- burn
- CPIR
- configurable margin
- policy comparison

## Priority 6 — Robustness
- adversarial DGP
- economics shift
- policy robustness

## Priority 7 — Productization
- reusable modules
- configs
- decision-support dashboard

---

# 66. Những thứ không nên mở rộng nữa

- Driver Agent
- Taxi GPS data
- Marketplace ABM
- MARL
- Surge pricing
- Matching simulator
- Real-time driver supply
- Model zoo lớn
- Production deployment

Đây là scope khác và làm loãng câu chuyện chính.

---

# 67. Acceptance Criteria cuối

## Pillar 1 — Data & Simulation

- [ ] Raw data quality report rõ
- [ ] EDA không chỉ visualization mà có calibration outputs
- [ ] EDA → simulation mapping
- [ ] Source/assumption registry
- [ ] Y0/ITE/Y1 documented
- [ ] Synthetic marginal validation
- [ ] Synthetic dependency validation
- [ ] User-level validation
- [ ] Known-DGP benchmark
- [ ] At least one adversarial DGP scenario

## Pillar 2 — Experimentation

- [ ] Experiment specification
- [ ] Power/MDE
- [ ] A/A repeated simulation
- [ ] SRM
- [ ] Covariate balance
- [ ] A/B ATE + CI
- [ ] Segment HTE
- [ ] Experiment health PASS/REVIEW/FAIL

## Pillar 3 — Uplift & Policy

- [ ] T-Learner baseline
- [ ] Out-of-sample Qini/AUUC
- [ ] CATE vs true ITE
- [ ] Uplift calibration
- [ ] Mass vs Segment vs Uplift vs Profit policy
- [ ] Oracle policy
- [ ] Policy regret
- [ ] GMV/Burn assumptions configurable

## Communication

- [ ] Simulation vs production boundary rõ
- [ ] Không overclaim
- [ ] Business wording rõ
- [ ] Final architecture rõ
- [ ] Transferability được giải thích

---

# 68. Final Project Positioning

## Tên tiếng Anh

> **Simulation-Based Promotion Experimentation: From Real-Data-Calibrated Causal Simulation to A/B Testing and Uplift-Based Policy Evaluation**

## Tên ngắn hơn

> **Ride-Hailing Promotion Experimentation & Uplift Sandbox**

## Tên tiếng Việt

> **Xây dựng hệ thống mô phỏng dữ liệu nhân quả, A/B Testing và Uplift Modeling cho bài toán đánh giá và phân bổ khuyến mãi trong dịch vụ gọi xe**

---

# 69. Final Objective

> **Xây dựng một experimentation-driven promotion sandbox bắt đầu từ Data Quality & EDA trên dữ liệu mobility công khai, chuyển empirical patterns thành synthetic user-level causal data có Y0/Y1/ITE ground truth, sử dụng A/B Testing để kiểm chứng incremental treatment effect, và mở rộng sang Uplift Modeling cùng business metrics để đánh giá các promotion targeting policies dưới controlled assumptions.**

---

# 70. Một câu chốt toàn bộ project

> **Data → Causal Evidence → Decision.**
>
> Project không bắt đầu ở A/B Test. Nó bắt đầu từ việc hiểu và kiểm soát data, xây được một causal experimental world đủ hợp lý, rồi mới đo treatment effect, học heterogeneous response và chuyển kết quả đó thành business policy evaluation.

---

# 71. Final Message dành cho doanh nghiệp

> **Project thực tập không chứng minh một promotion policy thật của GSM nên được triển khai như thế nào. Project chứng minh khả năng đi end-to-end từ Data Quality, EDA, empirical calibration, causal simulation, randomized experimentation, A/B estimation, Uplift Modeling đến business policy evaluation. Synthetic data không thay thế production data; nó là laboratory có known ground truth để kiểm chứng methodology. Khi có randomized business data phù hợp, synthetic generator có thể được thay bằng dữ liệu thật trong khi các layer experiment health, A/B estimation, uplift evaluation và policy comparison vẫn giữ nguyên logic cốt lõi.**

---

# 72. Source Map — các tài liệu repo dùng để chốt master document

Repo:
- https://github.com/thaibuivan/GSM-promotion-experimentation

Week 1:
- `docs/Week1_Data_Quality_Report.md`
- `docs/Week1_Data_Preprocessing_Report.md`
- `docs/Week1_Causal_Thinking_101.md`

Week 2:
- `notebooks/week2_synthetic_data/`
- `docs/Week2_Synthetic_Data_Comprehensive_Report.md`

Week 3:
- `docs/Week3_Comprehensive_Report.md`

Week 4:
- `docs/Week4_AA_AB_Testing_Report.md`

Week 5:
- `docs/Week5_Uplift_Modeling_Report.md`

Week 6:
- `docs/Week6_Stress_Test_Report.md`

README:
- `README.md`

> Tài liệu này là **MASTER FINAL DOCUMENT** và nên thay thế các file roadmap/góp ý trước đó.
