# Hướng dẫn sử dụng Dashboard

Dashboard là giao diện ra quyết định cho **customer-level synthetic sandbox**. Nó minh họa cách đi từ bằng chứng nhân quả đến chính sách phát voucher, không đại diện cho dữ liệu hay chính sách vận hành thực tế của GSM.

Truy cập: [Live Streamlit Dashboard](https://gsm-promotion-experimentation.streamlit.app)

## Assumption hiện tại

- Voucher bằng **15% giá cước mỗi chuyến và không cap**.
- Contribution margin bằng **70% giá cước**.
- Budget mặc định là **$50.000**.
- Đây là synthetic assumptions để kiểm tra promotion burn, không phải chính sách GSM.
- Policy theo ngân sách dùng **greedy budget heuristic**, không phải exact knapsack optimization.

## Model hiện tại

Champion là **simplified R-Learner-style residual model**:

1. Model đầu học outcome nền `m(X)`.
2. Outcome và treatment được residualize.
3. Model thứ hai học tác động khác biệt `τ(X)`.

Hai model được train không đồng nghĩa với full Double Machine Learning. Implementation hiện chưa có cross-fitting, vì vậy dashboard và tài liệu không gọi model này là full DML.

Dashboard hiện đọc snapshot đã khóa `week5_r_learner_qini_0_188`: test set 4.000 khách hàng, Qini Coef `0,188`, Profit Targeting chọn 888 khách hàng. Qini, calibration và bảng policy đều phải được lấy từ cùng snapshot này.

## Tab 1: Bài toán kinh doanh

Tab này trả lời: **Phát voucher đại trà có tạo thêm lợi nhuận không?**

- KPI hiển thị tổng voucher burn, doanh thu tăng thêm, lợi nhuận ròng và ROI.
- Waterfall tách lợi nhuận gộp tăng thêm khỏi chi phí voucher.
- Phân rã promotion burn chỉ mang tính minh họa; không phải phép đo cannibalization production.

Kết luận cần trình bày: mass voucher có thể tạo thêm chuyến nhưng vẫn làm economics âm vì voucher được trả trên cả chuyến nền và chuyến tăng thêm.

## Tab 2: Bằng chứng nhân quả

Tab này kiểm tra thí nghiệm và ước lượng tác động trung bình.

- Experiment Health hiển thị số lần A/A Monte Carlo, FPR, SRM p-value và max |SMD|.
- `ATE thô` là chênh lệch trung bình giữa treatment và control.
- `ATE đã hiệu chỉnh` đến từ hồi quy `Y ~ Treatment + monthly_rides_history` với HC1.
- Bảng segment economics dùng synthetic potential outcomes `Y0/Y1` làm benchmark, không phải ROI production.

Trạng thái ĐẠT chỉ xuất hiện khi FPR, SRM và SMD cùng nằm trong ngưỡng đã định nghĩa.

## Tab 3: Ai nhạy với voucher?

Tab này chuyển từ average effect sang heterogeneous effect.

- Histogram CATE cho biết phân phối số chuyến dự kiến tăng thêm ở cấp khách hàng.
- Qini đánh giá khả năng đưa responsive users lên đầu danh sách tốt hơn random.
- Calibration so sánh CATE dự báo, uplift quan sát và synthetic ground truth theo decile.
- Scatter CATE và Expected Value cho thấy uplift cao chưa chắc tạo profit dương.

Công thức quyết định:

```text
EV_i = CATE_i × margin_per_ride_i
       - predicted_rides_treated_i × voucher_cost_per_ride_i
```

## Tab 4: Mô phỏng chính sách

Người dùng có thể thay đổi mức discount, margin và budget rồi so sánh:

- Không phát voucher.
- Phát voucher đại trà.
- Phát theo phân khúc ngoại thành.
- Phát cho 30% CATE cao nhất.
- Phát theo lợi nhuận kỳ vọng `EV > 0`.
- Phân bổ theo ngân sách bằng greedy heuristic.

Khi budget lớn hơn tổng burn của toàn bộ khách hàng EV dương, policy ngân sách sẽ giống Profit Targeting. Đây là hành vi đúng, không phải lỗi simulator.

## Tab 5: Kiểm tra độ vững

Tab cuối tóm tắt robustness trong các synthetic scenarios đã thử:

- Tăng kích thước mẫu.
- True effect bằng 0.
- Treatment/control mất cân bằng 90/10.
- Bổ sung outcome noise.

Các kết quả này kiểm tra measurement logic dưới DGP đã thiết kế. Chúng không chứng minh production robustness hay cho phép rollout tự động.

Roadmap được trình bày theo ba cấp:

```text
KHÁCH HÀNG NÀO
→ KHÁCH HÀNG NÀO + KHI NÀO
→ KHÁCH HÀNG NÀO + KHI NÀO + MỨC BAO NHIÊU
```

## Flow demo đề xuất

1. Tab 1: chứng minh mass voucher tạo burn.
2. Tab 2: xác nhận randomization và ATE.
3. Tab 3: giải thích CATE, Qini, Calibration và EV.
4. Tab 4: thay discount hoặc budget và quan sát policy table.
5. Tab 5: kết thúc bằng robustness limits và roadmap.

## Những điều không được kết luận

- Không gọi model hiện tại là full DML.
- Không gọi greedy budget heuristic là nghiệm tối ưu chính xác.
- Không diễn giải synthetic ROI là ROI có thể đạt được trên khách hàng GSM.
- Không coi stress tests hiện tại là bằng chứng production-ready.
- Mọi candidate policy phải được kiểm chứng bằng randomized pilot trên dữ liệu thật trước khi mở rộng.
