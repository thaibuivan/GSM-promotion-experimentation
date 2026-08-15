# GSM Streamlit Dashboard — Final UI/UX Review & Improvement Guide

> **Mục tiêu tài liệu:** Tổng hợp chi tiết đánh giá giao diện Streamlit hiện tại của project `GSM-promotion-experimentation`, chỉ rõ phần nào đã ổn, phần nào chưa phản ánh đúng giá trị project, các lỗi UX/logic cần sửa, và thứ tự ưu tiên để đưa dashboard lên trạng thái final-review-ready.
>
> **Vai trò của tài liệu này:** Đây là **UI/UX audit riêng cho Streamlit dashboard**, dùng bổ sung cho:
>
> - `GSM_Promotion_Experimentation_MASTER_FINAL.md` — kiến trúc và framing chuẩn của toàn project.
> - `GSM_Repo_Audit_After_MASTER_FINAL.md` — audit repo tổng thể.
>
> Tài liệu này không thay thế hai file trên, mà đi sâu riêng vào **presentation layer / dashboard experience**.

---

# 1. Kết luận tổng thể

Giao diện Streamlit hiện tại:

- đã có cấu trúc hợp lý,
- có theme nhất quán,
- có interactive experiment setup,
- có experiment health,
- có business metrics,
- có policy simulator,
- có thể dùng để demo.

Tuy nhiên dashboard **chưa phản ánh tối đa điểm mạnh thực sự của project**, đặc biệt là phần:

```text
EDA
→ Empirical Calibration
→ Synthetic Causal Data
```

Trong khi đây lại là một trong những technical contributions lớn nhất.

Đánh giá định hướng:

```text
Visual Theme           ~8/10
Navigation             ~7/10
Data Storytelling      ~6/10
Experiment UX          ~8/10
Business Policy UX     ~8.5/10
Evidence Discipline    ~6.5/10
Final Presentation     ~7.5/10
```

Mục tiêu sau khi sửa:

> **Không redesign toàn bộ dashboard.**
>
> Giữ architecture hiện tại, nhưng cải thiện:
>
> 1. hierarchy,
> 2. wording,
> 3. consistency,
> 4. business/simulation boundary,
> 5. Data Foundation storytelling.

---

# 2. Cấu trúc dashboard hiện tại

Dashboard đang đi theo flow:

```text
Data Foundation
→ Experiment Setup
→ Experiment Health
→ A/B Result
→ Heterogeneity
→ Business Metrics
→ Policy Simulator
→ Admin Pipeline
```

Đây là flow đúng về logic.

Điểm cần cải thiện:

- 8 tab ngang hơi dày.
- `Tab 1`, `Tab 2`, ... không cần thiết.
- Admin Pipeline đang đứng ngang hàng với business tabs.
- Data Foundation chưa đủ trực quan.

---

# 3. Dashboard nên kể câu chuyện gì?

Storyline lý tưởng:

```text
REAL DATA
   ↓
DATA FOUNDATION
   ↓
CAUSAL SIMULATION
   ↓
EXPERIMENT DESIGN
   ↓
EXPERIMENT HEALTH
   ↓
A/B EFFECT
   ↓
HETEROGENEITY / UPLIFT
   ↓
GMV / BURN / ECONOMICS
   ↓
POLICY DECISION
```

Người review mở dashboard nên hiểu trong 30–60 giây:

> Đây không phải một dashboard campaign production.
>
> Đây là một **synthetic experimentation sandbox** dùng để validate toàn bộ chuỗi Data → Causal Evidence → Decision.

---

# 4. P0 — Title và framing phải sửa trước

Title hiện tại nếu mang cảm giác:

> “GSM Promotion Executive Dashboard”

hoặc:

> “Báo cáo Hiệu quả Chiến dịch Khuyến mãi GSM”

thì quá gần production dashboard thật.

Điều này mâu thuẫn với project boundary đã chốt.

## 4.1. Title đề xuất

