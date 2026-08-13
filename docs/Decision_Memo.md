# DECISION MEMO: Promotion Policy Recommendation (Synthetic Sandbox)

**Subject:** Đánh giá hiệu quả chiến dịch khuyến mãi trong môi trường mô phỏng  
**Scope:** Prototype trên Synthetic Causal Data — Kết quả cần validation trên dữ liệu GSM thật trước khi áp dụng thực tế

---

## A. Decision Question
Với budget giới hạn và voucher economics giả định, policy nào tối đa hóa **incremental profit** (doanh thu tăng thêm trừ chi phí voucher) trên eligible population?

---

## B. Evidence (Bằng chứng đã được kiểm chứng)

### B.1. Kiểm định Nền tảng A/B (A/A Trust Checks)
Pipeline randomization đã được kiểm định qua 5.000 vòng lặp Monte Carlo:
- **SRM Check:** Tỷ lệ cảnh báo 5.26% — nằm trong vùng phương sai ngẫu nhiên kỳ vọng (Binomial P-value = 0.3988). Không phát hiện mismatch đáng kể.
- **Covariate Balance (SMD):** Tất cả biến kiểm soát có |SMD| < 0.1. Không phát hiện selection bias trong settings đã thử.
- **False Positive Rate:** 5.08% — phù hợp với ngưỡng lý thuyết α = 0.05.
- **Kết luận:** Không phát hiện randomization/statistical calibration issue đáng kể dưới các thiết lập mô phỏng đã kiểm tra.

### B.2. A/B Effect Estimation (trong Synthetic Sandbox)
Kết quả A/B Test trên synthetic data với assumptions HTE đã thiết kế:

| Persona | N Users | ATE | ROI (dưới assumptions) | Kết luận trong Sandbox |
|---|---|---|---|---|
| Urban Regulars | 8,424 | +1.00 | -40.7% | Mass voucher gây cannibalization |
| Rain Riders | 2,592 | +0.86 | -38.9% | Phụ thuộc thời tiết, chi phí > lợi nhuận |
| Airport Business | 1,131 | +1.21 | -18.0% | ATE dương nhưng margin không bù voucher cost |
| **Suburban Card** | 2,792 | +1.04 | **+20.7%** | Phù hợp assumptions — ROI dương trong sandbox |
| **Suburban Cash** | 5,061 | +0.79 | **+24.7%** | Phù hợp assumptions — ROI dương trong sandbox |

### B.3. Uplift Model Evaluation
- X-Learner (XGBoost) cho profit tốt nhất ở top 30-50% population.
- Profit Targeting (rank theo Expected Value_i = CATE_i × Margin − Voucher Cost) vượt trội Segment Targeting thuần.
- Oracle Regret so với true ITE: [xem notebook Week5].

---

## C. Recommendation IN SANDBOX
Trong synthetic sandbox với assumptions hiện tại về treatment effect, voucher cost và contribution margin:

> **Profit-based Uplift Targeting** (rank toàn eligible population theo Expected Incremental Value, phát đến hết budget) cho policy value tốt hơn Mass Voucher và Segment Targeting.

Mức Voucher giả định 15% → Top 30-50% population → Expected Incremental Profit ~$10,500 (trong sandbox).

---

## D. Conditions Required (Điều kiện để kết luận đúng)
- Margin per incremental ride ≈ 0.75 × average fare (assumption hiện tại)
- Voucher cost = 15% of user's average revenue (assumption hiện tại)
- Uplift model được calibrated đúng (predicted CATE ≈ observed uplift)
- SUTVA: không có marketplace interference
- Eligible population có cùng DGP distribution như training data

---

## E. What We Cannot Claim (Giới hạn bằng chứng)
- **Không** chứng minh khách hàng thật của GSM có treatment response như đã mô phỏng
- **Không** khẳng định các ROI trên là achievable trong vận hành thực tế
- **Không** thể rollout policy này mà không có pilot experiment trên real GSM data
- Kết quả A/A chỉ xác nhận pipeline hoạt động đúng trong settings đã thử, không chứng minh production correctness

---

## F. Next Real Experiment (Bước tiếp theo nếu có GSM data)
Để kiểm chứng recommendations trên trong thực tế, cần:

1. **Experiment Design:**
   - Eligibility: xác định eligible population thực tế
   - Randomization unit: user-level
   - Treatment ratio: 50/50 (hoặc 80/20 với holdout)
   - Exposure window: 14 ngày
   - Outcome window: 30 ngày

2. **MDE & Sample Size:**
   - Baseline rides/user: đo từ GSM data thật
   - Desired MDE: ≥ 0.5 rides/user incremental
   - Power = 0.8, α = 0.05

3. **Trust Checks:** SRM, Covariate Balance, Invariant Metrics

4. **Primary Metric:** Incremental rides per eligible user

5. **Guardrails:** Voucher cost per user, cancellation rate, completion rate

6. **Champion–Challenger:** So sánh Segment Targeting (champion) vs Profit-based Uplift Targeting (challenger) trên split traffic

---

*Document này là output của synthetic simulation. Tất cả số liệu phản ánh kết quả trong sandbox với assumptions đã thiết kế, không phải dữ liệu vận hành thực tế của GSM.*
