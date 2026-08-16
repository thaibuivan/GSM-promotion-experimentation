# 📖 Sổ tay Hướng dẫn Sử dụng Dashboard (Product Manual)

Kính gửi Mentor và Quản lý Dự án (PM),

Tài liệu này là Sổ tay hướng dẫn (User Guide) chi tiết dành cho ứng dụng **GSM Promotion Experimentation Sandbox**. Dashboard này đóng vai trò là một "Data Product" hoàn chỉnh, giúp chuyển hóa các mô hình Toán học phức tạp (Double Machine Learning, Causal Inference) thành một công cụ Hỗ trợ Ra quyết định (Decision-Support Tool) trực quan và dễ sử dụng.

Xin mời anh/chị truy cập vào Dashboard thông qua link: **[Live Streamlit Dashboard](https://gsm-promotion-experimentation.streamlit.app)** và làm theo hướng dẫn dưới đây để khám phá chi tiết từng Tab.

---

## Tab 1: 📚 Data Foundation (Nền tảng Dữ liệu & Mô phỏng)
**Mục đích:** Khẳng định tính hợp lệ của Dữ liệu mô phỏng (Synthetic DGP) trước khi đi vào phân tích.

- **4 Chỉ số (KPIs) trên cùng:** Cung cấp quy mô của tập dữ liệu (Được hiệu chuẩn từ 3.04 triệu chuyến đi thực tế của NY TLC để sinh ra 20,000 user ảo).
- **Biểu đồ "Phân phối Cước phí" & "Khung giờ":** Anh/chị có thể quan sát đường cong đứt nét màu trắng (Reference Curve) ôm sát vào các cột Histogram của Sandbox. Điều này chứng minh Sandbox tuân thủ chính xác các tham số vật lý của đời thực (Ví dụ: Khách chủ yếu đi vào 8h sáng và 18h chiều).
- **📝 Key Takeaway:** Dữ liệu hoàn toàn đủ tiêu chuẩn (đã qua bước Calibration) để thực hiện các bài test nhân quả.

## Tab 2: 📏 Experiment Setup (Lập kế hoạch A/B Test)
**Mục đích:** Trình giả lập tính toán Cỡ mẫu (Sample Size) dành cho đội ngũ Marketing Planning.

- **Tính năng tương tác:** Anh/chị hãy thử kéo thanh trượt **Minimum Detectable Effect (MDE)** hoặc **Tỷ lệ chia nhóm Treatment**.
- **Quan sát kết quả:** Khung màu xanh bên dưới sẽ tự động tính toán lại số lượng user tối thiểu cần thiết để chiến dịch đạt chuẩn thống kê (Statistical Power = 80% hoặc 90%).
- **📝 Key Takeaway:** Đây là công cụ hữu ích trước khi chạy chiến dịch thực tế, giúp Marketing trả lời câu hỏi: *"Tôi cần phát voucher cho bao nhiêu người để đo lường được hiệu quả?"*

## Tab 3: 🩺 Experiment Health (Kiểm tra Sức khỏe Thí nghiệm)
**Mục đích:** Rào chắn bảo vệ (Guardrail Metrics) giúp phát hiện lỗi cấu trúc dữ liệu trước khi phân tích lợi nhuận.

- **SRM Check & A/A Calibration:** Hai chỉ số màu xanh "PASS" khẳng định hệ thống chia A/B Test chuẩn xác (tỷ lệ 50/50), không thiên vị và tỷ lệ báo động giả (False Positive) nằm ở ngưỡng an toàn 5%.
- **Biểu đồ SMD (Standardized Mean Difference):** Anh/chị chú ý hai đường đứt nét màu đỏ ở ngưỡng `-0.1` và `0.1`. Tất cả các biến số (Covariates) đều nằm gọn trong dải an toàn này, chứng tỏ nhóm nhận Voucher (Treatment) và nhóm Không nhận (Control) hoàn toàn tương đồng về mặt đặc điểm trước khi thí nghiệm diễn ra.
- **📝 Key Takeaway:** Thí nghiệm hợp lệ. Kết quả ATE phía sau hoàn toàn đáng tin cậy.

## Tab 4: 📊 A/B Results (Kết quả A/B Test Truyền thống)
**Mục đích:** Đo lường Hiệu ứng Trung bình (ATE) khi phát Voucher đại trà (Mass Targeting).

- **Khối Đánh giá Thống kê:** Hiển thị số chuyến đi tăng thêm trung bình (ATE Incremental Rides) kèm theo khoảng tin cậy 95% và p-value.
- **Khối Phân dịch Kinh doanh:** Anh/chị sẽ thấy nghịch lý xảy ra ở đây. Mặc dù số chuyến đi có TĂNG (Significant), nhưng ở ô **Net Profit (Lợi nhuận Ròng)** lại báo âm (màu đỏ).
- **📝 Key Takeaway:** Bảng cảnh báo màu vàng đã chỉ rõ: Phát Voucher đại trà cho tất cả mọi người gây Lỗ (do hiện tượng Cannibalization - khách không cần voucher vẫn đi xe). Chúng ta cần giải pháp thông minh hơn.

## Tab 5: 🎯 Heterogeneous Response (Nghịch lý Lợi nhuận)
**Mục đích:** Mổ xẻ sâu hơn hành vi của từng phân khúc khách hàng để tìm ra "Ai là người sinh lời?".

- **Bảng Persona Profiling:** Anh/chị click vào "Mở rộng" để xem định nghĩa của 5 nhóm khách hàng (vd: Airport Business, Rain Riders, v.v.).
- **Bảng Drill-down Tài chính:** Bảng này phân tích ROI theo từng nhóm. Những dòng màu xanh (ROI dương) là các mỏ vàng, trong khi những dòng màu đỏ tốn rất nhiều Burn (Chi phí khuyến mãi) nhưng Incremental GMV cực thấp.
- **Biểu đồ "Nghịch lý Lòng trung thành":** Phân tích ROI theo Recency. Khách càng gắn bó (Recency 0-4 ngày) thì ROI càng âm nặng nhất. Càng phát voucher cho khách quen, GSM càng lỗ vốn.
- **📝 Key Takeaway:** Phương pháp Segment Targeting (phát theo quy tắc phân khúc) tốt hơn Mass Targeting, nhưng vẫn chưa tối ưu triệt để.

## Tab 6: 💰 Policy Comparison (So sánh 6 Chiến lược)
**Mục đích:** Đánh giá hiệu suất của thuật toán AI (R-Learner) đối đầu với các chiến lược khác.

- **Chart A (Dự đoán) & Chart B (Thực tế - Oracle):** Anh/chị chú ý vào cột màu Cyan (**AI Profit Targeting**). Chiến lược này chỉ nhắm vào 22.2% khách hàng nhưng lại mang về Lợi nhuận cao nhất (~$7,939), lật ngược tình thế "Lỗ sấp mặt" của Mass Voucher.
- **Đường Qini Curve (trong Tab 5):** Thể hiện khả năng "Ranking" của mô hình AI, ưu tiên những người nhạy cảm với voucher lên đầu.
- **📝 Key Takeaway:** Mô hình R-Learner chứng minh được khả năng chọn lọc (targeting) xuất sắc và sẵn sàng cho việc Pilot ở môi trường thực tế.

## Tab 7: ⚙️ Policy Simulator (Trình Giả lập Chính sách)
**Mục đích:** Trải nghiệm cảm giác ra quyết định của một Quản lý Kinh doanh. 

Đây là phần tương tác cốt lõi nhất của Dashboard:
1. Mời anh/chị thử chỉnh **"Mức Khuyến mãi"** từ 15% lên 20%, hoặc giảm **"Biên lợi nhuận gộp"** xuống 50%.
2. Giới hạn **Ngân sách Chiến dịch** xuống một con số nhỏ hơn.
3. Quan sát Bảng So sánh Kịch bản bên tay phải tự động cập nhật lại Lợi nhuận dự kiến.
- **📝 Key Takeaway:** Công cụ này giúp Team Kinh doanh và Data làm việc chung với nhau. Data cung cấp thuật toán (EV prediction), Kinh doanh nhập constraints (Ngân sách, Margin) để tìm ra Policy tối ưu nhất cho từng thời điểm.

---
*Hy vọng cuốn Sổ tay này sẽ giúp anh/chị có một trải nghiệm liền mạch và hiểu rõ hơn về giá trị thực tiễn (Business Value) mà dự án mang lại!*