### Option A — rõ nhất

> **Promotion Experimentation Sandbox**

Subtitle:

> *A/B Testing · Uplift Modeling · Policy Evaluation*

### Option B — technical hơn

> **Ride-Hailing Promotion Experimentation & Uplift Sandbox**

### Option C — giữ context internship

> **GSM-Inspired Promotion Experimentation Sandbox**

Không nên dùng title khiến người đọc nghĩ:

> Đây là dashboard production của GSM.

---

# 5. Sandbox Banner

Ngay dưới title nên có một banner rõ:

```text
🧪 Synthetic Experimentation Sandbox

Results shown here are generated from public/reference data
and synthetic causal assumptions.
They are not GSM production estimates.
```

Hoặc tiếng Việt:

> **🧪 Môi trường mô phỏng nhân quả**
>
> Các kết quả trong dashboard được tạo từ public/reference data và synthetic causal assumptions, không phải kết quả production của GSM.

Đây là một trong những UI elements quan trọng nhất về evidence discipline.

---

# 6. Navigation — 8 tabs có thể giữ nhưng nên tinh gọn

Không cần:

```text
Tab 1:
Tab 2:
Tab 3:
```

Nên:

```text
📚 Data Foundation
📏 Experiment Setup
🩺 Experiment Health
📊 A/B Results
🎯 Heterogeneity
💰 Policy Evaluation
⚙️ Simulator
🛠 Developer Tools
```

Nếu muốn polish thêm có thể nhóm thành 4 section:

```text
DATA
├── Data Foundation

EXPERIMENT
├── Setup
├── Health
└── A/B Results

LEARNING & DECISION
├── Heterogeneity
├── Policy Evaluation
└── Simulator

DEVELOPER
└── Admin Tools
```

Nhưng không bắt buộc phải refactor navigation lớn nếu thời gian ít.

---

# 7. Tab Data Foundation — phần cần cải thiện mạnh nhất

Đây là tab hiện chưa tương xứng với khối lượng công việc thực tế.

Nếu hiện chỉ render:

```text
EDA_Simulation_Mapping.md
Calibration_Scorecard.md
```

thì người xem sẽ cảm giác:

> “Đây là nơi đọc tài liệu.”

Trong khi thực tế đây là:

> **Data & Simulation validation module.**

---

# 8. Data Foundation nên mở bằng KPI cards

Gợi ý:

```text
3.04M
Clean Trips

20K
Synthetic Users

Known Ground Truth
Y0 / Y1 / CATE

Calibration
PASS / REVIEW
```

Các giá trị phải lấy đúng từ pipeline/report hiện tại.

Mục tiêu:

> Người review nhìn ngay được quy mô và cấu trúc dữ liệu.

---

# 9. Data Foundation nên có architecture visual

Một sơ đồ đơn giản:

```text
NYC TLC
   ↓
Data Quality & EDA
   ↓
Empirical Pattern Extraction
   ↓
Synthetic User Population
   ↓
Y0 / CATE / Y1
   ↓
Randomized Experiment
```

Có thể dùng:

- `st.markdown`
- columns
- cards
- simple Mermaid nếu có hỗ trợ
- HTML block nhẹ

Không cần visualization phức tạp.

---

# 10. Real vs Synthetic Comparison

Data Foundation nên có ít nhất 2–3 chart.

Ưu tiên:

## Chart 1 — Fare distribution

```text
Real
vs
Synthetic
```

## Chart 2 — Hour-of-day pattern

```text
Real demand pattern
vs
Synthetic preferred/activity pattern
```

## Chart 3 — Calibration status

Bar/table:

```text
Variable
Target
Synthetic
Gap
Status
```

---

# 11. Assumption Registry

Một expander nên có:

> **What is empirical vs assumed?**

Bảng:

