# Metric Specification: GSM Promotion Experimentation

Tài liệu này định nghĩa chính xác về mặt toán học (Mathematical Definition) cho các chỉ số được sử dụng trong hệ thống đánh giá Policy Simulator và A/B Testing.

---

## 1. Incremental Rides (Chuyến đi tăng thêm do Voucher)
Đo lường sự thay đổi trong hành vi đi lại của khách hàng do tác động trực tiếp của Voucher.

- **Tên kỹ thuật:** `incremental_rides_30d`
- **Tử số (Numerator):** Tổng số chuyến đi hoàn thành trong 30 ngày của nhóm Treatment (Có nhận Voucher) trừ đi Tổng số chuyến đi của nhóm Control (Không nhận Voucher) với cùng quy mô mẫu.
- **Mẫu số (Denominator):** Tổng số User hợp lệ (Eligible Users) trong nhóm.
- **Tính toán Uplift (CATE):** $E[Y_i(1) - Y_i(0) | X_i]$


---

## 2. Expected Incremental Profit (Lợi nhuận Kỳ vọng Tăng thêm)
Chỉ số Kinh doanh (North Star Metric) cốt lõi của toàn bộ dự án. Xác định xem công ty Lời hay Lỗ khi phát Voucher.

- **Tên kỹ thuật:** `expected_incremental_profit`
- **Công thức:** 
  $$\text{Profit} = (\text{CATE} \times \text{Margin per Ride}) - (\text{Predicted Rides} \times \text{Voucher Cost})$$
- **Diễn giải các thành phần:**
  - `CATE`: Số chuyến đi tăng thêm do mô hình AI dự báo.
  - `Margin per Ride`: Lợi nhuận gộp công ty thu được trên mỗi chuyến (Khấu trừ chi phí xăng xe, tài xế). (Configurable trong `config.json`).
  - `Predicted Rides`: Tổng số chuyến đi dự báo của User đó nếu được nhận Voucher.
  - `Voucher Cost`: Số tiền công ty phải bù giá cho User đó trên mỗi chuyến. (Configurable trong `config.json`).
- **Missing Rule:** Nếu không có dữ liệu lịch sử giá cước của user, sử dụng Average Fare toàn hệ thống.

---

## 3. Policy ROI (Tỷ suất Hoàn vốn của Chiến lược)
Đo lường hiệu quả sử dụng vốn Marketing.

- **Tên kỹ thuật:** `est_roi_pct`
- **Tử số:** Tổng `expected_incremental_profit` của toàn bộ những người được Targeting (Phát Voucher).
- **Mẫu số:** Tổng `voucher_cost` tài trợ cho nhóm đó.
- **Công thức:** $\frac{\sum \text{Profit}_i}{\sum \text{Cost}_i} \times 100$
- **Ràng buộc:** Nếu Tổng Cost = 0, ROI = 0% (Để tránh lỗi chia cho 0).

---

## 4. Voucher Cannibalization Cost (Chi phí Ăn thịt Doanh thu)
Chỉ số ẩn nhưng cực kỳ quan trọng để giải thích tại sao Mass Voucher lại thất bại.

- **Định nghĩa:** Chi phí công ty phải trả để trợ giá cho những chuyến đi mà Khách hàng ĐẰNG NÀO CŨNG SẼ ĐI (Sure Things) kể cả khi không có Voucher.
- **Công thức:** $Y_0 \times \text{Voucher Cost}$
- *(Trong đó $Y_0$ là Base Rides - số chuyến đi tự nhiên không có tác động khuyến mãi).*
