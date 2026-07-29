import json

with open('notebooks/week7_uplift_modeling/1_uplift_modeling_tlearner.ipynb', 'r', encoding='utf-8') as f:
    nb = json.load(f)

# The last cell contains the Top 20% logic. We will replace it with a loop that checks 10%, 20%, 30%...
new_business_cell = """# Tính toán Lợi nhuận tại nhiều ngưỡng khác nhau (Profit Curve)
print("=== TÌM KIẾM NGƯỠNG LỢI NHUẬN TỐI ƯU (PROFIT OPTIMIZATION) ===")

best_profit = -float('inf')
best_threshold = 0
best_savings = 0

mass_trips = df_qini['Qini'].iloc[-1]
mass_vouchers = df_qini['T_count'].iloc[-1]
mass_profit = (mass_trips * profit_per_ride) - (mass_vouchers * voucher_cost)

for threshold_pct in [10, 20, 30, 40, 50]:
    # Lấy Top K%
    threshold_idx = int(len(df_qini) * (threshold_pct / 100.0))
    if threshold_idx == 0: continue
    
    k_trips = df_qini['Qini'].iloc[threshold_idx]
    k_vouchers = df_qini['T_count'].iloc[threshold_idx]
    
    k_revenue = k_trips * profit_per_ride
    k_cost = k_vouchers * voucher_cost
    k_profit = k_revenue - k_cost
    savings = k_profit - mass_profit
    
    print(f"Top {threshold_pct}% -> Profit: {k_profit:,.0f} VND | Tránh lỗ so với Mass: {savings:,.0f} VND")
    
    if k_profit > best_profit:
        best_profit = k_profit
        best_threshold = threshold_pct
        best_savings = savings

print("\\n=== KẾT LUẬN CHIẾN LƯỢC ===")
if best_profit > 0:
    print(f"✅ Mức tối ưu là Top {best_threshold}%: Lợi nhuận ĐẠT MỨC DƯƠNG ({best_profit:,.0f} VND). Khuyến nghị triển khai ngay!")
else:
    print(f"⚠️ Ngay cả khi tối ưu nhất ở mức Top {best_threshold}%, chiến dịch vẫn Lỗ ({best_profit:,.0f} VND).")
    print("Nguyên nhân: Tập khách hàng Urban Cash quá bảo thủ. Chi phí Voucher (15k) đang cao hơn biên lợi nhuận kỳ vọng mà họ mang lại.")
    print(f"-> Quyết định: KHÔNG PHÁT VOUCHER cho nhóm này. Dừng chiến dịch để bảo toàn vốn.")
"""

for cell in reversed(nb['cells']):
    if cell['cell_type'] == 'code':
        # Replace the entire source of the last cell with this loop
        cell['source'] = [line + '\n' for line in new_business_cell.split('\n')][:-1]
        break

with open('notebooks/week7_uplift_modeling/1_uplift_modeling_tlearner.ipynb', 'w', encoding='utf-8') as f:
    json.dump(nb, f, indent=1, ensure_ascii=False)
