# SCRIPT THUYẾT TRÌNH MENTOR - 10 PHÚT

Deck sử dụng: `docs/Mentor_Uplift_Presentation_15min.pptx`

## Phân bổ thời gian

```text
Slide 1: 0:00 - 0:50   Hành trình 6 tuần
Slide 2: 0:50 - 2:10   EDA, synthetic data, segmentation
Slide 3: 2:10 - 3:20   ATE dương nhưng ROI âm
Slide 4: 3:20 - 4:30   So sánh uplift models
Slide 5: 4:30 - 5:30   CATE sang Expected Value
Slide 6: 5:30 - 6:25   Stress test Week 6
Demo:    6:25 - 8:30   Chỉ Policy Simulator
Slide 7: 8:30 - 9:30   Kết luận và xin phản biện
Buffer:  9:30 - 10:00
```

Không đọc toàn bộ chữ trên slide. Mỗi slide chỉ nói một kết luận, bằng chứng chính và lý do chuyển sang bước tiếp theo.

## 0:00 - 0:50 | Slide 1 - Hành trình 6 tuần

> Em xin trình bày project theo hành trình 6 tuần, thay vì chỉ bắt đầu từ uplift model. Câu hỏi xuyên suốt là: voucher tạo thêm chuyến cho ai và phần tăng thêm đó có thật sự sinh lời không?
>
> Em bắt đầu từ data quality và EDA, sau đó xây synthetic causal data có potential outcomes, tạo segmentation để diễn giải business, kiểm tra A/A và A/B, so sánh uplift models, rồi stress test toàn bộ measurement framework.
>
> Vì vậy đầu ra của project không chỉ là một model, mà là chuỗi reasoning từ dữ liệu đến quyết định policy.

**Câu chuyển:**

> Trước hết, em xin giải thích dữ liệu đầu vào và vì sao cần một synthetic sandbox.

## 0:50 - 2:10 | Slide 2 - EDA, synthetic data và segmentation

> Nguồn public mobility data có khoảng 3,72 triệu chuyến và 20 biến. EDA phát hiện structural missing khoảng 29,2%, cùng các vấn đề như negative fares, zero distance và outliers. Những kiểm tra này giúp em hiểu phân phối thực tế và xác định các ràng buộc hợp lý.
>
> Tuy nhiên trip-level observational data không cho biết đồng thời một khách hàng sẽ đi bao nhiêu chuyến khi có và khi không có voucher. Vì vậy em xây synthetic causal data ở cấp 20.000 khách hàng, trong cửa sổ 30 ngày: từ đặc trưng X tạo baseline Y0, treatment effect ITE, rồi Y1 bằng Y0 cộng ITE.
>
> Em tiếp tục chia thành 5 behavioral personas để có lớp diễn giải cho business. Điểm quan trọng là persona không tạo ra treatment effect; effect đã được sinh trước, còn segmentation dùng để mô tả và vận hành theo nhóm.

**Câu chuyển:**

> Từ dữ liệu này, em kiểm tra trước tác động trung bình và economics ở cấp segment.

## 2:10 - 3:20 | Slide 3 - ATE dương nhưng ROI âm

> A/B randomized cho Adjusted ATE khoảng 0,95 chuyến trên mỗi khách hàng trong 30 ngày, với khoảng tin cậy 95% từ 0,76 đến 1,14. Như vậy voucher có tạo causal uplift trung bình trong sandbox.
>
> Nhưng cả 5 persona đều có ATE dương trong khi ROI đều âm. Nhóm tốt nhất là Suburban Card vẫn âm 7,5%; Urban Regulars âm 73,1%.
>
> Đây là insight làm thay đổi hướng project: response không đồng nghĩa với profit. Segment targeting vẫn quá thô vì hai user trong cùng persona có thể có baseline rides, mức phản ứng và voucher burn khác nhau. Do đó em cần CATE ở cấp user.

**Câu chuyển:**

> Em so sánh nhiều uplift learners trên cùng một test set để chọn model xếp hạng user.

## 3:20 - 4:30 | Slide 4 - Lựa chọn model

> Em thử S-Learner, T-Learner, X-Learner, simplified R-Learner-style và DR-Learner trên cùng held-out test set 4.000 khách hàng.
>
> Metric chính là Qini Coefficient vì mục tiêu ở đây là ranking uplift. R-Learner-style đạt 0,188, cao nhất; S-Learner đạt 0,153; DR-Learner 0,138; X-Learner 0,038 và T-Learner âm 0,320.
>
> R-Learner-style được chọn vì ranking tốt nhất trong các model đã thử. Model học baseline m(X), residualize outcome và treatment, sau đó học tau(X). Implementation hiện chưa cross-fitting nên em không gọi đây là full DML.
>
> Qini 0,188 chứng minh ranking tốt hơn random trong test hiện tại, không tự động chứng minh model sẵn sàng production.

**Câu chuyển:**

> Ranking CATE vẫn chưa phải quyết định cuối, vì user phản ứng mạnh vẫn có thể gây lỗ.

## 4:30 - 5:30 | Slide 5 - Từ CATE sang Expected Value

> Em chuyển CATE thành Expected Value bằng cách lấy incremental margin trừ expected voucher burn. Synthetic assumptions hiện tại là contribution margin 70% và voucher 15% không cap. Đây là assumptions của sandbox, không phải chính sách chính thức của GSM.
>
> Điểm thường bị bỏ sót là chi phí voucher được trả trên toàn bộ số chuyến dự kiến khi có treatment, không chỉ phần chuyến tăng thêm. Vì vậy baseline cao có thể làm burn lớn dù CATE dương.
>
> Policy chỉ phát khi EV lớn hơn 0. Tỷ lệ được chọn không phải quota top 20% hay 30% cố định; nó thay đổi theo economics và budget.

