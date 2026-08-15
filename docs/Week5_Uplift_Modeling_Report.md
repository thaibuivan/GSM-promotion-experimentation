# BÁO CÁO KỸ THUẬT: UPLIFT MODELING (TUẦN 5)

## 1. Mục tiêu (Objective)
Áp dụng thuật toán Causal Machine Learning (Uplift Modeling) để xác định chính xác những cá nhân nào trong tập khách hàng có khả năng sinh lời cao nhất nếu được tặng Voucher. Mục tiêu cốt lõi là giải quyết bài toán "Cannibalization" (ăn lẹm doanh thu từ những khách hàng kiểu gì cũng sẽ sử dụng dịch vụ) bằng cách chuyển từ mô hình dự đoán hành vi thông thường (dự đoán $Y$) sang mô hình dự đoán hiệu ứng can thiệp (dự đoán Incremental Treatment Effect - $CATE$).

## 2. Thiết kế Mô hình Toán học: R-Learner (Double Machine Learning)
Dự án sử dụng kiến trúc **R-Learner (Residual Learner)** thay vì các phương pháp truyền thống như T-Learner (Two-Model) hay S-Learner (Single-Model) để cô lập hoàn toàn tín hiệu nhân quả khỏi các yếu tố nhiễu nền (Base Outcome Bias). 

Quy trình huấn luyện bao gồm 2 bước (Double Machine Learning) trên dữ liệu A/B Testing giả lập:

- **Bước 1: Khử nhiễu nền (Orthogonalization)**
  - Train một mô hình cơ sở (XGBoost Regressor) để dự đoán số chuyến đi tự nhiên $\hat{m}(X)$ của người dùng mà không cần biết họ có nhận Voucher hay không.
  - Tính phần dư của Outcome (Lượng chuyến đi bất thường): $\tilde{Y} = Y - \hat{m}(X)$
  - Tính phần dư của Treatment (Độ lệch so với xác suất nhận Voucher ngẫu nhiên $p=0.5$): $\tilde{T} = T - p$

- **Bước 2: Huấn luyện CATE (Conditional Average Treatment Effect)**
  - Mục tiêu huấn luyện mới (Uplift Target): $Y_{target} = \tilde{Y} / \tilde{T}$
  - Trọng số mẫu (Sample Weights): $W = \tilde{T}^2$
  - Huấn luyện mô hình XGBoost thứ hai dự đoán $CATE$ bằng cách fit trên $Y_{target}$ với trọng số $W$. Bằng cách này, mô hình tập trung hoàn toàn vào việc tối ưu hóa tín hiệu nhân quả tinh khiết.

## 3. Business Translation (Từ Khoa học Dữ liệu đến Tài chính)
Một mô hình CATE tốt chỉ dự đoán được số lượng chuyến đi tăng thêm (Incremental Rides). Để tối ưu hóa lợi nhuận thực tế, dự án sử dụng hệ thống chuyển đổi **Expected Value (EV)**.

Giá trị biên lợi nhuận kỳ vọng của mỗi User $i$ khi được tặng Voucher được tính bằng công thức:
$$ EV_i = (CATE_i \times Margin) - (\hat{Y}_{treated, i} \times Voucher\_Cost) $$
*Trong đó:*
- $CATE_i$: Số chuyến đi tăng thêm (do mô hình R-Learner dự đoán).
- $Margin$: Lợi nhuận biên trên mỗi chuyến đi.
- $\hat{Y}_{treated, i} = \hat{m}(X_i) + \frac{1}{2} CATE_i$: Tổng số chuyến đi dự kiến nếu được tặng Voucher.
- $Voucher\_Cost$: Chi phí Voucher (tỷ lệ phần trăm trên giá cước).

**Luật nhắm mục tiêu (Targeting Rule):** Chỉ phân phối Voucher cho những người có $EV_i > 0$.

## 4. Kết quả Thực nghiệm (Policy Comparison trên Tập Test)
Mô hình được đưa vào một cuộc đua mô phỏng (Policy Simulator) đối đầu với 5 chiến lược phân bổ khác. Dưới điều kiện giả định của Sandbox hiện tại:

- **Kết quả Profit Targeting (R-Learner):**
  - Số lượng nhắm mục tiêu: **888 / 4000 users (22.2%)**
  - Lợi nhuận kỳ vọng (Predicted Profit): **~$7,939**
  - Đây là chiến lược mang lại lợi nhuận cao nhất trong số các phương pháp tiếp cận thực tế.

- **Đánh giá Benchmark & Oracle Regret:**
  - Lợi nhuận của Benchmark Causal (Synthetic Causal Benchmark Profit): **~$7,060**
  - Lợi nhuận Tối đa Lý thuyết (Oracle Benchmark - Sử dụng Ground-Truth CATE): **~$10,818**
  - Mức độ tiếc nuối (Oracle Regret): **~$3,758 (34.7%)**. 

## 5. Đánh giá Mô hình (Model Evaluation)
- **Qini Curve & Ranking Signal:** R-Learner shows positive ranking signal relative to random in the held-out synthetic test set. Đường Qini vồng lên rõ rệt chứng tỏ AI có khả năng ưu tiên những khách hàng nhạy cảm với khuyến mãi tốt hơn việc phát ngẫu nhiên.
- **Calibration Status:** Mặc dù khả năng Ranking là rất hữu ích cho bài toán tối ưu (Useful Ranking Signal), khả năng hiệu chuẩn ở cấp độ CATE (CATE level calibration) vẫn còn imperfect.

> [!TIP]
> **Kết luận Hành động:** Khung học máy (R-Learner) và bộ quy tắc Business Translation đã sẵn sàng để trở thành lõi (Engine) cho hệ thống nhắm mục tiêu. Khi triển khai trên dữ liệu thực (Real-world Data), kiến trúc này dự kiến sẽ tiếp tục phát huy khả năng "lọc" khách hàng sinh lời.
