# GSM Promotion Experimentation — FINAL REPO AUDIT (Latest Public `main`)
## 9 hạng mục cần xem xét trước khi coi project là bản final mentor/PM review

> **Thời điểm audit:** 15/08/2026  
> **Nguồn audit:** public branch `main` của repo `thaibuivan/GSM-promotion-experimentation` tại thời điểm kiểm tra gần nhất.  
> **Mục đích:** Đây là checklist cuối cùng dựa trên **repo mới nhất đang public**, không dựa trên bản review cũ.
>
> **Lưu ý quan trọng:** Streamlit đã có Live Demo trong README và nếu link public đang mở ổn thì **đã đủ để gửi demo**. Các mục dưới đây chủ yếu nhằm làm cho repo/code/docs **nhất quán về technical story và đủ sạch để mentor/PM soi sâu**.

---

# A. Những điểm đã sửa tốt trong bản mới nhất

Trước khi liệt kê phần còn lại, một số góp ý trước **đã được sửa đúng**:

### 1. README đã có Live Demo

README hiện có:

```text
🚀 Live Demo
gsm-promotion-experimentation.streamlit.app
```

Đây là đúng hướng cho việc gửi PM/mentor.

---

### 2. Streamlit đã framing đúng là Synthetic Sandbox

Dashboard mở đầu bằng:

```text
Promotion Experimentation Sandbox
```

và có disclaimer:

```text
không phải kết quả production của GSM
```

Điều này đã giải quyết phần lớn rủi ro overclaim ở UI.

---

### 3. A/B tab đã có statistical causal result

Bản mới hiện có:

```text
ATE (Incremental Rides)
95% Confidence Interval
p-value
Statistical Significance
```

sau đó mới chuyển sang:

```text
Incremental GMV
Burn
Net Profit
ROI
```

Đây là cải thiện đúng với core scope A/B Testing.

---

### 4. Qini trên Streamlit đã đổi sang R-Learner

Dashboard hiện ghi:

```text
Qini Curve (R-Learner Champion)
```

và policy engine thực tế cũng train:

```text
R-Learner / residual learner
```

Tức **dashboard ↔ code đã đồng bộ ở điểm này**.

---

### 5. Budget-Constrained Simulator đã tốt hơn

Simulator hiện đã:

```text
filter expected_value > 0
→ sort descending
→ apply Max Target %
→ apply Budget
```

Đây là logic tốt hơn bản trước.

---

### 6. Simulator đã tách Predicted và Ground Truth

Policy Simulator hiện hiển thị:

```text
Predicted Profit
Ground-Truth Profit (Synthetic-only)
```

Đây là cách trình bày đúng cho synthetic sandbox.

---

# B. 9 HẠNG MỤC CÒN LẠI

---

# 1. 🔴 Chốt và đồng bộ model story: R-Learner vs T-Learner

## Trạng thái repo mới nhất

### Code hiện tại

`src/pipeline/policy_comparison_engine.py` đang train:

```text
R-Learner (Residual Learner)
```

và dùng prediction của R-Learner để:

```text
cate_pred
→ Qini Curve
→ Uplift Targeting
→ Profit Targeting
```

### Dashboard hiện tại

Streamlit cũng đã ghi:

```text
Qini Curve (R-Learner Champion)
```

### Nhưng documentation vẫn nói T-Learner

README hiện vẫn ghi:

```text
T-Learner (XGBoost) làm Champion Model
```

`Decision_Memo.md`:

```text
T-Learner (XGBoost) cho profit tốt nhất...
```

`experiment_specification.md`:

```text
Causal ML (T-Learner)
```

`Week5_Uplift_Modeling_Report.md`:

```text
Thuật toán: T-Learner + XGBoost
```

## Vì sao đây là vấn đề?

Mentor đọc code sẽ thấy:

```text
R-Learner
```

nhưng đọc README/report lại thấy:

```text
T-Learner
```

=> Không rõ **champion model cuối cùng là model nào**.

