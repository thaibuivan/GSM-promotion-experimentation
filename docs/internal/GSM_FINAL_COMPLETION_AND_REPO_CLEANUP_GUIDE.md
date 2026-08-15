# GSM Promotion Experimentation — FINAL COMPLETION CHECKLIST
## Streamlit Hardening + Repo Cleanup + Final-Ready Actions

> **Trạng thái:** FINAL ACTION GUIDE  
> **Mục tiêu:** Đây là checklist cuối cùng để hoàn thiện project trước khi review với PM/mentor.  
> Tài liệu này tổng hợp:
>
> 1. Các lỗi/điểm chưa ổn còn lại trong Streamlit.
> 2. Các cải thiện technical correctness cần sửa trước khi gọi dashboard là final.
> 3. Các cải thiện UI/UX nên làm nếu còn thời gian.
> 4. Các file Markdown nên giữ, archive hoặc xóa để repo gọn và dễ review.
> 5. Definition of Done trước khi final demo.
>
> **Nguyên tắc:** Không mở rộng thêm scope mới. Từ thời điểm này, ưu tiên:
>
> ```text
> Correctness
> → Consistency
> → Reproducibility
> → Presentation
> ```
>
> Không ưu tiên thêm model mới, thêm dataset mới hay mở rộng sang marketplace/driver optimization.

---

# 1. Kết luận trạng thái hiện tại

Project hiện đã có đầy đủ ba trụ cột chính:

```text
PILLAR 1
DATA FOUNDATION & CAUSAL SIMULATION

EDA
→ empirical calibration
→ synthetic users
→ Y0 / CATE / Y1
→ randomized treatment

PILLAR 2
EXPERIMENTATION

K-Means
→ Experiment Design
→ A/A
→ SRM
→ SMD
→ A/B
→ ATE / HTE

PILLAR 3
UPLIFT & BUSINESS POLICY

Uplift Modeling
→ CATE
→ GMV / Burn
→ Policy Evaluation
→ Policy Simulator
```

Streamlit hiện đã đủ tốt để demo WIP.

Tuy nhiên để gọi là **final-ready**, còn một số lỗi technical correctness và consistency phải sửa trước.

---

# 2. FINAL PRIORITY MAP

Thứ tự sửa cuối cùng:

```text
P0 — MUST FIX
1. Qini model mismatch
2. true_ite vs true_cate terminology
3. ROI formula inconsistency
4. A/B Result thiếu statistical core output
5. Policy value ground-truth vs predicted
6. Simulator budget logic
7. Hard-coded path / reproducibility

P1 — SHOULD FIX
8. Add A/A result to Experiment Health
9. Real vs Synthetic validation charts
10. Metric/horizon consistency
11. Model story consistency across repo
12. Clean overclaim wording

P2 — POLISH
13. Semantic colors
14. Remove duplicate texts / noisy headlines
15. Improve tooltips
16. Archive old docs
17. Simplify repo root
```

---

# 3. P0.1 — Qini Curve đang ghi sai model

Dashboard hiện có thể hiển thị:

```text
Qini Curve — T-Learner Champion
```

trong khi file `qini_curve.csv` hiện được sinh từ policy engine dùng một **R-Learner-style residual approach**.

Logic hiện tại gần như:

```text
Outcome Model
→ residualized outcome

Treatment
→ residualized treatment

Y_tilde / T_tilde
→ R-style target

XGBoost
→ predicted CATE
```

Do đó:

```text
Dashboard says:
T-Learner

Actual Qini source:
R-Learner-style model
```

## Cách sửa

Không chỉ đổi text.

Trước tiên cần chốt:

```text
Which model generated:
qini_curve.csv
```

Sau đó dashboard lấy tên model từ result/config:

```python
champion_model_name
```

UI:

```text
Qini Curve — {Champion Model}
```

## Definition of Done

- [ ] Qini source model xác định rõ.
- [ ] README đúng model.
- [ ] Week 5 Report đúng model.
- [ ] Decision Memo đúng model.
- [ ] Dashboard đúng model.
- [ ] Không còn T/X/R-Learner mâu thuẫn.

---

# 4. P0.2 — `true_ite` đang thực chất là `true_cate`

Causal pipeline đã phân biệt:

```text
cate_true
=
E[Y1 - Y0 | X]

ite_realized
=
Y1 - Y0
```

Đây là phân biệt đúng.

Nhưng policy engine có logic kiểu:

