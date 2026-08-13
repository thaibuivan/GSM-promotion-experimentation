# GSM Promotion Experimentation: Từ A/B Testing đến Causal Inference & Uplift Modeling

## 📌 Tổng quan Dự án
Dự án này xây dựng một pipeline toàn diện — từ thiết kế thí nghiệm, phân tích nhân quả, đến Uplift Modeling — nhằm **minh họa cách một doanh nghiệp ride-hailing có thể chuyển từ mass promotion sang experimentation-driven, uplift-informed và profit-aware targeting**.

Câu hỏi kinh doanh trung tâm: *"Voucher có tạo thêm chuyến đi hay chỉ trợ giá cho những khách vốn đã sử dụng dịch vụ, và với ngân sách giới hạn nên phát voucher cho ai để tối đa hóa incremental profit?"*

> **⚠️ Lưu ý quan trọng:** Toàn bộ kết quả trong dự án này được kiểm chứng **trong môi trường mô phỏng (synthetic sandbox)** với dữ liệu tổng hợp. Các kết luận chứng minh pipeline ra quyết định hoạt động đúng dưới các assumptions đã thiết kế — không phải bằng chứng về hành vi khách hàng thực tế của GSM/Xanh SM. Policy thực tế cần được kiểm chứng bằng randomized experiment trên dữ liệu GSM thật.

---

## 🗂️ Nguồn Dữ liệu (Data Sources)
Dự án sử dụng phương pháp lai ghép (Hybrid Approach):
1. **TLC NYC Yellow Taxi (Public mobility data):** Cung cấp tham số vật lý chuyến đi (giá cước, quãng đường, khung giờ). Đây là dữ liệu giao thông công khai từ NYC, được dùng để hiệu chỉnh tham số mô phỏng — không phải dữ liệu vận hành thực tế của GSM.
2. **Kaggle Ride-Sharing (Community reference data):** Cung cấp tham chiếu cấu trúc người dùng và phân phối chuyến đi.
3. **Synthetic Causal User-Level Data (Mô phỏng):** Dữ liệu nhân quả tổng hợp (Synthetic DGP) tuân theo Structural Causal Model với Y0/Y1/true ITE được thiết kế sẵn. Đây là nền tảng cho toàn bộ evaluation.

---

## 🚀 Lộ trình Thực thi & Thành quả (6 Tuần)

### Giai đoạn 1: Khám phá Dữ liệu & Thiết kế Thí nghiệm (Tuần 1 & 2)
- Khai phá dữ liệu thô, phân tích Time-series và hành vi khách hàng.
- Xây dựng Synthetic DGP với Zero-Inflated Negative Binomial, nhúng heterogeneous treatment effect (HTE).
- Thiết kế kịch bản A/B Testing cấp độ người dùng.

### Giai đoạn 2: Phân khúc Khách hàng & Phân tích Nhân quả (Tuần 3 & 4)
- Sử dụng K-Means Clustering (K=5 với PCA) để gán nhãn Persona. K-Means phục vụ **giải thích nghiệp vụ và reporting**, không phải engine nhắm mục tiêu cuối cùng.
- A/A Testing (5000 lần Monte Carlo): Xác minh không phát hiện calibration issue đáng kể dưới các settings đã thử.
- A/B Testing với OLS HC1 covariate adjustment để đo ATE và ROI theo persona.
- Kết quả: Trong sandbox với assumptions hiện tại, segment-targeting cho policy value tốt hơn mass-targeting.

### Giai đoạn 3: Uplift Modeling & Policy Optimization (Tuần 5 & 6)
- Triển khai T-Learner, S-Learner, X-Learner (XGBoost) trên toàn eligible population.
- Đánh giá bằng Qini Curve, AUUC, và **profit-based policy comparison** (No Voucher / Mass / Segment / Uplift / Profit Targeting).
- Stress Test: Kiểm định robustness dưới tỷ lệ chia mẫu lệch và Gaussian noise.

---

## 📁 Cấu trúc Kho lưu trữ (Repository Structure)
```
├── data/               # Dữ liệu Raw & Processed (Đã ignore trên Git)
├── docs/               # Báo cáo, Data Dictionary, Decision Memo
├── notebooks/          # Notebooks phân tích theo tuần
├── src/
│   ├── dashboard/      # Streamlit Decision-Support Dashboard
│   └── pipeline/       # Data pipeline scripts
└── README.md
```

## 🎯 Kết luận & Định vị Đúng
Pipeline prototype này minh họa cách chuyển từ "A/B Testing + Uplift Model" thành **"Experimentation-Driven Promotion Decision System"**: đo incremental effect, dự đoán heterogeneous response, chuyển response thành expected profit, rồi chọn targeting policy tối ưu dưới ràng buộc ngân sách.

Khi có randomized GSM data thật, cùng pipeline có thể được dùng để estimate treatment response thực tế và benchmark policy mới trong champion–challenger experiments.

## 👥 Người thực hiện (Collaborators)
- **Thai Bui Van** (Data Science Intern)
