# DECISION MEMO: CHIẾN LƯỢC KHUYẾN MÃI XANH SM

**To:** Ban Giám đốc (C-Level), Trưởng phòng Marketing  
**From:** Data Science Team  
**Date:** [Ngày hiện tại]  
**Subject:** Tối ưu hóa ROI Khuyến mãi bằng phương pháp Causal Inference & Uplift Modeling  

---

## 1. Tóm tắt Thực thi (Executive Summary)
Chiến lược "Mass Voucher" (Phát mã khuyến mãi đại trà) hiện tại đang gây ra tình trạng **bào mòn lợi nhuận nghiêm trọng**. Phân tích A/B Testing và mô hình Uplift trên tập khách hàng giả lập cho thấy một tỷ lệ lớn khách hàng nhận Voucher là nhóm "Sure Things" (Không có mã vẫn đi) - dẫn đến chi phí khuyến mãi (CPIT) cao hơn biên lợi nhuận gộp.

**Khuyến nghị chính:**
1. **Dừng ngay lập tức** việc phát mã đại trà cho nhóm `Urban Cash` (Khách nội thành đi tiền mặt). Kể cả khi áp dụng AI tối ưu, nhóm này vẫn không thể vượt qua ngưỡng hòa vốn.
2. **Chuyển hướng ngân sách** sang nhóm `Suburban Occasionals` (Khách ngoại ô thỉnh thoảng đi). Việc áp dụng chiến lược nhắm mục tiêu cơ bản (Segment Targeting) vào nhóm này đã chứng minh mang lại lợi nhuận ròng dương.
3. Áp dụng thuật toán **Uplift Modeling** làm bộ lọc tiêu chuẩn cho toàn bộ các chiến dịch Marketing trong tương lai để tối thiểu hóa thất thoát ngân sách.

## 2. Bối cảnh Kinh doanh & Thách thức
Trong thời gian qua, các chiến dịch khuyến mãi nhắm vào việc thúc đẩy số chuyến đi gặp phải hiện tượng **Cannibalization (Ăn thịt doanh thu)**. Hàng triệu đồng đã bị lãng phí cho nhóm khách hàng lẽ ra không cần trợ giá.

Câu hỏi đặt ra là: *"Làm thế nào để chỉ chi tiền cho những khách hàng thực sự thay đổi hành vi nhờ vào khuyến mãi?"*

## 3. Kết quả Phân tích Dữ liệu (Findings)

### A. Giai đoạn 1: Đo lường Hiệu quả bằng A/B Testing
Chúng ta đã chạy một kịch bản A/B Test nhắm vào 2 phân khúc chính. Kết quả cho thấy:
- **Mass Voucher (Đại trà):** Chi phí để tạo ra 1 chuyến đi tăng thêm (CPIT) lên tới $29.65. Với biên lợi nhuận gộp là $20/chuyến, chiến dịch bị **LỖ -$9.65 trên mỗi chuyến**.
- **Segment Targeting (Nhắm mục tiêu cơ bản):** Khi chỉ nhắm vào nhóm *Suburban Occasionals*, CPIT giảm xuống còn $15.92. Điều này giúp chiến dịch đảo chiều, mang lại **LÃI $4.08 trên mỗi chuyến**.

### B. Giai đoạn 2: Tối ưu hóa bằng Uplift Modeling (AI)
Nhóm *Urban Cash* đang là một "hố đen" hút ngân sách. Chúng tôi đã sử dụng thuật toán **T-Learner XGBoost** để tìm kiếm nhóm khách hàng sinh lời trong phân khúc này. 

**Kết quả từ mô hình AI:**
- Thuật toán giúp dự đoán chính xác sự gia tăng số chuyến đi (CATE) của từng cá nhân.
- Khi so sánh chiến lược **Top-20% Targeting** với việc phát đại trà, mô hình đã giúp **tránh thất thoát (tránh lỗ thêm) lên tới 3.78 triệu VND** (Giảm thiểu 87% rủi ro thua lỗ trên tập Test).
- Tuy nhiên, khi tối ưu hóa điểm chuẩn CATE hòa vốn (Break-even threshold), mô hình xác nhận rằng **0% khách hàng** trong nhóm này đủ khả năng sinh lời dương. 

## 4. Kiểm định Độ bền (Stress Test)
Để đảm bảo các kết luận trên là vững chắc, hệ thống đã được thử nghiệm dưới các kịch bản khắc nghiệt (Stress Test):
- **Tỷ lệ chia mẫu lệch (90/10)**: Phương sai tăng lên nhưng bản chất của ATE không thay đổi.
- **Bơm nhiễu ngẫu nhiên (Noise Injection)**: Kết quả đo lường hiệu ứng nhân quả vẫn chính xác, chứng minh phương pháp A/B Test loại bỏ hoàn toàn được nhiễu bên ngoài.

## 5. Kế hoạch Hành động (Next Steps)
1. **Triển khai kỹ thuật:** Tích hợp mô hình Uplift (T-Learner) vào hệ thống phát hành Voucher tự động (Rule Engine). Bất kỳ chiến dịch nào cũng phải chạy qua bộ lọc tính điểm CATE.
2. **Quy tắc Kinh doanh:** Thiết lập tham số CATE hòa vốn tự động dựa trên (Chi phí Voucher / Lãi gộp chuyến). Chặn đứng việc phát mã cho những người có CATE dưới ngưỡng này.
3. **Thử nghiệm mới:** Khởi tạo chiến dịch A/B Test đợt 2, nhắm riêng vào nhóm Suburban để tinh chỉnh mức độ nhạy cảm về giá (Price Elasticity).
