# GSM Promotion Experimentation — Repo Audit & Final Improvement Checklist

> **Mục tiêu tài liệu:** Tổng hợp chi tiết trạng thái repo mới nhất sau khi đối chiếu với `GSM_Promotion_Experimentation_MASTER_FINAL.md`, chỉ rõ phần nào đã được cập nhật tốt, phần nào còn thiếu, phần nào đang mâu thuẫn giữa code/documentation/dashboard, và thứ tự ưu tiên cần xử lý trước final review.
>
> **Repo được audit:** `https://github.com/thaibuivan/GSM-promotion-experimentation`
>
> **Kết luận tổng quát:** Repo đã cập nhật rất nhiều theo hướng đã chốt trong MASTER FINAL, đặc biệt ở ba mảng:
>
> 1. Data Foundation & Causal Simulation đã được đưa lên đúng vị trí quan trọng.
> 2. Uplift đã được nối sang Policy Evaluation và economics.
> 3. Dashboard đã tiến gần mô hình Experimentation & Policy Simulator.
>
> Tuy nhiên repo vẫn chưa nên coi là “final-ready”. Vấn đề lớn nhất hiện không phải thiếu model mới, mà là **documentation coherence, một số statistical/business wording quá mạnh, economics chưa thống nhất hoàn toàn, stress test chưa đủ sâu, và repo reproducibility chưa sạch.**

---

# 1. Đánh giá tổng thể theo MASTER FINAL

Ước lượng hiện trạng:

```text
Pillar 1 — Data Foundation & Simulation
████████▌░  ~85%

Pillar 2 — Experimentation
████████░░  ~80%

Pillar 3 — Uplift & Policy
████████▌░  ~85%

Documentation coherence
██████░░░░  ~60%

Stress-test depth
█████░░░░░  ~50%

Repo reproducibility / hygiene
██████░░░░  ~60%
```

Các tỷ lệ trên là **audit estimate mang tính định hướng**, không phải benchmark khách quan.

Điểm quan trọng:

> Project đã có đủ technical breadth. Việc cần làm tiếp theo không phải “thêm thuật toán”, mà là **hardening, cleanup, consistency và evidence discipline**.

---

# 2. Đánh giá theo từng mục đã từng góp ý

| Hạng mục | Trạng thái | Nhận xét |
|---|---|---|
| Simulation-based framing | ✅ | Đã đúng hướng |
| Data Foundation được nhấn mạnh | ✅ | Rất tốt |
| EDA → Simulation Mapping | ✅ | Đã có |
| Calibration Scorecard | ✅ | Có nhưng cần rà số liệu |
| Empirical vs Assumption separation | ✅ | Đã rõ hơn |
| Y0 → ITE → Y1 trước K-Means | ✅ | Đúng trong pipeline |
| Data Contract | ✅ | Tốt |
| Feature cutoff / leakage prevention | ✅ | Tốt |
| A/A + SRM + SMD | ✅ | Tốt, wording cần sửa |
| Experiment Health Gate | ✅ | Đã có trên dashboard |
| Power/MDE | ✅ | Đã có |
| Uplift toàn population | ✅ | Có trong policy layer |
| Multiple policies | ✅ | Rất tốt |
| GMV / Burn / CPIR | ✅ | Đã productize |
| Oracle Policy / Regret | ✅ | Rất tốt |
| Uplift calibration | ✅ | Đã có |
| Policy Simulator | ✅ | Đúng hướng |
| Adversarial DGP | ❌ | Chưa đủ |
| Economics shift stress test | ❌ | Chưa đủ |
| Documentation consistency | ⚠️ | Lỗi lớn |
| Production/sandbox boundary | ⚠️ | Một số file còn overclaim |
| Reproducibility | ⚠️ | Còn hard-coded path / repo hygiene |

---

# 3. PILLAR 1 — Data Foundation & Causal Simulation

## 3.1. Điểm cải thiện rõ nhất

Repo hiện đã thể hiện tốt hơn rằng:

