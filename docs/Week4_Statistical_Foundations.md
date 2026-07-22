# Sổ tay Cốt lõi Thống kê trong A/B Testing
*(Ghi chú đúc kết từ quá trình thực chiến phân tích A/B Testing - Tuần 4)*

---

## 1. Triết lý của Kiểm định Thống kê (Hypothesis Testing)
Tại sao Toán học luôn đi theo lối mòn giả định "Không có gì xảy ra"?

> [!NOTE] 
> **Quy tắc Trách nhiệm chứng minh (Burden of Proof):** 
> Kẻ nào đưa ra tuyên bố mới, kẻ đó phải tự đi chứng minh. Toán học mặc định mọi thứ là Vô Tác Dụng (Vô Tội) cho đến khi Data chứng minh điều ngược lại.

> [!TIP]
> **Điểm Neo Toán Học (Math Anchor):**
> Toán học cần một điểm neo cố định là **Độ chênh lệch = 0** để làm tâm điểm vẽ biểu đồ phân phối xác suất. Ta không thể lấy "Có tác dụng" làm Giả thuyết ban đầu vì "Có tác dụng" là một khoảng vô tận (1, 10, 100 chuyến xe), Toán học không biết phải neo vào đâu.

---

## 2. Ba Thành phần Cốt lõi của Một Cuộc Kiểm Định

1. **Giả thuyết Không (Null Hypothesis - $H_0$):** 
   - Điểm mỏ neo cố định. 
   - Luôn là lời khẳng định *"Mọi thứ đang bình thường, 2 nhóm bằng nhau, Voucher vô tác dụng (Hiệu ứng = 0)"*.

2. **Bằng chứng (Data / Observation):** 
   - Những con số chênh lệch thực tế mà chúng ta quan sát được từ kết quả đo lường (VD: Nhóm có Voucher đi nhiều hơn 1 chuyến so với nhóm không có).

3. **P-value (Cái thước đo độ vô lý):** 
   - P-value KHÔNG PHẢI là xác suất 2 nhóm bằng nhau.
   - P-value là: **"GIẢ SỬ $H_0$ ĐÚNG (2 nhóm thực sự bằng nhau 100%), thì xác suất để ta vô tình bốc ra được một mẫu dữ liệu bị chênh lệch lớn cỡ này do trùng hợp ngẫu nhiên là bao nhiêu?"**

---

## 3. Bản chất của P-value (Từ Mỏ Neo đến Xác Suất)

Làm sao máy tính tính ra được P-value? Nó đi qua 3 bước:
- **Bước 1 (Đóng cọc & Vẽ Chuông):** Máy tính đặt một cái cọc mỏ neo tại vị trí Số 0 (Không chênh lệch). Xung quanh số 0, nó vẽ một đường cong hình quả chuông. Đỉnh chuông nằm ở 0 (Dễ xảy ra nhất), đuôi chuông nằm ở rất xa (Khó xảy ra nhất).
- **Bước 2 (Đo khoảng cách - T-Statistic):** Nó cầm kết quả chênh lệch thực tế (Ví dụ chênh +1 chuyến) ném lên trục của quả chuông xem khoảng cách từ kết quả thực tế đến cái cọc Số 0 là bao xa (đo bằng bước chân/Standard Error).
- **Bước 3 (Diện tích Đuôi):** P-value chính là **diện tích phần đuôi quả chuông** tính từ điểm thực tế đó hắt ra ngoài viền. 
  - Đứng càng xa trung tâm $\rightarrow$ Diện tích đuôi càng bé $\rightarrow$ P-value càng nhỏ $\rightarrow$ Khả năng xảy ra tự nhiên cực thấp $\rightarrow$ BÁC BỎ $H_0$!

---

## 4. Nghệ thuật "Chọn Phe" khi Đọc P-value

Cùng là con số Ngưỡng **Alpha = 0.05 (5%)**, nhưng tùy vào mục đích bài toán mà ta sẽ cầu nguyện P-value lớn hơn hay nhỏ hơn mức này.

### Trận chiến 1: Sanity Check (Kiểm tra Lỗi Hệ Thống Randomization)
- **Vai diễn của bạn:** Luật sư bào chữa.
- **Mục tiêu:** Muốn chứng minh thân chủ (Hệ thống chia nhóm) vô tội, không bị lỗi lầm thiên vị gì cả.
- **$H_0$:** 2 nhóm hoàn toàn cân bằng (Chênh lệch = 0).
- **Thái độ:** Bạn cầu mong mọi khác biệt đo được chỉ là do nhiễu ngẫu nhiên.
- **Kết quả kỳ vọng:** **P-value > 0.05** (Thậm chí càng to càng tốt). Bạn thở phào nhẹ nhõm: *"Chênh lệch này rất dễ xảy ra tự nhiên. Trắng án! Chấp nhận $H_0$"*.

### Trận chiến 2: OEC Analysis (Đo lường Tác động của Voucher)
- **Vai diễn của bạn:** Công tố viên.
- **Mục tiêu:** Muốn buộc tội cái Voucher chính là "Thủ phạm" gây ra sự tăng trưởng doanh thu.
- **$H_0$:** Voucher vô dụng, 2 nhóm bằng nhau (Chênh lệch = 0).
- **Thái độ:** Bạn KHÔNG HỀ MUỐN sự tăng trưởng 1 chuyến xe kia là do trùng hợp may mắn tự nhiên.
- **Kết quả kỳ vọng:** **P-value < 0.05** (Càng nhỏ càng vinh quang). Bạn đập bàn: *"Xác suất để sự tăng trưởng này là do trùng hợp ngẫu nhiên chỉ là 0.1%. Quá vô lý! Bác bỏ $H_0$. Chính Voucher của tôi đã tạo ra sự khác biệt!"*.

---

> [!IMPORTANT]
> **Câu thần chú ghi nhớ:**
> *"Kiểm tra hệ thống thì mong LỚN HƠN 0.05. Kiểm tra tính năng mới (Experiment) thì mong NHỎ HƠN 0.05."*