**Câu chuyển:**

> Trước khi dùng policy này, em kiểm tra measurement framework dưới các tình huống bất lợi.

## 5:30 - 6:25 | Slide 6 - Stress test Week 6

> A/A test 5.000 lần cho False Positive Rate 5,04%, gần alpha 5%, nên pipeline không thường xuyên tạo kết luận dương giả dưới null synthetic.
>
> Khi treatment/control lệch thành 10/90, độ lệch trung bình vẫn nhỏ nhưng standard deviation tăng từ 0,093 lên 0,157, tức uncertainty tăng khoảng 69%. Khi thêm Gaussian noise SD bằng 1, uncertainty chỉ tăng nhẹ trong setting đã thử.
>
> Kết luận đúng phạm vi là framework robust trong các synthetic scenarios đã kiểm tra, chưa phải production validation.

**Câu chuyển sang demo:**

> Các slide đã trình bày bằng chứng về dữ liệu, ATE, model và stress test. Em chỉ demo phần những con số đó được chuyển thành policy như thế nào.

## 6:25 - 8:30 | Demo - Chỉ Policy Simulator

> Ở Policy Simulator, em so sánh phát đại trà với rule EV lớn hơn 0 và policy có giới hạn budget. Mass Voucher có thể tăng demand nhưng vẫn âm profit vì promotion burn rơi cả vào các chuyến nền.
>
> Profit Targeting giữ lại user có incremental margin dự kiến đủ bù voucher burn. Em thay đúng một tham số, ví dụ voucher rate hoặc budget, để cho thấy số user được chọn và expected profit thay đổi theo economics.
>
> Đây là lý do em không khóa một tỷ lệ target cố định. Model cung cấp signal, còn policy kết hợp signal đó với chi phí và ràng buộc kinh doanh.

Không mở lại ATE, Qini hoặc calibration trong demo vì các nội dung đó đã có trên slide. Không thay quá một slider.

## 8:30 - 9:30 | Slide 7 - Kết luận và xin mentor phản biện

> Project đã chứng minh được một end-to-end causal sandbox: có data checks, synthetic ground truth, randomized measurement, model comparison, profit-aware policy và stress tests. R-Learner-style hiện là champion với Qini 0,188.
>
> Project chưa chứng minh profit trên dữ liệu GSM thật, độ đúng của economics assumptions hay stability dưới production drift. Vì vậy đề xuất phù hợp là randomized pilot quy mô nhỏ, có budget cap, stop-loss, SRM, balance checks và guardrails.
>
> Em muốn xin mentor phản biện ba điểm: logic chọn model đã đủ defend chưa; economics assumptions còn thiếu gì; và pilot cần thêm guardrail nào trước khi trình bày với PM.

**Câu kết:**

> Em xin dừng phần trình bày tại đây và mong mentor hỏi sâu vào ba điểm vừa nêu.

## 9:30 - 10:00 | Buffer

Nếu còn thời gian, chỉ nhắc lại một câu:

> Voucher tạo uplift trung bình, nhưng lợi nhuận chỉ xuất hiện khi chọn đúng user và tính đầy đủ promotion burn; bước tiếp theo phải là randomized validation, chưa phải rollout.

## Nếu demo gặp lỗi

Không sửa dashboard trong lúc trình bày. Nói:

> Dashboard là lớp trực quan của cùng pipeline. Logic quyết định đã có trên slide: CATE tạo signal, Expected Value đưa economics vào policy, và chỉ target khi EV dương. Em xin tiếp tục với kết luận và có thể mở lại demo sau phần hỏi đáp.

Sau đó chuyển thẳng sang slide 7.

## Câu trả lời ngắn cho câu hỏi dễ gặp

**Đây có phải dữ liệu GSM thật không?**

> Chưa. Đây là synthetic sandbox để kiểm chứng methodology và decision logic trước khi xin pilot trên dữ liệu thật.

**Tại sao cần synthetic data?**

> Vì dữ liệu quan sát chỉ cho thấy một outcome của mỗi user. Synthetic data cho em biết Y0, Y1 và CATE ground truth để kiểm tra estimator và policy trước khi có randomized production data.

**Persona có tạo ra CATE không?**

> Không. Treatment effect được sinh trước segmentation. Persona là lớp mô tả để giải thích và vận hành business.

**Tại sao chọn R-Learner-style?**

> Vì Qini cao nhất trên cùng held-out test set, đồng thời residualization giúp model tập trung vào treatment signal sau khi loại phần baseline có thể dự báo từ X.

**Qini 0,188 có đủ để deploy không?**

> Không. Nó chỉ cho thấy ranking tốt hơn random trong test hiện tại. Deploy còn cần calibration, policy value và randomized pilot trên dữ liệu thật.

**Tại sao không chọn DR-Learner?**

> DR-Learner hấp dẫn về lý thuyết nhưng trong snapshot hiện tại Qini thấp hơn và business value bị overestimate mạnh hơn R-Learner-style.

**Tại sao không chọn top 30% CATE?**

> Vì CATE chỉ đo phản ứng. Rule EV còn xét margin, baseline rides, voucher burn và budget nên sát quyết định kinh doanh hơn một quota cố định.
