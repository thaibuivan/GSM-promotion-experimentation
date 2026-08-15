# GSM Promotion Experimentation — 9 Hạng Mục Cải Thiện Cuối Cùng

> **Mục đích:** Tổng hợp 9 hạng mục cải thiện cuối cùng cần xem xét trước khi coi repo/dashboard là bản hoàn thiện để mentor/PM review.
>
> **Lưu ý:** Đây là checklist hoàn thiện project, **không phải điều kiện bắt buộc để gửi link Streamlit demo**. Nếu Streamlit đã deploy public, mở được bằng Incognito và các tab chính không lỗi, bạn vẫn có thể gửi demo ngay. Các mục dưới đây nhằm làm repo và technical story sạch, nhất quán và chuyên nghiệp hơn.

---

# 1. Dọn sạch root repository

## Vấn đề

Root repo đang có quá nhiều file hướng dẫn/roadmap nội bộ nằm ngang hàng với `README.md`, dễ khiến người review không biết đâu là tài liệu chính thức của project.

Các file dạng:

```text
GSM_Internship_Project_Framing_and_Improvement_Guide.md
GSM_Project_Review_and_Optimization_Roadmap.md
GSM_Promotion_Experimentation_Final_Project_Guide_v2.md
GSM_Promotion_Experimentation_MASTER_FINAL.md
```

không nên cùng xuất hiện ở root trong bản final.

Ngoài ra nếu còn:

```text
venv/
output_summary.txt
output_summary_slearner.txt
```

thì cũng nên dọn.

## Nên làm

### Xóa khỏi active repo

```text
GSM_Internship_Project_Framing_and_Improvement_Guide.md
GSM_Project_Review_and_Optimization_Roadmap.md
GSM_Promotion_Experimentation_Final_Project_Guide_v2.md
```

### `MASTER_FINAL`

Hai lựa chọn:

```text
A. Giữ local, không push
```

hoặc:

```text
B. docs/internal/PROJECT_MASTER_GUIDE.md
```

Khuyên dùng A nếu PM/mentor trực tiếp review repo.

### Xóa virtual environment khỏi Git tracking

Nếu `venv/` từng được commit:

```bash
git rm -r --cached venv
```

Sau đó đảm bảo `.gitignore` có:

```text
venv/
.venv/
```

### Xóa output text tạm

Ví dụ:

```text
output_summary.txt
output_summary_slearner.txt
```

Nếu chỉ là intermediate/debug output thì không nên nằm root.

## Trạng thái mong muốn

Root chỉ còn các thành phần chính:

```text
.streamlit/
data/
docs/
notebooks/
src/

.gitignore
README.md
config.json
requirements.txt
```

---

# 2. Dọn và tổ chức lại `docs/`

## Vấn đề

`docs/` hiện chứa nhiều loại tài liệu:

- weekly technical reports,
- learning notes,
- legacy reports,
- decision memo,
- specifications,
- slide files,
- calibration docs.

Nếu để chung một chỗ, người review khó xác định đâu là tài liệu chính.

## Nên giữ active

### Data foundation

```text
Week1_Data_Dictionary.md
Week1_Data_Quality_Report.md
Week1_Data_Preprocessing_Report.md
EDA_Simulation_Mapping.md
Calibration_Scorecard.md
data_contract.md
```

### Weekly technical reports

```text
Week2_Synthetic_Data_Comprehensive_Report.md
Week3_Comprehensive_Report.md
Week4_AA_AB_Testing_Report.md
Week5_Uplift_Modeling_Report.md
```

### Specifications

```text
experiment_specification.md
metric_specification.md
```

### Stakeholder / technical delivery

```text
Decision_Memo.md
TECHNICAL_DOCUMENTATION_W4.md
```

## Nên archive

### Learning note

```text
Week1_Causal_Thinking_101.md
```

Move:

```text
docs/archive/learning_notes/
```

### Legacy observational report

```text
Week6_Observational_Studies_Report.md
```

Move:

```text
docs/archive/legacy/
```

Lý do:

- có thể dùng persona/model story cũ,
- có wording production-like,
- dễ mâu thuẫn với project framing hiện tại.

## Stress test report

```text
Week6_Stress_Test_Report.md
```

Không nhất thiết xóa.

Nên:

```text
REWRITE → rồi giữ active
```