| Feature / Mechanism | Source |
|---|---|
| Fare | TLC empirical |
| Hour distribution | TLC empirical |
| Airport behavior | TLC-inspired |
| Age | Assumption |
| Income | Assumption |
| Treatment effect | Explicit causal assumption |
| Rain response | Assumption |
| Voucher bias | Simulation assumption |

Đây là phần rất mạnh về credibility.

---

# 12. Markdown methodology nên để trong expander

Thay vì render toàn bộ Markdown ngay:

```text
[View EDA → Simulation Mapping]
[View Calibration Details]
```

dùng:

```python
with st.expander("Methodology details"):
    ...
```

Như vậy:

- dashboard vẫn sạch,
- methodology vẫn accessible,
- không biến UI thành document viewer.

---

# 13. Experiment Setup — phần hiện tại khá tốt

MDE/Power calculator là một trong những phần thực chiến.

Nên giữ các input:

```text
Baseline Mean
Standard Deviation
MDE
Confidence Level
Power
Treatment Ratio
```

Output:

```text
Required Sample Size
Expected Group Size
Estimated Duration
```

---

# 14. Wording ở Experiment Setup

Không nên:

> “Đạt chuẩn thống kê.”

Nên:

> “Đạt target power dưới assumptions hiện tại.”

Hoặc:

> “Estimated sample size required for the selected MDE and power.”

Lý do:

> Power calculation phụ thuộc assumptions.

---

# 15. P0 bug — Treatment Ratio và SRM chưa đồng bộ

Nếu Experiment Setup cho phép:

```text
Treatment Ratio = 30%
```

nhưng Experiment Health vẫn dùng:

```python
expected = [total / 2, total / 2]
```

thì SRM logic sai.

Ví dụ:

```text
Designed ratio = 30/70
Observed ratio = 30.5/69.5

Health module kiểm 50/50
→ báo SRM failure
```

Trong khi experiment thực ra đúng.

---

# 16. Cách sửa SRM

Treatment ratio phải được lưu vào:

```text
session_state
```

hoặc:

```text
experiment config
```

Ví dụ logic:

```python
treatment_ratio = st.session_state["treatment_ratio"]

expected_t = total * treatment_ratio
expected_c = total * (1 - treatment_ratio)
```

Tất cả:

- sample size,
- SRM,
- group expected count,
- power,

phải dùng chung một experiment specification.

---

# 17. Experiment Health — wording cần giảm tuyệt đối hóa

Không nên:

- hoàn toàn ngẫu nhiên
- công bằng tuyệt đối
- hoàn toàn tương đồng
- cân bằng hoàn hảo

Nên:

> “Không phát hiện sample-ratio mismatch đáng kể dưới designed allocation.”

> “Không phát hiện pre-treatment imbalance đáng kể theo ngưỡng SMD đã chọn.”

---

# 18. Experiment Health nên có PASS / REVIEW / FAIL

UI có thể hiển thị:

```text
SRM               PASS
Covariate Balance PASS
Exposure Integrity REVIEW
A/A Calibration   PASS
```

Tổng:

```text
EXPERIMENT HEALTH
PASS
```

Hoặc:

```text
REVIEW REQUIRED
```

Điều này rõ hơn cho business user.

---

# 19. Semantic colors

Nên cố định meaning:

```text
Green  = PASS / Positive
Orange = REVIEW / Warning
Red    = FAIL / Negative
Gray   = Baseline / Control
Cyan   = Treatment / Main selected policy
```

Không nên dùng cyan/pink chỉ vì đẹp nếu semantic không nhất quán.

---

# 20. A/B Result — nên làm sạch

Hiện tab này nếu có:

- Incremental GMV
- Burn
- Net Profit
- Persona
- segment profile

thì đang trộn:

```text
Causal Result
+
Segmentation
+
Economics
```

Nên tách.

---

# 21. A/B Results nên chỉ trả lời causal question

Header:

> **Average Treatment Effect**

Cards:

```text
Control Mean
Treatment Mean
ATE
95% CI
p-value
Incremental Rides
Incremental GMV
```

