# DÀN Ý SLIDE THUYẾT TRÌNH TUẦN 7: UPLIFT MODELING

**Slide 1: Tại sao lại là Uplift Modeling?**
- A/B Test truyền thống chỉ cho biết kết quả Trung bình (ATE) của cả tập đông.
- Uplift Modeling giúp cá nhân hóa (Personalization) để tìm ra "Ai mới là người thực sự cần Voucher?".
- Chuyển hóa Machine Learning thành bài toán tối ưu Lợi nhuận (ROI Optimization).

**Slide 2: Cách thức hoạt động của T-Learner**
- Xây dựng 2 bộ não AI (XGBoost) song song:
  - Não 1 (Control): Dự đoán hành vi tự nhiên.
  - Não 2 (Treatment): Dự đoán hành vi bị kích thích.
- Chấm điểm CATE = (Não 2) - (Não 1).

**Slide 3: Bằng chứng Thành công (Qini Curve)**
- [Chèn hình ảnh Qini Curve]
- Mô hình không chỉ chạy được, mà còn phân loại cực kỳ xuất sắc những khách hàng có tiềm năng thay đổi hành vi (Đường xanh vượt xa đường đứt nét).

**Slide 4: Bài toán Lợi nhuận & Điểm Hòa Vốn**
- Lãi gộp = 20k | Chi phí = 15k $\rightarrow$ CATE hòa vốn = 0.75 chuyến.
- Phân tích Top-20%: Tuy vẫn lỗ, nhưng mô hình đã giúp **CỨU THUA** (tránh thất thoát) hàng triệu đồng so với việc phát đại trà.
- Phán quyết cuối cùng từ AI: Nhóm Urban Cash là "Sure Things" & "Lost Causes". Tuyệt đối không phát mã!