```text
EDA
→ Empirical calibration
→ Simulation assumptions
→ Synthetic data
→ Causal ground truth
```

thay vì:

```text
EDA
→ vài biểu đồ
→ generate synthetic tùy ý
```

Đây là thay đổi rất quan trọng về mặt story.

## 3.2. EDA → Simulation Mapping

`EDA_Simulation_Mapping.md` đã làm đúng vai trò:

- fare skew → distribution phù hợp,
- temporal demand → weighted preferred hour,
- airport behavior → airport indicator/multiplier,
- fare-distance-time dependency → không generate độc lập hoàn toàn,
- age/income → assumption,
- treatment effect → causal assumption.

Giá trị lớn nhất của artifact này:

> Nó cho người review thấy cái gì đến từ real/public data, cái gì là simulation assumption.

## 3.3. Calibration Scorecard

Đây là đúng hướng nhưng cần kiểm tra consistency.

Một số điểm cần rà:

### Fare target inconsistency

Nếu Week 2 / EDA report ghi:

```text
Avg Fare ≈ 17.60
Median ≈ 13.50
```

mà Scorecard lại dùng target:

```text
mean ≈ 20
```

thì phải giải thích rõ:

- có dùng subset khác?
- có transform?
- có dùng cleaned subset khác?
- hay số target bị lệch?

Nếu không có lý do rõ, cần sửa Scorecard về đúng statistic từ final clean dataset.

### Zero-rides rate

Nếu ghi:

```text
industry reference ≈ 30%
```

nhưng không có nguồn chắc chắn, nên đổi wording thành:

```text
chosen simulation target ≈ 30%
```

hoặc:

```text
assumption-driven target
```

---

# 4. Week 2 — Synthetic Causal Data

Đây là một trong những phần mạnh nhất của project và nên được giữ ở vị trí nổi bật.

## 4.1. Thứ tự causal đúng

Pipeline đúng:

```text
Synthetic covariates
        ↓
Y0
        ↓
ITE / expected CATE
        ↓
Y1
        ↓
Treatment assignment
        ↓
Observed outcome
        ↓
K-Means / Experiment / Uplift
```

Điểm rất quan trọng:

> K-Means không tạo treatment effect.

Treatment effect đã được định nghĩa trong causal DGP trước segmentation.

## 4.2. Distinction cần làm rõ trong docs

Code hiện có phân biệt:

```text
cate_true
=
expected treatment effect conditional on X

ite_realized
=
Y1 - Y0 after stochastic realization
```

Đây là distinction rất tốt, nhưng documentation cần nói rõ.

Không nên gọi mọi thứ là “true ITE”.

Nên dùng:

```text
Structural / Expected CATE
vs
Realized Individual Difference
```

Điều này giúp giải thích vì sao:

```text
Y1 - Y0
```

có thể có stochastic noise dù expected effect đã được xác định.

## 4.3. Wording cần sửa

Nếu report đang nói:

> age/income distributions “sát thực tế nhân khẩu học”

thì phải cẩn thận.

NYC TLC không có age/income.

Nên sửa thành:

> Age và income được generate theo distributional assumptions để tạo population heterogeneity; chúng không được calibrated trực tiếp từ NYC TLC.

---

# 5. Synthetic Validation cần trở thành deliverable hoàn chỉnh

Repo đã có calibration layer, nhưng final form nên gồm đủ 4 nhóm.

## 5.1. Marginal validation

So:

```text
Real / Reference
vs
Synthetic
```

cho:

- fare
- hour
- trip count
- airport share
- zero rate
- recency
- spend

## 5.2. Dependency validation

Không chỉ so từng biến.

Nên kiểm:

- fare vs distance
- duration vs distance
- hour vs demand
- geo vs fare
- covariance / correlation structure

## 5.3. User-level validation

- rides/user
- spend/user
- recency
- segment size
- activity long tail

## 5.4. Causal validation

- true ATE
- estimated ATE
- CI coverage
- true CATE vs predicted CATE
- Oracle Policy vs Learned Policy