Chart:

```text
Treatment vs Control
with CI
```

---

# 22. Statistical Decision Box

Ví dụ:

```text
STATISTICAL INTERPRETATION

Positive effect detected
95% CI excludes 0
```

hoặc:

```text
Uncertain
Point estimate positive but CI crosses 0
```

Không nên nhảy thẳng sang:

> Rollout.

---

# 23. Outcome Horizon cần hiển thị rõ

Repo hiện có dấu hiệu dùng cả:

```text
14-day outcome
```

và:

```text
30-day gross revenue
```

Dashboard phải ghi rõ:

```text
Outcome Window: 14 days
```

hoặc:

```text
Revenue Window: 30 days
```

Nếu hai metric dùng hai horizon khác nhau, cần label riêng.

Không để người dùng đoán.

---

# 24. K-Means nên chuyển hoàn toàn sang Heterogeneity

K-Means không nên nằm sâu trong A/B Results.

A/B:

> average effect.

K-Means:

> behavioral segmentation.

Uplift:

> individual treatment response.

Do đó:

```text
A/B Result
→ ATE

Heterogeneity
→ Segment ATE
→ Persona
→ CATE
```

---

# 25. Heterogeneity — giữ nội dung nhưng sửa tone

Các headline kiểu:

> “Vạch trần đốt tiền”

hoặc:

> “Phải ngừng phát voucher cho khách ruột”

không phù hợp với synthetic sandbox.

Dù catchy, chúng làm project mất credibility.

---

# 26. Heterogeneity title đề xuất

> **Heterogeneous Treatment Response**

Subtitle:

> How treatment response varies across personas and predicted CATE groups.

---

# 27. Insight wording đề xuất

Thay:

> “Phải ngừng phát voucher cho nhóm khách ruột.”

Bằng:

> **Trong synthetic DGP hiện tại, một số high-frequency personas có incremental response thấp hơn less-active personas. Kết quả này minh họa cannibalization risk trong simulation và không được diễn giải trực tiếp thành GSM production policy.**

Đây là cách nói chuyên nghiệp hơn.

---

# 28. Persona cards

Có thể giữ.

Mỗi persona:

```text
Persona Name
Size
Baseline Rides
ATE
Observed Uplift
Predicted CATE
Burn Efficiency
```

Nhưng nên ghi rõ:

> Persona = descriptive layer.

Không phải causal truth.

---

# 29. Uplift chart — không hard-code model name

Nếu chart đang ghi:

```text
Qini Curve (R-Learner)
```

trong khi repo có:

- S-Learner
- T-Learner
- X-Learner
- R-Learner-style

thì model name phải lấy từ benchmark/champion config.

Ví dụ:

```python
champion_model_name = model_registry["champion"]
```

UI:

> `Qini Curve — {champion_model_name}`

---

# 30. Champion Model Card

Sau khi chốt benchmark:

```text
CHAMPION MODEL
X-Learner

AUUC: ...
Qini: ...
CATE RMSE: ...
Policy Value: ...
```

Bên dưới:

> Selected based on out-of-sample policy/model criteria.

Không chọn champion chỉ theo một metric duy nhất.

---

# 31. Business Metrics — tab hiện tốt nhất

Đây nên trở thành nơi business decision được trình bày rõ.

Giữ:

- Incremental GMV
- Burn
- Burn/GMV
- Burn/Incremental GMV
- Incremental Rides
- CPIR
- Expected Profit
- ROI
- Oracle Regret

---

# 32. Policy Comparison — sửa naming

Nếu hiện title:

> “So sánh 5 Policy”

nhưng bảng có:

```text
No Voucher
Mass
Segment
Uplift
Profit
Budget-Constrained
Oracle
```

thì thực tế là 7 rows.

Nên gọi:

> **Policy Comparison**

Subtitle:

> 5 candidate targeting strategies + baseline + oracle benchmark

Ví dụ:

