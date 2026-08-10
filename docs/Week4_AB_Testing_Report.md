# Nền tảng Thống kê cho A/B Testing (Tuần 4)

## 1. Phương pháp Kiểm định Giả thuyết (Hypothesis Testing)
Quá trình phân tích A/B Testing trong dự án áp dụng phương pháp thống kê tần suất (Frequentist Hypothesis Testing) nhằm xác định mức độ ý nghĩa thống kê của sự khác biệt giữa hai nhóm.

- **Giả thuyết Không ($H_0$):** Giả định rằng không có sự khác biệt giữa nhóm Treatment và nhóm Control (nghĩa là tác động của Voucher bằng 0).
- **Giả thuyết Đối ($H_1$):** Giả định rằng có tồn tại một sự khác biệt mang ý nghĩa thống kê giữa hai nhóm.

Việc bác bỏ Giả thuyết $H_0$ phụ thuộc vào chỉ số **P-value**. Chỉ số này đại diện cho xác suất thu được một chênh lệch bằng hoặc lớn hơn mức đang quan sát thấy, với điều kiện $H_0$ là đúng. Dự án sử dụng mức ý nghĩa thống kê (Significance Level) $lpha = 0.05$ làm ngưỡng tiêu chuẩn. Nếu P-value < $lpha$, $H_0$ sẽ bị bác bỏ.

## 2. Tiêu chí Đánh giá trong A/B Testing
Hệ thống phân tích thực hiện hai phép đo lường thống kê độc lập tùy thuộc vào mục tiêu đánh giá:

### 2.1. Sanity Checks (Kiểm tra Cân bằng Hệ thống)
- **Mục tiêu:** Kiểm chứng thuật toán phân bổ ngẫu nhiên đã chia đều khách hàng vào các nhóm, đảm bảo tính đồng nhất (Comparability) trước khi phân tích kết quả.
- **Giả thuyết Không ($H_0$):** Hai nhóm hoàn toàn cân bằng về các đặc tính (Độ chênh lệch = 0).
- **Kết quả Kỳ vọng:** Mục tiêu ở bước này là **không thể bác bỏ $H_0$**. Do đó, yêu cầu **P-value > 0.05** để xác nhận hệ thống không gặp lỗi Mất cân bằng mẫu (Sample Ratio Mismatch - SRM) hoặc mất cân bằng biến hiệp phương sai (Covariate Imbalance).

### 2.2. Chỉ số Đánh giá Cốt lõi (Overall Evaluation Criterion - OEC)
- **Mục tiêu:** Đo lường tác động nhân quả thực sự của sự can thiệp (Voucher) lên chỉ số mục tiêu (Số chuyến đi tăng thêm).
- **Giả thuyết Không ($H_0$):** Sự can thiệp không mang lại tác động nào (Độ chênh lệch = 0).
- **Kết quả Kỳ vọng:** Mục tiêu ở bước này là **bác bỏ $H_0$** nhằm chứng minh hiệu quả của Voucher. Do đó, yêu cầu **P-value < 0.05** để kết luận mức độ tăng trưởng quan sát được có ý nghĩa thống kê và không xuất phát từ phương sai ngẫu nhiên.

## 3. Chỉ số An toàn Tài chính (Financial Guardrails)
Bên cạnh ý nghĩa thống kê, ý nghĩa thực tiễn (Practical Significance) của chiến dịch được đánh giá thông qua các chỉ số an toàn tài chính. Chỉ số **Tỷ suất Hoàn vốn (Return on Investment - ROI)** được tính toán bằng cách lấy doanh thu thuần (Net GMV) chia cho chi phí triển khai (Voucher Cost). Một chỉ số OEC dù có ý nghĩa thống kê cũng chỉ được đề xuất triển khai khi và chỉ khi chỉ số ROI tương ứng là một số dương, đáp ứng bài toán sinh lời của doanh nghiệp.

---

## 4. Kết quả Thực thi A/B Test (Empirical Results)

Dưới đây là kết quả A/B Testing thực tế được bóc tách theo các cụm khách hàng (Clusters) tìm được từ K-Means (Tuần 3). Dữ liệu này chứng minh hoàn toàn cơ chế Nhân quả (HTE) đã được thiết lập đúng.

| Phân khúc Khách hàng (Persona) | ATE (Chuyến tăng thêm) | P-value | ROI | Kết luận Hành động |
|---|---|---|---|---|
| **Airport Business** | +1.23 | 0.007 | **-48.3%** | ❌ **Dừng Voucher**. Kháng khuyến mãi. Tăng trưởng ảo do ngẫu nhiên, lợi nhuận cực kỳ âm. |
| **Urban Regulars** | +0.41 | 0.089 | **-78.4%** | ❌ **Dừng Voucher**. Hiệu ứng Cannibalization (Ăn mòn lợi nhuận). Đằng nào họ cũng đi xe. |
| **Rain Riders** | +1.32 | < 0.001 | **-53.8%** | ❌ **Dừng Voucher**. Phụ thuộc thời tiết. Doanh thu tăng không bù nổi chi phí Voucher. |
| **Suburban Cash** | +0.79 | < 0.001 | **-29.3%** | ⚠️ **Cân nhắc**. Nhạy cảm giá khá tốt nhưng doanh thu thấp. Cần chiến dịch ép liên kết thẻ. |
| **Suburban Card** | **+1.10** | **< 0.001** | **-18.2%** | 💡 **Điều chỉnh Khuyến mãi**. Đây là phân khúc nhạy cảm giá nhất và lỗ ít nhất. Tuy nhiên, mức giảm 25% hiện tại quá đắt đỏ so với ATE mang lại. Cần giảm Voucher xuống mức 10-15% để ROI dương. |

> **💡 Nhận xét cốt lõi cho Mentor:**
> Nếu ta chỉ chạy A/B Test đại trà (Mass Voucher) trên toàn bộ 20,000 user mà không phân cụm, **ATE trung bình ở mức +0.93 chuyến và làm công ty LỖ RÒNG hơn $556,000 USD**. 
> Khi bóc tách A/B Test theo nhóm K-Means (Tuần 4), mặc dù toàn bộ các cụm đều có ROI âm do Voucher 25% quá "đắt", ta vẫn xác định được `Suburban Card` là nhóm phản ứng tốt nhất. Bài học thực tiễn: A/B Test giúp chặn đứng một chiến dịch thảm họa tài chính trước khi Roll-out, và gợi ý việc tinh chỉnh lại Mức giảm giá (Discount Threshold) cho nhóm Suburban Card trong tương lai!
