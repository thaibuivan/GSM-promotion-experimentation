# SCRIPT THUYẾT TRÌNH MENTOR - 10 PHÚT

Deck sử dụng: `docs/Mentor_Uplift_Presentation_15min.pptx`

Mục tiêu thời gian:

```text
Slide 1: 0:00 - 1:30
Slide 2: 1:30 - 2:45
Slide 3: 2:45 - 4:30
Slide 4: 4:30 - 6:15
Demo:    6:15 - 8:15
Slide 5: 8:15 - 9:30
Buffer:  9:30 - 10:00
```

Không cần đọc toàn bộ chữ trên slide. Mỗi slide chỉ cần nói rõ kết luận chính, bằng chứng hỗ trợ và câu chuyển sang bước tiếp theo.

## 0:00 - 1:30 | Slide 1 - Bài toán kinh doanh

> Em xin trình bày ngắn gọn project GSM Promotion Experimentation theo một câu hỏi xuyên suốt: voucher có làm tăng số chuyến hay không, nên phát cho ai, và việc phát đó có thực sự tạo thêm lợi nhuận hay không.
>
> Trước hết, em xin nói rõ toàn bộ kết quả hiện tại được xây dựng trên synthetic sandbox gồm 20.000 khách hàng trong cửa sổ mô phỏng 30 ngày. Đây chưa phải dữ liệu vận hành thực tế của GSM.
>
> Trong kịch bản phát voucher đại trà, voucher tạo thêm số chuyến và incremental revenue khoảng 561 nghìn đô. Tuy nhiên voucher burn lên tới khoảng 662 nghìn đô. Khi chỉ tính 70% contribution margin trên phần doanh thu tăng thêm, net profit còn âm khoảng 269 nghìn đô và ROI là âm 40,7%.
>
> Insight ở đây là tăng chuyến chưa đồng nghĩa với tăng lợi nhuận. Một phần voucher được trả cho những chuyến vốn vẫn có thể tự phát sinh dù khách hàng không nhận ưu đãi.
>
> Vì vậy project cần trả lời hai câu hỏi: voucher có tạo causal uplift thật không, và nếu có thì nên phát cho nhóm khách hàng nào để incremental margin đủ bù promotion burn?

**Câu chuyển:**

> Bước đầu tiên là tách tương quan thông thường khỏi tác động nhân quả của voucher.

## 1:30 - 2:45 | Slide 2 - ATE dương nhưng segment targeting vẫn chưa đủ

> Từ dữ liệu thí nghiệm ngẫu nhiên, Adjusted ATE vào khoảng 0,95 chuyến trên mỗi khách hàng trong 30 ngày. Khoảng tin cậy 95% là từ 0,76 đến 1,14. Như vậy voucher thực sự tạo mức tăng chuyến trung bình trong synthetic experiment hiện tại.
>
> Tuy nhiên khi phân tích theo persona, cả 5 segment đều có ATE dương nhưng ROI vẫn âm. Ví dụ Suburban Card có ROI âm 7,5%, Airport Business âm 63,2% và Urban Regulars âm 73,1%.
>
> Điều này cho thấy segment targeting vẫn quá thô. Hai khách hàng trong cùng một persona có thể có baseline rides, mức phản ứng và voucher burn rất khác nhau. Vì vậy chỉ chọn theo segment chưa giải quyết được cannibalization.
>
> Project cần đi xuống cấp user, ước lượng CATE và kết hợp với EV để tìm những khách hàng tạo đủ incremental value.

**Câu chuyển:**

> Vì vậy bước tiếp theo là chuyển từ ATE sang CATE và so sánh các uplift models để xếp hạng khách hàng.

## 2:45 - 4:30 | Slide 3 - Lựa chọn model

> Em đã thử các hướng S-Learner, T-Learner, X-Learner, simplified R-Learner-style và DR-Learner trên cùng held-out test set gồm 4.000 khách hàng.
>
> Metric chính để so sánh ranking là Qini. R-Learner-style đạt Qini 0,188, cao nhất trong các model đã thử. S-Learner đạt 0,153, DR-Learner 0,138, X-Learner 0,038 và T-Learner âm 0,320.
>
> Ý tưởng của R-Learner-style là trước hết học baseline behavior từ các features, sau đó residualize outcome và treatment để model cuối tập trung hơn vào phần biến động gắn với voucher. Implementation hiện có hai tầng model nhưng chưa cross-fitting, nên em gọi chính xác là simplified R-Learner-style chứ không gọi là full Double Machine Learning.
>
> Trên biểu đồ, đường Qini của model nhìn chung nằm trên random baseline. Điều này cho thấy model có tín hiệu ranking hữu ích. Tuy nhiên calibration vẫn chưa hoàn hảo, nghĩa là thứ tự khách hàng tương đối tốt nhưng độ lớn CATE dự báo chưa phải lúc nào cũng khớp uplift quan sát.

**Câu chuyển:**

> Ranking tốt vẫn chưa đủ để ra quyết định kinh doanh, vì CATE cao chưa chắc tạo lợi nhuận nếu chi phí voucher quá lớn.

## 4:30 - 6:15 | Slide 4 - Từ CATE sang Expected Value

