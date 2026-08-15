# Illustrative Experiment Specification — Hypothetical Business Translation

> **Disclaimer:** All campaign parameters below (Voucher 15%, max 50,000 VND, 10% holdout, etc.) are illustrative assumptions for methodology demonstration unless explicitly confirmed by Business/Marketing.

**Author:** Data Science Team
**Status:** Draft / Ready for Review
**Target Launch:** Q4 2026

## 1. Thông tin Chung (Overview)
- **Experiment Name:** `GSM_PROMO_AI_VS_KMEANS_2026`
- **Business Question:** Việc áp dụng mô hình Causal ML (R-Learner) để chọn lọc khách hàng phát Voucher có mang lại Lợi nhuận tăng thêm (Incremental Profit) cao hơn so với chiến lược nhắm mục tiêu theo cụm tĩnh (K-Means) hiện tại hay không?
- **Hypothesis:** Mô hình AI Profit Targeting sẽ giảm thiểu chi phí "ăn thịt doanh thu" (Cannibalization) từ những khách hàng Sure Things, từ đó tăng ROI của chiến dịch lên ít nhất 15% so với nhóm K-Means.

## 2. Thiết kế Thử nghiệm (Experiment Design)
- **Population:** Toàn bộ khách hàng có mở app GSM trong 90 ngày qua (Active Users).
- **Eligibility:** 
  - Khách hàng không nằm trong danh sách đen (Blacklist).
  - Khách hàng chưa nhận bất kỳ Voucher nào khác trong 7 ngày qua để tránh hiệu ứng chéo (Interference).
- **Randomization Unit:** `user_id`
- **Assignment Ratio:**
  - **Group A (Holdout - 10%):** Không nhận Voucher. (Dùng để tính Incremental Baseline).
  - **Group B (Champion - 45%):** Áp dụng K-Means Segment Targeting (Chỉ phát cho nhóm Suburban).
  - **Group C (Challenger - 45%):** Áp dụng AI Profit Targeting (Chỉ phát nếu CATE dự đoán mang lại EV > 0).

## 3. Cấu hình Chiến dịch (Parameters)
- **Treatment:** Voucher giảm giá 15% (Max 50.000 VNĐ), áp dụng cho mọi chuyến đi.
- **Exposure Window:** Khách hàng phải đăng nhập vào App và thấy Popup Voucher thì mới tính là Exposed. Phân tích chính sẽ dùng Intention-to-Treat (ITT).
- **Outcome Window:** 30 ngày kể từ khi được phân bổ vào nhóm (T=0 đến T+30).

## 4. Chỉ số Đo lường (Metrics)
- **Primary Metric:** `expected_incremental_profit` (Lợi nhuận gộp tăng thêm trừ đi Chi phí Voucher trên mỗi User).
- **Secondary Metrics:**
  - `incremental_rides`: Số chuyến đi tăng thêm.
  - `voucher_redemption_rate`: Tỷ lệ sử dụng Voucher.
- **Guardrail Metrics (Chỉ số bảo vệ):**
  - `total_voucher_cost_per_user`: Đảm bảo không vượt quá ngân sách $20/người.
  - `app_uninstall_rate`: Tỷ lệ gỡ app (Kiểm tra xem KH không nhận được voucher có tức giận gỡ app không).
  - Sample Ratio Mismatch (SRM) p-value > 0.01.

## 5. Quy tắc Ra quyết định (Decision & Stop Rules)
- **Minimum Detectable Effect (MDE):** Kì vọng phát hiện mức tăng ROI 15%. (Xem công thức chi tiết trong `metric_specification.md` và Tab 6 trên Dashboard).
- **Stop Conditions:**
  - Lập tức dừng chiến dịch nếu `total_voucher_cost` vượt ngưỡng ngân sách được cấp.
  - Dừng nếu xuất hiện SRM (Lỗi chia tập) vào Ngày 2.
- **Rollout Decision:** Sẽ rollout (áp dụng 100%) Group C nếu `expected_incremental_profit` của Group C cao hơn Group B với ý nghĩa thống kê (p-value < 0.05).
