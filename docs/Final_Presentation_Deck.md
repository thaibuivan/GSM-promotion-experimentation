# BỐ CỤC SLIDE THUYẾT TRÌNH CẤP C-LEVEL
*(Dành cho Giám đốc Marketing / Giám đốc Dữ liệu)*

---

## Slide 1: Tiêu đề & Mục tiêu
- **Tiêu đề:** Tối ưu hóa ROI Khuyến mãi bằng Khoa học Dữ liệu
- **Phụ đề:** Từ "Phát đại trà" đến "Nhắm mục tiêu cá nhân hóa" với Uplift Modeling.
- **Mục tiêu:** Trình bày kết quả A/B Test và đề xuất thuật toán tối ưu phân bổ Voucher để loại bỏ hoàn toàn lãng phí (Cannibalization).
- **Trình bày bởi:** Data Science Team.

---

## Slide 2: Vấn đề hiện tại - "Nỗi đau" của Marketing truyền thống
- **Thực trạng:** Chiến dịch phát Voucher "Ai cũng có phần" (Mass Voucher) đang là con dao hai lưỡi.
- **Nỗi đau (Pain Point):** 
  - Một lượng lớn ngân sách đang đổ vào túi nhóm **Sure Things** (Khách hàng dù không có Voucher vẫn đi xe).
  - Công ty đang tự "Ăn thịt doanh thu" (Cannibalization) của chính mình.
- **Bằng chứng từ A/B Test:** CPIT (Cost per Incremental Trip) của chiến dịch Đại trà lên tới **$29.65**, trong khi biên lợi nhuận thu về chỉ là **$20.00**. Kết quả: Càng phát mã càng LỖ!

---

## Slide 3: Giải pháp 1 - Phân khúc Khách hàng (Segment Targeting)
- Thay vì phát đại trà, tập trung vào nhóm **Suburban Occasionals** (Khách ngoại ô đi ít).
- **Kết quả A/B Test:**
  - CPIT giảm mạnh từ $29.65 xuống còn **$15.92**.
  - Lợi nhuận ròng: **Đảo chiều từ Lỗ thành LÃI $4.08/chuyến**.
- **Kết luận bước 1:** Việc khoanh vùng theo phân khúc cơ bản đã cứu được chiến dịch. Nhưng liệu ta có thể làm tốt hơn đối với những phân khúc "khó nhằn" (như *Urban Cash*) không?

---

## Slide 4: Giải pháp 2 - Uplift Modeling (Làm chủ AI)
- **Concept:** Uplift Modeling không dự đoán "Ai sẽ đi xe", mà dự đoán "Ai sẽ ĐI THÊM nhờ sự tác động của cái Voucher".
- **Phương pháp tiếp cận (T-Learner):**
  - Sử dụng 2 bộ não AI (XGBoost) để so sánh hành vi giả lập của cùng 1 khách hàng: (Khi được nhận mã) vs (Khi không được nhận mã).
- **Kết quả đo lường bằng Qini Curve:** 
  - Đường cong Qini vút cao khẳng định AI đã tìm ra chính xác những cá nhân nhạy cảm với khuyến mãi.
  - [Chèn hình ảnh Qini Curve từ file Notebook Tuần 7 vào đây]

---

## Slide 5: Tối ưu Lợi nhuận - Thuật toán "Người Gác Cổng"
- Áp dụng bộ lọc Uplift vào tập khách hàng tệ nhất (*Urban Cash*):
  - **Mass Voucher (Đại trà):** Gây thất thoát lớn (VD: Lỗ -4,3 triệu VND trên tập Test).
  - **Uplift Top-20%:** Giảm thiểu thiệt hại xuống chỉ còn (Lỗ -535k VND). 
  - **Kết quả thực tế:** AI giúp công ty **TRÁNH THẤT THOÁT 87%** số tiền vô ích.
- **Phát hiện vĩ đại nhất (Ngưỡng hòa vốn):** 
  - Dựa trên chi phí (15k) và lãi gộp (20k), hệ thống tự động tính ra **Ngưỡng CATE Hòa vốn = 0.75**.
  - Hệ thống tự động chặn phát mã cho toàn bộ tập khách hàng *Urban Cash* vì không ai vượt qua ngưỡng sinh lời.

---

## Slide 6: Kết luận & Kế hoạch hành động
1. **Dừng hoàn toàn** các chiến dịch Mass Marketing mù quáng.
2. **Kích hoạt Rule Engine:** Đưa thuật toán Uplift Modeling (T-Learner) lên môi trường Production. Mọi tệp khách hàng trước khi nhận Voucher phải vượt qua ngưỡng điểm CATE > 0.75.
3. **Thử nghiệm mới:** Liên tục mở các mini-A/B Test để đo lường CATE trên các nhóm khách hàng mới nhằm tìm ra "Mỏ vàng" lợi nhuận.
