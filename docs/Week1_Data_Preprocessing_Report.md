# BÁO CÁO TIỀN XỬ LÝ DỮ LIỆU (DATA PREPROCESSING REPORT)
**Dự án:** Phân tích Dữ liệu Yellow Taxi New York (Tháng 01/2026)
**Trạng thái:** Đã hoàn thành làm sạch và xuất file `_CLEANED.parquet`

> [!NOTE]
> Báo cáo này ghi chép lại toàn bộ quy trình, logic và các quyết định chiến lược trong việc Gạn lọc (Filtering) và Điền khuyết (Imputation) dữ liệu, tuân thủ nguyên tắc "Tôn trọng dữ liệu thô" của Data Science.

---

## 1. CHIẾN LƯỢC XÓA DỮ LIỆU (DELETION)
Thay vì dùng các màng lọc gắt gao (như giới hạn thời gian chuyến đi < 12h hay cước phí < $300), dự án quyết định **chỉ xóa những quan sát vi phạm định luật vật lý hoặc lỗi logic hệ thống tuyệt đối**. 

Các dữ liệu cực đoan (như chuyến đi 50 tiếng hoặc cước phí $1000) nhưng hợp lý về mặt vật lý đều được GIỮ LẠI để phục vụ phân tích Hành vi khách hàng (Task 4).

**Danh sách các bộ lọc đã áp dụng (Dùng toán tử phủ định `~`):**

1. **Lỗi Mốc Thời gian:** 
   - Xóa các chuyến xe có thời gian đón (`tpep_pickup_datetime`) diễn ra trước 01/01/2026 hoặc sau 31/01/2026. 
   - *Lập luận:* Dữ liệu rác của hệ thống hoặc lỗi đồng hồ trên xe lưu nhầm năm.
2. **Lỗi Không gian & Vật lý:** 
   - Xóa `trip_distance <= 0` (Xe không di chuyển).
   - Xóa `tpep_dropoff_datetime <= tpep_pickup_datetime` (Dịch chuyển tức thời - Thời gian chuyến đi bằng 0 hoặc âm).
   - Xóa `speed_mph > 80` (Tốc độ trung bình trên 128km/h trong môi trường đô thị là phi vật lý, lỗi do đứt mạng GPS).
3. **Lỗi Giá trị Âm & Miễn phí:** 
   - Xóa `passenger_count <= 0`, `fare_amount <= 0`, `total_amount <= 0`.
   - *Lập luận:* Hệ thống TLC quy định phí tối thiểu khi lên xe là $3.00. Các cuốc xe âm tiền là cuốc bị hủy (Dispute) nhưng tài xế quên tắt meter.
4. **Lỗi Mâu thuẫn Toán học (Cross-column Logic):** 
   - Xóa các chuyến có `total_amount` nhỏ hơn các thành phần cấu tạo lên nó (Như `fare_amount`, `tip_amount`, `tolls_amount`).
   - *Lập luận:* Cột tổng tiền được lập trình cứng từ chục năm trước, không cộng dồn các loại phí mới sinh ra sau này, dẫn đến sai lệch. Cần loại bỏ để tính toán Doanh thu chính xác.

---

## 2. CHIẾN LƯỢC ĐIỀN KHUYẾT DỮ LIỆU (IMPUTATION)
Với tỷ lệ dữ liệu giữ lại đạt mức xuất sắc (**>95%**), chúng ta đối mặt với 2 nhóm dữ liệu bị Missing (Null). Thay vì xóa, chúng ta tiến hành điền khuyết dựa trên bản chất nghiệp vụ của ngành Taxi:

### Nhóm 1: Missing 29.21% (Cuốc xe qua Ứng dụng - Flex Fare)
Nhóm này có chung đặc điểm là `payment_type = 0` (Khách đặt xe qua App không có meter). Đây là tệp khách hàng công nghệ rất quan trọng.
* **Số lượng khách (`passenger_count`):** Điền `1.0`. (*Lý do: Mode Imputation - Hơn 70% các chuyến taxi là khách đi 1 mình*).
* **Mã loại cước (`RatecodeID` & `ratecode_name`):** Điền `99.0` và chữ `Unknown`. (*Lý do: Theo từ điển chuẩn của TLC, 99 là mã dành cho các cuốc xe không xác định loại cước*).
* **Phụ phí (`Airport_fee`, `congestion_surcharge`):** Điền `0.0`. (*Lý do: Đặt qua app là giá trọn gói, hệ thống không ghi nhận các phụ phí lắt nhắt này*).

### Nhóm 2: Missing < 1% (Lỗi Bản đồ Địa lý)
Khoảng 25,000 chuyến xe bị thiếu thông tin Quận/Khu vực (`pu_Borough`, `do_Zone`...). Thay vì dùng lệnh `dropna()` để xóa bỏ, chúng ta giữ lại và điền bằng chữ `Unknown`.
* **Lập luận chiến lược:** Qua kiểm tra chéo, nhóm dữ liệu "vô danh" này có Quãng đường trung bình cao gấp đôi (12.3 dặm) và **Cước phí trung bình cao gấp 3 lần ($63.90 so với $20.50)** so với nhóm bình thường. 
* Đây là các cuốc xe ngoại tỉnh / liên bang cao cấp. Nếu xóa bỏ, chúng ta sẽ xóa mất nhóm dữ liệu sinh lời (Premium Rides) quan trọng nhất của hãng, làm ảnh hưởng nghiêm trọng đến kết quả phân tích Doanh thu.

---
**=> KẾT LUẬN:** Tập dữ liệu `_CLEANED.parquet` cuối cùng hoàn toàn sạch bóng Missing Values (0 Null), loại bỏ triệt để các chuyến xe lỗi logic vật lý, nhưng vẫn bảo toàn nguyên vẹn 100% các chuyến xe ngoại lai có giá trị cao (Long-tail outliers). Tập dữ liệu đã sẵn sàng cho bước Khám phá Thời gian (Time Pattern Analysis).
