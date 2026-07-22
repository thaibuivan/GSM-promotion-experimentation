# Tiêu chuẩn Đo lường & Lựa chọn Metric (Metric Specification)

Tài liệu này định nghĩa các chỉ số đo lường (Metrics) cho Kịch bản A/B Testing: **Micro (User-targeted) - Tặng Voucher 25% cho Khách hàng ngủ đông (Churn/Inactive Users).** 

Theo đúng triết lý của Ron Kohavi (Ch.6 & Ch.7), việc tăng số chuyến đi (Rides) không đồng nghĩa với chiến dịch thành công, trừ khi nó mang lại giá trị kinh tế dài hạn và không phá vỡ hệ sinh thái.

---

## 1. OEC (Overall Evaluation Criterion) / Primary Metric
**OEC là tiêu chí tối thượng để ra quyết định (Go/No-go).** Đối với một nền tảng gọi xe, tặng Voucher chắc chắn làm tăng số chuyến, nhưng sẽ làm giảm biên lợi nhuận trên mỗi chuyến. Do đó, OEC phải đo lường được sự cân bằng này.

### **Incremental Net Revenue (Doanh thu thuần tăng thêm)**
Đây là chỉ số Kinh tế học (Economics Metric) bắt buộc phải có. Nó đo lường tổng lợi nhuận thực tế thu về trừ đi toàn bộ chi phí khuyến mãi.

* **Định nghĩa (Definition):** Tổng số tiền khách hàng trả (Fare) - Tiền chiết khấu (Voucher Cost) - Phí thanh toán/vận hành (Ops Cost).
* **Chiều hướng kỳ vọng (Direction):** 📈 **TĂNG**.
* **Đơn vị phân tích (Aggregation Level):** Cấp độ Khách hàng (`User_ID`). Trung bình mỗi khách hàng trong nhóm Treatment mang lại bao nhiêu lợi nhuận so với nhóm Control?
* **Khung thời gian (Exposure Window):** 14 ngày kể từ khi gửi Push Notification.
* **Failure Mode (Rủi ro đánh lừa):** Khách hàng có thể "bào" Voucher để đi các chuyến đi rất ngắn (dưới 1 dặm), khiến doanh thu không đủ bù đắp chi phí phát hành Voucher.

---

## 2. Guardrail Metrics (Các chỉ số Bảo vệ)
Guardrail metrics đóng vai trò như "Người gác đền". Ngay cả khi OEC (Doanh thu) tăng, nhưng nếu bất kỳ Guardrail nào bị vi phạm (chạm ngưỡng báo động đỏ), chiến dịch phải bị DỪNG LẠI lập tức để tránh hậu quả lâu dài.

### 2.1. Guardrail Kinh tế (Economics Guardrail)
**ROI (Return on Investment) / ROAS (Return on Ad Spend)**
* **Định nghĩa:** (Doanh thu thuần tăng thêm) / (Tổng chi phí Voucher phát hành).
* **Tại sao cần thiết:** Có thể chiến dịch mang lại Doanh thu dương (OEC tăng), nhưng ROI chỉ là 0.1% (Tốn 100 đồng để kiếm 1 đồng). Khi đó, tiền ngân sách nên đem đi gửi ngân hàng thay vì chạy khuyến mãi.
* **Ngưỡng an toàn (Threshold):** ROI phải lớn hơn Lãi suất cơ sở (hoặc lớn hơn chi phí cơ hội của công ty).
* **Failure Mode:** Cảnh báo đỏ (Red Alert) nếu ROI < 0.

### 2.2. Guardrail Tương tác (User Engagement Guardrail)
**App Uninstall Rate (Tỷ lệ gỡ ứng dụng) / Notification Opt-out Rate**
* **Định nghĩa:** Tỷ lệ người dùng tắt thông báo hoặc gỡ cài đặt ứng dụng sau khi nhận Push Notification.
* **Tại sao cần thiết:** Đây là rủi cụ điển hình khi gửi Push Notification. Nhóm khách hàng *Sleeping Dogs* (Đang ngủ yên) nếu bị làm phiền có thể nổi cáu và xóa luôn App. Nếu tỷ lệ này tăng cao, chiến dịch đang phá hủy tệp khách hàng.
* **Khung thời gian:** Trong vòng 3 ngày sau khi đẩy Push.
* **Failure Mode:** Cảnh báo đỏ (Red Alert) nếu tỷ lệ Unsubscribe/Uninstall ở nhóm Treatment cao hơn nhóm Control một cách có ý nghĩa thống kê (p < 0.05).

### 2.3. Guardrail Sức khỏe Hệ sinh thái (Ecosystem Health)
**Driver Cancellation Rate (Tỷ lệ tài xế hủy chuyến)**
* **Định nghĩa:** Số chuyến bị tài xế hủy / Tổng số cuốc xe được đặt thành công.
* **Tại sao cần thiết:** Khi tung Voucher, nhu cầu (Demand) có thể tăng đột biến trong khi nguồn cung tài xế (Supply) không đổi. Điều này dẫn đến kẹt xe, thời gian chờ lâu, khiến tài xế dễ bức xúc và hủy cuốc. 
* **Failure Mode:** Cảnh báo đỏ (Red Alert) nếu Tỷ lệ hủy chuyến vượt mức trung bình lịch sử quá 20% trong khung giờ cao điểm.

---

## 3. Quy tắc ra quyết định (Decision Rule)

Để chiến dịch này được Roll-out (Áp dụng thực tế cho 100% tập khách hàng mục tiêu), kết quả thí nghiệm phải đồng thời thỏa mãn **tất cả** các điều kiện sau:

1. **OEC (Incremental Net Revenue):** Tăng một cách có ý nghĩa thống kê (p-value < 0.05).
2. **ROI Guardrail:** Đạt mức tối thiểu 1.2x (Mang về 1.2 đồng cho mỗi 1 đồng Voucher chi ra).
3. **Opt-out Guardrail:** Tỷ lệ tắt thông báo không được cao hơn nhóm Control.
4. **Cancellation Guardrail:** Tỷ lệ tài xế hủy chuyến không vượt qua ngưỡng đỏ.

Nếu **OEC tăng mạnh** nhưng **Opt-out Guardrail bị vi phạm**, chiến dịch sẽ **DỪNG**, và đội ngũ phải xem xét lại nội dung thông điệp (Copywriting) hoặc giảm tần suất Push Notification.