```text
Baseline:
No Voucher

Candidate Policies:
Mass
Segment
Uplift
Profit
Budget-Constrained

Benchmark:
Oracle
```

---

# 33. Predicted vs Ground-Truth Policy Value

Đây là một trong những chỉnh sửa quan trọng nhất.

Nếu simulator dùng `true_ite` để evaluate policy selected by model, thì output phải tách:

```text
Predicted Policy Value
```

và:

```text
Ground-Truth Policy Value
Synthetic Only
```

Sau đó:

```text
Policy Value Error
```

---

# 34. Vì sao cần tách?

Nếu chỉ ghi:

```text
Profit = $...
```

người xem có thể hiểu:

> model dự đoán profit thật.

Trong khi thực tế:

> policy được chọn bởi model, nhưng value được chấm bằng synthetic ground truth.

Đây là điểm rất hay của sandbox, nên phải **khoe đúng cách**, không che đi.

---

# 35. Business Metrics should show confidence/uncertainty

Nếu có CI:

```text
Incremental Profit
$100k
95% CI [$30k, $170k]
```

sẽ mạnh hơn point estimate đơn thuần.

Decision box:

```text
Business Decision:
Positive under current assumptions
```

không nên:

> Deploy now.

---

# 36. Policy Simulator — architecture hiện đúng

Layout đề xuất giữ:

```text
LEFT
Budget
Voucher
Margin
Redemption
Max Target %

RIGHT
Policy Comparison
Expected Outcome
```

Đây là tab tương tác tốt.

---

# 37. Policy Simulator input cần ghi rõ “Assumption”

Các input như:

```text
Voucher Value
Contribution Margin
Burn
Budget
```

nên có tooltip:

> Scenario assumption — not official GSM value.

Đặc biệt với GMV/Burn vì current project chưa có internal metric definition chính thức.

---

# 38. Simulator nên hỗ trợ scenario comparison

Ví dụ:

```text
Scenario A — Low Burn
Scenario B — Base
Scenario C — High Burn
```

Output:

```text
Best Policy
Target %
Incremental Rides
Incremental GMV
Burn
Profit
```

Điều này làm stress-test/business robustness rõ hơn.

---

# 39. Policy Frontier

Optional nhưng rất đẹp:

```text
Voucher Cost × Margin
→ Best Policy
```

Heatmap hoặc matrix.

Ví dụ:

| Burn | Margin | Best Policy |
|---:|---:|---|
| Low | High | Uplift |
| Medium | High | Profit |
| High | Medium | Selective |
| Very High | Low | No Promotion |

---

# 40. Admin Pipeline — nên hạ xuống Developer Tools

Hiện Admin Pipeline không nên đứng ngang với:

- A/B Results
- Policy Evaluation

Nên đổi thành:

```text
🛠 Developer Tools
```

và đặt cuối.

Trong đó:

```text
Run Data Pipeline
Run Policy Engine
Refresh Results
View Logs
```

---

# 41. Không để business user chạy pipeline nhầm

Nếu button:

> Run Full Pipeline

nằm quá nổi bật thì mentor/demo dễ bấm nhầm.

Nên có:

```text
Developer Mode
```

hoặc expander:

> Advanced / Developer Tools

---

# 42. Theme — giữ nguyên

Dark navy + cyan hiện phù hợp với dashboard DS/AI.

Không cần redesign toàn bộ.

Nên giữ:

```text
Primary Background:
Dark Navy

Primary Accent:
Cyan
```

Nhưng phải dùng color semantic có kỷ luật.

---

# 43. Typography hierarchy

Nên có 4 cấp rõ:

```text
Page Title
Section Title
Metric Card
Supporting Text
```

Không dùng quá nhiều:

- bold,
- emoji,
- bright color,

trên cùng một khu vực.

---

# 44. Emoji

Hiện emoji dùng khá nhiều.

Có thể giữ vì Streamlit.

Nhưng nên giới hạn:

