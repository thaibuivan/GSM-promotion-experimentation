# Experiment Design v1: Kích cầu Giờ thấp điểm (Off-peak Demand Generation)

*Dự án: GSM Promotion Experimentation*
*Tác giả: [Tên của bạn]*

## 1. Context & Rationale (Bối cảnh)
Dựa trên phân tích EDA (Notebook 2), hệ thống ghi nhận một khoảng thời gian rảnh rỗi lớn của đội xe (idle time) vào khung giờ trưa (10AM - 4PM). Việc xe chạy rỗng gây lãng phí chi phí vận hành (fuel/driver cost).
Tuy nhiên, nếu phát voucher ngẫu nhiên, ta có nguy cơ rơi vào bẫy "Cannibalization" (khách hàng vốn dĩ sẽ đặt xe vào giờ đó vẫn nhận được mã, làm giảm doanh thu). Do đó, thiết kế Mechanism này nhắm vào việc thay đổi hành vi: **Thúc đẩy nhu cầu mới (Incremental rides)**.

## 2. Hypothesis (Giả thuyết)
**Nếu** chúng ta cấp mã Khuyến mãi "Happy Hour" (giảm 20%, tối đa $5) cho tập khách hàng mở app trong khung giờ 10AM - 4PM, 
**Thì** tổng số lượng chuyến xe (Total Rides) trong khung giờ này sẽ tăng lên, 
**Bởi vì** khách hàng nhạy cảm về giá (Price-sensitive users) sẽ có động lực để chuyển dịch nhu cầu đi lại từ khung giờ khác sang, hoặc phát sinh thêm nhu cầu đi lại mới.

## 3. Estimand (Đại lượng Causal cần ước lượng)
- **ATE (Average Treatment Effect):** Sự chênh lệch về *Số chuyến xe trung bình trên mỗi User* giữa nhóm nhận được tính năng Happy Hour và nhóm không nhận được.
- Mục tiêu là đo lường **Uplift/Incrementality** (Tác động nhân quả thực sự của Voucher), chứ không phải đo lường Conversion Rate.

## 4. Population (Tập khách hàng mục tiêu)
- **Tiêu chí lọc:** Tất cả các User có tương tác (mở App) trong vòng 30 ngày qua, sinh sống/hoạt động chủ yếu tại khu vực Manhattan (dựa theo hành vi lịch sử).
- **Loại trừ:** Các khách hàng VIP (vì họ có độ co giãn của cầu theo giá - Price Elasticity rất thấp, phát voucher chỉ gây tốn tiền).

## 5. Unit Randomization (Đơn vị phân bổ ngẫu nhiên)
- **Mức độ (Unit):** `User_ID` (Khách hàng). 
- **Lý do:** Randomize theo User đảm bảo trải nghiệm nhất quán. Nếu randomize theo Session (Phiên mở app), một khách hàng có thể mở app lúc 11h thấy có voucher, nhưng 12h mở lại thì không thấy, gây ra sự khó chịu và hiệu ứng lan truyền (Interference).

## 6. Treatment & Control (Thiết kế Can thiệp)
- **Treatment Group (Nhóm can thiệp):** Khi mở app trong khung giờ 10AM - 4PM, User sẽ thấy một Banner thông báo "Happy Hour: Giảm 20%". Mã tự động áp dụng khi đặt xe.
- **Control Group (Nhóm đối chứng):** Mở app bình thường. Giao diện mặc định. Không có Banner và không có Voucher.

## 7. Exposure & Analysis Window (Thời gian chạy thí nghiệm)
- **Exposure Window (Thời gian thu thập):** 14 ngày (Đủ 2 chu kỳ tuần để nắm bắt cả ngày thường lẫn cuối tuần).
- **Attribution Window:** Chuyến đi phải được hoàn thành trong vòng 24h kể từ khi User thấy Banner.

## 8. Metrics (Hệ thống Chỉ số)
### Primary Metric / OEC (Chỉ số đánh giá chính)
- **Incremental Rides per User (Số chuyến đi tăng thêm trên 1 user):** Đây là thước đo trực tiếp nhất xem Voucher có tạo ra nhu cầu mới hay không.

### Guardrail Metrics (Chỉ số bảo vệ & Game Theory)
Đảm bảo hệ sinh thái cân bằng giữa Khách hàng, Tài xế và Nền tảng:
- **Driver Cancellation Rate (Tỷ lệ tài xế hủy chuyến):** Đảm bảo voucher rẻ không làm tài xế đình công (Phản ứng Game Theory).
- **Cannibalization Rate (Tỷ lệ ăn thịt doanh thu giờ cao điểm):** Theo dõi xem số chuyến xe của nhóm Treatment vào khung giờ 8AM - 9AM có bị giảm đi so với nhóm Control hay không (Khách dời lịch đi lại).
- **Average Profit Margin per Ride (Biên lợi nhuận trung bình):** Đảm bảo không bị lỗ quá mức ngân sách cho phép.

## 9. Decision Rule (Luật ra quyết định)
Thí nghiệm sẽ được báo cáo thành công và tiến hành **Roll-out (mở rộng 100%)** nếu và chỉ nếu:
1. P-value của Primary Metric (Incremental Rides) < 0.05.
2. Incremental Rides tăng ít nhất +2% (Minimum Detectable Effect - MDE).
3. Các Guardrail Metrics không bị suy giảm đáng kể (Tỷ lệ tài xế hủy chuyến không tăng quá 1%, Biên lợi nhuận không âm).
