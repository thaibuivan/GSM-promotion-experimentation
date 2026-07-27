# Nền tảng Thống kê cho A/B Testing (Tuần 4)

## 1. Phương pháp Kiểm định Giả thuyết (Hypothesis Testing)
Quá trình phân tích A/B Testing trong dự án áp dụng phương pháp thống kê tần suất (Frequentist Hypothesis Testing) nhằm xác định mức độ ý nghĩa thống kê của sự khác biệt giữa hai nhóm.

- **Giả thuyết Không ($H_0$):** Giả định rằng không có sự khác biệt giữa nhóm Treatment và nhóm Control (nghĩa là tác động của Voucher bằng 0).
- **Giả thuyết Đối ($H_1$):** Giả định rằng có tồn tại một sự khác biệt mang ý nghĩa thống kê giữa hai nhóm.

Việc bác bỏ Giả thuyết $H_0$ phụ thuộc vào chỉ số **P-value**. Chỉ số này đại diện cho xác suất thu được một chênh lệch bằng hoặc lớn hơn mức đang quan sát thấy, với điều kiện $H_0$ là đúng. Dự án sử dụng mức ý nghĩa thống kê (Significance Level) $\alpha = 0.05$ làm ngưỡng tiêu chuẩn. Nếu P-value < $\alpha$, $H_0$ sẽ bị bác bỏ.

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
Bên cạnh ý nghĩa thống kê, ý nghĩa thực tiễn (Practical Significance) của chiến dịch được đánh giá thông qua các chỉ số an toàn tài chính. Chỉ số **Tỷ suất Hoàn vốn (Return on Investment - ROI)** được tính toán bằng cách lấy doanh thu gộp tăng thêm trừ đi chi phí triển khai (ví dụ: chi phí phát hành Voucher). Một chỉ số OEC dù có ý nghĩa thống kê cũng chỉ được đề xuất triển khai khi và chỉ khi chỉ số ROI tương ứng là một số dương, đáp ứng bài toán sinh lời của doanh nghiệp.

---

## 4. Kết quả Thực thi A/B Test (Empirical Results)

Dưới đây là kết quả A/B Testing thực tế được bóc tách theo các cụm khách hàng (Clusters) tìm được từ Tuần 3. Dữ liệu này chứng minh hoàn toàn cơ chế Nhân quả (HTE) đã được thiết lập.

| Phân khúc Khách hàng (Persona) | ATE (Chuyến tăng thêm) | P-value | Khoảng tin cậy 95% (CI) | ROI | Kết luận Hành động |
|---|---|---|---|---|---|
| **Urban Regulars (Đi làm)** | +0.84 | 0.042 | [0.03, 1.65] | **-28.7%** | ❌ **Dừng Voucher**. Hiệu ứng Cannibalization (Ăn mòn lợi nhuận). Họ vốn dĩ sẽ đi xe mà không cần mã. |
| **Airport Business (Đi sân bay)** | +0.41 | 0.210 | [-0.22, 1.04] | **-98.6%** | ❌ **Dừng Voucher**. (P-value > 0.05) Không có ý nghĩa thống kê. Lãng phí ngân sách. |
| **Urban Leisure (Đi chơi nội thành)** | **+2.52** | **< 0.001** | **[1.85, 3.19]** | **+115%** | ✅ **Tăng ngân sách**. Cầu co giãn cực mạnh, Voucher thực sự kích cầu đi lại. |
| **Suburban Occasionals (Vãng lai)** | **+3.05** | **< 0.001** | **[2.41, 3.69]** | **+140%** | ✅ **Tăng ngân sách**. Nhạy cảm giá nhất, mang lại biên lợi nhuận cao nhất. |

> **💡 Nhận xét cốt lõi cho Mentor:**
> Nếu ta chỉ chạy A/B Test trên toàn bộ 20,000 user mà không phân cụm, **ATE trung bình chỉ ở mức +1.2 chuyến và ROI tổng có thể ÂM**. Nhờ việc kết hợp K-Means (Tuần 3) và bóc tách A/B Test theo nhóm (Tuần 4), ta mới phát hiện ra "Mỏ vàng" Urban Leisure để tối ưu hóa chiến dịch.
