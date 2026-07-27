# Kế Hoạch Đề Xuất Uplift Modeling Với Mentor

Dưới đây là chiến lược chi tiết để bạn trao đổi với Mentor, thuyết phục anh/chị ấy chuyển hướng sang **Uplift Modeling** thay vì làm **Multi-Agent Simulation**.

---

## 1. Dữ liệu này có đủ chất lượng để làm Uplift Model không?
**Câu trả lời là CÓ, RẤT HOÀN HẢO.** 

Biểu đồ ROI bạn vừa chạy ra chính là "Bằng chứng vàng" (Golden Proof) cho sự tồn tại của **Hiệu ứng Dị thể (HTE - Heterogeneous Treatment Effect)**:
- **3 nhóm đốt tiền (ROI Âm):** Airport Business (-98.6%), Rain Riders (-44.4%), Urban Regulars (-28.7%). Họ đi xe bất chấp có Voucher hay không (Kháng sale).
- **2 nhóm mỏ vàng (ROI Dương):** Urban Leisure (+32.5%), Suburban Occasionals (+31.5%). Họ nhạy cảm với giá và chỉ đặt xe khi có Voucher.

**Tại sao dữ liệu này hoàn hảo cho Uplift?**
Vì dữ liệu đã được gán nhãn can thiệp ngẫu nhiên (`treatment_rand` = 0 hoặc 1), và có kết quả đầu ra rõ ràng (`y_rand`). Đây chính là định dạng chuẩn (Gold Standard) mà mọi thuật toán Uplift (như X-Learner, T-Learner, Uplift Random Forest) đều yêu cầu.

---

## 2. Kịch bản (Script) nói chuyện với Mentor

Bạn có thể dùng kịch bản sau, điều chỉnh lại theo văn phong của bạn:

> **Góc độ tiếp cận:** Đừng nói Multi-agent là sai. Hãy nói Uplift Model tạo ra "Impact" (Tác động kinh doanh) lớn hơn và sát với định hướng của phòng ban hơn.

**Phần mở đầu (Báo cáo kết quả 6 tuần):**
*"Em vừa hoàn thiện xong pipeline 6 tuần. Điểm nhấn lớn nhất là em phát hiện ra chiến dịch Voucher 25% đang bị **Cannibalization (Bào mòn lợi nhuận)** rất nặng ở nhóm khách đi sân bay và khách đi làm giờ cao điểm. Ngược lại, nhóm khách đi chơi cuối tuần lại mang về ROI dương tới hơn 30%. Biểu đồ phân tích HTE cho thấy sự khác biệt vô cùng rõ rệt."*

**Phần chuyển hướng (Pitching Uplift Model):**
*"Ban đầu, em định mở rộng dự án theo hướng mô phỏng Multi-agent. Nhưng sau khi nhìn biểu đồ ROI này, em nhận ra bài toán thực sự ở đây không phải là mô phỏng lại khách hàng, mà là làm sao **chỉ phát Voucher cho nhóm khách hàng mang lại ROI dương** (Nhóm Persuadables) và chặn Voucher khỏi nhóm Kháng sale.*

*Vì phòng ban mình đang tập trung rất mạnh vào bài toán tối ưu hóa chi phí Marketing, em nghĩ nếu 4 tuần tới em xây dựng một **Uplift Model** (như T-Learner hoặc Uplift Random Forest) trên chính tập dữ liệu A/B Test này thì sẽ tạo ra giá trị thực tiễn cao hơn rất nhiều. Model này sẽ dự đoán được ITE (Tác động Nhân quả Cá nhân) để quyết định có nên phát Voucher cho User A hay không.*

*Anh/chị thấy em bẻ lái sang Uplift Model cho 4 tuần cuối có hợp lý và mang lại nhiều value hơn cho team mình không ạ?"*

---

## 3. Lộ trình 4 Tuần Xây dựng Uplift Model (Dự kiến)

Nếu Mentor đồng ý, đây sẽ là lộ trình tiếp theo của bạn:
- **Tuần 7:** Tìm hiểu lý thuyết Uplift Modeling (T-Learner, S-Learner, X-Learner) và các thư viện (CausalML, EconML).
- **Tuần 8:** Xây dựng mô hình Baseline (T-Learner với XGBoost) sử dụng tập features hiện tại (`age`, `is_urban`, `fare_obs`...).
- **Tuần 9:** Đánh giá mô hình bằng **Qini Curve** và **Uplift Curve** (Các metric chuyên dụng cho Uplift, không dùng Accuracy/F1-score).
- **Tuần 10:** Báo cáo so sánh: Chiến lược phát Voucher bằng Uplift Model sẽ tiết kiệm được bao nhiêu tiền so với phát đại trà và so với K-Means segmentation.
