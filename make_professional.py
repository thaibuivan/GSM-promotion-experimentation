import json
import os

replacements = {
    "✅ Nếu tất cả cột đều cao hơn đường đỏ -> Covariate Balance Đạt!": "Conclusion: All features are above the 0.05 threshold, indicating Covariate Balance is achieved.",
    "🚀 KẾT LUẬN: Tác động mang ý nghĩa thống kê (Statistically Significant)!": "Conclusion: The treatment effect is statistically significant (p < 0.05).",
    "⚠️ KẾT LUẬN: Tác động KHÔNG có ý nghĩa thống kê (Not Statistically Significant).": "Conclusion: The treatment effect is not statistically significant (p >= 0.05).",
    "✅ ĐẠT YÊU CẦU: Chiến dịch có LÃI. Nên tiến hành Roll-out toàn hệ thống!": "Evaluation: The campaign generated positive ROI. Recommended for scaling.",
    "❌ CẢNH BÁO: Chiến dịch bị LỖ. Cần giảm chi phí Voucher hoặc tối ưu lại Targeting.": "Evaluation: The campaign resulted in negative ROI. Adjust targeting or reduce voucher costs.",
    "✅ Không phát hiện SRM (Hệ thống chia ngẫu nhiên hoạt động tốt).": "Conclusion: No Sample Ratio Mismatch (SRM) detected.",
    "❌ LỖI SRM: Phân bổ mẫu có vấn đề!": "Conclusion: Sample Ratio Mismatch (SRM) detected.",
    "✅ Đã huấn luyện xong 2 mô hình XGBoost cho T-Learner.": "Training completed for Control and Treatment XGBoost models.",
    "Nhận xét: Có khách hàng CATE > 0 (Tăng chuyến), nhưng cũng có người CATE < 0 hoặc = 0 (Không đổi hoặc giảm).": "Observation: CATE distribution shows variance in treatment effects (positive, neutral, and negative).",
    "✅ Qini Coefficient > 0 chứng tỏ T-Learner ưu việt hơn hẳn so với việc phát Voucher ngẫu nhiên!": "Conclusion: Qini Coefficient > 0 indicates the T-Learner model outperforms random targeting.",
    "🚀 KẾT LUẬN: Chiến lược Top-20% Targeting tạo ra LỢI NHUẬN DƯƠNG. Khuyến nghị áp dụng thay cho Mass Voucher!": "Recommendation: Top-20% Targeting yields positive incremental profit. Preferred over Mass Voucher policy.",
    "⚠️ KẾT LUẬN: Lợi nhuận vẫn âm, cần điều chỉnh mức chiết khấu Voucher thấp hơn!": "Recommendation: Incremental profit remains negative. Further discount optimization required.",
    "✅ Nhận xét: Khi Sample Size tăng lên, Estimated ATE ngày càng bám sát True ATE và Khoảng tin cậy (CI) hẹp lại.": "Observation: Estimated ATE converges to True ATE and Confidence Interval narrows as Sample Size increases.",
    "❌ FAIL: Hệ thống kết luận sai là có tác dụng (Lỗi Type I - False Positive)!": "Result: False Positive detected (Type I Error).",
    "✅ PASS: Hệ thống kết luận chính xác là KHÔNG có tác dụng (P-value > 0.05). Pipeline cực kỳ an toàn!": "Result: True Negative confirmed. The pipeline correctly avoids False Positives under null effect.",
    "T-Learner Pipeline Hoàn Tất!": "T-Learner pipeline execution completed.",
    "=== BẢNG SO SÁNH CHIẾN LƯỢC KINH DOANH (POLICY COMPARISON) ===": "=== POLICY EVALUATION ===",
    "🚀 NHẬN XÉT:": "Observations:",
    "- Nếu phát đại trà (Mass Voucher), công ty mất trắng hàng chục ngàn USD vì bị nhóm Kháng Sale (Sân bay, Mưa) đốt tiền.": "- Mass Voucher policy incurs significant losses due to unpersuadable segments.",
    "- Nếu nhắm mục tiêu cơ bản (Segment Targeting) vào Suburban Occasionals, công ty bắt đầu CÓ LÃI.": "- Segment Targeting (e.g., Suburban Occasionals) yields positive profitability.",
    "❓ CÂU HỎI MỞ CHO TUẦN 7: Làm sao để biến nhóm 'Urban Credit Card' từ Lỗ thành Lãi? Đáp án: Uplift Modeling!": "Next Step: Apply Uplift Modeling to optimize targeting within loss-making segments.",
    "Hai 'bộ não'": "Hai mô hình",
    "bắt cả 2 'bộ não' cùng dự đoán": "sử dụng 2 mô hình để dự đoán",
    "Đỉnh cao của Business": "Business Evaluation",
    "bộ não": "mô hình",
    "nhanh như chớp": "efficiently",
    "kiểu gì cũng đi": "Sure Things",
    "Đào mỏ": "Lost Causes",
    "tàn nhẫn và chính xác": "rule-based",
    "T-Learner sử dụng 2 mô hình độc lập:\\n\",\n    \"- **Model 0 (Control Model):** Huấn luyện trên nhóm KHÔNG nhận Voucher ($T=0$).\\n\",\n    \"- **Model 1 (Treatment Model):** Huấn luyện trên nhóm CÓ nhận Voucher ($T=1$)." : "T-Learner utilizes two independent models:\\n\",\n    \"- **Model 0 (Control Model):** Trained on control group ($T=0$).\\n\",\n    \"- **Model 1 (Treatment Model):** Trained on treated group ($T=1$).",
    "> **⚠️ DISCLAIMER QUAN TRỌNG:**\\n\",\n    \"> Uplift Modeling trong file này được thực hiện trên **Synthetic user-level dataset (Dữ liệu giả lập)** được hiệu chỉnh từ phân phối của NYC TLC, phục vụ cho mục đích nghiên cứu và thí nghiệm.\\n\",\n    \"> **KHÔNG được trình bày hoặc hiểu lầm** đây là mô hình đã học từ dữ liệu khách hàng thực tế của Xanh SM.": "> **DISCLAIMER:**\\n\",\n    \"> This Uplift Model is trained on a **Synthetic user-level dataset** adjusted from NYC TLC distributions for experimental purposes.\\n\",\n    \"> It does not represent actual customer data or models from Xanh SM."
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
        
        for old_text, new_text in replacements.items():
            content = content.replace(old_text, new_text)
            
        with open(nb_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Updated {nb_path}")
