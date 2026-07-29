import json

with open('notebooks/week7_uplift_modeling/1_uplift_modeling_tlearner.ipynb', 'r', encoding='utf-8') as f:
    nb = json.load(f)

# Find the last cell and append the CATE > 0 evaluation
eval_cate_code = """
# Đánh giá ĐỘC LẬP nhóm CATE > 0 (Nhóm 22 người "khả quan" nhất)
cate_pred = model_1.predict(X_test) - model_0.predict(X_test)
positive_cate_mask = (cate_pred > 0)
num_targeted = positive_cate_mask.sum()

print(f"\\n=== ĐÁNH GIÁ THỰC TẾ NHÓM {num_targeted} NGƯỜI CÓ CATE > 0 ===")

if num_targeted > 0:
    # Lấy ra những người có CATE > 0
    t_target = T_test[positive_cate_mask]
    y_target = y_test[positive_cate_mask]
    
    # Tính số lượng thực tế trong nhóm này
    n_treated = t_target.sum()
    n_control = len(t_target) - n_treated
    
    # Tính ATE cục bộ cho nhóm 22 người này
    y_t_mean = y_target[t_target == 1].mean() if n_treated > 0 else 0
    y_c_mean = y_target[t_target == 0].mean() if n_control > 0 else 0
    local_ate = y_t_mean - y_c_mean
    
    # Quy ra lợi nhuận
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
        print("✅ Thật bất ngờ! Bạn đã đúng. Nhóm này MANG LẠI LỢI NHUẬN DƯƠNG!")
    else:
        print("⚠️ Chứng minh bằng số liệu: Ngay cả 22 người TỐT NHẤT này vẫn GÂY LỖ nặng!")
"""

for cell in reversed(nb['cells']):
    if cell['cell_type'] == 'code':
        cell['source'].append(eval_cate_code)
        break

with open('notebooks/week7_uplift_modeling/1_uplift_modeling_tlearner.ipynb', 'w', encoding='utf-8') as f:
    json.dump(nb, f, indent=1, ensure_ascii=False)
