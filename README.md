# GSM Promotion Experimentation: Từ A/B Testing đến Causal Inference & Uplift Modeling

## 📌 Tổng quan Dự án
Dự án này là một chuỗi quy trình toàn diện từ việc thiết kế thí nghiệm, phân tích dữ liệu, đến việc xây dựng hệ thống Trí tuệ Nhân tạo (Machine Learning) để tối ưu hóa chiến lược khuyến mãi (Voucher) cho nền tảng gọi xe Xanh SM (Ride-hailing).

Mục tiêu tối thượng: Thiết kế cơ chế phát hành Voucher để **Tối ưu ROI**, giảm thiểu rủi ro **Cannibalization (Ăn thịt doanh thu)** và đo lường chính xác **Incremental Rides (Giá trị gia tăng thực sự)** bằng Uplift Modeling.

---

## 🗂️ Nguồn Dữ liệu (Data Sources)
Dự án sử dụng phương pháp luận lai ghép (Hybrid Approach) kết hợp dữ liệu thực tế và mô phỏng:
1. **TLC NYC Yellow Taxi (Thực tế):** Cung cấp các tham số vật lý của chuyến đi (Giá cước, Quãng đường, Khung giờ).
2. **Kaggle Ride-Sharing (Thực tế):** Cung cấp cấu trúc người dùng (User-level) và phân phối chuyến đi.
3. **Synthetic Data (Mô phỏng):** Gắn các thuộc tính Persona (Urban Cash, Suburban Occasionals) và nhúng **True Uplift Effect** để phục vụ việc kiểm chứng Machine Learning.

---

## 🚀 Lộ trình Thực thi & Thành quả (8 Tuần)

### Giai đoạn 1: Khám phá Dữ liệu & Thiết kế Thí nghiệm (Tuần 1 & 2)
- Khai phá dữ liệu thô, phân tích Time-series và hành vi khách hàng.
- Xác định biến Can thiệp (Treatment Unit) và biến Mục tiêu (Outcome).
- Thiết kế Kịch bản A/B Testing cấp độ người dùng (User-level Re-engagement).

### Giai đoạn 2: Mô phỏng Dữ liệu & Đánh giá A/B Test (Tuần 3 & 4)
- Xây dựng luồng tạo dữ liệu giả lập (Synthetic Data Generation) nhúng sẵn các hiệu ứng Causal.
- Đánh giá A/B Test cơ bản (Chi-Square Test, T-Test).
- Khám phá hiện tượng **Mâu thuẫn Simpson (Simpson's Paradox)** và phân tích **Covariate Balance** bằng biểu đồ Violin.
- **Thành quả kinh doanh:** Chứng minh được phương pháp "Mass Voucher" gây lỗ nặng, trong khi "Segment Targeting" mang lại lãi ròng.

### Giai đoạn 3: Phân khúc Khách hàng & Phân tích Nhân quả (Tuần 5 & 6)
- Sử dụng K-Means Clustering để gán nhãn Persona cho khách hàng (Urban Cash, Suburban...).
- Áp dụng Causal Inference cơ bản (Linear Regression có biến tương tác) để khám phá HTE (Heterogeneous Treatment Effect).

### Giai đoạn 4: Uplift Modeling & Stress Test (Tuần 7 & 8)
- Triển khai thuật toán **T-Learner (XGBoost)** kết hợp Early Stopping & Validation Set.
- Đánh giá sức mạnh phân loại của mô hình bằng **Qini Curve** và **AUUC**.
- Tối ưu hóa **Profit Curve** (Tìm kiếm ngưỡng cắt CATE hòa vốn) để chuyển đổi từ Machine Learning sang Decision Making.
- Đóng gói bằng **Stress Test**: Kiểm định khả năng chống chịu của mô hình trước Tỷ lệ chia mẫu lệch (90/10) và Nhiễu dữ liệu (Gaussian Noise).

---

## 📁 Cấu trúc Kho lưu trữ (Repository Structure)
```
├── data/               # Chứa dữ liệu Raw & Processed (Đã ignore trên Git)
├── docs/               # Báo cáo, Data Dictionary, Decision Memo & Dàn ý Thuyết trình
├── notebooks/          # Notebooks phân tích (Jupyter) chia theo lộ trình 8 tuần
└── README.md           # Tài liệu tổng quan toàn bộ dự án
```

## 🎯 Kết luận Kinh doanh
Bằng việc ứng dụng Uplift Modeling để thiết lập **Ngưỡng CATE Hòa vốn**, hệ thống có khả năng tự động chặn phát mã cho những nhóm "Sure Things" hoặc "Lost Causes", giúp công ty tránh thất thoát hàng chục phần trăm ngân sách vô ích, mang lại lợi thế cạnh tranh tuyệt đối trên thị trường gọi xe công nghệ.

## 👥 Người thực hiện (Collaborators)
- **Thai Bui Van** (Data Science Intern)