---

# 6. Known-DGP vs Adversarial-DGP

Current generator phù hợp cho:

> **Known-DGP correctness test**

Câu hỏi:

> Pipeline có recover được truth khi truth được biết rõ không?

Điều này là điểm mạnh, không phải lỗi.

Nhưng MASTER FINAL đã yêu cầu thêm:

> **Adversarial / Misspecified DGP**

Hiện chưa thấy đủ.

Nên thêm ít nhất:

```text
1. Nonlinear HTE
2. Negative uplift
3. Rare persuadables
4. Hidden effect modifier
5. Train/test shift
6. Segment composition shift
```

Nếu thời gian ít, ưu tiên:

```text
Treatment-effect shift
Population shift
Economics shift
```

---

# 7. PILLAR 2 — Experimentation

## 7.1. Đây là core mentor scope

A/B Testing vẫn phải được trình bày là core deliverable.

Uplift là extension.

Story đúng:

```text
Core:
Randomized Experiment
→ A/A
→ SRM / Balance
→ A/B
→ ATE / HTE

Extension:
Uplift
→ Individual CATE
→ Policy
```

---

# 8. Experiment Specification đang quá production-like

Đây là một file cần sửa sớm.

Nếu file hiện có các chi tiết kiểu:

```text
Target Launch: Q4 2026
Voucher 15%, max 50,000 VND
10% Holdout
45% K-Means
45% AI
blacklist
rollout 100%
```

mà các parameter này không được mentor/business chính thức cung cấp, thì nó dễ tạo hiểu nhầm:

> Project đang thiết kế experiment production thật.

Nên đổi tiêu đề thành:

> **Illustrative Experiment Specification — Hypothetical Business Translation**

và thêm disclaimer:

> All campaign parameters below are illustrative assumptions for methodology demonstration unless explicitly confirmed by Business/Marketing.

## 8.1. Champion vs Challenger naming

Thông thường:

```text
Champion
=
current/existing policy

Challenger
=
new policy
```

Nếu currently đang gọi AI là Champion và K-Means là Challenger, nên kiểm tra lại logic naming.

---

# 9. A/A Testing và Experiment Health

Repo đã làm tốt:

- Monte Carlo A/A
- SRM
- SMD
- false positive behavior
- dashboard health tab

Đây là phần mạnh.

## 9.1. Nhưng wording còn quá mạnh

Các câu nên loại:

- công bằng tuyệt đối
- cân bằng hoàn hảo
- kiểm soát hoàn hảo
- miễn nhiễm với nhiễu
- p-value hoàn toàn chính xác
- sẵn sàng deploy

Nên đổi thành:

- no material mismatch detected
- balance consistent with randomization expectation
- no major issue found in tested simulation settings
- robust within evaluated scenarios
- requires real-world validation

## 9.2. Type-I Error typo

Nếu report hiện ghi:

```text
Type I Error = 0.502
```

trong khi diễn giải là khoảng 5%, thì phải sửa thành một trong:

```text
0.0502
```

hoặc:

```text
5.02%
```

Đây là lỗi nhỏ nhưng rất dễ bị bắt.

---

# 10. Dashboard Experiment Health có một bug thiết kế tiềm năng

Experiment Setup cho phép treatment ratio thay đổi.

Nhưng Health tab đang kiểm:

```text
expected = total/2, total/2
```

tức hard-code 50/50.

Nếu user set 30/70 nhưng Health vẫn kiểm 50/50:

> dashboard sẽ báo SRM sai.

Cần truyền:

```text
expected treatment ratio
```

từ:

- config
- experiment spec
- session state

sang SRM check.

---

# 11. A/B Estimation

Current setup dùng:

- randomized treatment
- OLS
- HC1 robust SE
- pre-treatment covariate adjustment

Đây là baseline tốt.

Nhưng documentation cần tránh các claim như:

> HC1 đảm bảo p-value hoàn toàn chính xác.

Nên nói:

> HC1 cung cấp heteroskedasticity-robust standard error estimates dưới fitted model.

