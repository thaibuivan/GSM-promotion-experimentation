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

# Khắc phục lỗi nếu Persona chưa được update hoàn chỉnh (như phát hiện lúc nãy)
if 'Persona A' in df['persona'].values:
    persona_names = {0: 'Suburban Commuters', 1: 'Urban Commuters', 2: 'Urban Leisure', 3: 'Suburban Occasionals'}
    df['persona'] = df['cluster_id'].map(persona_names)
    df.to_csv('../../data/processed/segmented_simulation_data.csv', index=False)

# Lọc nhóm mục tiêu
target_persona = 'Suburban Commuters'
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
print('='*60 + '
')

personas_to_test = ['Suburban Commuters', 'Urban Leisure']
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
    print(f'ROI (Return on Investment): {roi:.1f}%

')

plt.figure(figsize=(8, 5))
sns.barplot(x=personas_to_test, y=rois, palette=['#e74c3c', '#2ecc71'])
plt.title('So sánh ROI giữa 2 nhóm khách hàng', fontsize=14, fontweight='bold')
plt.ylabel('ROI (%)')
plt.axhline(0, color='black', linewidth=1)
for i, roi in enumerate(rois):
    plt.text(i, roi + 5, f'{roi:.1f}%', ha='center', fontsize=12, fontweight='bold')
plt.show()

