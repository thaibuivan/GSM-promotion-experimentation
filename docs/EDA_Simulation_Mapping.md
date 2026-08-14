# EDA → Simulation Mapping (Bản đồ Mô phỏng Dữ liệu)

Dưới đây là bảng ghi nhận cách chúng tôi chuyển các quan sát từ dữ liệu thực tế (EDA trên TLC NYC Taxi) thành các quyết định thiết lập trong hệ thống mô phỏng nhân quả (Causal Sandbox).

| EDA / External Observation | Simulation Decision (Quyết định Mô phỏng) | Source Type (Loại Nguồn) |
|---|---|---|
| Phân phối cước xe (Fare distribution) bị lệch phải | `fare_obs` sử dụng phân phối Log-Normal. | TLC empirical (Dữ liệu thật NYC TLC) |
| Nhu cầu gọi xe tăng mạnh vào giờ cao điểm | `preferred_hour` sử dụng xác suất theo trọng số thực tế. | TLC empirical |
| Các chuyến đi Sân bay (Airport) có mô hình kinh tế khác biệt | Thiết lập biến `airport indicator` + Hệ số nhân giá cước. | TLC-inspired (Lấy cảm hứng từ TLC) |
| Cước phí, quãng đường, thời gian có sự phụ thuộc lẫn nhau | Không sinh dữ liệu độc lập, sử dụng ma trận tương quan nội tại. | TLC empirical |
| Tần suất sử dụng dịch vụ của người dùng (User trip frequency) | Hiệu chỉnh tỷ lệ tập khách hàng thường xuyên (Heavy users). | External / Synthetic (Tham chiếu ngành) |
| Độ tuổi (Age) | Sử dụng phân phối tổng hợp ngẫu nhiên. | Assumption (Giả định hợp lý) |
| Thu nhập (Income) | Sử dụng phân phối Log-Normal chuẩn hóa. | Assumption / External source |
| Hiệu ứng can thiệp (Treatment effect) | Thiết lập phương trình Structural Causal Model (SCM). | Explicit causal assumption |
| Ảnh hưởng của thời tiết (Rain response) | Mô phỏng kịch bản nhiễu (Confounding scenario). | Assumption |
| Thiên kiến phân bổ Voucher (Assignment bias) | Cơ chế gán nhãn dựa trên đặc tính quan sát được. | Observational Assumption |

> **Ghi chú quan trọng:** Không phải mọi biến số ảo (synthetic variables) đều được sinh ra từ tập dữ liệu NYC TLC. Các đặc tính về người dùng (Demographics) và Hiệu ứng Nhân quả (Treatment Response) là những giả định có chủ đích (Assumptions) để xây dựng **Ground Truth**, nhằm mục tiêu kiểm chứng độ chính xác của các thuật toán A/B Testing và Uplift Modeling.
