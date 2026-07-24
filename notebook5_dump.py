import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
from tqdm import tqdm

# Cài đặt giao diện
plt.style.use('ggplot')
sns.set_palette("Set2")

import warnings
warnings.filterwarnings('ignore')

df = pd.read_csv('../../data/processed/segmented_simulation_data.csv')
target_persona = 'Suburban Commuters'
df_target = df[df['persona'] == target_persona].copy()

print(f"Kích thước tệp khách hàng dùng để test: {len(df_target)}")

n_simulations = 5000
p_values = []
srm_p_values = []

np.random.seed(42) # Set seed for reproducibility

for _ in tqdm(range(n_simulations), desc="Đang chạy A/A Test Simulations"):
    # 1. Randomization: Gán 0 hoặc 1 ngẫu nhiên
    random_assignment = np.random.binomial(1, 0.5, size=len(df_target))
    
    group_a = df_target['y_obs'][random_assignment == 0]
    group_a_prime = df_target['y_obs'][random_assignment == 1]
    
    # 2. SRM Check (Chi-Square Test cho tỷ lệ 50/50)
    obs_counts = [len(group_a), len(group_a_prime)]
    exp_counts = [len(df_target)/2, len(df_target)/2]
    _, p_srm = stats.chisquare(f_obs=obs_counts, f_exp=exp_counts)
    srm_p_values.append(p_srm)
    
    # 3. Tính P-value của Metric (y_obs)
    t_stat, p_val = stats.ttest_ind(group_a, group_a_prime, equal_var=False)
    p_values.append(p_val)

print("Hoàn thành mô phỏng!")

plt.figure(figsize=(10, 6))
sns.histplot(p_values, bins=20, color='purple', stat='density', alpha=0.7)
plt.axhline(y=1, color='r', linestyle='--', label='Uniform Expected (Mức Lý Tưởng)')
plt.title('Phân phối của 1000 P-values trong A/A Test')
plt.xlabel('P-value')
plt.ylabel('Mật độ (Density)')
plt.legend()
plt.show()

# Kiểm tra tỷ lệ False Positive (False Positive Rate - FPR)
fpr = sum(p < 0.05 for p in p_values) / n_simulations
print(f"Tỷ lệ False Positive (Kỳ vọng ~5%): {fpr*100:.2f}%")
if 0.04 <= fpr <= 0.06:
    print("✅ HỆ THỐNG AN TOÀN: Tỷ lệ nhiễu FPR nằm trong ngưỡng chấp nhận được.")
else:
    print("❌ CẢNH BÁO ĐỎ: Hệ thống quá nhạy cảm hoặc quá ì ạch!")

# Kiểm định Kolmogorov-Smirnov (KS-test) để đo độ bằng phẳng (Uniformity)
ks_stat, ks_pval = stats.kstest(p_values, 'uniform')
print(f"
KS-Test P-value: {ks_pval:.4f}")
if ks_pval > 0.05:
    print("✅ HỆ THỐNG AN TOÀN: Phân phối P-value là một đường thẳng Uniform hoàn hảo!")
else:
    print("❌ LỖI RANDOMIZATION: Phân phối P-value bị méo mó!")

srm_failures = sum(p < 0.05 for p in srm_p_values)
print(f"Số lần hệ thống bị lỗi SRM (P-value < 0.05) trong {n_simulations} lần test: {srm_failures}")
print(f"Tỷ lệ lỗi SRM: {srm_failures/n_simulations * 100:.2f}%")

if srm_failures/n_simulations <= 0.05:
    print("✅ HỆ THỐNG AN TOÀN: Tỷ lệ phân bổ user 50/50 là hoàn hảo!")
else:
    print("❌ CẢNH BÁO SRM: Thuật toán Randomization bị lệch trọng số!")