```python
df["true_ite"] = df["cate_true"]
```

Điều này làm terminology sai.

## Cách sửa

Nếu policy evaluation dùng expected conditional effect:

```text
true_cate
```

thì giữ đúng tên đó.

Nên đổi:

```text
true_ite
→ true_cate
```

ở:

- policy engine,
- output CSV,
- dashboard,
- tooltips,
- Oracle Policy label.

## Oracle label

Không nên:

> Oracle Policy — True ITE

Nên:

> **Oracle Policy — Synthetic True CATE**

hoặc:

> **Oracle Benchmark — Known Causal Ground Truth**

## Vì sao?

Policy expected value nên dùng expected effect:

```text
E[Y1-Y0 | X]
```

chứ không nhất thiết dùng realized stochastic difference.

---

# 5. P0.3 — ROI formula đang không nhất quán

Một phần dashboard tính:

```text
gross_profit
=
incremental_revenue × margin_rate

ROI
=
(gross_profit - voucher_cost)
/
voucher_cost
```

Nhưng một chart khác tính:

```text
ROI
=
(incremental_revenue - voucher_cost)
/
voucher_cost
```

tức bỏ mất margin.

Hai chart đang dùng hai định nghĩa khác nhau.

## Công thức nên thống nhất

```text
Incremental Contribution
=
Incremental GMV × Contribution Margin %

Incremental Profit
=
Incremental Contribution - Burn

ROI
=
Incremental Profit / Burn
```

Nếu primary economic input là incremental rides:

```text
Incremental Contribution
=
Incremental Rides × Contribution Margin per Ride
```

## Definition of Done

- [ ] Persona ROI dùng cùng formula.
- [ ] Recency ROI dùng cùng formula.
- [ ] Policy ROI dùng cùng formula.
- [ ] Simulator ROI dùng cùng formula.
- [ ] `metric_specification.md` định nghĩa duy nhất một công thức.

---

# 6. P0.4 — A/B Result phải ưu tiên core causal result

Hiện dashboard A/B có thể đang nhấn mạnh:

```text
Incremental GMV
Burn
Net Profit
```

nhưng A/B Testing là core deliverable của mentor.

UI phải ưu tiên:

```text
PRIMARY CAUSAL RESULT

Control Mean Rides
Treatment Mean Rides
ATE Rides
95% CI
p-value
```

Sau đó mới:

```text
BUSINESS TRANSLATION

Incremental GMV
Burn
Incremental Profit
ROI
```

## Layout đề xuất

```text
A/B RESULTS

┌────────────┬────────────┬────────────┐
│ Control    │ Treatment  │ ATE        │
│ Mean       │ Mean       │            │
└────────────┴────────────┴────────────┘

95% CI
p-value

──────────────────────────

BUSINESS TRANSLATION
Incremental Rides
Incremental GMV
Burn
Profit
ROI
```

## Wording

Không gọi economics box là:

> Statistical Interpretation

Nên:

> **Business Interpretation — under current sandbox assumptions**

---

# 7. P0.5 — Predicted Policy Value và Ground-Truth Value phải tách

Synthetic sandbox có lợi thế đặc biệt:

```text
Model selects users
+
Simulator knows true CATE
```

Do đó ta có thể chấm:

```text
Predicted Policy Value
```

và:

```text
Ground-Truth Policy Value
```

Hiện một số policy table có thể đang gọi ground-truth evaluated value là:

```text
Expected Incremental Profit
```

dễ gây hiểu nhầm.

## Cách sửa

Bảng nên có:

| Policy | Predicted Value | Ground-Truth Value | Error / Regret |
|---|---:|---:|---:|
| Mass | ... | ... | ... |
| Segment | ... | ... | ... |
| Uplift | ... | ... | ... |
| Profit | ... | ... | ... |
| Budget | ... | ... | ... |

Oracle:

```text
Oracle Policy
=
benchmark only
```

Không coi Oracle là deployable policy.

## UI badge

```text
Synthetic-only ground truth
```

nên xuất hiện cạnh:

- true CATE,
- Oracle,
- Ground-Truth Policy Value,
- Policy Regret.

---

# 8. P0.6 — Budget-Constrained Policy logic cần sửa

Budget policy không chỉ:

```text
Sort EV
→ take until budget exhausted
```

mà phải loại:

```text
EV <= 0
```

trước.

## Correct logic

```text
1. Compute Expected Value
2. Filter EV > 0
3. Sort EV descending
4. Apply Max Target %
5. Apply Budget Constraint
6. Select users
```

