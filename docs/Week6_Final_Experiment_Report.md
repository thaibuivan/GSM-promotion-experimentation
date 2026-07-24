# Báo cáo Đánh giá Thí nghiệm: Chiến dịch Khuyến mãi Voucher 25%

**Bối cảnh Dự án:** Đo lường tác động nhân quả (Causal Measurement) của Voucher giảm giá 25% lên mức độ tương tác của người dùng.
**Đơn vị thực hiện:** Nhóm Khoa học Dữ liệu (Data Science Team)
**Trạng thái Hệ thống:** TIN CẬY (Đã được xác minh qua Mô phỏng A/A Testing 5000 vòng lặp)

---

## 1. Tóm tắt Thực thi (Executive Summary)
Một chiến dịch thử nghiệm ngẫu nhiên (A/B Testing) đã được tiến hành nhằm đánh giá tính khả thi và ROI của Voucher 25%. Trái với nhận định ban đầu, chiến dịch đã vạch trần một sự thật quan trọng về Hiệu ứng Dị thể (HTE):
- **Cái bẫy Lợi nhuận:** Phân khúc mục tiêu ban đầu (`Suburban Commuters`) chỉ tạo ra ROI rất thấp hoặc hòa vốn (ATE = 0.8), do doanh thu tăng thêm không đủ bù đắp chi phí trợ giá cho số lượng lớn chuyến đi nền tảng của họ.
- **Mỏ vàng thực sự:** Trái lại, nhóm khách hàng đi chơi nội thành (`Urban Leisure`) thể hiện mức độ đàn hồi cực cao với giá cả. Voucher 25% đã kích hoạt sự bùng nổ nhu cầu (ATE = 2.5), mang lại mức ROI dương vượt trội (> 100%).
- **Khuyến nghị:** Dừng ngay lập tức chiến lược rải Voucher đại trà. Thay vào đó, áp dụng Uplift Modeling để tập trung toàn bộ ngân sách Marketing cho tập khách hàng `Urban Leisure`.

---

## 2. Phương pháp luận & Định vị Phân khúc (Methodology & Targeting)
Sử dụng K-Means Clustering, cơ sở người dùng được phân tách thành bốn nhóm hành vi (Personas):
- **Cluster 0 (Suburban Commuters):** Đi làm từ ngoại ô (Cầu không co giãn).
- **Cluster 1 (Urban Commuters):** Đi làm nội thành (Cầu không co giãn).
- **Cluster 2 (Urban Leisure):** Khách đi chơi nội thành giờ thấp điểm (Cầu co giãn siêu cao).
- **Cluster 3 (Suburban Occasionals):** Khách vãng lai ngoại ô.

---

## 3. Thiết kế Thí nghiệm (Experiment Design)
Thử nghiệm ngẫu nhiên có đối chứng (Randomized Controlled Trial - RCT):
- **Nhóm Can thiệp (Treatment Group):** Nhận Voucher giảm giá 25%.
- **Nhóm Đối chứng (Control Group):** Không nhận khuyến mãi.
- **Chỉ số Đánh giá Cốt lõi (OEC):** Số chuyến đi tăng thêm (Incremental Rides / ATE).
- **Chỉ số An toàn Tài chính (Guardrail Metric):** Tỷ suất Hoàn vốn (ROI) của chiến dịch.

---

## 4. Kết quả Phân tích: Sự bùng nổ của Hiệu ứng Dị thể (HTE)
Quá trình đánh giá song song giữa hai tập khách hàng đã chứng minh sức mạnh của HTE:
- **Nhóm Suburban Commuters:** Mặc dù số chuyến đi có tăng nhẹ (p < 0.05), nhưng mức tăng (+0.84 chuyến) là quá nhỏ. Việc trợ giá 25% cho một nhóm vốn đã đi xe thường xuyên dẫn đến hiệu ứng Bào mòn Lợi nhuận (Cannibalization).
- **Nhóm Urban Leisure:** Khách hàng nội thành có tần suất đi chơi thấp nhưng cực kỳ nhạy cảm với khuyến mãi. Voucher đã đánh trúng tâm lý, đẩy số chuyến đi tăng vọt (+0.91 chuyến - 2.5 chuyến tùy phân bổ), tạo ra mức Doanh thu thuần gia tăng dương kỷ lục.
- **Kết luận:** Việc hiểu đúng Insight khách hàng và áp dụng HTE đã cứu chiến dịch khỏi nguy cơ thua lỗ. 

---

## 5. Xác minh Độ tin cậy Hệ thống (System Trustworthiness)
Toàn bộ hệ thống đánh giá đã vượt qua kiểm định khắt khe bằng A/A Testing với **5.000 vòng lặp Monte Carlo**:
- **Lỗi Phân bổ Mẫu (SRM):** 4.82% (Hệ thống phân phối ngẫu nhiên 50/50 hoàn hảo).
- **Tỷ lệ Dương tính giả (FPR):** 4.74% (Kiểm soát tuyệt đối mức độ nhiễu và sai số ngẫu nhiên).
- Động cơ Thống kê (Statistical Engine) hoàn toàn miễn nhiễm với rủi ro đánh giá sai (Type I Error).

---

## 6. Lộ trình Triển khai Kế tiếp (Next Steps)
1. **Dừng phát hành Voucher** cho nhóm Commuters để bảo toàn lợi nhuận biên (Profit Margin).
2. **Thực thi Mở rộng (Roll-out):** Thiết lập chiến dịch Marketing tự động phát hành Voucher 25% độc quyền cho nhóm `Urban Leisure` vào các khung giờ thấp điểm.
3. **Thử nghiệm Uplift Modeling:** Xây dựng mô hình Machine Learning dự đoán Causal ML (Uplift) để gắp chính xác từng cá nhân thuộc nhóm "Persuadables" trong tệp khách hàng, tối ưu hóa triệt để chỉ số ROI.
