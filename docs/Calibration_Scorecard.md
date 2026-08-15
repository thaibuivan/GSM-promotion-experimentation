#### Calibration Scorecard (Thẻ điểm Hiệu chuẩn)

Bảng dưới đây đánh giá mức độ hội tụ giữa dữ liệu Synthetic (dữ liệu được sinh ra) và các mục tiêu thực tế (Target Statistic).

| Variable (Biến số) | Source (Nguồn gốc) | Target Statistic (Mục tiêu) | Synthetic Statistic (Thực tế mô phỏng) | Status (Trạng thái) |
|---|---|---|---|---|
| `fare` (Cước phí) | TLC (Dữ liệu thật NYC) | Lệch phải, Mean ~$20 | Log-Normal, Mean ~$19.5 | PASS |
| `preferred_hour` (Giờ gọi xe) | TLC | Bimodal (2 đỉnh: Sáng & Chiều) | Bimodal tương ứng | PASS |
| `zero_rides_rate` (Tỷ lệ 0 chuyến) | Tham chiếu ngành | ~30% khách hàng không đi | Zero-Inflated (Tỷ lệ 28.5%) | PASS |
| `airport_share` (Chuyến đi sân bay) | TLC / Giả định | ~5% - 10% | Cài đặt hệ số ngẫu nhiên 7% | PASS |
| `age` (Độ tuổi) | Giả định | N/A | Mean 35, SD 10 | ASSUMPTION |
| `income` (Thu nhập) | Giả định | N/A | Lệch phải, phản ánh sức mua | ASSUMPTION |
| `ground_truth_cate` (Hiệu ứng Can thiệp thật) | Causal SCM | Mức ATE tổng thể dương | Expected ATE ≈ 0.8 rides / 30 days | PASS |
| `voucher_cost` / `margin` | Giả định tài chính | N/A | Dựa trên config.json | ASSUMPTION |

> **Tại sao bảng này quan trọng?**  
> Người đọc (Đặc biệt là các Mentor/Data Scientist) có thể nhìn ngay lập tức vào thẻ điểm này để biết được yếu tố nào trong mô hình đã được "Căn chỉnh" (Calibrated) với thế giới thực, và yếu tố nào chỉ đơn thuần là "Giả định" (Assumption) nhằm phục vụ mục đích thử nghiệm thuật toán.
