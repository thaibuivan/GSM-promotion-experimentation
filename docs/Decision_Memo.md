# BÁO CÁO PHÂN TÍCH & ĐỀ XUẤT: CHIẾN LƯỢC TỐI ƯU HÓA KHUYẾN MÃI

**To:** Product Manager, Marketing Team  
**From:** Data Analyst / Data Science Intern  
**Date:** [Ngày hiện tại]  
**Subject:** Đánh giá hiệu quả chiến dịch khuyến mãi bằng Causal Inference & Uplift Modeling  

---

## 1. Tóm tắt Nội dung (Executive Summary)
Dựa trên việc phân tích dữ liệu thử nghiệm (A/B Testing) và mô hình hóa hành vi khách hàng (Uplift Modeling), báo cáo này cung cấp cái nhìn định lượng về hiệu quả thực sự của các chiến dịch khuyến mãi (Voucher). Dữ liệu cho thấy việc phát hành mã đại trà (Mass Voucher) đang gặp rủi ro chi phí cao hơn lợi nhuận gộp do một lượng lớn khách hàng thuộc nhóm "Sure Things" (khách hàng vẫn sử dụng dịch vụ kể cả khi không có khuyến mãi).

**Các đề xuất từ góc độ dữ liệu:**
1. **Cân nhắc điều chỉnh chiến lược đối với nhóm `Urban Cash` (Khách nội thành đi tiền mặt):** Mô hình Uplift cho thấy nhóm này có độ nhạy cảm với khuyến mãi rất thấp. Việc tiếp tục phát mã đại trà cho nhóm này có khả năng khó đạt được điểm hòa vốn. Đề xuất tạm ngưng hoặc thử nghiệm các hình thức marketing khác thay vì giảm giá trực tiếp.
2. **Ưu tiên ngân sách cho nhóm `Suburban Occasionals` (Khách ngoại ô thỉnh thoảng đi):** Phân tích A/B Test chỉ ra rằng khi thu hẹp mục tiêu (Segment Targeting) vào nhóm này, chi phí trên mỗi cuốc xe tăng thêm (CPIT) giảm đáng kể, giúp chiến dịch đạt được tiềm năng lợi nhuận ròng dương.
3. **Thử nghiệm tích hợp thuật toán Uplift Modeling:** Đề xuất đội ngũ xem xét việc sử dụng điểm số CATE (Conditional Average Treatment Effect) từ mô hình Uplift như một tham số tham khảo trước khi phân bổ tập khách hàng nhận khuyến mãi trong các chiến dịch tới.

## 2. Bối cảnh & Phương pháp Phân tích
Trong thời gian qua, các chiến dịch khuyến mãi nhắm vào việc thúc đẩy số chuyến đi có dấu hiệu gặp phải hiện tượng **Cannibalization (Ăn thịt doanh thu)**. 
Để giải quyết vấn đề này, nhóm Dữ liệu đã áp dụng hai phương pháp kiểm định:
- **A/B Testing:** Để đo lường Tác động Trung bình (ATE) và tính toán Chi phí/Lợi nhuận thực tế.
- **Uplift Modeling (Machine Learning):** Để đi sâu vào Tác động Cá nhân hóa (ITE/CATE), tìm ra những khách hàng thực sự thay đổi hành vi nhờ khuyến mãi (Persuadables).

## 3. Kết quả Phân tích Chi tiết (Key Findings)

### A. Đánh giá chiến lược A/B Testing
Chúng tôi đã mô phỏng kịch bản A/B Test trên 2 phân khúc. Số liệu ước tính cho thấy:
- **Phát đại trà (Mass Voucher):** Chi phí để tạo ra 1 chuyến đi tăng thêm (CPIT) ước tính là $29.65. So với giả định biên lợi nhuận gộp là $20/chuyến, tỷ suất ROI đang ở mức âm.
- **Nhắm mục tiêu cơ bản (Segment Targeting):** Khi chỉ nhắm vào nhóm *Suburban Occasionals*, CPIT ước tính giảm xuống còn $15.92. Điều này cho thấy khả năng sinh lời (ước tính lãi $4.08 trên mỗi chuyến tăng thêm).

### B. Kết quả Tối ưu hóa bằng Uplift Modeling (AI)
Đi sâu vào nhóm *Urban Cash* (nhóm có hiệu suất thấp), chúng tôi đã thử nghiệm thuật toán **T-Learner XGBoost**.
- Khi chạy giả lập mô hình để lọc ra **Top 20% khách hàng tiềm năng nhất**, hệ thống giúp **giảm thiểu 87% rủi ro chi phí (tránh thất thoát khoảng 3.78 triệu VND trên tập Test)** so với việc phát đại trà.
- Tuy nhiên, khi đối chiếu với bài toán tài chính (Break-even threshold), mô hình nhận định rằng ngay cả những người nhạy cảm nhất trong nhóm này cũng chưa vượt qua ngưỡng sinh lời.

## 4. Kiểm định Độ tin cậy (Robustness Check)
Để đảm bảo các kết luận trên không bị nhiễu bởi yếu tố ngẫu nhiên, hệ thống đã được kiểm tra chéo (Stress Test):
- Khi thay đổi tỷ lệ chia mẫu (Sample split 90/10) hoặc thêm các biến nhiễu ngẫu nhiên (Noise Injection), kết quả đo lường ATE từ A/B Test và khả năng xếp hạng của Uplift Model vẫn giữ được tính ổn định và nhất quán.

## 5. Đề xuất Kế hoạch Tiếp theo (Next Steps)
Nếu định hướng này được sự đồng thuận từ Business/Marketing, nhóm Dữ liệu đề xuất các bước tiếp theo:
1. **Pilot Test mô hình Uplift:** Triển khai thử nghiệm (A/B/C Test) mô hình T-Learner ở quy quy mô nhỏ (ví dụ 5% lượng traffic) để đối chiếu trực tiếp với rule-based hiện tại của Marketing.
2. **Thiết lập Dashboard theo dõi:** Xây dựng dashboard giám sát phân phối điểm CATE của khách hàng, giúp đội ngũ Business dễ dàng ra quyết định thiết lập ngưỡng (threshold) hòa vốn phù hợp cho từng chiến dịch.
3. **Khảo sát độ co giãn của giá:** Thu thập thêm dữ liệu về Price Elasticity ở nhóm Suburban để tinh chỉnh mức giảm giá tối ưu (Ví dụ: Cân nhắc giữa giảm 10% hay 20%).
