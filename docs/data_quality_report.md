# Báo cáo Chất lượng Dữ liệu (Data Quality Report)
**Tập dữ liệu:** Yellow Tripdata (2026-01)
**Giai đoạn:** Khám phá & Đánh giá Dữ liệu (EDA - Data Quality Assessment)

> [!NOTE]
> Báo cáo này thống kê hiện trạng lỗi của bộ dữ liệu gốc **(chưa qua xử lý/xóa bỏ)** để cung cấp bức tranh toàn cảnh về chất lượng dữ liệu trước khi bước vào giai đoạn Tiền xử lý (Pre-processing).

## 1. Tổng quan Dữ liệu (Dataset Overview)
- **Tổng số dòng (Records):** 3,724,889 chuyến xe.
- **Tổng số cột (Features):** 20 cột (đã bao gồm các biến được merge thêm như Borough, Zone).
- **Dữ liệu trùng lặp (Duplicates):** **0 dòng** trùng lặp hoàn toàn. Dữ liệu ghi nhận rất độc lập.

## 2. Tính Toàn Vẹn & Khuyết Thiếu (Completeness & Missing Values)
> [!WARNING]
> Tồn tại một nhóm 6 biến có tỷ lệ thiếu hụt (Missing rate) khá cao lên tới **~29.2%**. Tuy nhiên, đây là dữ liệu **Missing có hệ thống (Structural Missing)**, mang giá trị nghiệp vụ rất cao.

**Chi tiết các biến bị Missing:**
- **Nhóm thiếu hụt cao (29.21% - 1,088,058 dòng):**
  - Bao gồm: `passenger_count`, `RatecodeID` (và `ratecode_name`), `store_and_fwd_flag`, `Airport_fee`, `congestion_surcharge`.
  - **Phát hiện đột phá (Key Insight):** 100% các dòng dữ liệu bị khuyết thiếu này đều có `payment_type = 0` (Flex Fare trip - Giá vé linh hoạt). Đây chính là các chuyến xe được đặt trước qua ứng dụng gọi xe (App-based/E-hail) với giá cước định trước. Hệ thống điều phối không sử dụng đồng hồ vật lý trên xe nên không ghi nhận số lượng hành khách và mã cước. Nhóm này đại diện cho tệp khách hàng công nghệ cốt lõi và BẮT BUỘC phải được giữ lại.
- **Nhóm thiếu hụt thấp (< 1%):**
  - Thiếu do không mapping được thông tin khu vực (`taxi_zone_lookup.csv`).
  - `do_service_zone` (0.60% - 22,302 dòng), `do_Borough` (0.44% - 16,286 dòng), `do_Zone` (0.16% - 6,016 dòng).
  - Tương tự với khu vực đón (PULocation): tỷ lệ missing cực kỳ thấp (0.04% - 0.16%).

## 3. Tính Hợp Lệ & Logic Kinh Doanh (Business Logic Validity)
> [!CAUTION]
> Đã phát hiện hàng chục nghìn chuyến đi có dữ liệu vi phạm logic vận hành thực tế.

- **Dữ liệu "Âm" (Negative Money):** 
  - Có tới **39,463 chuyến xe** có cước phí (`fare_amount`) bị âm.
  - Các phụ phí cũng bị âm theo (Extra: 20,035 chuyến, mta_tax: 37,730 chuyến...).
- **Giá trị bằng 0 vô lý:**
  - Có **125,738 chuyến xe** ghi nhận quãng đường di chuyển bằng 0 dặm (`trip_distance` <= 0).
- **Mâu thuẫn Logic Nghiệp Vụ (Cross-column Logic):**
  - **24 chuyến** trả Tiền mặt (`payment_type=2`) nhưng hệ thống lại báo có tiền Tip.
  - **2,465 chuyến** đi JFK (`RatecodeID=2`) nhưng giá cước rẻ hơn mức giá cố định (< $20).
  - **12,886 chuyến** đi xa (> 5 dặm) nhưng giá cước lại rẻ bèo (<= $5).
  - **25,251 chuyến** bắt/thả khách ở các Zone Vô danh (Unknown zones 264, 265).
- **Lỗi mốc thời gian kép:** **1 chuyến xe** ghi nhận thời điểm trả khách diễn ra *trước* thời điểm đón khách.

## 4. Ranh Giới Thời Gian (Time Constraints)
> [!IMPORTANT]
> Bộ dữ liệu mặc định dành cho Tháng 01/2026. Phát hiện tỷ lệ lỗi thời gian siêu nhỏ.

- **Chuyến xe vắt tháng (Hợp lệ):** **6 chuyến xe** bắt đầu từ rạng sáng/đêm ngày 31/12/2025 (Chuyến đi Giao thừa).
- **Lỗi từ tương lai:** **1 chuyến xe** ghi nhận đón khách sau ngày 31/01/2026 (tháng 02/2026).

## 5. Dấu hiệu Ngoại lai Cực đoan (Extreme Outliers)
Phân tích sơ bộ để phát hiện các chuyến xe có thông số vượt qua giới hạn vật lý và đời sống thường ngày tại New York.
- **Vận tốc:** **732 chuyến xe** ghi nhận tốc độ trung bình > 100 dặm/giờ (mph). Hoàn toàn phi lý trong nội đô NYC.
- **Thời gian chạy:** **35 chuyến xe** kéo dài liên tục > 24 tiếng đồng hồ (đỉnh điểm có chuyến lên tới 59 tiếng).
- **Tiền cước:** Dựa theo chuẩn 3-IQR, mức cước trần (Upper bound) phổ biến rơi vào khoảng **$74.40**. Tuy nhiên, có **442 chuyến xe** bị ghi nhận cước phí lên tới > $300 (Thậm chí có chuyến > $2,500 cho 48 dặm di chuyển).
