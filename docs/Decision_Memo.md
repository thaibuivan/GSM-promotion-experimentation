# DECISION MEMO: Promotion Policy Recommendation (Synthetic Sandbox)

**Subject:** Đánh giá hiệu quả chiến dịch khuyến mãi trong môi trường mô phỏng  
**Scope:** Prototype trên Synthetic Causal Data — Kết quả cần validation trên dữ liệu GSM thật trước khi áp dụng thực tế

---

## A. Decision Question
Với budget giới hạn và promotion economics giả định, policy nào tối đa hóa **incremental GMV** và **incremental profit**, đồng thời đảm bảo hiệu quả đốt tiền (**Burn Efficiency / CPIR**) trên eligible population?

---

## B. Evidence (Bằng chứng đã được kiểm chứng)

### B.1. Kiểm định Nền tảng A/B (A/A Trust Checks)
Pipeline randomization đã được kiểm định qua 5.000 vòng lặp Monte Carlo:
- **SRM Check:** Tỷ lệ cảnh báo 5.26% — nằm trong vùng phương sai ngẫu nhiên kỳ vọng (Binomial P-value = 0.3988). Không phát hiện mismatch đáng kể.
- **Covariate Balance (SMD):** Tất cả biến kiểm soát có |SMD| < 0.1. Không phát hiện material imbalance trên các observed pre-treatment covariates trong settings đã thử.
- **False Positive Rate:** 5.08% — phù hợp với ngưỡng lý thuyết α = 0.05.
- **Kết luận:** Không phát hiện randomization/statistical calibration issue đáng kể dưới các thiết lập mô phỏng đã kiểm tra.

### B.2. A/B Effect Estimation (trong Synthetic Sandbox)
Kết quả A/B Test trên synthetic data với assumptions HTE đã thiết kế:

| Persona | N Users | ATE | ROI (dưới assumptions) | Kết luận trong Sandbox |
|---|---|---|---|---|
| Urban Regulars | 8,568 | +0.79 | -69.3% | Chi phí voucher lớn hơn lợi nhuận tăng thêm |
| Rain Riders | 2,651 | +0.91 | -71.4% | Phản ứng dương nhưng economics vẫn âm |
| Airport Business | 720 | +0.00 | -106.8% | Không tạo uplift trong DGP hiện tại |
| Suburban Card | 5,381 | +0.87 | -12.0% | Tốt hơn mass voucher nhưng vẫn âm |
| Suburban Cash | 2,680 | +0.75 | -15.1% | Tốt hơn mass voucher nhưng vẫn âm |

### B.3. Uplift Model Evaluation
- Champion hiện tại là **simplified R-Learner-style residual model**: model đầu học `m(X)`, sau đó residualization và model thứ hai học `τ(X)`. Chưa có cross-fitting, nên không gọi là full DML.
- Mô hình có useful ranking signal, trong khi CATE level calibration vẫn chưa hoàn hảo.
- Profit Targeting: Nhắm mục tiêu 873 / 4.000 users (21,8%).
- Predicted Profit: ≈ $6.369.
- Synthetic Causal Benchmark: ≈ $6.579.
- Oracle Benchmark: ≈ $9.063.
- Oracle Regret: ≈ $2.484 (27,4%).

---

## C. Recommendation IN SANDBOX
Trong synthetic sandbox với assumptions hiện tại về treatment effect, voucher cost và contribution margin:

> **Profit-based Uplift Targeting** cho policy value tốt hơn Mass Voucher và Segment Targeting trong sandbox hiện tại.

Mức voucher giả định 15% không cap → lọc theo Expected Value > 0 → áp dụng greedy budget heuristic → Predicted Profit khoảng $6.369 trong sandbox. Với budget $50.000 hiện tại, budget không binding nên policy ngân sách trùng với Profit Targeting.

---

## D. Conditions Required (Điều kiện để kết luận đúng)
- Margin per incremental ride ≈ 0.70 × average fare (assumption hiện tại)
- Voucher cost mỗi chuyến = 15% average fare, không cap (synthetic assumption hiện tại, không phải chính sách GSM)
- Simplified R-Learner-style residual model có useful ranking signal trong held-out synthetic test set; CATE level calibration vẫn còn imperfect và cần được theo dõi.
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
