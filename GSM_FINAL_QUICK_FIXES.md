# GSM Promotion Experimentation — Final Quick Fixes

> Repo hiện đã đủ tốt để demo và gần sẵn sàng mentor/PM review. Chỉ sửa nốt các điểm dưới đây rồi freeze repo.

## 1. Bỏ claim Early Stopping trong Week5 report
`Week5_Uplift_Modeling_Report.md` đang nói Validation được dùng cho Early Stopping, nhưng code hiện không dùng `eval_set` hay `early_stopping_rounds`.

Sửa thành:
> Dữ liệu được chia Train 60%, Validation 20%, Test 20%; Test set được giữ riêng cho final evaluation. Validation split được reserved cho model selection/tuning.

## 2. Chuẩn hóa “Ground-Truth Profit”
Policy engine hiện dùng True CATE nhưng voucher cost vẫn dựa trên predicted treated rides, nên chưa phải ground truth economics hoàn toàn.

Cách nhanh: đổi label thành:
- `Synthetic Causal Benchmark Profit`
- hoặc `CATE-Grounded Policy Value`

Chỉ gọi `Ground-Truth Expected Profit` nếu cost cũng được tính từ expected treated outcome của DGP.

## 3. Không trộn Predicted Policy Value với Oracle Truth trên cùng chart
Nên tách:
- **Chart A — Decision-time view:** Predicted Profit của Mass / Segment / Uplift / Profit / Budget.
- **Chart B — Synthetic benchmark:** Synthetic Benchmark Value của các policy + Oracle.

Mục tiêu: tách rõ *model thinks what is best* và *what is best under known synthetic truth*.

## 4. Mass Voucher phải luôn = 100% eligible population
Trong Simulator, `Mass Voucher` không nên bị `Max Target %` giới hạn.

Nên dùng:
```python
mass_mask = pd.Series(True, index=preds_df.index)
```

`Max Target %` chỉ áp cho Profit Targeting và Budget-Constrained Policy.

## 5. Sửa Calibration Scorecard: ATE ~1.0 → ~0.8
DGP hiện calibrate:
```text
TARGET_ATE = 0.8 rides / 30 days
```
Vì vậy scorecard nên ghi:
```text
Expected ATE ≈ 0.8 rides / 30 days
```

## 6. Dọn `.gitignore`
Xóa rule lặp, giữ một block gọn cho:
```text
venv/
.venv/
__pycache__/
*.pyc
.ipynb_checkpoints/
.env
data/raw/
*.parquet
```
Đảm bảo không làm mất các demo assets Streamlit đang cần.

## 7. Cập nhật Tech Doc W4 về horizon
Nếu `TECHNICAL_DOCUMENTATION_W4.md` vẫn nói còn inconsistency 14-day vs 30-day, đổi thành:

> At the Week 4 snapshot, some artifacts used inconsistent analysis horizons. This was standardized to a 30-day primary outcome window in subsequent project iterations.

## 8. Wording nhỏ trong Stress Test
Đổi:
- `không có False Positive` → `không ghi nhận false positive trong scenario này`
- `Randomization tự động triệt tiêu noise` → `Randomization giúp cân bằng exogenous noise theo kỳ vọng, nhưng noise vẫn làm tăng uncertainty.`

## Phần đã hoàn thành
```text
✅ Repo root sạch
✅ Tech Doc W4
✅ Live Demo
✅ Demo assets đầy đủ
✅ 30-day outcome horizon
✅ R-Learner story
✅ A/A 5,000 runs
✅ SRM ratio logic
✅ Welch vs OLS explanation
✅ ROI formula
✅ CATE terminology chính
✅ Predicted vs synthetic benchmark columns
✅ Champion vs Challenger
✅ Week5 report đã chuyển sang R-Learner
✅ Week6 đã bỏ production overclaim lớn
```

## Final Priority
Nếu chỉ sửa tối thiểu:
```text
1. Bỏ Early Stopping claim
2. Rename/chuẩn hóa Ground-Truth Profit
3. Tách Predicted vs Oracle chart
4. Mass Voucher = 100%
5. ATE 1.0 → 0.8
6. Dọn .gitignore
7. Update Tech Doc W4 wording
```

Sau đó:
> **Freeze repo. Không thêm model, feature hay scope mới.**

Chuyển sang:
```text
Demo
Tech Doc
Final Presentation
Mentor/PM Review
```