Nếu có pre-treatment covariate adjustment:

> có thể giúp giảm residual variance và tăng precision.

Không nên gọi toàn bộ setup là CUPED nếu chưa triển khai đúng CUPED formulation.

---

# 12. Power / MDE

Repo đã có calculator — đây là điểm tốt.

Nên giữ các input:

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

Nếu dashboard cho đổi ratio thì toàn bộ health/design phải dùng ratio đó một cách nhất quán.

---

# 13. PILLAR 3 — Uplift & Policy

Đây là phần đã tiến rất xa.

## 13.1. Điểm mạnh

Repo đã có:

- CATE
- Qini / AUUC
- policy comparison
- GMV/Burn economics
- Oracle Policy
- Policy Regret
- Uplift calibration
- Policy Simulator

Đây đúng là strategic extension phù hợp với hướng Data/AI.

---

# 14. Lỗi coherence lớn nhất: model story không thống nhất

Hiện documentation/code/dashboard có thể đang nói các model khác nhau:

```text
README:
S-Learner / T-Learner / X-Learner

Week 5 report:
T-Learner

Decision Memo:
X-Learner

Policy engine / dashboard:
R-Learner-style residual model
```

Đây là một trong những điểm cần chốt gấp nhất.

Mentor hỏi:

> “Cuối cùng model nào là model chính?”

repo phải trả lời đúng **một câu**.

## 14.1. Cách sửa

Tạo bảng benchmark:

| Model | Qini | AUUC | CATE RMSE | Policy Value | Runtime |
|---|---:|---:|---:|---:|---:|
| S-Learner | | | | | |
| T-Learner | | | | | |
| X-Learner | | | | | |
| R-Learner-style | | | | | |

Sau đó chốt:

```text
Champion model = ...
```

và sửa đồng bộ:

- README
- Week 5 Report
- Decision Memo
- Dashboard
- pipeline comments

Không nên tự chọn model chỉ vì code cuối dùng model đó; phải dựa vào benchmark thực tế.

---

# 15. Uplift nên train toàn eligible population

Nếu Week 5 cũ vẫn tập trung quá nhiều vào `Urban Cash`, thì giữ Urban Cash như:

> case study / interpretability example

nhưng final targeting engine nên dùng:

```text
All Eligible Users
```

rồi policy mới quyết định ai được chọn.

---

# 16. Uplift Calibration

Repo đã có decile-style comparison:

```text
Predicted CATE
Observed Uplift
True ITE / CATE
```

Đây là một điểm tốt.

Cần đảm bảo report phân biệt:

```text
ranking performance
```

và:

```text
calibration performance
```

AUUC/Qini tốt chưa chứng minh scale của CATE đúng.

---

# 17. Oracle Policy & Policy Regret

Đây là lợi thế rất mạnh của synthetic sandbox.

Logic:

```text
Oracle EV_i
=
True CATE_i × Value_i
− Burn_i
```

Learned policy:

```text
Predicted EV_i
=
Predicted CATE_i × Value_i
− Expected Burn_i
```

Regret:

```text
Oracle Policy Value
− Learned Policy Value
```

Nên làm metric này nổi bật trong final report.

---

# 18. Policy Evaluation đang dùng synthetic ground truth — cần ghi nhãn rõ

Nếu policy engine:

1. dùng model để chọn user,
2. nhưng evaluate selected users bằng `true_ite` / oracle ground truth,

thì đây là cách đánh giá rất hay trong synthetic sandbox.

Nhưng không nên gọi output đơn giản là:

```text
Expected Incremental Profit
```

vì dễ gây hiểu nhầm.

Nên tách:

```text
Predicted Policy Value
```

và:

```text
Ground-Truth Policy Value
(Synthetic Only)
```

sau đó thêm:

```text
Policy Value Error
```

Điều này giúp tận dụng synthetic ground truth tốt hơn.

---

# 19. Business Metrics — GMV/Burn

Code/dashboard hiện đã tiến đúng hướng.