nếu report vẫn có wording kiểu:

```text
độ tin cậy tuyệt đối
sẵn sàng deploy diện rộng
```

## Cấu trúc docs gợi ý

```text
docs/
│
├── TECHNICAL_DOCUMENTATION_W4.md
├── Decision_Memo.md
│
├── data/
├── reports/
├── specifications/
└── archive/
```

Không bắt buộc phải refactor ngay nếu việc đổi path gây tốn thời gian; điều quan trọng là active vs legacy phải rõ.

---

# 3. Đảm bảo Streamlit có đầy đủ demo assets

## Vấn đề

Dashboard không chỉ đọc một file dataset chính mà còn có thể phụ thuộc vào:

```text
segmented_simulation_data.csv
qini_curve.csv
policy_comparison.csv
test_predictions.csv
oracle_regret.json
uplift_calibration.csv
```

Nếu một số file chỉ có ở local mà chưa được push, app deploy trên Streamlit Cloud có thể:

- không hiển thị Qini,
- không hiển thị policy comparison,
- không chạy simulator,
- hiện cảnh báo “Run pipeline first”.

## Nên làm

### Cách nhanh

Commit các output cuối mà dashboard cần.

Ví dụ:

```text
data/processed/
```

hoặc sạch hơn:

```text
demo_assets/
```

### Nguyên tắc

Public demo nên:

```text
READ stable precomputed outputs
```

thay vì:

```text
bắt viewer chạy lại toàn pipeline
```

## Check

Sau deploy, mở app bằng Incognito và kiểm tra:

```text
Data Foundation       OK
Experiment Setup      OK
Experiment Health     OK
A/B Results           OK
Heterogeneity         OK
Policy Evaluation     OK
Policy Simulator      OK
```

Không có:

```text
File not found
Run pipeline first
Traceback
```

---

# 4. Làm sạch `.gitignore`

## Vấn đề

`.gitignore` có thể đang:

- lặp rule,
- ignore toàn bộ `data/`,
- ignore `*.csv`,
- sau đó cố unignore một số file con.

Điều này dễ khiến output cần cho Streamlit không được Git track.

## Nên làm

Giữ một block duy nhất, ví dụ:

```text
# Python
venv/
.venv/
__pycache__/
*.pyc

# Notebook
.ipynb_checkpoints/

# Environment
.env

# Large/raw data
data/raw/
*.parquet

# Optional generated outputs
# Chỉ ignore những file không dùng cho demo
```

Nếu giữ demo assets trong repo:

```text
demo_assets/
```

thì đừng ignore folder đó.

## Mục tiêu

Khi chạy:

```bash
git status
```

phải nhìn rõ:

- file nào cần commit,
- file nào intentionally ignored.

Không có tình trạng:

> “Local có file nhưng GitHub không có mà không biết vì sao.”

---

# 5. Sửa 3 lỗi technical consistency quan trọng trong Streamlit/policy engine

Đây là hạng mục quan trọng nhất về correctness.

## 5.1. Qini đang gắn sai model name

### Vấn đề

Dashboard có thể ghi:

```text
Qini Curve — T-Learner Champion
```

nhưng `qini_curve.csv` lại được sinh từ R-Learner-style residual model.

Điều này tạo mâu thuẫn:

```text
README        → T-Learner
Dashboard     → T-Learner
Policy Engine → R-Learner-style
```

### Cách sửa

Chốt một model story duy nhất.

#### Nếu T-Learner là champion

Thì:

```text
qini_curve.csv
```

phải được sinh từ T-Learner prediction.

#### Nếu R-Learner là champion

Thì đồng bộ:

```text
README
Week5 Report
Decision Memo
Dashboard
Policy Engine
```

sang R-Learner.

### Tốt nhất

Có benchmark:

| Model | Qini | AUUC | CATE RMSE | Policy Value |
|---|---:|---:|---:|---:|
| S-Learner | | | | |
| T-Learner | | | | |
| X-Learner | | | | |
| R-Learner | | | | |

Sau đó chọn một champion theo tiêu chí rõ.

---

## 5.2. `true_ite` vs `true_cate`

### Vấn đề

Synthetic pipeline đã phân biệt:

```text
cate_true
=
E[Y1 - Y0 | X]

ite_realized
=
Y1 - Y0
```