## Hai constraints

```text
Total Burn <= Budget
```

và:

```text
Targeted Users <= Max Target %
```

## Mass Policy

Nếu gọi:

```text
Mass Voucher
```

thì phải target:

```text
100% eligible population
```

Nếu muốn cap:

```text
Broad Targeting — capped at X%
```

Không lấy arbitrary first rows.

---

# 9. P0.7 — Reproducibility

Repo không nên chứa path kiểu:

```python
D:\Intern VSF\GSM-promotion-experimentation
```

## Cách sửa

```python
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
DATA_DIR = PROJECT_ROOT / "data"
OUTPUT_DIR = PROJECT_ROOT / "outputs"
```

Hoặc dùng config/env.

## Definition of Done

Một người khác phải có thể:

```bash
git clone ...
pip install -r requirements.txt
streamlit run src/dashboard/app.py
```

mà không sửa source code.

---

# 10. P1.1 — Experiment Health nên có A/A

Current dashboard đã có:

```text
SRM
SMD
```

Nên bổ sung:

```text
A/A False Positive Calibration
```

Health view:

```text
SRM                    PASS
Covariate Balance      PASS
A/A Calibration        PASS
Exposure Integrity     N/A — Synthetic Sandbox
```

Tổng:

```text
EXPERIMENT HEALTH
PASS / REVIEW / FAIL
```

---

# 11. P1.2 — Data Foundation cần Real vs Synthetic charts

Data Foundation hiện đã cải thiện nhiều.

Nhưng chart cuối nên là validation thực sự:

```text
Real TLC
vs
Synthetic
```

Ưu tiên:

## Chart 1

```text
Fare Distribution
Real vs Synthetic
```

## Chart 2

```text
Hour-of-Day Distribution
Real vs Synthetic
```

## Chart 3 — optional

```text
Airport Share / Trip Behavior
Real vs Synthetic
```

## Calibration Scorecard

Không hard-code:

```text
100% PASS
```

nếu một số biến là assumption-driven.

Nên hiển thị:

```text
Empirical Calibration: PASS
Assumption-driven Features: DOCUMENTED
```

---

# 12. P1.3 — Metric horizon phải thống nhất

Repo có dấu hiệu dùng:

```text
14-day experiment window
```

và một số biến:

```text
gross_revenue_30d
```

Final phải ghi rõ.

## Option A

Thống nhất toàn bộ về:

```text
14-day outcome
```

## Option B

Giữ cả hai nhưng label:

```text
Primary Outcome Window: 14 days
Revenue Proxy Window: 30 days
```

Không để metric có horizon ẩn.

---

# 13. P1.4 — Model story phải có một source of truth

Repo hiện có thể nhắc:

```text
S-Learner
T-Learner
X-Learner
R-Learner-style
```

Không vấn đề nếu benchmark nhiều model.

Vấn đề là:

> Mỗi file chọn một champion khác nhau.

## Final model structure

```text
Benchmarked Models
├── S-Learner
├── T-Learner
├── X-Learner
└── R-Learner-style

Champion
→ selected using final evaluation criteria
```

## Evaluation table

| Model | Qini | AUUC | CATE RMSE | Policy Value | Runtime |
|---|---:|---:|---:|---:|---:|
| S | | | | | |
| T | | | | | |
| X | | | | | |
| R | | | | | |

Champion nên dựa trên:

```text
Out-of-sample causal ranking
+
ground-truth recovery
+
policy value
```

không chỉ một metric.

---

# 14. P1.5 — Wording cleanup

Search toàn repo:

```text
tuyệt đối
hoàn hảo
miễn nhiễm
triển khai ngay
deploy
rollout 100%
vạch trần
phải ngừng
mỏ vàng
sẵn sàng production
```

## Đổi sang

```text
validated in simulation
no material issue detected
consistent with expected behavior
under current assumptions
illustrative
requires real randomized validation
```

---

# 15. Streamlit — UI changes cuối cùng

## Keep

- Dark theme
- Cyan primary accent
- Tab structure
- Policy Simulator
- MDE calculator

## Sửa

### Title

```text
Promotion Experimentation Sandbox
```

### Subtitle

```text
Data Foundation · A/B Testing · Uplift · Policy Evaluation
```

### Banner

```text
Synthetic Sandbox
Not GSM production estimates
```

### Navigation

