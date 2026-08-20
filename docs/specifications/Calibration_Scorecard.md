#### Calibration Scorecard (Thẻ điểm Hiệu chuẩn)

Bảng dưới đây đánh giá mức độ hội tụ giữa dữ liệu Synthetic (dữ liệu được sinh ra) và các mục tiêu thực tế (Target Statistic).

**Calibration Status: REVIEWED**
**Empirical Targets: PASS**
**Assumptions: DOCUMENTED**

| Variable (Biến số) | Source (Nguồn gốc) | Target Statistic (Mục tiêu) | Synthetic Statistic (Thực tế mô phỏng) | Phân loại |
|---|---|---|---|---|
| `fare` (Cước phí) | TLC (Dữ liệu thật NYC) | Lệch phải, Mean ~$20 | Log-Normal, Mean ~$19.5 | EMPIRICALLY CALIBRATED |
| `preferred_hour` (Giờ gọi xe) | TLC | Bimodal (2 đỉnh: Sáng & Chiều) | Bimodal tương ứng | EMPIRICALLY CALIBRATED |
| `zero_rides_rate` (Tỷ lệ 0 chuyến) | reference/assumption | 20% | Zero-Inflated | REFERENCE-CALIBRATED |
| `airport_share` (Chuyến đi sân bay) | reference/assumption | ~5% - 10% | P=8% urban, 2% suburban | REFERENCE-CALIBRATED |
| `age` (Độ tuổi) | assumption | N/A | Shifted Gamma; urban mean≈28, suburban mean≈34 | ASSUMPTION-DRIVEN |
| `ground_truth_cate` (Hiệu ứng Can thiệp thật) | Causal SCM | Mức ATE tổng thể dương | Expected ATE ≈ 0.8 rides / 30 days | ASSUMPTION-DRIVEN |
| `voucher_cost` / `margin` | Giả định tài chính | N/A | Dựa trên config.json | ASSUMPTION-DRIVEN |

> **Tại sao bảng này quan trọng?**  
> Người đọc có thể nhìn ngay vào thẻ điểm này để biết được yếu tố nào trong mô hình đã được "Căn chỉnh" (Calibrated) với thế giới thực (EMPIRICAL), yếu tố nào tham chiếu ngoài (REFERENCE), và yếu tố nào là "Giả định" (ASSUMPTION) nhằm phục vụ mục đích thử nghiệm thuật toán.
