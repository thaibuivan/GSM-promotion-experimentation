# Báo cáo Đánh giá Thí nghiệm: Chiến dịch Khuyến mãi Voucher 25%

**Bối cảnh Dự án:** Đo lường tác động nhân quả (Causal Measurement) của Voucher giảm giá 25% lên mức độ tương tác của người dùng.
**Đơn vị thực hiện:** Nhóm Khoa học Dữ liệu (Data Science Team)
**Trạng thái Hệ thống:** TIN CẬY (Đã được xác minh qua Mô phỏng A/A Testing)

---

## 1. Tóm tắt Thực thi (Executive Summary)
Một chiến dịch A/B Testing đã được triển khai tập trung vào phân khúc khách hàng `Suburban Commuters` nhằm đánh giá hiệu quả thực tiễn của Voucher giảm giá 25%. Kết quả thử nghiệm cho thấy những tín hiệu tích cực về cả mặt thống kê và tài chính:
- **Chỉ số Cốt lõi (OEC):** Việc áp dụng Voucher đã mang lại sự gia tăng có ý nghĩa thống kê về số lượng chuyến đi trung bình trên mỗi khách hàng.
- **Tác động Tài chính (ROI):** Doanh thu gộp gia tăng từ các chuyến đi phát sinh đã bù đắp hoàn toàn chi phí phát hành Voucher ($5/người dùng), dẫn đến Tỷ suất Hoàn vốn (ROI) dương.
- **Khuyến nghị:** Dựa trên các dữ liệu đánh giá toàn diện, nhóm dự án khuyến nghị triển khai mở rộng (Roll-out) toàn bộ chiến dịch này trên phân khúc khách hàng mục tiêu.

---

## 2. Phương pháp luận & Định vị Phân khúc (Methodology & Targeting)
Nhằm tối ưu hóa chi phí Marketing, dự án áp dụng phương pháp Học máy Không giám sát (Unsupervised Learning - K-Means Clustering) để phân tách cơ sở người dùng thành các phân khúc chuyên biệt.
- Thuật toán đã định danh thành công bốn nhóm hành vi (Personas) chính.
- Các phân khúc có mức độ tương tác sẵn có cao (ví dụ: `Urban Commuters`) được loại trừ để tránh lãng phí ngân sách (Cannibalization).
- **Lựa chọn Phân khúc Mục tiêu:** Nhóm `Suburban Commuters` (chiếm 17.5% tổng quy mô người dùng) được chọn làm đối tượng thử nghiệm. Nhóm này sở hữu tiềm năng di chuyển cao (thường di chuyển vào giờ cao điểm) nhưng đang có dấu hiệu giảm tần suất tương tác (Recency cao), do đó rất phù hợp để áp dụng các đòn bẩy kích cầu.

---

## 3. Thiết kế Thí nghiệm (Experiment Design)
Thử nghiệm ngẫu nhiên có đối chứng (Randomized Controlled Trial - RCT) được thiết lập để cô lập tác động nhân quả của Voucher:
- **Nhóm Can thiệp (Treatment Group - 50%):** Nhận Voucher giảm giá 25%.
- **Nhóm Đối chứng (Control Group - 50%):** Không nhận khuyến mãi.
- **Chỉ số Đánh giá Cốt lõi (OEC):** Số chuyến đi tăng thêm (Incremental Rides).
- **Chỉ số An toàn Tài chính (Guardrail Metric):** Tỷ suất Hoàn vốn (ROI) của chiến dịch (Yêu cầu > 0).

---

## 4. Kết quả Phân tích Thống kê & Tài chính
Quá trình phân tích dữ liệu thực nghiệm bằng phép kiểm định Independent T-Test đã đưa ra những kết luận sau:
- **Độ tin cậy của Hệ thống phân bổ (Sanity Check):** Các biến hiệp phương sai nền tảng (như `age`, `monthly_rides_history`) thể hiện sự cân bằng hoàn hảo giữa nhóm Treatment và Control (P-value > 0.05), xác nhận quá trình phân bổ ngẫu nhiên hoạt động chính xác.
- **Hiệu quả Chiến dịch (OEC Uplift):** Nhóm Treatment ghi nhận sự gia tăng đáng kể về tần suất sử dụng dịch vụ. Chỉ số P-value < 0.05 khẳng định mức tăng trưởng quan sát được có ý nghĩa thống kê và hoàn toàn bắt nguồn từ sự can thiệp của Voucher, loại trừ khả năng dao động ngẫu nhiên của thị trường.
- **Tính Sinh lời:** Doanh thu thuần gia tăng từ nhóm Treatment vượt trội so với tổng chi phí chiến dịch, mang lại mức Lợi nhuận Thuần và ROI dương tính.

---

## 5. Xác minh Độ tin cậy Hệ thống (System Trustworthiness)
Để đảm bảo tính trung thực của các phát hiện trên, toàn bộ quy trình thử nghiệm đã trải qua quá trình kiểm tra giới hạn (Stress-testing) thông qua Mô phỏng Monte Carlo A/A Testing (1.000 vòng lặp):
- **Lỗi Phân bổ Mẫu (SRM):** Tỷ lệ lỗi SRM đo được ở mức 4.90%, khẳng định hệ thống phân phối lưu lượng không có thiên kiến.
- **Độ phân phối P-Value:** Kiểm định Kolmogorov-Smirnov (KS) chứng minh phân phối của P-value là phân phối đều chuẩn mực (Tỷ lệ Dương tính giả đạt 5.60%).
Sự xác minh này cung cấp bằng chứng kỹ thuật đảm bảo rằng động cơ phân tích hoàn toàn ổn định, và các mức tăng trưởng được báo cáo có độ tin cậy cực kỳ cao.

---

## 6. Lộ trình Triển khai Kế tiếp (Next Steps)
1. **Thực thi Mở rộng (Roll-out):** Cấu hình hệ thống Marketing Automation để phân phối tự động Voucher 25% cho toàn bộ phân khúc `Suburban Commuters`.
2. **Giám sát Hậu triển khai:** Theo dõi sát sao các chỉ số an toàn phụ trợ (như Tỷ lệ hủy chuyến của đối tác tài xế, Tỷ lệ gỡ cài đặt ứng dụng do thông báo spam) trong 72 giờ đầu tiên của giai đoạn Roll-out.
3. **Thử nghiệm Kế tiếp:** Bắt đầu quy trình thiết kế và tối ưu hóa các kịch bản thử nghiệm mới dành riêng cho phân khúc tiềm năng tiếp theo (`Suburban Occasionals`).
