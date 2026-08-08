# BÁO CÁO PHÂN TÍCH & ĐỀ XUẤT: CHIẾN LƯỢC TỐI ƯU HÓA KHUYẾN MÃI
**Subject:** Đánh giá hiệu quả chiến dịch khuyến mãi bằng Causal Inference & Uplift Modeling  

---

## 1. Tóm tắt Nội dung (Executive Summary)
Dựa trên việc phân tích dữ liệu thử nghiệm (A/B Testing) và mô hình hóa hành vi khách hàng (Uplift Modeling), báo cáo này cung cấp cái nhìn định lượng về hiệu quả thực sự của các chiến dịch khuyến mãi (Voucher). Dữ liệu cho thấy việc phát hành mã đại trà (Mass Voucher) đang gặp rủi ro chi phí vô cùng lớn, gây lỗ ròng khổng lồ do phần lớn ngân sách bị lãng phí vào nhóm khách hàng kháng khuyến mãi (như *Airport Business*, *Urban Regulars*).

**Các đề xuất từ góc độ dữ liệu:**
1. **Dừng hoàn toàn việc phát mã đại trà (Mass Voucher):** Phân tích Economics Guardrail cho thấy chiến lược này đang làm tổn thất hơn $668,000 doanh thu thuần.
2. **Ưu tiên ngân sách tuyệt đối cho nhóm `Suburban Card`:** Phân tích A/B Test chỉ ra rằng đây là "mỏ vàng" duy nhất. Nhóm khách hàng Ngoại ô dùng Thẻ cực kỳ nhạy cảm với giá (ATE +1.36 chuyến) và khi nhắm mục tiêu vào nhóm này, công ty ghi nhận Doanh thu thuần (Net GMV) dương (+$4,548).
3. **Chiến thuật thay thế cho nhóm `Suburban Cash`:** Nhóm Ngoại ô dùng tiền mặt có độ nhạy Voucher khá (ATE +0.97 chuyến) nhưng giá trị chuyến đi thấp hơn khiến ROI âm (-24.5%). Đề xuất tạm ngưng tặng Voucher đi xe trực tiếp, thay vào đó chạy chiến dịch "Tặng 50k khi liên kết Thẻ Tín Dụng" để chuyển đổi họ thành tập `Suburban Card`.
4. **Thử nghiệm tích hợp thuật toán Uplift Modeling (Tuần 7):** Đề xuất đội ngũ xem xét việc sử dụng điểm số CATE (Conditional Average Treatment Effect) từ mô hình Uplift để tối ưu hóa việc phân bổ ngân sách xuống cấp độ cá nhân (ITE) thay vì chỉ phân khúc.

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
