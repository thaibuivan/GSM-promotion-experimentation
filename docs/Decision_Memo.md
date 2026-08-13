# BÁO CÁO PHÂN TÍCH & ĐỀ XUẤT: CHIẾN LƯỢC TỐI ƯU HÓA KHUYẾN MÃI
**Subject:** Đánh giá hiệu quả chiến dịch khuyến mãi bằng Causal Inference & Uplift Modeling  

---

## 1. Tóm tắt Nội dung (Executive Summary)
Dựa trên việc phân tích dữ liệu thử nghiệm (A/B Testing) và mô hình hóa hành vi khách hàng (Uplift Modeling), báo cáo này cung cấp cái nhìn định lượng về hiệu quả thực sự của các chiến dịch khuyến mãi (Voucher). Dữ liệu cho thấy việc phát hành mã đại trà (Mass Voucher) đang gặp rủi ro chi phí vô cùng lớn, gây lỗ ròng khổng lồ do phần lớn ngân sách bị lãng phí vào nhóm khách hàng kháng khuyến mãi (như *Airport Business*, *Urban Regulars*).

**Các đề xuất từ góc độ dữ liệu:**
1. **Dừng hoàn toàn việc phát mã đại trà (Mass Voucher):** Phân tích Economics Guardrail cho thấy chiến lược này đang làm tổn thất hơn $116,000 doanh thu thuần do lãng phí vào nhóm kháng khuyến mãi (như *Airport Business*, *Urban Regulars*).
2. **Triển khai Chiến dịch Kép dựa trên PCA Segmentation:** Phương pháp PCA đã bóc tách thành công 2 tập khách hàng ngoại ô mang lại lợi nhuận, nhưng yêu cầu 2 chiến lược vận hành khác nhau:
   - **Chiến dịch Tối ưu Lợi nhuận (Target: `Suburban Card`):** Triển khai ngay Voucher 15%. Đây là tập khách hàng thanh toán thẻ, nhạy cảm giá (ROI +20.7%). Trải nghiệm thanh toán mượt mà mang lại lợi nhuận trực tiếp.
   - **Chiến dịch Chuyển đổi Hành vi (Target: `Suburban Cash`):** Khám phá mới cho thấy nhóm này có ROI tiềm năng cực cao (+24.7%). Tuy nhiên, để tránh rủi ro vận hành tiền mặt, đề xuất KHÔNG phát Voucher đi xe trực tiếp. Thay vào đó, chạy chiến dịch "Tặng Combo 3 mã 20% khi liên kết Thẻ" để ép chuyển đổi (Cashless Conversion), tăng giá trị vòng đời (LTV) dài hạn.
4. **Tiến tới Cá nhân hóa bằng Uplift Modeling (Tuần 5):** Đề xuất áp dụng Meta-Learners (T-Learner/X-Learner) để tính toán ITE (Tác động Cá nhân). Thay vì nhắm mục tiêu toàn bộ cụm `Suburban Card`, hệ thống sẽ chỉ phát mã cho những cá nhân "Persuadables" thực sự, tối đa hóa ROI.

## 2. Bối cảnh & Phương pháp Phân tích
Trong thời gian qua, các chiến dịch khuyến mãi nhắm vào việc thúc đẩy số chuyến đi có dấu hiệu gặp phải hiện tượng **Cannibalization (Ăn thịt doanh thu)**. 
Để giải quyết vấn đề này, nhóm Dữ liệu đã áp dụng hai phương pháp kiểm định:
- **A/B Testing:** Để đo lường Tác động Trung bình (ATE) và tính toán Chi phí/Lợi nhuận thực tế.
- **Uplift Modeling (Machine Learning):** Để đi sâu vào Tác động Cá nhân hóa (ITE/CATE), tìm ra những khách hàng thực sự thay đổi hành vi nhờ khuyến mãi (Persuadables).

## 3. Kết quả Phân tích Chi tiết (Key Findings)

### A. Đánh giá chiến lược A/B Testing & Phân khúc (K-Means)
Dựa trên thuật toán K-Means (K=5), chúng tôi đã tách được tập khách hàng thành 5 Personas với hành vi hoàn toàn khác biệt. Kết quả A/B Test mô phỏng trên các nhóm này cho thấy:
- **Phát đại trà (Mass Voucher):** Chiến dịch gây lỗ nặng (-$668,077) vì chi phí phát sinh khổng lồ trên những khách hàng đằng nào cũng đi xe.
- **Nhắm mục tiêu cơ bản (Segment Targeting):** Khi chỉ nhắm vào nhóm *Suburban Card*, chiến dịch tạo ra +3,776 chuyến đi tăng thêm. Trừ đi chi phí Voucher, chiến dịch này giữ lại được mức lợi nhuận ròng dương (+$4,548).

### B. Tối ưu hóa bằng Uplift Modeling (Định hướng)
Mặc dù Target theo Persona (như Suburban Card) đã mang lại ROI dương, nhưng nó vẫn là Target cấp độ nhóm. Bằng cách áp dụng các mô hình Machine Learning như T-Learner XGBoost trong tương lai, hệ thống sẽ lọc ra các khách hàng **Persuadables** ở mức độ cá nhân, từ đó có thể biến cả những nhóm đang có ROI âm trở thành các mỏ vàng mới.

## 4. Kiểm định Độ tin cậy (Robustness Check)
Để đảm bảo các kết luận trên không bị nhiễu bởi yếu tố ngẫu nhiên, hệ thống đã chạy một bài kiểm tra **A/A Test & Monte Carlo Simulation (1000 lần)**:
- Kết quả kiểm tra SRM (Sample Ratio Mismatch) và phân phối P-Value đều vượt qua ngưỡng kiểm định thống kê một cách hoàn hảo (FPR ~4.8%). Điều này chứng minh thuật toán Randomization hoạt động chính xác tuyệt đối.

## 5. Đề xuất Kế hoạch Tiếp theo (Next Steps)
Nếu định hướng này được sự đồng thuận từ Business/Marketing, nhóm Dữ liệu đề xuất các bước tiếp theo:
1. **Pilot Test mục tiêu `Suburban Card`:** Triển khai ngay chiến dịch thu hẹp trên tệp khách hàng Ngoại ô dùng Thẻ và theo dõi sự thay đổi của Gross Revenue trong 2 tuần.
2. **Thiết lập Dashboard theo dõi:** Xây dựng dashboard giám sát phân phối điểm CATE của khách hàng, giúp đội ngũ Business dễ dàng ra quyết định thiết lập ngưỡng (threshold) hòa vốn.
3. **Chạy chiến dịch liên kết thẻ:** Làm việc với Product Team để ra mắt in-app campaign thúc đẩy nhóm `Suburban Cash` nhập thông tin thẻ.
