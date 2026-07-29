import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats

# Cài đặt giao diện
plt.style.use('ggplot')
sns.set_palette("Set2")

# Tải dữ liệu
df = pd.read_csv('../../data/processed/segmented_simulation_data.csv')

# Lọc nhóm mục tiêu
target_persona = 'Urban Credit Card'  # Chọn nhóm mục tiêu có ATE dương (dùng thẻ tín dụng)
df_target = df[df['persona'] == target_persona].copy()

print(f"Tổng số khách hàng trong nhóm {target_persona}: {len(df_target)}")
print(f"Nhóm Control: {len(df_target[df_target['treatment_rand'] == 0])} người")
print(f"Nhóm Treatment: {len(df_target[df_target['treatment_rand'] == 1])} người")

def check_balance(df, feature):
    control = df[df['treatment_rand'] == 0][feature]
    treatment = df[df['treatment_rand'] == 1][feature]
    
    t_stat, p_val = stats.ttest_ind(control, treatment, equal_var=False)
    
    print(f"--- Kiểm tra cân bằng biến: {feature} ---")
    print(f"Control Mean: {control.mean():.2f}")
    print(f"Treatment Mean: {treatment.mean():.2f}")
    print(f"P-value: {p_val:.4f} -> {'CÂN BẰNG' if p_val > 0.05 else 'MẤT CÂN BẰNG (LỖI SRM)'}\n")

check_balance(df_target, 'age')
check_balance(df_target, 'monthly_rides_history')
check_balance(df_target, 'recency_days')

control_rides = df_target[df_target['treatment_rand'] == 0]['y_rand']
treatment_rides = df_target[df_target['treatment_rand'] == 1]['y_rand']

# Trực quan hóa
plt.figure(figsize=(10, 5))
sns.histplot(control_rides, color='blue', alpha=0.5, label='Control (Không Voucher)', kde=True, stat="density")
sns.histplot(treatment_rides, color='red', alpha=0.5, label='Treatment (Có Voucher)', kde=True, stat="density")
plt.title('Phân phối số chuyến xe giữa nhóm Treatment và Control')
plt.xlabel('Số chuyến (y_rand)')
plt.ylabel('Mật độ')
plt.legend()
plt.show()

# Tính ATE và T-Test
mean_control = control_rides.mean()
mean_treatment = treatment_rides.mean()
ate = mean_treatment - mean_control
relative_uplift = (ate / mean_control) * 100

t_stat, p_val = stats.ttest_ind(treatment_rides, control_rides, equal_var=False)

# Tính Confidence Interval 95%
se_control = control_rides.std() / np.sqrt(len(control_rides))
se_treatment = treatment_rides.std() / np.sqrt(len(treatment_rides))
se_diff = np.sqrt(se_control**2 + se_treatment**2)

margin_of_error = 2.576 * se_diff # Z-score 2.576 for 99% CI
ci_lower = ate - margin_of_error
ci_upper = ate + margin_of_error

print("=== KẾT QUẢ A/B TEST (OEC) ===")
print(f"Trung bình nhóm Control: {mean_control:.2f} chuyến/user")
print(f"Trung bình nhóm Treatment: {mean_treatment:.2f} chuyến/user")
print(f"Absolute Uplift (ATE): +{ate:.2f} chuyến/user")
print(f"Relative Uplift: +{relative_uplift:.2f}%")
print(f"99% Confidence Interval: [{ci_lower:.2f}, {ci_upper:.2f}]")
print(f"P-value: {p_val:.6f}")

if p_val < 0.05:
    print("\n🚀 KẾT LUẬN: Tác động mang ý nghĩa thống kê (Statistically Significant)!")
else:
    print("\n⚠️ KẾT LUẬN: Tác động KHÔNG có ý nghĩa thống kê (Not Statistically Significant).")

control_fare = df_target[df_target['treatment_rand'] == 0]['fare_rand']
treatment_fare = df_target[df_target['treatment_rand'] == 1]['fare_rand']

mean_fare_control = control_fare.mean()
mean_fare_treatment = treatment_fare.mean()

incremental_gross_revenue = mean_fare_treatment - mean_fare_control
voucher_cost = mean_fare_treatment * 0.25 # Tính bằng 25% doanh thu

incremental_net_revenue = incremental_gross_revenue - voucher_cost
roi = incremental_net_revenue / voucher_cost

print("=== KẾT QUẢ KINH TẾ HỌC (ECONOMICS GUARDRAIL) ===")
print(f"Doanh thu trung bình nhóm Control: ${mean_fare_control:.2f}/user")
print(f"Doanh thu trung bình nhóm Treatment: ${mean_fare_treatment:.2f}/user")
print(f"Doanh thu gộp tăng thêm: +${incremental_gross_revenue:.2f}/user")
print(f"Chi phí phát hành Voucher: ${voucher_cost:.2f}/user")
print("-" * 40)
print(f"Doanh thu thuần tăng thêm (Net Revenue): ${incremental_net_revenue:.2f}/user")
print(f"ROI (Return on Investment): {roi*100:.1f}%")

if roi > 0:
    print("\n✅ ĐẠT YÊU CẦU: Chiến dịch có LÃI. Nên tiến hành Roll-out toàn hệ thống!")
else:
    print("\n❌ CẢNH BÁO: Chiến dịch bị LỖ. Cần giảm chi phí Voucher hoặc tối ưu lại Targeting.")

print('='*60)
print('SO SÁNH HIỆU QUẢ VOUCHER TRÊN CÁC TẬP KHÁCH HÀNG (HTE)')
print('='*60 + '\n')

