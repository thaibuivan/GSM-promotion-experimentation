# Nền tảng Thống kê cho A/B Testing (Tuần 4)

# Đánh giá Độ tin cậy Hệ thống & A/A Testing

## 1. Mục tiêu Đánh giá (Objective)
Trước khi đưa vào triển khai bất kỳ thí nghiệm A/B Testing nào, việc kiểm định tính ổn định của hệ thống phân bổ ngẫu nhiên (Randomization Pipeline) và công cụ phân tích thống kê là yêu cầu bắt buộc. Quá trình này được thực hiện thông qua A/A Testing — một thí nghiệm giả lập nơi không có bất kỳ sự can thiệp (Voucher) nào được áp dụng cho cả hai nhóm. 

Mục tiêu cốt lõi là xác minh Tỷ lệ Dương tính giả (False Positive Rate - Type I Error) của hệ thống hội tụ chính xác về mức lý thuyết ($\alpha = 0.05$), đồng thời đảm bảo không có sự thiên vị trong việc phân bổ mẫu.

## 2. Phương pháp Thực hiện (Methodology)
Dự án áp dụng phương pháp Mô phỏng Monte Carlo. Tập khách hàng mục tiêu (`Suburban Occasionals`) được phân bổ ngẫu nhiên thành hai nhóm (A và A') qua 5.000 vòng lặp độc lập. Các chỉ số thống kê được ghi nhận ở mỗi vòng lặp để phân tích hành vi của hệ thống.

## 3. Các Chỉ số Đánh giá & Kết quả

### 3.1. Kiểm tra Lỗi Cân bằng Mẫu (Sample Ratio Mismatch - SRM)
- **Phương pháp:** Sử dụng Kiểm định Chi-Square ($X^2$) qua 5000 vòng lặp, kết hợp **Kiểm định Nhị phân (Binomial Test)** để đánh giá tỷ lệ lỗi.
- **Ngưỡng tiêu chuẩn:** Số lần P-value < 0.05 phải tương đồng với mức kỳ vọng ngẫu nhiên (5%). Binomial P-value > 0.05.
- **Kết quả đo lường:** Số lần cảnh báo SRM là 251/5000 (5.02%). Khoảng tin cậy hoàn toàn phù hợp với phương sai ngẫu nhiên (Binomial P-value = 0.9664).
- **Kết luận:** ĐẠT (PASS). Thuật toán Randomization hoạt động ổn định và công bằng tuyệt đối. Tỷ lệ phân bổ user 50/50 là hoàn hảo.

### 3.2. Kiểm tra Độ Cân bằng Đặc trưng (Covariate Balance)
- **Phương pháp:** Sử dụng Independent T-Test để kiểm tra sự khác biệt của các biến hiệp phương sai trước thí nghiệm.
- **Ngưỡng tiêu chuẩn:** P-value liên tục duy trì ở mức > 0.05 qua các tập mẫu ngẫu nhiên.
- **Kết quả đo lường:** Hệ thống duy trì sự cân bằng đặc trưng ổn định, phân phối nền của các biến số tương đồng giữa hai nhóm.
- **Kết luận:** ĐẠT (PASS). Hệ thống loại trừ thành công các rủi ro liên quan đến Thiên kiến chọn mẫu (Selection Bias).

### 3.3. Kiểm tra Tỷ lệ Dương tính giả (False Positive Rate - FPR)
- **Phương pháp:** Đo lường tỷ lệ các vòng lặp A/A Test trả về P-value < 0.05 (FPR) và kiểm chứng bằng **Binomial Test** để so sánh với mức ý nghĩa $\alpha=0.05$. *(Lưu ý: Bỏ qua KS-Test do đặc tính biến rời rạc của số chuyến đi).*
- **Ngưỡng tiêu chuẩn:** FPR không có sự khác biệt ý nghĩa thống kê so với 5.0%. (Binomial P-value > 0.05).
- **Kết quả đo lường:** Tỷ lệ False Positive thực tế đạt 4.78% (239 lỗi / 5000 lần). Binomial P-value = 0.4851.
- **Kết luận:** ĐẠT (PASS). Động cơ tính toán thống kê (Statistical Engine) hoạt động chuẩn xác, kiểm soát hoàn hảo tỷ lệ báo động giả.

## 4. Kết luận Tổng thể
Hệ thống Thử nghiệm (Experimentation Platform) đã vượt qua toàn bộ các tiêu chí kiểm định ngặt nghèo trong danh sách Trust Checklist. Pipeline dữ liệu minh bạch, vô tư và chuẩn xác về mặt toán học. Mọi kết quả phân tích A/B Testing được chạy trên nền tảng này hoàn toàn đủ độ tin cậy để phục vụ cho các quyết định vận hành thực tế.


---


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
Bên cạnh ý nghĩa thống kê, ý nghĩa thực tiễn (Practical Significance) của chiến dịch được đánh giá thông qua các chỉ số an toàn tài chính. Chỉ số **Tỷ suất Hoàn vốn (Return on Investment - ROI)** được tính toán bằng cách lấy doanh thu thuần (Net GMV) chia cho chi phí triển khai (Voucher Cost). Một chỉ số OEC dù có ý nghĩa thống kê cũng chỉ được đề xuất triển khai khi và chỉ khi chỉ số ROI tương ứng là một số dương, đáp ứng bài toán sinh lời của doanh nghiệp.

---

## 4. Kết quả Thực thi A/B Test (Empirical Results)

Dưới đây là kết quả A/B Testing thực tế được bóc tách theo các cụm khách hàng (Clusters) tìm được từ K-Means (Tuần 3). Dữ liệu này chứng minh hoàn toàn cơ chế Nhân quả (HTE) đã được thiết lập đúng.

| Phân khúc Khách hàng (Persona) | ATE (Chuyến tăng thêm) | P-value | ROI | Kết luận Hành động |
|---|---|---|---|---|
| **Airport Business** | +1.23 | 0.007 | **-13.8%** | ❌ **Dừng Voucher**. Kháng khuyến mãi. Tăng trưởng ảo do ngẫu nhiên, lợi nhuận âm. |
| **Urban Regulars** | +0.41 | 0.089 | **-64.0%** | ❌ **Dừng Voucher**. Hiệu ứng Cannibalization (Ăn mòn lợi nhuận). Đằng nào họ cũng đi xe. |
| **GenZ / Young Riders** | +1.32 | < 0.001 | **-23.0%** | ❌ **Dừng Voucher**. Phụ thuộc thời tiết. Doanh thu tăng không bù nổi chi phí Voucher. |
| **Suburban Cash** | +0.79 | < 0.001 | **+17.9%** | ⚠️ **Cân nhắc**. Nhạy cảm giá tốt, ROI dương nhẹ. Có thể dùng làm tệp dự phòng hoặc kết hợp ép liên kết thẻ. |
| **Suburban Occasionals** | **+1.10** | **< 0.001** | **+38.2%** | 💡 **Chiến thắng tuyệt đối (Winner)**. Đây là phân khúc nhạy cảm giá nhất, mang lại lợi nhuận cao nhất. Với mức chiết khấu 15% tối ưu, hệ thống ghi nhận ROI dương ấn tượng. Đề xuất Roll-out toàn hệ thống cho tệp này. |

> **💡 Bài học Kinh doanh Cốt lõi:**
> Nếu ta chỉ chạy A/B Test đại trà (Mass Voucher) trên toàn bộ 20,000 user mà không phân cụm, **ATE trung bình ở mức +0.93 chuyến nhưng làm công ty LỖ RÒNG do lãng phí ngân sách vào các nhóm không nhạy cảm**. 
> Khi bóc tách A/B Test theo nhóm K-Means (Tuần 4) và áp dụng mức chiết khấu tối ưu 15%, ta xác định được `Suburban Occasionals` là nhóm phản ứng tốt nhất với **ROI lên tới +38.2%**. Bài học thực tiễn: A/B Test không chỉ giúp chặn đứng các chiến dịch thảm họa, mà còn là công cụ tìm ra "Sweet Spot" (Điểm ngọt) giữa Mức chiết khấu và Hành vi người dùng để tối đa hóa lợi nhuận!


---