```text
📚 Data Foundation
📏 Experiment Setup
🩺 Experiment Health
📊 A/B Results
🎯 Heterogeneity
💰 Policy Evaluation
⚙️ Policy Simulator
🛠 Developer Tools
```

---

# 16. Semantic colors

Nên thống nhất:

```text
Gray
=
Control / Baseline

Cyan
=
Treatment / Selected

Green
=
Positive / PASS

Orange
=
Review / Warning

Red
=
Negative / FAIL
```

Không dùng color chỉ vì decoration.

---

# 17. Heterogeneity wording

Không dùng:

> Ai đang làm công ty LỖ?

Nên:

> **Net Incremental Profit by Persona**

Không dùng:

> Phải ngừng phát voucher cho khách ruột

Nên:

> **Under the current synthetic DGP, some high-frequency personas show lower incremental economics than less-active personas.**

Và luôn có note:

```text
Synthetic result — not production recommendation.
```

---

# 18. Developer Tools

`Admin Pipeline` nên đổi:

```text
Developer Tools
```

Nằm cuối.

Có thể chứa:

```text
Run Data Pipeline
Run Policy Evaluation
Refresh Outputs
View Logs
```

Không cần nổi bật với business user.

---

# 19. Markdown files — nguyên tắc cleanup

Repo public-facing không nên chứa:

> File “AI góp ý cho mình nên làm gì”.

Repo nên chứa:

> Project docs, evidence, specs, technical reports, stakeholder deliverables.

Do đó cần dọn root và docs.

---

# 20. ROOT — file nên GIỮ

## `README.md`

**GIỮ ở root.**

Vai trò:

```text
Project landing page
```

README phải trả lời:

- project là gì,
- scope,
- architecture,
- quick start,
- repo structure,
- current status.

## Không nên có nhiều roadmap ở root

Root nên sạch.

---

# 21. ROOT — file nên XÓA khỏi active repo

Các file cũ:

```text
GSM_Internship_Project_Framing_and_Improvement_Guide.md

GSM_Project_Review_and_Optimization_Roadmap.md

GSM_Promotion_Experimentation_Final_Project_Guide_v2.md
```

**Xóa khỏi active repo.**

Lý do:

- bản cũ,
- trùng nội dung,
- không phải deliverable,
- dễ làm người review không biết đâu là source of truth.

---

# 22. MASTER FINAL nên xử lý thế nào?

File:

```text
GSM_Promotion_Experimentation_MASTER_FINAL.md
```

là internal guide rất hữu ích cho bản thân project owner.

Nhưng không cần nằm root.

Hai lựa chọn:

## Option A — khuyên dùng

Giữ local, không push public repo.

## Option B

Move:

```text
docs/internal/PROJECT_MASTER_GUIDE.md
```

Nếu repo được PM review, Option A sạch hơn.

---

# 23. Hai audit file không nên push vào repo

Các file:

```text
GSM_Repo_Audit_After_MASTER_FINAL.md

GSM_Streamlit_Dashboard_Final_UI_UX_Review.md
```

**Không nên push.**

Đây là:

```text
development guidance
```

không phải:

```text
project documentation
```

Giữ local.

---

# 24. TECH DOC W4 — phải GIỮ

File:

```text
docs/TECHNICAL_DOCUMENTATION_W4.md
```

**GIỮ.**

Đây là artifact PM yêu cầu.

Vai trò:

> Technical snapshot of WIP after first four weeks.

---

# 25. Docs — Data Foundation nên GIỮ

```text
Week1_Data_Dictionary.md
Week1_Data_Quality_Report.md
Week1_Data_Preprocessing_Report.md
EDA_Simulation_Mapping.md
Calibration_Scorecard.md
data_contract.md
```

Tất cả có vai trò rõ.

---

# 26. Docs — Weekly Reports nên GIỮ

```text
Week2_Synthetic_Data_Comprehensive_Report.md
Week3_Comprehensive_Report.md
Week4_AA_AB_Testing_Report.md
Week5_Uplift_Modeling_Report.md
```

Đây là technical evidence/history.

Nhưng cần sửa wording/inconsistency.

---

# 27. `Week1_Causal_Thinking_101.md`

Khuyên:

```text
ARCHIVE
```

Move:

```text
docs/archive/learning_notes/
```

Lý do:

- learning note,
- causal concepts đã được thể hiện ở Week 2/3/4,
- không phải active deliverable.

---

# 28. `Week6_Observational_Studies_Report.md`

Khuyên:

