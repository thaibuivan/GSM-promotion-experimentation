# DÀN Ý SLIDE THUYẾT TRÌNH TUẦN 8: STRESS TEST

**Slide 1: Tại sao chúng ta cần Stress Test?**
- Phân tích tốt trên dữ liệu quá khứ là chưa đủ.
- Ban Giám Đốc cần câu trả lời: *"Hệ thống này có bị sập khi ra môi trường thực tế hỗn loạn không?"*
- Stress Test là bước Quality Assurance (Đảm bảo chất lượng) cuối cùng để cam kết sự an toàn cho dòng tiền của công ty.

**Slide 2: Các bài kiểm tra độ bền của Hệ thống**
- **Bài test 1 - Mở rộng quy mô:** Chạy cho 100,000 người, ATE không đổi, kết quả càng vững chắc.
- **Bài test 2 - A/A Test:** Giả lập Voucher bị hỏng (Tác dụng = 0). Hệ thống lập tức nhận diện và báo không có tác dụng $\rightarrow$ Loại bỏ hoàn toàn bệnh "ảo giác số liệu".

**Slide 3: Các kịch bản Cực đoan (Extreme Cases)**
- **Kịch bản Ngân sách hạn hẹp (Tỷ lệ 90/10):** Chuyện gì xảy ra nếu chỉ đủ tiền phát mã cho 10% khách hàng? Hệ thống vẫn tìm ra True Effect.
- **Kịch bản Thế giới thực (Bơm nhiễu):** Chuyện gì xảy ra nếu bão số 3 đổ bộ làm loạn số liệu? A/B Test chứng minh khả năng kháng nhiễu tuyệt đối nhờ việc san đều rủi ro cho cả 2 nhóm C và T.

**Slide 4: Lời khẳng định cuối cùng**
- Phương pháp đánh giá khuyến mãi của Xanh SM hiện tại không chỉ là "Đọc số liệu", mà là một **Hệ thống Khoa học Nhân quả (Causal Science)** bất khả xâm phạm.
- Chúng ta hoàn toàn có thể ra quyết định hàng tỷ đồng dựa trên báo cáo của hệ thống này!