```text
📚 Data
📏 Setup
🩺 Health
📊 Results
🎯 Heterogeneity
💰 Policy
⚙️ Simulator
🛠 Developer
```

Không cần thêm emoji vào mọi subheader.

---

# 45. Card hierarchy

Mỗi tab chỉ nên có:

```text
3–5 primary KPI cards
```

Sau đó chart/table.

Nếu card quá nhiều, user không biết metric nào là chính.

---

# 46. Tooltip / help text

Các metric nên có `help=`:

### ATE

> Average Treatment Effect on the selected outcome.

### Burn/GMV

> Promotion burn divided by total GMV under the current simulation assumptions.

### CPIR

> Burn per incremental ride.

### Oracle Regret

> Gap between learned policy value and synthetic oracle policy value.

Điều này rất quan trọng khi mentor không chuyên sâu causal/uplift.

---

# 47. Simulation Badge trên các metric synthetic-only

Các metric:

```text
True CATE
Oracle Policy
Oracle Regret
Ground-Truth Policy Value
```

nên có label:

> `Synthetic-only`

hoặc:

> `Ground truth available only in simulation`

---

# 48. Dashboard landing summary

Ngay đầu app nên có một short summary:

```text
PROJECT FLOW

Data Foundation
→ Experimentation
→ Uplift
→ Policy Evaluation
```

và:

```text
Current Dataset:
Synthetic causal population

Core Mentor Scope:
A/B Testing

Extension:
Uplift & Policy Evaluation
```

Điều này giúp reviewer hiểu scope ngay.

---

# 49. Suggested final navigation

Nếu giữ 8 tabs:

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

Đây là layout tôi khuyên dùng.

---

# 50. Final Data Foundation layout

```text
TITLE
Data Foundation & Causal Simulation

KPI CARDS
Clean Trips | Synthetic Users | Ground Truth | Calibration Status

FLOW
Real Data → EDA → Calibration → Synthetic Population → Y0/CATE/Y1

CHARTS
Real vs Synthetic Fare
Real vs Synthetic Time Pattern

TABLE
Calibration Scorecard

EXPANDERS
EDA → Simulation Mapping
Assumption Registry
Methodology Details
```

---

# 51. Final Experiment Setup layout

```text
TITLE
Experiment Design

LEFT
Baseline
Variance
MDE
Power

RIGHT
Treatment Ratio
Outcome Window
Eligibility

OUTPUT
Required N
Group Size
Estimated Duration
```

---

# 52. Final Experiment Health layout

```text
TITLE
Experiment Health

STATUS CARDS
SRM
Balance
Exposure
A/A Calibration

OVERALL STATUS
PASS / REVIEW / FAIL

DETAILS
SMD chart
Assignment ratio
A/A p-value distribution
```

---

# 53. Final A/B Results layout

```text
TITLE
Average Treatment Effect

CARDS
Control Mean
Treatment Mean
ATE
95% CI
p-value

BUSINESS EFFECT
Incremental Rides
Incremental GMV

DECISION BOX
Positive / Uncertain / No Effect
```

---

# 54. Final Heterogeneity layout

```text
TITLE
Heterogeneous Treatment Response

PERSONA OVERVIEW

SEGMENT ATE

CHAMPION UPLIFT MODEL

QINI / AUUC

CATE CALIBRATION

DECILE TABLE
```

---

# 55. Final Policy Evaluation layout

```text
TITLE
Policy Comparison

TABLE
No Voucher
Mass
Segment
Uplift
Profit
Budget-Constrained
Oracle

KPI
Incremental GMV
Burn
CPIR
Profit
ROI
Regret
```

---

# 56. Final Policy Simulator layout

```text
TITLE
Scenario-Based Policy Simulator

INPUT
Budget
Voucher Value
Burn
Margin
Target Cap

OUTPUT
Best Policy
Targeted Users
Incremental Rides
Incremental GMV
Burn
Profit
ROI

GROUND TRUTH
Synthetic-only evaluation
```