## Cách sửa

Nếu code cuối cùng thực sự dùng R-Learner:

### README

Đổi:

```text
T-Learner (XGBoost) làm Champion Model
```

thành:

```text
R-Learner (XGBoost-based residual learner) làm current champion model.
```

Nếu trước đó đã benchmark S/T/X/R thì tốt hơn ghi:

```text
Benchmarked S-Learner, T-Learner, X-Learner và R-Learner;
R-Learner được chọn làm current champion cho policy evaluation.
```

### Đồng bộ các file:

```text
README.md
docs/Decision_Memo.md
docs/Week5_Uplift_Modeling_Report.md
docs/experiment_specification.md
Streamlit dashboard
policy_comparison_engine.py
```

## Definition of Done

```text
[ ] Chỉ có 1 champion model cuối cùng
[ ] README đúng
[ ] Dashboard đúng
[ ] Decision Memo đúng
[ ] Week5 report đúng
[ ] Experiment Spec đúng
```

---

# 2. 🔴 ROI theo Recency vẫn đang dùng sai công thức

## Trạng thái hiện tại

### Persona ROI — đang đúng

Dashboard tính:

```text
Incremental Contribution
=
Incremental GMV × Margin %

Net Profit
=
Incremental Contribution - Burn

ROI
=
Net Profit / Burn
```

Code tương ứng:

```python
gross_profit = d_rev * (MARGIN_PERCENT / 100.0)
cost = (DISCOUNT_PERCENT / 100.0) * rev_t
roi = (gross_profit - cost) / cost * 100
```

### Recency ROI — vẫn chưa đồng bộ

Hiện code:

```python
d_rev = rev_t - rev_c
cost = (DISCOUNT_PERCENT / 100.0) * rev_t
roi = (d_rev - cost) / cost * 100
```

Ở đây:

```text
d_rev
```

được dùng trực tiếp như profit contribution và **không nhân contribution margin**.

## Vì sao sai?

Nếu:

```text
Incremental GMV = $10
Margin = 70%
```

thì incremental contribution là:

```text
$7
```

không phải:

```text
$10
```

Nếu dùng hai công thức khác nhau:

```text
Persona chart
vs
Recency chart
```

thì hai biểu đồ ROI không còn comparable.

## Cách sửa

```python
d_rev = rev_t - rev_c
gross_profit = d_rev * (MARGIN_PERCENT / 100.0)
cost = (DISCOUNT_PERCENT / 100.0) * rev_t

roi = (
    (gross_profit - cost) / cost * 100
    if cost > 0 else 0
)
```

## Sau khi sửa

Search toàn repo:

```text
ROI
Est_ROI_pct
```

đảm bảo:

```text
Persona ROI
Recency ROI
Policy ROI
Simulator ROI
metric_specification.md
```

đều dùng cùng một definition.

---

# 3. 🔴 Policy Comparison vẫn đang trộn Predicted Value và Synthetic Ground Truth

## Simulator đã sửa đúng

Policy Simulator đã tách:

```text
Predicted Profit
Ground-Truth Profit (Synthetic-only)
```

Đây là đúng.

## Nhưng `policy_comparison_engine.py` vẫn chưa tách

Trong `evaluate_policy()` hiện có logic:

```python
if 'oracle_ev' in df_eval.columns:
    total_ev = targeted['oracle_ev'].sum()
    total_inc_rides = targeted['cate_true'].sum()
else:
    total_ev = targeted['expected_value'].sum()
    total_inc_rides = targeted['cate_pred'].sum()
```

Vì synthetic test set có `oracle_ev`, nên column:

```text
Expected_Incremental_Profit
```

thực tế lại đang chứa **Ground-Truth Policy Value**.

Dashboard sau đó gọi nó là:

```text
Lợi nhuận Kỳ vọng
Expected Incremental Profit
```

=> terminology chưa chính xác.

## Cách sửa tốt nhất

Engine nên export riêng:

