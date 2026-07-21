# Experiment Design v2: Kích hoạt Lại Khách hàng Ngủ Đông (Re-engagement Campaign)

> **Nâng cấp từ v1:** v1 nhắm theo **Khung giờ** (Time-based) → v2 nhắm theo **Tệp Khách hàng** (User-segment-based).  
> **Dữ liệu nền:** Yellow Taxi EDA (Notebook 2-4) cung cấp tham số chuyến đi; Kaggle Ride-Sharing EDA (Notebook 6) cung cấp schema User và phân phối hành vi.

---

## 1. Context & Rationale (Bối cảnh)

Từ phân tích EDA (Notebook 6), chúng ta biết rằng phần lớn người dùng của nền tảng gọi xe có mức độ sử dụng tập trung ở **4-6 chuyến/tháng** (Regular Users). Đây là tệp khách hàng có giá trị nhất về mặt kinh tế: đủ trung thành để tiếp cận, nhưng chưa đạt ngưỡng Heavy User (>8 chuyến/tháng).

**Vấn đề kinh doanh phát sinh:** Một phần trong tệp Regular Users này có xu hướng rơi vào trạng thái "Ngủ Đông" (Dormant) — họ không mở app trong 5-10 ngày liên tiếp, có nguy cơ bỏ ứng dụng (Churn). Nếu không kịp thời kích hoạt lại, họ sẽ trôi sang đối thủ (Grab, Be).

**Tại sao v2 tốt hơn v1 (Happy Hour):**
- v1 phát mã cho **tất cả** người mở app → Rủi ro "Cannibalization" cao (tặng tiền người vốn đã đặt xe).
- v2 chỉ nhắm vào **tệp cụ thể đang có nguy cơ rời bỏ** → Chi phí tập trung, tác động nhân quả (Causal Effect) được kiểm soát tốt hơn.

---

## 2. Hypothesis (Giả thuyết)

**Nếu** chúng ta gửi Push Notification kèm Voucher giảm giá 25% (tối đa 50,000 VNĐ) đến tệp khách hàng Regular Users đã không mở app trong 5+ ngày,  
**Thì** số chuyến đi trung bình của nhóm này trong 14 ngày tiếp theo sẽ tăng lên,  
**Bởi vì** việc nhắc nhở cá nhân hóa (Personalized Nudge) kết hợp với ưu đãi sẽ vượt qua ngưỡng quán tính (Inertia) đang cản trở họ mở app trở lại.

---

## 3. Estimand (Đại lượng Causal cần ước lượng)

- **ATE (Average Treatment Effect):**  
  `ATE = E[Rides(Treatment=1)] - E[Rides(Treatment=0)]`  
  Sự chênh lệch số chuyến đi trung bình/user trong 14 ngày giữa nhóm nhận Voucher và nhóm không nhận.

- **CATE (Conditional ATE):** Ưu tiên phân tích thêm theo:
  - `customer_type` (Regular vs Occasional): Voucher tác động mạnh hơn với ai?
  - `days_inactive` (5-7 ngày vs 8-14 ngày): Người mới ngủ đông vs ngủ đông lâu, ai phục hồi tốt hơn?

- **Không đo lường:** Click-through rate của Push Notification (Đây là Proxy Metric, không phải Causal Outcome).

---

## 4. Population (Tập khách hàng mục tiêu)

### Tiêu chí chọn vào (Inclusion):
| Tiêu chí | Điều kiện |
|---|---|
| Lịch sử sử dụng | Đã đặt **4-8 chuyến** trong 30 ngày trước thí nghiệm |
| Trạng thái hiện tại | **Không mở app trong 5-14 ngày** liên tiếp |
| Khu vực | Sinh hoạt chủ yếu tại **vùng đô thị** (Urban) |
| Tình trạng tài khoản | Tài khoản Active, chưa bị khóa |

### Tiêu chí loại trừ (Exclusion):
- ❌ **Heavy Users (>8 chuyến/tháng):** Họ sẽ tự quay lại, tặng voucher là lãng phí ngân sách.
- ❌ **New Users (< 30 ngày tuổi):** Hành vi chưa ổn định, không đủ lịch sử để phân tích.
- ❌ **Khách hàng đã nhận Voucher trong 14 ngày qua:** Tránh hiệu ứng "Voucher Fatigue".
- ❌ **Khách hàng đã unsubscribe thông báo:** Không thể tiếp cận qua Push Notification.

---

## 5. Unit Randomization (Đơn vị phân bổ ngẫu nhiên)

- **Đơn vị:** `User_ID` (Định danh tài khoản khách hàng).
- **Lý do:** Randomize theo User_ID đảm bảo:
  1. Mỗi người dùng chỉ thuộc đúng 1 nhóm (Treatment hoặc Control) trong suốt thí nghiệm.
  2. Tránh Interference Effect: Khách hàng không thể vừa thấy voucher vừa không thấy trong cùng một lần dùng app.
- **Tỷ lệ phân bổ:** 50% Treatment — 50% Control (Random Assignment).
- **Phương pháp:** Hash `User_ID` bằng hàm deterministic để đảm bảo tái lập (Reproducibility).

---