```text
ARCHIVE hoặc DELETE
```

Lý do:

- legacy persona count,
- production-like claims,
- mâu thuẫn với current framing,
- wording quá mạnh.

Nếu giữ:

```text
docs/archive/legacy/
```

Không để active docs.

---

# 29. `Week6_Stress_Test_Report.md`

Không xóa hẳn.

Khuyên:

```text
REWRITE
```

Current version nếu còn:

- “TUẦN 8”
- “độ tin cậy tuyệt đối”
- “ready to deploy”

thì phải sửa.

Final stress test cần có:

```text
Statistical Shift
DGP Shift
Population Shift
Economics Shift
Policy Stability
```

Sau khi rewrite mới để active.

---

# 30. `experiment_specification.md`

**GIỮ nhưng sửa.**

Nếu có:

```text
Launch Q4
Voucher 15%
Max 50k
10% Holdout
45% Segment
45% AI
```

mà không phải verified GSM parameters:

Tiêu đề nên thành:

> **Illustrative Experiment Specification**

Disclaimer:

> Campaign parameters are hypothetical assumptions for methodology demonstration unless explicitly confirmed.

---

# 31. `metric_specification.md`

**GIỮ nhưng update.**

Phải có definitions:

```text
ATE
Incremental Rides
GMV
Incremental GMV
Burn
Burn/GMV
Burn/Incremental GMV
CPIR
Incremental Contribution
Incremental Profit
ROI
Oracle Regret
```

---

# 32. `Decision_Memo.md`

**GIỮ.**

Nhưng phải đảm bảo:

```text
Synthetic Sandbox
```

xuất hiện rõ.

Nên có:

```text
What We Can Claim
What We Cannot Claim
```

Không dùng wording production recommendation.

---

# 33. Repo root sau cleanup

Mục tiêu:

```text
GSM-promotion-experimentation/
│
├── README.md
├── requirements.txt
├── .gitignore
├── config/
├── data/
├── notebooks/
├── src/
├── docs/
└── .streamlit/
```

Không để 4–5 roadmap `.md` ở root.

---

# 34. Docs structure đề xuất

Không bắt buộc refactor ngay, nhưng cleanest structure:

```text
docs/
│
├── TECHNICAL_DOCUMENTATION_W4.md
│
├── data/
│   ├── Week1_Data_Dictionary.md
│   ├── Week1_Data_Quality_Report.md
│   ├── Week1_Data_Preprocessing_Report.md
│   ├── EDA_Simulation_Mapping.md
│   ├── Calibration_Scorecard.md
│   └── data_contract.md
│
├── reports/
│   ├── Week2_Synthetic_Data_Comprehensive_Report.md
│   ├── Week3_Comprehensive_Report.md
│   ├── Week4_AA_AB_Testing_Report.md
│   ├── Week5_Uplift_Modeling_Report.md
│   └── Week6_Stress_Test_Report.md
│
├── specifications/
│   ├── experiment_specification.md
│   └── metric_specification.md
│
├── Decision_Memo.md
│
└── archive/
    ├── learning_notes/
    │   └── Week1_Causal_Thinking_101.md
    │
    └── legacy/
        └── Week6_Observational_Studies_Report.md
```

---

# 35. `.gitignore`

Đảm bảo có:

```text
venv/
.venv/
__pycache__/
.ipynb_checkpoints/
*.pyc
.env
```

Không track Python virtual environment.

---

# 36. Final Streamlit checklist

## Data Foundation

- [ ] KPI cards đúng số liệu.
- [ ] Real vs Synthetic chart.
- [ ] Calibration scorecard.
- [ ] Assumption registry.
- [ ] Không hard-code “100% calibrated”.

## Experiment Setup

- [ ] Treatment ratio dynamic.
- [ ] MDE / Power consistent.
- [ ] Outcome horizon visible.

## Experiment Health

- [ ] SRM dynamic.
- [ ] SMD.
- [ ] A/A.
- [ ] PASS / REVIEW / FAIL.
- [ ] No absolute wording.

## A/B Result

- [ ] Control rides.
- [ ] Treatment rides.
- [ ] ATE.
- [ ] 95% CI.
- [ ] p-value.
- [ ] Incremental GMV.
- [ ] Burn.
- [ ] Profit / ROI.

## Heterogeneity

- [ ] Persona.
- [ ] Segment ATE.
- [ ] Champion model.
- [ ] Qini/AUUC.
- [ ] Calibration.
- [ ] No overclaim headline.

