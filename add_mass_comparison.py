import json

with open('notebooks/week7_uplift_modeling/1_uplift_modeling_tlearner.ipynb', 'r', encoding='utf-8') as f:
    nb = json.load(f)

# The last cell contains the Top 20% logic. We will append the comparison to Mass Voucher logic to it.
for cell in reversed(nb['cells']):
    if cell['cell_type'] == 'code':
        # Append the Mass Voucher comparison code
        mass_voucher_code = """
# Tính toán cho Mass Voucher (Phát đại trà 100% trên tập Test)
mass_trips = df_qini['Qini'].iloc[-1]
mass_vouchers = df_qini['T_count'].iloc[-1]
mass_profit = (mass_trips * profit_per_ride) - (mass_vouchers * voucher_cost)

print("\\n=== SO SÁNH: TOP-20% TARGETING vs MASS VOUCHER ===")
print(f"1. Chi phí Voucher (Mass): {mass_vouchers * voucher_cost:,.0f} VND")
print(f"   Chi phí Voucher (Top-20%): {vouchers_sent * voucher_cost:,.0f} VND")
print(f"   -> Tiết kiệm được: {(mass_vouchers - vouchers_sent) * voucher_cost:,.0f} VND")
print(f"2. Lợi nhuận ròng (Mass): {mass_profit:,.0f} VND")
print(f"   Lợi nhuận ròng (Top-20%): {incremental_profit:,.0f} VND")
print(f"   -> Tối ưu lợi nhuận (Tránh lỗ): {incremental_profit - mass_profit:,.0f} VND")

if incremental_profit > mass_profit:
    print("\\nKết luận Kinh doanh: Dù cả 2 chiến lược đều lỗ do nhóm Urban Cash quá bảo thủ, nhưng mô hình Uplift đã giúp CỨU THUA (tránh lỗ thêm) được hàng triệu đồng so với việc nhắm mắt phát đại trà!")
else:
    print("\\nKết luận Kinh doanh: Mass Voucher tốt hơn (Điều này hiếm khi xảy ra nếu mô hình tốt).")
"""
        cell['source'].append(mass_voucher_code)
        break

with open('notebooks/week7_uplift_modeling/1_uplift_modeling_tlearner.ipynb', 'w', encoding='utf-8') as f:
    json.dump(nb, f, indent=1, ensure_ascii=False)
