# Hướng dẫn Sử dụng Streamlit Dashboard (Dành cho Mentor / Reviewer)

Dashboard này là cầu nối (Data Product) giữa các mô hình khoa học dữ liệu phức tạp (Causal Inference, R-Learner) và quyết định kinh doanh. Thay vì đọc hàng nghìn dòng code hay bảng số liệu thô, Mentor/PM có thể sử dụng giao diện này để tương tác trực tiếp với kết quả dự án.

Dưới đây là hướng dẫn chi tiết ý nghĩa của từng Tab trên Dashboard:

## 1. 📚 Data Foundation (Nền tảng Dữ liệu)
- **Mục tiêu:** Chứng minh nguồn gốc dữ liệu và tính hợp lệ của môi trường mô phỏng (Sandbox).
- **Cách xem:** So sánh biểu đồ phân phối giữa Dữ liệu tham chiếu (Reference Data) và Dữ liệu mô phỏng (Synthetic Sandbox). Mục đích là để đảm bảo môi trường giả lập (Synthetic DGP) bảo toàn được các đặc trưng hành vi khách hàng giống đời thực (Giờ cao điểm, Phân phối giá cước).

## 2. 📏 Experiment Setup (Tính toán Cỡ mẫu)
- **Mục tiêu:** Công cụ hỗ trợ Marketing Planning.
- **Cách xem:** Trước khi chạy một chiến dịch khuyến mãi ngoài đời thực, PM có thể nhập các kỳ vọng (MDE - Minimum Detectable Effect) vào form. Công cụ sẽ tính ra chính xác cần bao nhiêu khách hàng tham gia (Sample Size) để A/B Test đạt chuẩn thống kê. Nếu số quá lớn (>100.000), hệ thống sẽ cảnh báo không khả thi.

## 3. 🩺 Experiment Health (Kiểm tra Sức khỏe Thí nghiệm)
- **Mục tiêu:** Chứng minh dữ liệu thí nghiệm không bị lỗi cấu trúc trước khi đem đi phân tích kết quả.
- **Cách xem:**
  - **SRM Check:** Đảm bảo hệ thống phân bổ đúng tỷ lệ 50/50, không có lỗi kỹ thuật (Sample Ratio Mismatch).
  - **A/A Calibration:** Chứng minh hệ thống không bị False Positive (báo động giả).
  - **SMD (Standardized Mean Difference):** Biểu đồ thể hiện tính đồng nhất (Balance) giữa nhóm Control và Treatment. Các thanh SMD phải nằm trong khoảng an toàn `[-0.1, 0.1]`.

## 4. 📊 A/B Results (Kết quả Trung bình ATE)
- **Mục tiêu:** Đọc kết quả A/B Test theo phương pháp truyền thống.
- **Cách xem:** Đọc cột Incremental GMV và Net Profit. Lưu ý bảng cảnh báo màu vàng: Việc phát Voucher ĐẠI TRÀ (Mass Voucher) đang gây LỖ RÒNG vì hiệu ứng tăng thêm (ATE) không bù đắp nổi chi phí phát voucher cho người vốn dĩ đã có ý định đi xe (Cannibalization).

## 5. 🎯 Heterogeneous Response (Nghịch lý Lợi nhuận)
- **Mục tiêu:** Mổ xẻ sâu hơn tại sao Mass Voucher lại lỗ, và nhóm khách hàng nào mới là nhóm sinh lời.
- **Cách xem:**
  - **Bảng Persona ROI:** Xem ROI của từng nhóm. Có nhóm lợi nhuận dương (màu xanh), có nhóm lỗ nặng (màu đỏ).
  - **Nghịch lý Lòng trung thành:** Biểu đồ chứng minh rằng khách càng "ruột" (Recency thấp) thì hiệu quả Voucher càng kém do bị ăn lẹm doanh thu tự nhiên. Đây là cơ sở tiền đề bắt buộc phải dùng AI Targeting.

## 6. 💰 Policy Comparison (So sánh 6 Chiến lược)
- **Mục tiêu:** Thấy được sức mạnh vượt trội của R-Learner (AI Profit Targeting).
- **Cách xem:** So sánh chiều cao của các cột lợi nhuận (Predicted Profit). Cột màu Cyan (AI Profit Targeting) nhắm vào khoảng 22.2% khách hàng nhưng mang lại lợi nhuận Dương cao nhất, đánh bại cả Rule-based Segment Targeting. So sánh với cột Oracle (Màu xanh lá) để xem mức độ "tiếc nuối" (Oracle Regret).

## 7. ⚙️ Policy Simulator (Trình Giả lập Chính sách)
- **Mục tiêu:** Trải nghiệm "What-if" scenario planning.
- **Cách xem:** Kéo các thanh trượt bên trái (thay đổi Ngân sách chiến dịch, Biên lợi nhuận, Mức giảm giá). Bảng bên phải sẽ realtime tính toán lại Lợi nhuận kỳ vọng của tất cả các chiến lược dưới bối cảnh kinh tế mới. Từ đó giúp PM ra quyết định: "Với 50.000$ ngân sách, nên chọn Policy nào?".

## 8. 🛠️ Developer Tools
- **Mục tiêu:** Khu vực dành riêng cho Data Engineer/Scientist.
- **Cách xem:** (Hiện đã bị khóa trên Public Cloud). Dùng để trigger chạy lại toàn bộ Pipeline (Data Generation -> A/A Test -> Model Training) từ đầu.