Các metric nên giữ:

```text
GMV
Incremental GMV
Burn
Burn / GMV
Burn / Incremental GMV
Incremental GMV / Burn
Incremental Rides
CPIR
Incremental Contribution Margin
Incremental Profit
ROI
```

---

# 20. Nhưng metric specification chưa theo kịp code

`metric_specification.md` cần đồng bộ với dashboard/policy engine.

Nên định nghĩa rõ:

## GMV
Gross transaction value trong sandbox.

## Incremental GMV
Causal difference relative to counterfactual/control.

## Burn
Promotion subsidy assumption.

## Burn / GMV
Promotion spend intensity.

## Burn / Incremental GMV
Causal cost efficiency.

## CPIR
Burn / Incremental Rides.

## Incremental Profit
Contribution margin from incremental behavior minus burn.

---

# 21. Không suy diễn nguyên nhân từ extreme user

Nếu metric spec có câu kiểu:

> top 0.1% >50 trips → nghi tài xế tự book

thì không có evidence đủ để kết luận.

Nên đổi:

> Flag as extreme high-frequency behavior for separate review.

Không tự gán nguyên nhân.

---

# 22. Currency và Outcome Horizon đang chưa thống nhất

Repo có dấu hiệu trộn:

```text
USD
VND
14-day outcome
30-day revenue
```

Final project cần thống nhất rõ.

Nên tách:

## Sandbox economics

```text
currency = USD / abstract unit
horizon = fixed experiment window
```

## Hypothetical GSM translation

```text
currency = VND
parameters = illustrative only
```

Hoặc dùng currency-agnostic `monetary units` trong core methodology.

Quan trọng nhất:

> cùng một metric không được khi thì 14 ngày, khi thì 30 ngày mà không ghi rõ.

---

# 23. Stress Test là phần còn thiếu nhiều nhất

Current Week 6 chủ yếu có:

```text
Sample size
Null effect
90/10 treatment
Gaussian noise
```

Đây là baseline tốt nhưng chưa đủ theo MASTER FINAL.

Cần thêm:

## DGP Shift

- nonlinear HTE
- sign flip
- negative uplift
- rare responders
- hidden modifier

## Economics Shift

- burn tăng
- margin giảm
- redemption thay đổi
- budget thay đổi

## Population Shift

- covariate shift
- persona share shift
- recency/activity shift

## Experiment Failure

- SRM
- exposure mismatch
- logging loss
- contamination

---

# 24. Stress Test nên đánh giá Policy Stability

Không chỉ hỏi:

> ATE có còn đúng không?

Mà hỏi:

> Policy recommendation có đổi không?

Ví dụ:

```text
Low burn
→ Uplift policy

Medium burn
→ Profit targeting

High burn
→ Highly selective targeting

Extreme burn
→ No promotion
```

Đây là business robustness.

---

# 25. Legacy Observational Studies Report nên archive hoặc rewrite

Nếu file cũ:

- dùng 4 persona trong khi repo hiện có 5,
- nói “system reliable” quá mạnh,
- có wording “rollout ngay”,
- có các kết luận production-like,

thì nó đang phá narrative của repo mới.

Hai lựa chọn:

## Option A — Archive

```text
docs/archive/legacy/
```

## Option B — Rewrite

Đổi thành:

> **Future Work — Observational Causal Methods When Randomization Is Not Available**

và chỉ trình bày:

- Matching
- Regression Adjustment
- DiD
- RD
- IV

ở mức concept/future direction.

---

# 26. Repo Hygiene

Root hiện không nên giữ quá nhiều guide cũ.

Nên chỉ giữ:

```text
README.md
GSM_Promotion_Experimentation_MASTER_FINAL.md
```

Các file góp ý/roadmap cũ:

```text
archive/
```

hoặc xóa.

Nếu `venv/` đang tracked:

> bỏ khỏi Git.

Thêm vào `.gitignore`:

```text
venv/
.venv/
__pycache__/
.ipynb_checkpoints/
*.pyc
```