---

# 57. P0 fixes trước khi final demo

- [ ] Đổi title thành sandbox framing.
- [ ] Thêm synthetic disclaimer banner.
- [ ] Fix SRM dynamic treatment ratio.
- [ ] Sửa absolute wording trong Health/Heterogeneity.
- [ ] Tách K-Means khỏi A/B Results.
- [ ] Không hard-code R-Learner.
- [ ] Tách Predicted vs Ground-Truth Policy Value.
- [ ] Hiển thị rõ outcome horizon.
- [ ] Đổi “5 Policy” thành Policy Comparison.
- [ ] Hạ Admin thành Developer Tools.

---

# 58. P1 fixes để nâng dashboard rõ rệt

- [ ] Data Foundation KPI cards.
- [ ] Real vs Synthetic charts.
- [ ] Calibration scorecard UI.
- [ ] Assumption Registry.
- [ ] Experiment Health PASS/REVIEW/FAIL.
- [ ] Champion model card.
- [ ] Metric tooltips.
- [ ] Synthetic-only badges.
- [ ] CI propagation cho economics.

---

# 59. P2 polish

- [ ] Scenario comparison.
- [ ] Policy frontier.
- [ ] Better responsive layout.
- [ ] Reduce unnecessary emoji.
- [ ] Standardized semantic colors.
- [ ] Download result summary.
- [ ] Export decision memo.

---

# 60. Những gì không cần làm

Không cần:

- redesign UI framework,
- chuyển sang React,
- custom frontend,
- phức tạp hóa CSS,
- tạo production auth,
- tạo production database,
- thêm MLOps controls.

Streamlit đủ cho mục tiêu internship prototype.

---

# 61. Final UI framing

Dashboard nên được định vị là:

> **Interactive Simulation & Decision-Support Prototype**

Không phải:

> Production Promotion Dashboard.

---

# 62. Câu nên đặt ở landing page

> **From Data Foundation to Causal Decision-Making**
>
> This sandbox demonstrates how public/reference mobility patterns can be transformed into synthetic causal data, validated through randomized experimentation, extended with uplift modeling, and translated into promotion policy evaluation under configurable business assumptions.

---

# 63. Final Evaluation

Dashboard hiện tại đã có foundation tốt.

Điểm mạnh:

```text
Experiment Setup
Experiment Health
Business Metrics
Policy Simulator
```

Điểm chưa tốt nhất:

```text
Data Foundation storytelling
Evidence wording
Model consistency
Ground-truth labeling
```

Nếu xử lý đúng các mục trên, dashboard sẽ phản ánh đúng hơn bản chất project:

```text
Data
→ Causal Simulation
→ Experiment
→ Uplift
→ Business Policy
```

thay vì trông như:

```text
Campaign Dashboard
```

---

# 64. Final Priority Order

Nếu chỉ có thời gian sửa theo thứ tự:

```text
1. Data Foundation visualization
2. Sandbox title + disclaimer
3. SRM ratio bug
4. Wording cleanup
5. A/B / Heterogeneity separation
6. Champion model consistency
7. Ground-truth vs predicted value
8. Outcome horizon consistency
9. Policy naming
10. Developer tools cleanup
```

---

# 65. Final Conclusion

Không cần xây lại Streamlit app.

Khung hiện tại đã đúng.

Việc cần làm là chuyển dashboard từ:

> **“một app có nhiều tab và metric”**

thành:

> **“một coherent experimentation story: Real Data → Synthetic Causal World → A/B Evidence → Uplift → Burn-Aware Policy Decision.”**

Đặc biệt, phần **Data Foundation phải được nâng lên rõ rệt**, vì đây là phần nặng, khó và có giá trị lớn trong project nhưng giao diện hiện tại chưa thể hiện đủ.

Sau khi hoàn thiện các P0/P1 trong tài liệu này, dashboard sẽ phù hợp hơn nhiều cho final presentation với mentor/team.