```text
Predicted_Incremental_Profit
Ground_Truth_Incremental_Profit
Policy_Regret
```

Ví dụ:

```python
predicted_value = targeted['expected_value'].sum()
ground_truth_value = targeted['oracle_ev'].sum()
regret = oracle_best_value - ground_truth_value
```

Dashboard:

| Policy | Predicted Value | Ground-Truth Value | Regret |
|---|---:|---:|---:|
| Mass | ... | ... | ... |
| Segment | ... | ... | ... |
| Uplift | ... | ... | ... |
| Profit | ... | ... | ... |
| Budget | ... | ... | ... |
| Oracle | N/A | ... | 0 |

## Vì sao đáng sửa?

Đây không chỉ là sửa wording.

Synthetic sandbox có điểm mạnh lớn:

```text
model predicts policy value
+
simulation knows causal truth
```

=> Có thể đánh giá **policy error / policy regret** một cách rõ ràng.

---

# 4. 🔴 Chốt một outcome horizon và một economics source of truth

Repo mới nhất hiện vẫn có nhiều definition song song.

## 4.1. Outcome horizon

### Main causal DGP

`main_pipeline.py` đang rõ ràng dùng:

```text
BASELINE_MEAN = 8 rides / 30 days
gross_revenue_30d
discount_cost_30d
```

### Streamlit A/B Result

Hiện ghi:

```text
Outcome Window: 30 days
```

### Nhưng MDE calculator

Vẫn ghi:

```text
Baseline rides / 14 ngày
```

### Experiment Specification

Vẫn ghi:

```text
Outcome Window: 14 ngày
```

### Metric Specification

Vẫn có:

```text
incremental_rides_14d
```

## Khuyến nghị

Vì core synthetic DGP đã được xây theo monthly / 30-day:

```text
CHỐT 30 DAYS
```

làm primary outcome window cho sandbox.

Sau đó sửa:

```text
MDE Calculator
experiment_specification.md
metric_specification.md
README/docs nếu còn
```

cho nhất quán.

---

## 4.2. Voucher economics

### `config.json`

Hiện:

```text
voucher_rate = 15%
margin_rate = 70%
budget = $50,000
```

### Dashboard và policy engine

Đang đọc trực tiếp `config.json`.

Đây là tốt.

### Nhưng `main_pipeline.py`

Data generation vẫn hard-code:

```text
Voucher discount = 20%
cap = $3/trip
```

để sinh:

```text
discount_cost_30d
net_contribution
```

### Decision Memo

Lại ghi:

```text
Margin ≈ 0.75 × fare
Voucher = 15%
```

=> Có:

```text
15%
20%
70%
75%
```

ở các lớp khác nhau.

## Khuyến nghị

Chọn:

```text
config.json
```

làm **single source of truth** cho economics.

Main pipeline nên load:

```text
voucher_rate
margin_rate
budget
```

từ config nếu các biến economics được dùng cho dashboard/policy.

Nếu `discount_cost_30d` chỉ là legacy simulation field thì phải label rõ và không dùng lẫn với final policy economics.

## Definition of Done

```text
[ ] Outcome horizon = 30d ở mọi active docs/UI
[ ] Voucher = một giá trị duy nhất
[ ] Margin = một giá trị duy nhất
[ ] Decision Memo khớp config
[ ] Metric Spec khớp config
```

---

# 5. 🔴 Data Foundation đang gọi reference curve là “Real TLC” dù không load empirical TLC curve

## Trạng thái hiện tại

Dashboard viết:

```text
Phân phối Cước phí: Real TLC vs Synthetic
```

Nhưng đường `Real TLC (Reference)` đang được tạo bằng:

```python
stats.lognorm.pdf(...)
```

với các parameter hard-coded.

Hour-of-day reference cũng được tạo bằng:

```python
Normal peak around 8h
+
Normal peak around 18h
```

chứ không load histogram/hour distribution thật từ Week 1 TLC.

## Vì sao cần sửa?