---

# 27. Hard-coded Windows Path là P0 bug

Nếu pipeline có:

```python
base_path = r"D:\Intern VSF\GSM-promotion-experimentation"
```

thì mentor clone repo sang máy khác sẽ fail.

Phải dùng project-relative path.

Ví dụ:

```python
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
DATA_DIR = PROJECT_ROOT / "data"
```

hoặc config/env variable.

Đây là lỗi cần sửa trước final review.

---

# 28. Production/Sandbox Boundary cần đồng bộ toàn repo

README đã tốt hơn.

Nhưng các file khác vẫn có thể overclaim.

Nên search toàn repo các từ:

```text
deploy
production
rollout
launch
GSM customer
actual
real ROI
sẵn sàng
hoàn hảo
tuyệt đối
miễn nhiễm
```

Sau đó phân loại.

## Wording nên dùng

- validated in simulation
- under controlled assumptions
- illustrative
- synthetic ground truth
- requires real randomized data
- methodology demonstration
- policy evaluation sandbox

---

# 29. Experiment Specification nên là “Hypothetical Business Translation”

Nếu muốn giữ file này để demonstrate production thinking:

> Giữ.

Nhưng đổi wording.

Cấu trúc:

```text
SECTION A
Validated in Sandbox

SECTION B
Illustrative Translation to Real Business Setting
```

Mọi số:

- voucher value
- target ratio
- launch timing
- blacklist
- holdout %

nếu không được xác nhận phải gắn:

```text
illustrative assumption
```

---

# 30. Final Dashboard Architecture — hiện đúng hướng

Các tab hợp lý:

```text
1. Data Foundation
2. Experiment Setup
3. Experiment Health
4. A/B Result
5. Heterogeneity
6. Business Metrics
7. Policy Simulator
8. Admin Pipeline
```

Nên giữ.

Nhưng cần bổ sung 3 chi tiết:

### A. Data Foundation

Thêm:

- Real vs Synthetic plots
- Calibration Scorecard
- Assumption Registry

### B. Policy Simulator

Tách:

```text
Predicted Policy Value
vs
Synthetic Ground-Truth Policy Value
```

### C. Experiment Health

SRM ratio phải lấy từ experiment config.

---

# 31. Thứ tự ưu tiên sửa repo

## P0 — phải sửa trước mentor review

### 1. Chốt model story

Benchmark:

- S
- T
- X
- R

và chọn Champion.

Sau đó đồng bộ toàn repo.

### 2. Fix overclaim wording

Đặc biệt:

- Week 2
- Week 4
- Week 6
- Dashboard

### 3. Fix Experiment Specification

Đổi sang illustrative/hypothetical.

### 4. Fix hard-coded path

Đảm bảo clone repo chạy được.

### 5. Archive legacy docs

Đặc biệt Observational Studies Report nếu mâu thuẫn.

---

# 32. P1 — nên hoàn thiện trước final presentation

### 6. Đồng bộ Metric Specification

Thêm:

- GMV
- Burn
- CPIR
- Incremental GMV
- Burn / Incremental GMV

### 7. Thống nhất unit/horizon

- USD vs VND
- 14d vs 30d

### 8. Ground-truth vs predicted policy value

Tách hai metric.

### 9. Synthetic validation report

Hoàn thiện calibration.

### 10. Experiment Health Gate

Dùng dynamic treatment ratio.

---

# 33. P2 — nâng chất lượng project

### 11. Adversarial DGP

Ít nhất:

- nonlinear effect
- negative uplift
- population shift

### 12. Economics stress test

- burn
- margin
- budget

### 13. Policy stability

Theo dõi policy switch dưới assumptions khác nhau.

### 14. Champion–Challenger simulation

Current/segment policy vs uplift/profit policy.

---

# 34. Những gì không nên làm lúc này

Không nên mở rộng:

- Driver Agent
- MARL
- Marketplace Simulation
- New GPS dataset
- Matching
- Surge Pricing
- Large model zoo
- Production API phức tạp