> Để chuyển model signal thành decision rule, project sử dụng Expected Value. Công thức rút gọn là incremental margin trừ expected voucher burn.
>
> Synthetic assumptions hiện tại là voucher bằng 15%, không áp dụng cap, và contribution margin bằng 70%. Em nhấn mạnh đây là assumptions của sandbox, không phải chính sách chính thức của GSM.
>
> Policy chỉ phát voucher nếu EV lớn hơn 0. Trên held-out test set, rule này chọn 888 trên 4.000 khách hàng, tương đương 22,2%.
>
> Predicted profit là khoảng 7.939 đô, trong khi synthetic causal benchmark là khoảng 7.060 đô. Hai con số này đều là kết quả mô phỏng. Predicted profit đến từ model estimate, còn benchmark sử dụng potential outcomes đã biết trong synthetic data để kiểm tra policy.
>
> Tỷ lệ 22,2% không phải quota cố định. Nó là kết quả của điều kiện EV lớn hơn 0 dưới assumptions hiện tại. Khi voucher rate, contribution margin hoặc budget thay đổi, tập khách hàng được chọn cũng phải thay đổi.

**Câu chuyển sang demo:**

> Em xin demo nhanh hai phần: model xếp hạng như thế nào và business policy thay đổi ra sao khi đưa economics vào quyết định.

## 6:15 - 8:15 | Demo dashboard

### Màn hình 1 - Qini và Calibration, khoảng 60 giây

> Ở đây, Qini trả lời câu hỏi model có đưa những khách hàng phản ứng tốt lên đầu danh sách hay không. Đường model nằm trên random ở phần lớn population nên ranking có giá trị.
>
> Biểu đồ calibration trả lời một câu hỏi khác: độ lớn CATE dự báo có gần uplift quan sát theo từng decile hay không. Kết quả cho thấy xu hướng ranking tồn tại nhưng magnitude chưa được hiệu chỉnh hoàn hảo. Vì vậy em không dùng riêng predicted CATE để quyết định phát voucher.

### Màn hình 2 - Policy Simulator, khoảng 60 giây

> Tại Policy Simulator, Mass Voucher cho thấy việc phát rộng có thể làm tăng demand nhưng vẫn âm profit. Profit Targeting sử dụng EV lớn hơn 0 để giữ lại nhóm có incremental margin đủ bù chi phí.
>
> Khi thay đổi một tham số, ví dụ voucher rate hoặc budget, số khách hàng được chọn và expected profit thay đổi theo. Đây là lý do policy phải kết hợp causal effect với economics thay vì chọn cố định top 20% hoặc top 30% theo CATE.

Không thay quá một slider. Sau khi nói xong, quay lại slide 5 ngay.

## 8:15 - 9:30 | Slide 5 - Kết luận và xin feedback

> Về robustness, A/A test Week 6 cho False Positive Rate 5,04%, gần mức alpha 5%. Thiết kế treatment 10/90 không tạo directional bias đáng kể trong simulation nhưng làm uncertainty tăng rõ. Mean-zero noise với SD bằng 1 chỉ làm uncertainty tăng nhẹ trong setting đã thử.
>
> Kết luận của em không phải model đã sẵn sàng rollout. Kết luận đúng phạm vi là project đã có synthetic evidence đủ để đề xuất một randomized pilot có guardrails, nhưng chưa có production evidence.
>
> Em muốn xin mentor phản biện ba điểm. Thứ nhất, logic chọn simplified R-Learner-style đã đủ defend chưa. Thứ hai, assumptions economics và cách chuyển CATE sang EV còn thiếu thành phần nào. Thứ ba, nếu chuyển sang randomized pilot thì cần bổ sung guardrails hoặc experiment checks nào.

**Câu kết:**

> Trên đây là phần trình bày ngắn của em. Em xin dừng tại đây và mong mentor tập trung hỏi vặn vào ba điểm vừa nêu.

## 9:30 - 10:00 | Buffer

Nếu còn thời gian, không bổ sung thêm nội dung mới. Dùng khoảng 30 giây để nhắc lại:

> Voucher tạo uplift trung bình, nhưng profit chỉ xuất hiện khi chọn đúng khách hàng và tính đầy đủ promotion burn. Model hiện cho tín hiệu ranking hữu ích, còn quyết định production vẫn cần randomized validation.

## Phương án nếu demo gặp lỗi

Không cố sửa dashboard trong lúc trình bày. Nói:

> Dashboard là lớp triển khai trực quan của cùng pipeline. Kết quả chính đã được cố định trên slide: Qini 0,188 cho ranking và policy EV lớn hơn 0 chọn 888 trên 4.000 khách hàng. Em xin tiếp tục với kết luận và có thể mở lại demo sau phần hỏi đáp.

Sau đó chuyển thẳng sang slide 5.

## Câu trả lời ngắn cho các câu hỏi dễ gặp

**Đây có phải dữ liệu GSM thật không?**

> Chưa. Đây là synthetic sandbox để kiểm chứng methodology và decision logic trước khi xin pilot trên dữ liệu thật.

**Tại sao chọn R-Learner-style?**

> Vì model có Qini cao nhất trên cùng held-out test set, đồng thời residualization phù hợp với mục tiêu tách baseline behavior khỏi treatment signal.

**Qini 0,188 có đủ tốt để deploy không?**

> Không thể kết luận deploy chỉ từ Qini. Nó chứng minh ranking tốt hơn random trong test hiện tại; vẫn cần calibration, policy value và randomized pilot.

**Tại sao không chọn DR-Learner?**

> DR-Learner hấp dẫn về lý thuyết nhưng trong snapshot hiện tại Qini thấp hơn và business value bị overestimate mạnh hơn R-Learner-style.

**Tại sao net profit không bằng revenue trừ voucher burn?**

> Vì chỉ contribution margin 70% của incremental revenue được tính là phần đóng góp để bù voucher burn.

**888 khách hàng có phải tỷ lệ rollout cố định không?**

> Không. Đây là số khách hàng có EV lớn hơn 0 trong test set và assumptions hiện tại; tỷ lệ sẽ thay đổi khi economics thay đổi.
