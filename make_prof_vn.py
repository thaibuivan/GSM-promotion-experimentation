import json
import os

replacements_to_vn = {
    "Conclusion: All features are above the 0.05 threshold, indicating Covariate Balance is achieved.": "Kết luận: Tất cả các thuộc tính đều vượt ngưỡng 0.05, đạt yêu cầu cân bằng Covariate Balance.",
    "Conclusion: The treatment effect is statistically significant (p < 0.05).": "Kết luận: Tác động mang ý nghĩa thống kê (p < 0.05).",
    "Conclusion: The treatment effect is not statistically significant (p >= 0.05).": "Kết luận: Tác động không mang ý nghĩa thống kê (p >= 0.05).",
    "Evaluation: The campaign generated positive ROI. Recommended for scaling.": "Đánh giá: Chiến dịch mang lại ROI dương. Khuyến nghị mở rộng triển khai.",
    "Evaluation: The campaign resulted in negative ROI. Adjust targeting or reduce voucher costs.": "Đánh giá: Chiến dịch mang lại ROI âm. Cần điều chỉnh đối tượng mục tiêu hoặc giảm chi phí chiết khấu.",
    "Conclusion: No Sample Ratio Mismatch (SRM) detected.": "Kết luận: Không phát hiện lỗi phân bổ mẫu (Sample Ratio Mismatch - SRM).",
    "Conclusion: Sample Ratio Mismatch (SRM) detected.": "Kết luận: Phát hiện lỗi phân bổ mẫu (Sample Ratio Mismatch - SRM).",
    "Training completed for Control and Treatment XGBoost models.": "Hoàn tất quá trình huấn luyện mô hình XGBoost cho nhóm Control và Treatment.",
    "Observation: CATE distribution shows variance in treatment effects (positive, neutral, and negative).": "Nhận xét: Phân phối CATE cho thấy sự đa dạng trong tác động của can thiệp (tích cực, trung tính, và tiêu cực).",
    "Conclusion: Qini Coefficient > 0 indicates the T-Learner model outperforms random targeting.": "Kết luận: Hệ số Qini > 0 chứng minh mô hình T-Learner hiệu quả hơn so với chiến lược phân bổ ngẫu nhiên.",
    "Recommendation: Top-20% Targeting yields positive incremental profit. Preferred over Mass Voucher policy.": "Khuyến nghị: Chiến lược nhắm mục tiêu Top-20% mang lại lợi nhuận ròng dương, tối ưu hơn chiến lược phát Voucher đại trà.",
    "Recommendation: Incremental profit remains negative. Further discount optimization required.": "Khuyến nghị: Lợi nhuận ròng vẫn ở mức âm. Cần tối ưu thêm tỷ lệ chiết khấu.",
    "Observation: Estimated ATE converges to True ATE and Confidence Interval narrows as Sample Size increases.": "Nhận xét: Khi kích thước mẫu tăng, Estimated ATE hội tụ dần về True ATE và Khoảng tin cậy thu hẹp.",
    "Result: False Positive detected (Type I Error).": "Kết quả: Phát hiện lỗi Loại I (False Positive).",
    "Result: True Negative confirmed. The pipeline correctly avoids False Positives under null effect.": "Kết quả: Xác nhận True Negative. Pipeline tránh được lỗi False Positive khi True Effect = 0.",
    "T-Learner pipeline execution completed.": "Hoàn tất thực thi Pipeline T-Learner.",
    "=== POLICY EVALUATION ===": "=== ĐÁNH GIÁ CHIẾN LƯỢC KINH DOANH ===",
    "Observations:": "Nhận xét:",
    "- Mass Voucher policy incurs significant losses due to unpersuadable segments.": "- Chiến lược phát đại trà (Mass Voucher) gây lỗ do chi phí phát sinh từ các phân khúc không phản ứng với khuyến mãi.",
    "- Segment Targeting (e.g., Suburban Occasionals) yields positive profitability.": "- Chiến lược nhắm mục tiêu cơ bản (VD: Suburban Occasionals) bước đầu mang lại biên lợi nhuận dương.",
    "Next Step: Apply Uplift Modeling to optimize targeting within loss-making segments.": "Định hướng: Áp dụng Uplift Modeling để tối ưu hóa việc phân bổ ngân sách trong các phân khúc đang gây lỗ.",
    "> **DISCLAIMER:**\\n\",\n    \"> This Uplift Model is trained on a **Synthetic user-level dataset** adjusted from NYC TLC distributions for experimental purposes.\\n\",\n    \"> It does not represent actual customer data or models from Xanh SM.": "> **LƯU Ý:**\\n\",\n    \"> Mô hình Uplift này được huấn luyện trên **Dữ liệu giả lập (Synthetic dataset)** dựa trên phân phối của NYC TLC, phục vụ cho mục đích nghiên cứu.\\n\",\n    \"> Các số liệu và mô hình trong đây không đại diện cho dữ liệu khách hàng thực tế của hệ thống."
}

notebooks = [
    'notebooks/week4_ab_testing/1_ab_test_analysis.ipynb',
    'notebooks/week7_uplift_modeling/1_uplift_modeling_tlearner.ipynb',
    'notebooks/week8_stress_test/1_stress_test.ipynb'
]

for nb_path in notebooks:
    if os.path.exists(nb_path):
        with open(nb_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        for old_text, new_text in replacements_to_vn.items():
            content = content.replace(old_text, new_text)
            
        with open(nb_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Updated {nb_path} to Formal Vietnamese")
