# BÁO CÁO KỸ THUẬT: STRESS TEST & CHAMPION-CHALLENGER (TUẦN 6)

## 1. Mục tiêu và phạm vi

Stress Test kiểm tra khung đo lường A/B Testing có phản ứng phù hợp với lý thuyết trong các synthetic scenarios đã thiết kế hay không. Phần này kiểm tra **measurement framework**, không huấn luyện lại uplift model Tuần 5 và không chứng minh production robustness.

Nguồn số liệu chính thức là:

```text
notebooks/week6_stress_test/1_stress_test.ipynb
data/processed/week6_stress_test_metrics.json
```

Mỗi scenario đều lấy mẫu từ synthetic population hiện tại, gán treatment mới, dựng lại outcome quan sát từ `Y0/Y1`, rồi ước lượng:

```text
Y ~ Treatment + monthly_rides_history
```

Standard error dùng HC1. Việc dùng cùng estimator giúp khác biệt giữa các kết quả đến từ stress scenario thay vì do thay đổi phương pháp tính.

## 2. Hai mốc ATE trong synthetic data

Dataset có hai khái niệm cần phân biệt:

```text
DGP expected ATE = mean(cate_true) = 0,8000 chuyến
Finite-population potential-outcome ATE = mean(Y1 - Y0) = 0,9310 chuyến
```

Stress test so estimator với mốc `mean(Y1 - Y0)` vì đây là potential-outcome benchmark của chính dataset 20.000 khách hàng đã sinh. Các mức sample size lớn hơn 20.000 được tạo bằng bootstrap resampling; chúng không đại diện cho khách hàng GSM thật.

## 3. Kết quả các kịch bản

### 3.1 Tăng kích thước mẫu

Thiết lập:

- Sample size: 1.000, 5.000, 10.000, 20.000, 50.000 và 100.000.
- 100 lần lặp tại mỗi sample size.
- Treatment/control 50/50.
- Các mức trên 20.000 dùng bootstrap resampling từ synthetic population.

Kết quả tiêu biểu:

| Sample size | Mean Adjusted ATE | Estimator SD | Mean HC1 SE | Coverage 95% |
|---:|---:|---:|---:|---:|
| 1.000 | 0,952 | 0,421 | 0,425 | 98% |
| 10.000 | 0,939 | 0,131 | 0,135 | 99% |
| 20.000 | 0,923 | 0,087 | 0,095 | 100% |
| 100.000 | 0,935 | 0,044 | 0,043 | 99% |

Estimator vẫn centered quanh finite-population benchmark và độ phân tán giảm khi sample size tăng. Coverage cao hơn 95% trong các lần chạy hiện tại cho thấy HC1 hơi bảo thủ trong setting này; không nên diễn giải là coverage luôn hoàn hảo.

### 3.2 A/A Test với True Effect bằng 0

Thiết lập:

- 5.000 lần mô phỏng độc lập.
- 2.000 quan sát mỗi lần.
- Treatment/control 50/50.
- Cả hai nhóm dùng outcome `Y0`, nên true effect bằng 0.

Kết quả:

```text
False Positive Rate = 5,04%
95% binomial interval = [4,45%, 5,68%]
Mean estimated ATE under null = -0,0013 chuyến
```

FPR nằm gần alpha 5% như kỳ vọng. Đây là kết quả riêng của notebook Tuần 6; dashboard Experiment Health vẫn hiển thị artifact A/A Tuần 4 với FPR 5,08%.

### 3.3 Treatment/control mất cân bằng 10/90

Thiết lập:

- 300 lần lặp cho mỗi thiết kế.
- 20.000 quan sát mỗi lần.
- So sánh treatment/control 50/50 với 10/90.
- Treatment được gán lại trước khi outcome được dựng từ `Y0/Y1`.

| Thiết kế | Mean Adjusted ATE | Bias | Estimator SD | Mean HC1 SE | Coverage 95% |
|---|---:|---:|---:|---:|---:|
| 50/50 | 0,935 | -0,0004 | 0,093 | 0,095 | 98,3% |
| 10/90 | 0,940 | 0,0053 | 0,157 | 0,162 | 97,0% |

Thiết kế 10/90 không tạo directional bias đáng kể trong synthetic randomized setting, nhưng estimator SD tăng khoảng 69% và mean HC1 SE tăng khoảng 70%. Rủi ro chính là uncertainty lớn hơn và statistical power thấp hơn.

### 3.4 Mean-zero Gaussian noise

Thiết lập:

- 300 lần lặp.
- 20.000 quan sát mỗi lần.
- Treatment/control 50/50.
- So sánh outcome gốc với outcome được cộng `N(0, 1)` trên cùng sample và treatment assignment.

| Scenario | Mean Adjusted ATE | Bias | Estimator SD | Mean HC1 SE |
|---|---:|---:|---:|---:|
| Không thêm noise | 0,929 | -0,0028 | 0,091 | 0,095 |
| Gaussian noise SD=1 | 0,929 | -0,0024 | 0,092 | 0,096 |

Mean-zero noise không tạo directional bias trong setting đã thử. Với `SD=1`, uncertainty chỉ tăng nhẹ vì outcome gốc đã có phương sai tương đối lớn. Kết quả này không đại diện cho systematic shocks, interference hoặc distribution shift.

## 4. Kiến trúc Champion-Challenger cho pilot tương lai

Để kiểm chứng liệu AI Profit Targeting có vượt phương pháp rule-based hay không, dự án phác thảo A/B/C test:

- **Group A - Holdout (10%):** Không nhận voucher, dùng làm control.
- **Group B - Champion (45%):** Segment Targeting dựa trên persona.
- **Group C - Challenger (45%):** Profit Targeting bằng simplified R-Learner-style residual model, chỉ phát khi `EV > 0`.

Chỉ cân nhắc tăng traffic cho Group C nếu incremental profit cao hơn Group B với ý nghĩa thống kê và các guardrail không xấu đi. Thiết kế này là experiment proposal, chưa phải rollout plan đã được phê duyệt.

## 5. Kết luận đúng phạm vi

Trong các synthetic scenarios đã chạy:

1. Adjusted ATE bám finite-population benchmark khi sample size tăng.
2. A/A FPR nằm gần alpha 5%.
3. Tỷ lệ 10/90 làm tăng variance và standard error nhưng không tạo bias có hệ thống.
4. Mean-zero noise SD=1 làm uncertainty tăng nhẹ mà không tạo directional bias.

Các test chưa bao phủ logging/exposure failure, non-compliance, interference, spillover, seasonality hay production distribution shift. Bước tiếp theo vẫn là experiment contract và randomized pilot trên dữ liệu GSM thật trước mọi quyết định mở rộng.