## 6. Treatment & Control (Thiết kế Can thiệp)

### Treatment Group (Nhóm can thiệp):
Vào ngày thứ 5 kể từ khi user không mở app:
1. Hệ thống tự động gửi **Push Notification** với nội dung cá nhân hóa:  
   *"Lâu rồi không gặp! Mã giảm 25% cho chuyến đi tiếp theo của bạn — Hết hạn sau 48h."*
2. Khi user mở app, hiển thị **In-app Banner** nhắc nhở về voucher còn hiệu lực.
3. Mã voucher tự động áp dụng khi thanh toán, không cần nhập tay.

### Control Group (Nhóm đối chứng):
- Không nhận Push Notification.
- Không thấy In-app Banner.
- Trải nghiệm bình thường nếu tự mở app.
- ⚠️ **Không được** chạy bất kỳ can thiệp nào khác song song với nhóm này trong thời gian thí nghiệm.

---

## 7. Exposure & Analysis Window (Thời gian chạy thí nghiệm)

| Giai đoạn | Thời gian | Mô tả |
|---|---|---|
| **Pre-experiment (Look-back)** | 30 ngày trước | Thu thập lịch sử để xác định đủ điều kiện tham gia |
| **Exposure Window** | 14 ngày | Cửa sổ chạy thí nghiệm, gửi voucher và theo dõi |
| **Attribution Window** | 48 giờ | Chuyến đi phải hoàn thành trong 48h kể từ khi nhận Push |
| **Cooldown (Washout)** | 7 ngày sau | Không chạy campaign khác để tránh lây nhiễm kết quả |

---

## 8. Metrics (Hệ thống Chỉ số)

### Primary Metric / OEC:
- **Incremental Rides per User:** Số chuyến đi tăng thêm trên mỗi user trong 14 ngày.  
  `= avg_rides(Treatment) - avg_rides(Control)`

### Secondary Metrics:
- **Re-engagement Rate:** Tỷ lệ % user Dormant mở lại app sau khi nhận Push.
- **Day-14 Retention Rate:** Tỷ lệ % user vẫn còn đặt xe ở cuối tuần thứ 2 (Đo lường tính bền vững).

### Guardrail Metrics (Chỉ số bảo vệ):
- **Profit Margin per Ride:** Đảm bảo margin không âm sau khi trừ chi phí voucher.
- **Voucher Redemption Rate:** Nếu < 5% → Push Notification không hiệu quả, cần xem lại nội dung.
- **User Complaint Rate:** Đảm bảo Push Notification không bị đánh dấu là Spam.

---

## 9. Confounders cần kiểm soát (Biến nhiễu)

Đây là điểm nâng cấp quan trọng nhất so với v1, trực tiếp phục vụ cho bài toán Causal Inference ở Tuần 3:

| Confounder | Vì sao là biến nhiễu? | Cách kiểm soát |
|---|---|---|
| `customer_type` (VIP/Regular/Casual) | VIP đặt xe nhiều hơn bất kể có voucher hay không | Stratified Randomization (Phân tầng theo loại KH) |
| `days_inactive` (5-7 vs 8-14 ngày) | User ngủ đông ít ngày dễ kéo lại hơn | Đưa vào mô hình như Covariate |
| `preferred_time_slot` (Giờ cao/thấp điểm) | User thường đi vào giờ cao điểm có thể đặt xe dù không có voucher | Kiểm soát trong phân tích hồi quy |
| `location` (Urban/Suburban) | User ở nội thành đặt xe nhiều hơn | Block Randomization theo khu vực |

---

## 10. Decision Rule (Luật ra quyết định)

Thí nghiệm được tuyên bố **thành công** và tiến hành Roll-out nếu **đồng thời** thỏa mãn:

1. ✅ **Statistical Significance:** p-value của Incremental Rides < **0.05**
2. ✅ **Practical Significance:** Incremental Rides tăng ít nhất **+1.5 chuyến/user** (MDE = Minimum Detectable Effect)
3. ✅ **Guardrail an toàn:** Profit Margin per Ride vẫn dương; User Complaint Rate < 2%
4. ✅ **Retention bền vững:** Day-14 Retention Rate của nhóm Treatment cao hơn Control ít nhất +5%

---

## 11. So sánh v1 vs v2 (Tóm tắt tiến hóa tư duy)

| Chiều | v1 (Time-based) | v2 (User-targeted) |
|---|---|---|
| **Câu hỏi** | Khi nào nên giảm giá? | Ai nên nhận giảm giá? |
| **Dữ liệu cần** | Chỉ cần dữ liệu chuyến đi (Trip-level) | Bắt buộc có User_ID + Lịch sử cá nhân |
| **Cơ chế** | Banner hiển thị theo giờ cho tất cả | Push Notification cá nhân hóa |
| **Cannibalization** | 🔴 Cao | 🟢 Thấp |
| **Chi phí** | 🔴 Dàn trải, kém hiệu quả | 🟢 Tập trung, ROI cao |
| **Confounder** | Thời gian trong ngày | Customer type, Days inactive, Location |
| **Ứng dụng** | Campaign đại trà (Mass Marketing) | Personalized Re-engagement |