Người xem có thể hiểu:

> Đường trắng chính là empirical distribution của 3.04M trips.

Trong khi thực tế:

> Nó là analytical/reference curve được parameterized dựa trên simulation assumptions/EDA insight.

## Có 2 cách

### Cách nhanh nhất

Rename:

```text
Real TLC (Reference)
```

thành:

```text
EDA-Calibrated Reference Curve
```

và title:

```text
Calibration Reference vs Synthetic
```

Thêm note:

```text
Reference curve is parameterized from EDA insights;
it is not a direct plot of raw TLC observations.
```

### Cách tốt nhất

Export summary thật từ Week1:

```text
tlc_fare_distribution.csv
tlc_hour_distribution.csv
```

rồi overlay:

```text
Observed TLC
vs
Synthetic
```

Đây sẽ là validation mạnh hơn nhiều.

---

## Calibration card cũng đang quá mạnh

Dashboard hiện ghi:

```text
Calibration Status = PASS
Scorecard = 100%
```

Trong khi project có các biến:

```text
age
income
causal effect parameters
economics
```

là assumption-driven.

Nên đổi thành:

```text
Calibration Status: REVIEWED

Empirical targets:
PASS

Assumption-driven features:
DOCUMENTED
```

Không dùng `100%` như thể toàn bộ synthetic population đã empirically validated.

---

# 6. 🟠 `true ITE` và `true CATE` vẫn chưa được đồng bộ toàn repo

## Core pipeline hiện làm đúng

`main_pipeline.py` hiện có:

```text
ite_realized = Y1 - Y0
cate_true = E[Y1 - Y0 | X]
```

Đây là distinction đúng.

## Nhưng documentation/output vẫn còn gọi sai

### README

Vẫn viết:

```text
Y0/Y1/true ITE
```

### Policy calibration output

Trong `policy_comparison_engine.py`:

```python
true_uplift = subset['cate_true'].mean()
```

nhưng export tên column:

```text
True_ITE
```

### Decision Memo

Vẫn viết:

```text
Oracle Regret so với true ITE
```

## Cách sửa

### Expected structural effect

Gọi:

```text
True CATE
Synthetic Ground-Truth CATE
```

### Realized individual difference

Chỉ gọi:

```text
Realized ITE
=
Y1 - Y0
```

## Sửa cụ thể

```text
README.md
policy_comparison_engine.py
uplift_calibration.csv column
Decision_Memo.md
Calibration_Scorecard.md
dashboard labels nếu còn
```

---

# 7. 🟠 A/A result đang có hai source of truth

## Dashboard

Hiện hard-code:

```text
1,000 simulations
FPR = 4.8%
```

và wording:

```text
Synthetic Sandbox không có thiên lệch cấu trúc
```

## Decision Memo

Lại ghi:

```text
5,000 Monte Carlo
SRM alert = 5.26%
FPR = 5.08%
```

## Vấn đề

Hai con số có thể đều từng đúng ở hai phiên bản chạy khác nhau.

Nhưng final project cần:

```text
ONE FINAL A/A RESULT
```

## Khuyến nghị

Chọn output của final A/A notebook/run, rồi lưu:

```text
data/processed/aa_validation_summary.json
```

Ví dụ:

```json
{
  "n_simulations": 5000,
  "fpr": 0.0508,
  "srm_alert_rate": 0.0526,
  "srm_binomial_p": 0.3988
}
```

Dashboard đọc file này thay vì hard-code.

Decision Memo cũng lấy cùng source.

## Wording nên sửa

Không nên:

```text
Dữ liệu Synthetic Sandbox không có thiên lệch cấu trúc
```

Nên:

```text
Không phát hiện calibration issue đáng kể
trong các A/A simulation settings đã kiểm tra.
```

A/A không chứng minh toàn bộ DGP “không có bias”.

---

# 8. 🟠 Repo public `main` vẫn chưa sạch về structure/docs

## Root mới nhất tôi kiểm tra vẫn còn