## Policy Evaluation

- [ ] 5 candidate policies.
- [ ] Baseline.
- [ ] Oracle benchmark.
- [ ] Predicted value.
- [ ] Ground-truth value.
- [ ] Regret.

## Simulator

- [ ] EV > 0 filter.
- [ ] Budget constraint.
- [ ] Max-target constraint.
- [ ] Mass policy correct.
- [ ] Business assumptions labeled.
- [ ] Ground-truth label.

---

# 37. Final repo consistency checklist

Search toàn repo:

```text
T-Learner
X-Learner
R-Learner
S-Learner
```

Sau đó đảm bảo:

```text
benchmark story consistent
```

Search:

```text
true_ite
```

và đổi các chỗ thực chất dùng `cate_true`.

Search:

```text
ROI
```

đảm bảo một formula.

Search:

```text
14-day
30-day
```

đảm bảo horizon rõ.

Search:

```text
deploy
rollout
production
tuyệt đối
hoàn hảo
```

đảm bảo wording đúng sandbox framing.

---

# 38. Final demo story

PM/mentor demo nên đi:

```text
1. Data Foundation
2. Synthetic Causal Data
3. Experiment Setup
4. Experiment Health
5. A/B Result
6. Heterogeneity
7. Week 5 Uplift Extension
8. Policy Simulator
```

Nếu đang báo cáo WIP 4 tuần:

```text
Stop core story at A/B
```

sau đó nói:

> Uplift/Policy là Week 5 extension.

---

# 39. Không làm thêm các scope sau

Từ thời điểm này không mở rộng:

```text
Driver Agent
Marketplace ABM
MARL
Surge Pricing
Driver Repositioning
GPS Dataset
Model Zoo lớn
Production API
Full MLOps
```

Các phần này không giải quyết bottleneck final.

---

# 40. Definition of Done — PROJECT FINAL

Project có thể gọi là final-ready khi:

## Correctness

- [ ] Qini model đúng.
- [ ] True CATE terminology đúng.
- [ ] ROI formula thống nhất.
- [ ] A/B có CI + p-value.
- [ ] Policy evaluation đúng logic.
- [ ] Budget policy không target negative EV.

## Consistency

- [ ] Model champion thống nhất.
- [ ] Metrics thống nhất.
- [ ] Horizon thống nhất.
- [ ] Wording thống nhất.

## Reproducibility

- [ ] Không absolute path.
- [ ] `venv` không tracked.
- [ ] `requirements.txt` chạy được.
- [ ] Streamlit clone-and-run được.

## Documentation

- [ ] README là landing page duy nhất.
- [ ] Tech Doc W4 có trong `docs/`.
- [ ] Legacy docs archive.
- [ ] Roadmap nội bộ không nằm root.
- [ ] Experiment spec marked illustrative.

## Presentation

- [ ] Synthetic disclaimer.
- [ ] Data Foundation rõ.
- [ ] Core A/B result rõ.
- [ ] Uplift là extension.
- [ ] Business assumptions rõ.
- [ ] No production overclaim.

---

# 41. Final Expected Repo State

Sau khi xử lý checklist này, repo nên thể hiện rõ:

```text
REAL/PUBLIC DATA
      ↓
DATA FOUNDATION
      ↓
EMPIRICALLY INFORMED SYNTHETIC CAUSAL WORLD
      ↓
RANDOMIZED EXPERIMENT
      ↓
A/B CAUSAL EVIDENCE
      ↓
UPLIFT / HETEROGENEITY
      ↓
BUSINESS POLICY EVALUATION
```

Không phải:

```text
Random notebooks
+
Multiple roadmaps
+
Conflicting model names
+
Production-like claims
```

---

# 42. Final Conclusion

Project hiện không thiếu thêm thuật toán.

Điều quyết định chất lượng final review bây giờ là:

```text
Does every number mean the same thing everywhere?

Does every model name match the code?

Does every business claim match the evidence?

Can another person clone and run the project?

Can PM understand the story in 5–10 minutes?
```

Nếu 5 câu trên đều trả lời được:

```text
YES
```

thì project đã đủ chín để final review.

**Ưu tiên cuối cùng:**

```text
1. Fix correctness bugs
2. Align model/metric terminology
3. Clean repo docs
4. Ensure reproducibility
5. Polish Streamlit
```

Sau đó dừng mở rộng scope và tập trung vào tech doc, demo và final presentation.