personas_to_test = ['Airport Business', 'Rain Riders', 'Urban Credit Card', 'Urban Cash', 'Suburban Occasionals']
rois = []

for target in personas_to_test:
    print(f'--- ĐÁNH GIÁ NHÓM: {target.upper()} ---')
    df_t = df[df['persona'] == target].copy()
    
    control = df_t[df_t['treatment_rand'] == 0]['y_rand']
    treatment = df_t[df_t['treatment_rand'] == 1]['y_rand']
    _, p_val = stats.ttest_ind(control, treatment, equal_var=False)
    
    ate = treatment.mean() - control.mean()
    print(f'Incremental Rides (ATE): +{ate:.2f} chuyến/user')
    print(f'P-Value: {p_val:.6f}')
    
    c_fare = df_t[df_t['treatment_rand'] == 0]['fare_rand'].mean()
    t_fare = df_t[df_t['treatment_rand'] == 1]['fare_rand'].mean()
    
    inc_gross = t_fare - c_fare
    cost = t_fare * 0.25
    inc_net = inc_gross - cost
    roi = (inc_net / cost) * 100 if cost > 0 else 0
    rois.append(roi)
    
    print(f'Doanh thu thuần tăng thêm (Net Revenue): ${inc_net:.2f}/user')
    print(f'ROI (Return on Investment): {roi:.1f}%\n\n')

plt.figure(figsize=(9, 5))
sns.barplot(x=personas_to_test, y=rois, palette=['#e74c3c', '#2ecc71', '#3498db', '#f1c40f', '#9b59b6'])
plt.title('So sánh ROI giữa các nhóm khách hàng', fontsize=14, fontweight='bold')
plt.ylabel('ROI (%)')
plt.axhline(0, color='black', linewidth=1)
for i, roi in enumerate(rois):
    plt.text(i, roi + 5, f'{roi:.1f}%', ha='center', fontsize=12, fontweight='bold')
plt.show()

import pandas as pd
import numpy as np

# Giả định Kinh doanh
margin_per_trip = 10.0 # Lãi ròng 10 USD/chuyến (hoặc 10,000 VND)

policies = []

# 1. Policy: No Voucher
policies.append({
    'Policy': 'No Voucher',
    'Target Audience': 'None',
    'Treated Users': 0,
    'Incremental Trips': 0,
    'Voucher Cost ($)': 0,
    'Incremental Profit ($)': 0,
    'Cost per Incremental Trip ($)': 0
})

# Tính toán cho toàn bộ tập dữ liệu
total_users = len(df)

# 2. Policy: Mass Voucher (Tất cả)
# Tổng ATE và Cost của mọi người
mass_control = df[df['treatment_rand'] == 0]['y_rand'].mean()
mass_treatment = df[df['treatment_rand'] == 1]['y_rand'].mean()
mass_ate = mass_treatment - mass_control
mass_inc_trips = mass_ate * total_users
mass_voucher_cost = df[df['treatment_rand'] == 1]['fare_rand'].mean() * 0.25 * total_users
mass_inc_profit = (mass_inc_trips * margin_per_trip) - mass_voucher_cost
mass_cpit = mass_voucher_cost / mass_inc_trips if mass_inc_trips > 0 else np.inf

policies.append({
    'Policy': 'Mass Voucher',
    'Target Audience': 'All Segments',
    'Treated Users': total_users,
    'Incremental Trips': int(mass_inc_trips),
    'Voucher Cost ($)': int(mass_voucher_cost),
    'Incremental Profit ($)': int(mass_inc_profit),
    'Cost per Incremental Trip ($)': round(mass_cpit, 2)
})

# 3. Policy: Segment Targeting (Chỉ Suburban Occasionals)
seg_df = df[df['persona'] == 'Suburban Occasionals']
seg_users = len(seg_df)
seg_control = seg_df[seg_df['treatment_rand'] == 0]['y_rand'].mean()
seg_treatment = seg_df[seg_df['treatment_rand'] == 1]['y_rand'].mean()
seg_ate = seg_treatment - seg_control
seg_inc_trips = seg_ate * seg_users
seg_voucher_cost = seg_df[seg_df['treatment_rand'] == 1]['fare_rand'].mean() * 0.25 * seg_users
seg_inc_profit = (seg_inc_trips * margin_per_trip) - seg_voucher_cost
seg_cpit = seg_voucher_cost / seg_inc_trips if seg_inc_trips > 0 else np.inf

policies.append({
    'Policy': 'Segment Targeting',
    'Target Audience': 'Suburban Occasionals',
    'Treated Users': seg_users,
    'Incremental Trips': int(seg_inc_trips),
    'Voucher Cost ($)': int(seg_voucher_cost),
    'Incremental Profit ($)': int(seg_inc_profit),
    'Cost per Incremental Trip ($)': round(seg_cpit, 2)
})

# Hiển thị bảng
policy_df = pd.DataFrame(policies)
print("=== BẢNG SO SÁNH CHIẾN LƯỢC KINH DOANH (POLICY COMPARISON) ===")
display(policy_df)

print("\n🚀 NHẬN XÉT:")
print("- Nếu phát đại trà (Mass Voucher), công ty mất trắng hàng chục ngàn USD vì bị nhóm Kháng Sale (Sân bay, Mưa) đốt tiền.")
print("- Nếu nhắm mục tiêu cơ bản (Segment Targeting) vào Suburban Occasionals, công ty bắt đầu CÓ LÃI.")
print("❓ CÂU HỎI MỞ CHO TUẦN 7: Làm sao để biến nhóm 'Urban Credit Card' từ Lỗ thành Lãi? Đáp án: Uplift Modeling!")


