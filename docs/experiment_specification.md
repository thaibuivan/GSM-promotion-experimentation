# Illustrative Experiment Specification — Hypothetical Business Translation

> **Disclaimer:** Synthetic sandbox hiện dùng voucher 15% không cap. Mọi tham số cho real pilot, gồm cap, holdout và eligibility, phải được Business/Marketing xác nhận lại.

**Author:** Data Science Team
**Status:** Draft / Ready for Review
**Target Launch:** Q4 2026

## 1. Thông tin Chung (Overview)
- **Experiment Name:** `GSM_PROMO_PROFIT_TARGETING_PILOT`
- **Business Question:** Simplified R-Learner-style residual model kết hợp Profit Targeting có tạo incremental profit cao hơn Segment Targeting hay không?
- **Hypothesis:** Profit Targeting giảm promotion burn trên khách hàng có EV âm và tạo incremental profit cao hơn Segment Targeting.

## 2. Thiết kế Thử nghiệm (Experiment Design)
- **Population:** Toàn bộ khách hàng có mở app GSM trong 90 ngày qua (Active Users).
- **Eligibility:** 
  - Khách hàng không nằm trong danh sách đen (Blacklist).
  - Khách hàng chưa nhận bất kỳ Voucher nào khác trong 7 ngày qua để tránh hiệu ứng chéo (Interference).
- **Randomization Unit:** `user_id`
- **Assignment Ratio:**
  - **Group A (Holdout - 10%):** Không nhận Voucher. (Dùng để tính Incremental Baseline).
  - **Group B (Champion - 45%):** Áp dụng rule-based Segment Targeting (chỉ phát cho nhóm Suburban).
  - **Group C (Challenger - 45%):** Áp dụng AI Profit Targeting (Chỉ phát nếu CATE dự đoán mang lại EV > 0).

## 3. Cấu hình Chiến dịch (Parameters)
- **Treatment trong synthetic sandbox:** Voucher giảm giá 15%, không cap. Đây không phải cấu hình GSM thực tế; cap cho pilot thật là tham số cần Business phê duyệt.
- **Exposure Window:** Khách hàng phải đăng nhập vào App và thấy Popup Voucher thì mới tính là Exposed. Phân tích chính sẽ dùng Intention-to-Treat (ITT).
- **Outcome Window:** 30 ngày kể từ khi được phân bổ vào nhóm (T=0 đến T+30).

## 4. Chỉ số Đo lường (Metrics)
- **Primary Metric:** `expected_incremental_profit` (Lợi nhuận gộp tăng thêm trừ đi Chi phí Voucher trên mỗi User).
- **Secondary Metrics:**
  - `incremental_rides`: Số chuyến đi tăng thêm.
  - `voucher_redemption_rate`: Tỷ lệ sử dụng Voucher.
- **Guardrail Metrics (Chỉ số bảo vệ):**
  - `total_voucher_cost_per_user`: Theo dõi chi phí để không vượt guardrail ngân sách được Business phê duyệt cho pilot thật.
  - `app_uninstall_rate`: Tỷ lệ gỡ app (Kiểm tra xem KH không nhận được voucher có tức giận gỡ app không).
  - Sample Ratio Mismatch (SRM) p-value > 0.01.

## 5. Quy tắc Ra quyết định (Decision & Stop Rules)
- **Minimum Detectable Effect (MDE):** Cần tính lại từ baseline variance và economics trên dữ liệu GSM thật trước pilot.
- **Stop Conditions:**
  - Lập tức dừng chiến dịch nếu `total_voucher_cost` vượt ngưỡng ngân sách được cấp.
  - Dừng nếu xuất hiện SRM (Lỗi chia tập) vào Ngày 2.
- **Expansion Decision:** Chỉ cân nhắc mở rộng traffic khi `expected_incremental_profit` của Group C cao hơn Group B với ý nghĩa thống kê và các guardrail không xấu đi. Tài liệu này không phê duyệt rollout production.