```text
venv/

GSM_Internship_Project_Framing_and_Improvement_Guide.md
GSM_Project_Review_and_Optimization_Roadmap.md
GSM_Promotion_Experimentation_Final_Project_Guide_v2.md
GSM_Promotion_Experimentation_MASTER_FINAL.md

output_summary.txt
output_summary_slearner.txt
```

Nếu bạn đã xóa local mà GitHub vẫn còn thì khả năng là:

```text
chưa commit/push cleanup
```

hoặc `venv` đã được tracked từ trước.

## Nên xử lý

### Xóa 3 guide cũ

```text
GSM_Internship_Project_Framing_and_Improvement_Guide.md
GSM_Project_Review_and_Optimization_Roadmap.md
GSM_Promotion_Experimentation_Final_Project_Guide_v2.md
```

### MASTER FINAL

Giữ local hoặc:

```text
docs/internal/PROJECT_MASTER_GUIDE.md
```

### Venv

Nếu đã được track:

```bash
git rm -r --cached venv
```

### Temporary summaries

Nếu chỉ là debug/intermediate:

```text
output_summary.txt
output_summary_slearner.txt
```

→ remove khỏi final root.

---

## `docs/` mới nhất vẫn còn legacy docs

Hiện active docs vẫn có:

```text
Week1_Causal_Thinking_101.md
Week6_Observational_Studies_Report.md
Week6_Stress_Test_Report.md
```

và nhiều slide `.pptx` nằm chung.

### `Week1_Causal_Thinking_101.md`

Move:

```text
docs/archive/learning_notes/
```

### `Week6_Observational_Studies_Report.md`

Move:

```text
docs/archive/legacy/
```

### `Week6_Stress_Test_Report.md`

Hiện vẫn có title:

```text
TUẦN 8
```

và conclusion:

```text
sẵn sàng Deploy trên diện rộng
```

=> rewrite trước khi giữ active.

---

## Tech Doc W4

Trong public `docs/` mà tôi kiểm tra hiện vẫn chưa thấy:

```text
TECHNICAL_DOCUMENTATION_W4.md
```

Nếu PM đã yêu cầu tech doc thì file này nên được push.

---

# 9. 🟠 Weekly docs / business spec vẫn còn nội dung legacy hoặc production-like

Đây là consistency/documentation issue cuối cùng.

---

## 9.1. `Week5_Uplift_Modeling_Report.md`

Hiện vẫn ghi:

```text
BÁO CÁO KỸ THUẬT TUẦN 7
```

mặc dù filename là:

```text
Week5_Uplift_Modeling_Report.md
```

Nội dung vẫn:

```text
T-Learner
Urban Cash
ngừng hoàn toàn chiến dịch
```

trong khi code hiện tại đã chuyển sang:

```text
R-Learner
whole eligible population
profit/policy evaluation
```

=> File này cần rewrite hoặc archive.

---

## 9.2. `Week6_Stress_Test_Report.md`

Hiện:

```text
TUẦN 8
```

và kết luận:

```text
sẵn sàng Deploy trên diện rộng
```

Nên đổi thành:

```text
Các stress tests hiện tại không phát hiện failure nghiêm trọng
trong các simulation scenarios đã kiểm tra.
Real-world use vẫn cần randomized production validation.
```

---

## 9.3. `experiment_specification.md`

Điểm tốt:

```text
đã có disclaimer Illustrative / Hypothetical
```

Nhưng vẫn còn các nội dung rất production-like:

```text
Target Launch Q4 2026
All active GSM customers
Blacklist
Popup exposure
app uninstall guardrail
rollout 100%
T-Learner
```

Nếu đây không phải thông tin mentor/business xác nhận:

### Khuyên đổi framing

```text
Illustrative Future Experiment Translation
```

và tránh tạo cảm giác đây là kế hoạch launch thật.

Đặc biệt:

```text
Group C (Champion)
```

nên xem lại naming.

