# Từ Điển Dữ Liệu (Data Dictionary) - Yellow Tripdata

Dưới đây là bảng giải thích chi tiết, chuẩn xác 100% về ý nghĩa các cột theo tài liệu mới nhất của Ủy ban Taxi và Limousine (TLC) New York:

| Tên Cột (Feature) | Ý nghĩa chi tiết |
| :--- | :--- |
| **VendorID** | Mã nhà cung cấp thiết bị TPEP ghi nhận dữ liệu chuyến đi.<br>• `1` = Creative Mobile Technologies, LLC<br>• `2` = Curb Mobility, LLC<br>• `6` = Myle Technologies Inc<br>• `7` = Helix |
| **tpep_pickup_datetime** | Ngày và giờ chính xác lúc đồng hồ tính tiền bắt đầu chạy (khách lên xe). |
| **tpep_dropoff_datetime** | Ngày và giờ chính xác lúc đồng hồ tính tiền dừng lại (khách xuống xe). |
| **passenger_count** | Số lượng hành khách trên chuyến xe. *(Lưu ý: Giá trị này do tài xế tự nhập).* |
| **trip_distance** | Chiều dài quãng đường chuyến đi (tính bằng dặm - miles) được ghi nhận bởi đồng hồ. |
| **RatecodeID** | Mã biểu giá áp dụng vào cuối chuyến đi.<br>• `1` = Standard rate (Biểu giá tiêu chuẩn)<br>• `2` = JFK (Sân bay JFK)<br>• `3` = Newark (Sân bay Newark)<br>• `4` = Nassau hoặc Westchester<br>• `5` = Negotiated fare (Giá thỏa thuận)<br>• `6` = Group ride (Đi ghép)<br>• `99` = Null/unknown (Trống/Không xác định) |
| **store_and_fwd_flag** | Cờ báo hiệu xe có bị mất kết nối mạng và phải lưu tạm dữ liệu trên xe hay không.<br>• `Y` = Lưu và chuyển tiếp (do mất kết nối máy chủ)<br>• `N` = Gửi ngay lập tức (không lưu tạm) |
| **PULocationID** | Mã khu vực (TLC Taxi Zone) nơi khách **lên xe** (Pick-up). |
| **DOLocationID** | Mã khu vực (TLC Taxi Zone) nơi khách **xuống xe** (Drop-off). |
| **payment_type** | Hình thức thanh toán của hành khách.<br>• `0` = Flex Fare trip (Giá vé linh hoạt)<br>• `1` = Credit card (Thẻ tín dụng)<br>• `2` = Cash (Tiền mặt)<br>• `3` = No charge (Miễn phí)<br>• `4` = Dispute (Tranh chấp/Từ chối trả)<br>• `5` = Unknown (Không rõ)<br>• `6` = Voided trip (Chuyến đi bị hủy) |
| **fare_amount** | Phí di chuyển thuần túy do đồng hồ tính (dựa trên thời gian và quãng đường). |
| **extra** | Các khoản phụ thu khác (ví dụ: phụ thu giờ cao điểm hoặc ban đêm). |
| **mta_tax** | Thuế MTA. Được hệ thống tự động cộng thêm dựa trên biểu giá đang sử dụng. |
| **tip_amount** | Số tiền Tip (boa). Cột này **chỉ ghi nhận khoản tip trả qua thẻ tín dụng**, không bao gồm tip trả bằng tiền mặt. |
| **tolls_amount** | Tổng số tiền phí cầu đường hành khách đã trả trong chuyến đi. |
| **improvement_surcharge** | Phụ thu cải thiện dịch vụ, áp dụng lúc bắt đầu cuốc xe. (Bắt đầu thu từ năm 2015). |
| **total_amount** | Tổng số tiền khách hàng bị tính phí (không bao gồm tiền tip bằng tiền mặt). |
| **congestion_surcharge** | Tổng số tiền thu cho phụ phí chống ùn tắc giao thông của bang New York (NYS). |
| **airport_fee** | Phụ phí chỉ thu khi đón khách tại sân bay LaGuardia hoặc sân bay John F. Kennedy. |
| **cbd_congestion_fee** | Phí đánh vào Vùng Giảm Ùn Tắc (Congestion Relief Zone) của MTA, tính trên mỗi chuyến đi. Bắt đầu áp dụng từ ngày 05/01/2025. |
