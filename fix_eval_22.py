import json

with open('notebooks/week7_uplift_modeling/1_uplift_modeling_tlearner.ipynb', 'r', encoding='utf-8') as f:
    nb = json.load(f)

eval_cate_code = """
# Đánh giá ĐỘC LẬP nhóm CATE > 0.75 (Nhóm 22 người "Hòa vốn" / "Có Lãi" duy nhất)
cate_pred = model_1.predict(X_test) - model_0.predict(X_test)
profit_per_ride = 20000
voucher_cost = 15000
break_even_cate = voucher_cost / profit_per_ride # 0.75

positive_cate_mask = (cate_pred > break_even_cate)
num_targeted = positive_cate_mask.sum()

print(f"\\n=== ĐÁNH GIÁ THỰC TẾ NHÓM {num_targeted} NGƯỜI CÓ CATE > 0.75 (VƯỢT NGƯỠNG HÒA VỐN) ===")

if num_targeted > 0:
    t_target = T_test[positive_cate_mask]
    y_target = y_test[positive_cate_mask]
    
    n_treated = t_target.sum()
    n_control = len(t_target) - n_treated
    
    y_t_mean = y_target[t_target == 1].mean() if n_treated > 0 else 0
    y_c_mean = y_target[t_target == 0].mean() if n_control > 0 else 0
    local_ate = y_t_mean - y_c_mean
    
    incremental_trips = local_ate * num_targeted
    cost = n_treated * voucher_cost
    revenue = incremental_trips * profit_per_ride
    profit = revenue - cost
    
    print(f"1. Số voucher thực tế đã phát cho nhóm này (Nhóm T): {n_treated}")
    print(f"2. Uplift thực tế (Local ATE): {local_ate:.4f} chuyến/người")
    print(f"3. Số chuyến tăng thêm kỳ vọng: {incremental_trips:.2f} chuyến")
    print(f"4. Chi phí phát Voucher: {cost:,.0f} VND")
    print(f"5. Doanh thu gộp mang lại: {revenue:,.0f} VND")
    print(f"-> LỢI NHUẬN RÒNG: {profit:,.0f} VND")
    
    if profit > 0:
        print("✅ Thật bất ngờ! Thuật toán Machine Learning đã TÌM RA ĐÚNG nhóm sinh lời!")
    else:
        print("⚠️ Chứng minh bằng số liệu: Kể cả khi nhắm đúng 22 người vượt ngưỡng, do mẫu (sample size) quá nhỏ và nhiễu dữ liệu, chiến dịch vẫn chưa thể gánh được lỗ!")
"""

# Replace the last cell (which has the wrong evaluation block)
for cell in reversed(nb['cells']):
    if cell['cell_type'] == 'code':
        # Remove the previous evaluation block (anything after "# Đánh giá ĐỘC LẬP")
        source = cell['source']
        clean_source = []
        for line in source:
            if "# Đánh giá ĐỘC LẬP" in line:
                break
            clean_source.append(line)
        
        # Append the corrected block
        clean_source.extend([line + '\\n' for line in eval_cate_code.split('\\n')][:-1])
        cell['source'] = clean_source
        break

with open('notebooks/week7_uplift_modeling/1_uplift_modeling_tlearner.ipynb', 'w', encoding='utf-8') as f:
    json.dump(nb, f, indent=1, ensure_ascii=False)