Thông thường:

```text
current policy = Champion
new policy = Challenger
```

Nếu Segment Targeting là current baseline:

```text
Segment = Champion
Uplift/Profit = Challenger
```

---

## 9.4. `Decision_Memo.md`

Điểm tốt:

```text
Synthetic Sandbox
What We Cannot Claim
```

đã rõ.

Nhưng cần sync:

```text
T-Learner → R-Learner
true ITE → true CATE
margin 75% → config 70%
A/A result → final source of truth
```

---

# C. Demo assets / deployment — note riêng

Public `data/processed/` mà tôi kiểm tra hiện chỉ hiển thị:

```text
segmented_simulation_data.csv
```

Trong khi dashboard đọc:

```text
qini_curve.csv
policy_comparison.csv
test_predictions.csv
oracle_regret.json
```

Nếu Streamlit deployed hiện vẫn chạy đầy đủ thì có thể:

```text
pipeline đã generate outputs trên cloud runtime
```

hoặc state hiện tại vẫn còn trong deployment.

Nhưng để deployment reproducible sau reboot/redeploy, nên đảm bảo một trong hai:

## Option A — Precomputed assets

Commit các output demo cần thiết.

## Option B — Deterministic startup generation

App tự generate toàn bộ required assets khi missing, với runtime chấp nhận được.

Với app gửi mentor/PM, Option A thường ổn định hơn.

---

# D. Priority cuối cùng

Nếu chỉ muốn sửa phần **thực sự quan trọng về technical correctness**, làm 5 mục này trước:

```text
P0
1. Sync R-Learner toàn repo
2. Fix Recency ROI formula
3. Split Predicted vs Ground-Truth policy value
4. Chốt 30-day + economics config làm source of truth
5. Fix/rename Real TLC reference validation
```

Sau đó:

```text
P1
6. true CATE terminology
7. A/A source of truth
8. Repo cleanup
9. Rewrite/archive legacy docs
```

---

# E. Final Definition of Done

## Demo-ready

```text
[ ] Streamlit public
[ ] Incognito mở được
[ ] tất cả tab chính load
[ ] không traceback
[ ] không missing assets
```

=> Có thể gửi PM/mentor demo.

---

## Mentor technical-review-ready

```text
[ ] Champion model nhất quán
[ ] ROI formula nhất quán
[ ] Predicted vs Ground Truth tách rõ
[ ] Outcome horizon nhất quán
[ ] Economics config nhất quán
[ ] TLC calibration không overclaim
[ ] CATE/ITE terminology đúng
[ ] A/A result có một source of truth
[ ] Root/docs sạch
[ ] Legacy reports archive/rewrite
[ ] Tech Doc W4 đã push
```

---

# F. Kết luận audit bản mới nhất

Bản hiện tại đã tiến bộ rõ so với các version trước:

```text
A/B statistical story        ✅
Streamlit framing             ✅
R-Learner Qini UI             ✅
Budget policy simulator       ✅
Predicted vs Truth simulator  ✅
Live Demo README              ✅
```

Phần còn lại **không yêu cầu thêm thuật toán hay mở scope mới**.

Bottleneck cuối là:

```text
Consistency
+
Metric correctness
+
Documentation hygiene
+
Reproducibility
```

Sau khi xử lý 5 P0 ở trên, project nên được **freeze về feature scope** và chuyển hoàn toàn sang:

```text
demo
tech doc
final presentation
mentor review
```

---

# G. Repo paths đã kiểm tra trong audit này

```text
README.md

config.json

src/dashboard/app.py
src/pipeline/main_pipeline.py
src/pipeline/policy_comparison_engine.py

docs/Decision_Memo.md
docs/Week5_Uplift_Modeling_Report.md
docs/Week6_Stress_Test_Report.md
docs/experiment_specification.md
docs/metric_specification.md

data/processed/
.gitignore
```

Repo:

```text
https://github.com/thaibuivan/GSM-promotion-experimentation
```