Lý do:

> Không giải quyết bottleneck hiện tại.

Bottleneck hiện tại là:

```text
Consistency
+
Evidence
+
Robustness
+
Reproducibility
```

---

# 35. Định vị hiện tại của project

Bản chất repo hiện tại đã tiến từ:

```text
EDA
+
A/B Test
+
Uplift
```

sang:

```text
DATA FOUNDATION
→ CAUSAL SIMULATION
→ EXPERIMENTATION
→ UPLIFT
→ BUSINESS POLICY
```

Đây là hướng đúng.

---

# 36. Điểm mạnh nhất hiện tại

## 1. Data Foundation không còn bị chìm

EDA đã nối trực tiếp với simulation.

## 2. Causal simulator có known ground truth

Y0 / CATE / Y1 tạo environment kiểm chứng estimator.

## 3. Core A/B đúng scope mentor

Không bị Uplift lấn át completely.

## 4. Uplift trở thành extension hợp lý

Từ ATE → individual response.

## 5. Policy layer đã có real decision logic

Không dừng ở Qini/AUUC.

## 6. GMV/Burn đã được đưa vào business layer

Nhưng vẫn giữ caveat rằng đây chưa phải official GSM definitions.

---

# 37. Điểm yếu lớn nhất hiện tại

## 1. Model inconsistency

T/X/R/S story chưa đồng nhất.

## 2. Documentation overclaim

Một số report vẫn mang wording cũ.

## 3. Stress test còn nông

Chưa đủ DGP/economics/policy stress.

## 4. Production assumptions quá cụ thể

Một số file tạo cảm giác production thật.

## 5. Reproducibility chưa sạch

Hard-coded path + repo hygiene.

---

# 38. Definition of Done trước final review

Repo có thể coi là final-ready khi:

## Data

- [ ] Calibration scorecard không còn inconsistency
- [ ] Empirical vs Assumption clear
- [ ] Y0 / cate_true / ite_realized / Y1 documented
- [ ] Synthetic validation report complete

## Experiment

- [ ] Experiment specification marked illustrative
- [ ] A/A wording corrected
- [ ] Type-I Error typo fixed
- [ ] SRM dynamic ratio
- [ ] Power/MDE consistent
- [ ] A/B report no overclaim

## Uplift

- [ ] Model benchmark table
- [ ] Champion model chosen
- [ ] README/docs/dashboard consistent
- [ ] Whole-population evaluation
- [ ] Calibration
- [ ] Oracle regret

## Economics

- [ ] GMV/Burn defined
- [ ] unit/horizon consistent
- [ ] predicted vs ground-truth policy value separated
- [ ] Business assumptions configurable

## Robustness

- [ ] DGP shift
- [ ] economics shift
- [ ] population shift
- [ ] policy stability

## Engineering

- [ ] no absolute paths
- [ ] venv untracked
- [ ] legacy docs archived
- [ ] project runs from relative paths/config
- [ ] README reflects current champion model

---

# 39. Final audit conclusion

Repo hiện tại đã cập nhật **thực chất** theo phần lớn những gì được đề xuất trong MASTER FINAL.

Các phần quan trọng đã làm đúng:

```text
Data Foundation
Causal Simulation
Experiment Health
A/B
Uplift
Policy Evaluation
GMV/Burn
Oracle Policy
Policy Simulator
```

Điều còn thiếu không phải là một framework mới.

Điều cần làm là:

```text
1. Chốt model story
2. Sửa wording
3. Đồng bộ docs ↔ code ↔ dashboard
4. Làm rõ economics
5. Nâng stress test
6. Fix reproducibility
7. Archive legacy artifacts
```

Nếu xử lý tốt các phần này, project sẽ chuyển từ:

> **“Một repo có rất nhiều thành phần kỹ thuật hay.”**

sang:

> **“Một end-to-end experimentation project có logic, evidence, business framing và engineering discipline nhất quán.”**

Đó là trạng thái nên hướng tới trước final review với mentor/doanh nghiệp.