Nhưng một số chỗ policy engine/dashboard có thể dùng:

```text
true_ite
```

trong khi nguồn thực chất là:

```text
cate_true
```

### Cách sửa

Nếu source là `cate_true`:

```text
true_ite
→ true_cate
```

UI nên ghi:

```text
Synthetic True CATE
```

hoặc:

```text
Known Causal Ground Truth
```

Oracle:

```text
Oracle Benchmark — Synthetic True CATE
```

Không gọi `cate_true` là realized ITE.

---

## 5.3. ROI formula không nhất quán

### Vấn đề

Một số chart tính:

```text
Incremental Profit
=
Incremental GMV × Margin
- Voucher Cost
```

nhưng chart khác lại:

```text
Incremental Profit
=
Incremental GMV
- Voucher Cost
```

tức bỏ contribution margin.

### Công thức nên thống nhất

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

### Cần kiểm tra

```text
Persona ROI
Recency ROI
Policy ROI
Simulator ROI
metric_specification.md
```

Tất cả phải cùng một định nghĩa.

---

# 6. A/B Result phải thể hiện rõ core statistical result

## Vấn đề

Dashboard hiện có xu hướng nhấn mạnh business outcome như:

```text
GMV
Burn
Net Profit
ROI
```

nhưng core project của mentor là experimentation/A-B testing.

A/B tab cần làm rõ:

> “Promotion có tạo incremental rides không?”

trước khi:

> “Incremental effect đó đáng giá bao nhiêu về business?”

## Layout nên dùng

### Primary causal result

```text
Control Mean Rides
Treatment Mean Rides
ATE Rides
95% Confidence Interval
p-value
```

### Business translation

```text
Incremental Rides
Incremental GMV
Burn
Incremental Profit
ROI
```

## Wording

Không nên gọi business box là:

```text
Statistical Interpretation
```

Nên:

```text
Business Interpretation
— under current sandbox economics assumptions
```

## Ý nghĩa

Story đúng:

```text
Randomized Experiment
→ ATE
→ uncertainty
→ business translation
```

Không nhảy thẳng từ treatment/control sang ROI.

---

# 7. Sửa logic Budget-Constrained Policy trong Policy Simulator

## Vấn đề

Nếu policy chỉ:

```text
sort expected_value descending
→ lấy cho tới hết budget
```

thì với budget lớn, model có thể tiếp tục target user có:

```text
Expected Value <= 0
```

Điều này không hợp logic profit-aware targeting.

Ngoài ra `Max Target %` cần được áp đồng thời với budget.

## Logic nên dùng

```text
1. Estimate Expected Value per user
2. Filter Expected Value > 0
3. Sort descending
4. Apply Max Target %
5. Apply Budget Constraint
6. Select users
```

## Constraints

```text
Total Burn <= Budget
```

và:

```text
Targeted Users <= Max Target %
```

## Mass policy

Nếu gọi:

```text
Mass Voucher
```

thì target:

```text
100% eligible users
```

Nếu chỉ target X% thì đổi tên:

```text
Broad Targeting — capped at X%
```

Không lấy arbitrary first rows.

---

# 8. Tách Predicted Policy Value và Synthetic Ground-Truth Policy Value

## Vấn đề

Synthetic sandbox có hai loại giá trị:

### Model belief

```text
Predicted CATE
→ Predicted Policy Value
```

### Known simulation truth

```text
True CATE
→ Ground-Truth Policy Value
```

Nếu policy table dùng ground truth nhưng lại gọi:

```text
Expected Incremental Profit
```

thì người xem có thể hiểu nhầm đó là model prediction.

## Cách hiển thị tốt hơn

| Policy | Predicted Value | Ground-Truth Value | Regret |
|---|---:|---:|---:|
| No Voucher | | | |
| Mass | | | |
| Segment | | | |
| Uplift | | | |
| Profit | | | |
| Budget-Constrained | | | |
| Oracle | N/A | | 0 |

## Oracle

Oracle chỉ là:

```text
Synthetic benchmark
```

không phải deployable policy.

## Badge nên dùng

```text
Synthetic-only
```

cạnh:

- True CATE,
- Ground-Truth Policy Value,
- Oracle,
- Policy Regret.

## Lợi ích

Đây thực ra là một điểm mạnh của project:

> Model đưa ra policy, còn simulator cho phép đo policy đó lệch bao nhiêu so với causal truth đã biết.

---

# 9. Sửa các report/documentation còn wording hoặc timeline cũ

## Vấn đề

Một số weekly report có thể còn:

- week number không khớp tên file,
- persona cũ,
- model champion cũ,
- “deploy ngay”,
- “hoàn hảo”,
- “tuyệt đối”,
- “ngừng hoàn toàn campaign”,
- production-like conclusion.

Điều này dễ làm mentor thấy repo thiếu consistency dù code đã tốt.

## Cần rà

### `Week5_Uplift_Modeling_Report.md`

Kiểm tra:

```text
Week number
Champion model
Target population
Persona names
Qini/AUUC
Policy conclusion
```

Nếu report nói:

```text
T-Learner champion
```

thì phải đồng bộ với code final.

Nếu chỉ target một persona trong phiên bản cũ nhưng current project uplift toàn eligible population, phải sửa.

### `Week6_Stress_Test_Report.md`

Không nên kết luận:

```text
sẵn sàng deploy diện rộng
độ tin cậy tuyệt đối
```

Nên:

> Các stress tests hiện tại không phát hiện failure nghiêm trọng trong các simulation scenarios đã kiểm tra. Việc áp dụng thực tế vẫn cần randomized production validation và kiểm tra operational constraints.

### `experiment_specification.md`

Nếu có các thông số như:

```text
voucher %
voucher cap
holdout %
launch quarter
rollout %
```

mà mentor/business chưa xác nhận:

Nên ghi:

```text
Illustrative / Hypothetical Parameters
```

Không gọi là GSM official parameters.

### `Decision_Memo.md`

Nên có rõ:

```text
What We Can Claim
What We Cannot Claim
```

Ví dụ:

**Can claim**

```text
Pipeline recovers treatment effects in controlled simulation.
Policy evaluation can compare targeting strategies under assumed economics.
```

**Cannot claim**

```text
Real GSM promotion causal effect.
Official GSM ROI.
Production rollout readiness.
```

---

# 10. Thứ tự ưu tiên nếu không muốn sửa tất cả ngay

## P0 — nên sửa trước mentor technical review

```text
1. Qini / champion model consistency
2. True CATE terminology
3. ROI formula
4. A/B Result: ATE + CI + p-value
5. Policy value predicted vs truth
6. Budget policy logic
```

## P1 — repo professionalism

```text
7. Root cleanup
8. docs cleanup
9. report wording consistency
10. .gitignore
```

## P2 — polish

```text
Real vs Synthetic charts
semantic colors
tooltips
folder refactor
```

---

# 11. Những gì KHÔNG cần làm thêm

Không cần mở scope sang:

```text
Driver agent
Marketplace ABM
MARL
Surge pricing
GPS optimization
Full MLOps
Production API
React/Vercel rewrite
```

Project hiện không thiếu thêm thuật toán.

Bottleneck cuối là:

```text
correctness
consistency
documentation
presentation
```

---

# 12. Khi nào có thể coi là hoàn thiện?

## Demo-ready

Có thể gửi link Streamlit ngay nếu:

```text
[ ] public
[ ] Incognito mở được
[ ] không tab chính nào lỗi
[ ] không thiếu file
```

## Repo-review-ready

Nên thêm:

```text
[ ] root sạch
[ ] tech doc W4 có mặt
[ ] legacy docs archive
[ ] model champion thống nhất
[ ] True CATE terminology thống nhất
[ ] ROI thống nhất
[ ] A/B statistical output đầy đủ
[ ] policy semantics đúng
[ ] no production overclaim
```

---

# 13. Kết luận

Chín hạng mục trên không có nghĩa project chưa dùng được.

Streamlit deploy thành công và chạy ổn đã đủ để:

```text
send demo link
```

Những cải thiện này nhằm nâng project từ:

```text
working internship prototype
```

lên:

```text
clean, technically consistent, mentor-review-ready project
```

Ưu tiên cuối cùng nên là:

```text
1. Correctness
2. Consistency
3. Repo cleanup
4. Documentation
5. Presentation polish
```

Sau khi các điểm P0 đã được xử lý, nên dừng mở rộng scope và tập trung vào demo + tech doc + final presentation.
