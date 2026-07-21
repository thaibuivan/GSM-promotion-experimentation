# GSM Promotion Experimentation: A/B Testing & Causal Inference

## 📌 Project Overview
Dự án này tập trung vào việc phân tích dữ liệu, thiết kế thí nghiệm (A/B Testing) và ứng dụng Causal Inference để tối ưu hóa chiến lược khuyến mãi cho nền tảng gọi xe (Ride-hailing). Mục tiêu là thiết kế cơ chế phát hành Voucher tối ưu ROI, giảm thiểu rủi ro "Cannibalization" (ăn thịt doanh thu) và đo lường chính xác giá trị gia tăng (Incremental Rides).

## 🗂️ Datasets
Dự án sử dụng phương pháp luận lai ghép (Hybrid Approach) từ 2 bộ dữ liệu để chuẩn bị cho bước Mô phỏng (Simulation) ở Tuần 3:
1. **TLC NYC Yellow Taxi (Thực tế):** Cung cấp các tham số vật lý của chuyến đi (Giá cước, Quãng đường, Khung giờ cao điểm, Mùa vụ).
2. **Kaggle Ride-Sharing (Mô phỏng):** Cung cấp cấu trúc cơ sở dữ liệu (Schema) ở cấp độ Khách hàng (User-level) với các định danh `User_ID`, `Driver_ID` và phân phối số lượng chuyến đi/người.

## 🚀 Lộ trình & Thành quả đạt được

### Tuần 1: Khám phá Dữ liệu (Exploratory Data Analysis - EDA)
- **`notebooks/week1_eda/`**: Phân tích làm sạch dữ liệu, xử lý Outliers và phân tích hành vi khách hàng.
  - Phân tích chuỗi thời gian (Time-pattern) để xác định giờ cao/thấp điểm.
  - Phân tích tương quan Giá cước - Quãng đường.
  - **Notebook 6:** Kiểm định chéo (Sanity Check) tính logic thực tế của dữ liệu Kaggle, bóc tách các trường dữ liệu ngẫu nhiên (Randomized) và các trường có logic kinh tế để chuẩn bị tham số cho mô phỏng Tuần 3.

### Tuần 2: Thiết kế Thí nghiệm (Experiment Design)
- **`docs/Week2_Experiment_Design_v1.md`**: Kịch bản **Macro (Time-based)**. Kích cầu giờ thấp điểm (Happy Hour 10AM-4PM). Đơn vị phân bổ (Randomization Unit) là các khu vực địa lý (Zone_ID).
- **`docs/Week2_Experiment_Design_v2.md`**: Kịch bản **Micro (User-targeted)**. Chiến dịch Re-engagement nhắm vào tệp khách hàng Regular (4-8 chuyến/tháng) đang có dấu hiệu "Ngủ đông". Đơn vị phân bổ là `User_ID`. Đây là kịch bản chính sẽ được dùng để chạy Causal Inference.

## 📁 Repository Structure
```
├── data/               # Chứa dữ liệu Raw & Processed (Đã ignore trên Git)
├── docs/               # Báo cáo chất lượng dữ liệu, Data Dictionary & Kịch bản A/B Test
├── notebooks/          # Notebooks phân tích (Jupyter) chia theo từng tuần
├── reports/            # Slide thuyết trình & Feature Catalogs
└── README.md           # Tài liệu tổng quan dự án
```

## 👥 Collaborators
- **Thai Bui Van** (Data Science Intern)
