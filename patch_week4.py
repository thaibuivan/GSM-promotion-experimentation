import json

with open('notebooks/week4_ab_testing/1_ab_test_analysis.ipynb', 'r', encoding='utf-8') as f:
    nb = json.load(f)

# The cell to find is the one containing `def check_balance`
target_idx = -1
for i, cell in enumerate(nb['cells']):
    if cell['cell_type'] == 'code':
        if any('def check_balance' in line for line in cell['source']):
            target_idx = i
            break

if target_idx != -1:
    srm_cell = {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": [
            "from scipy.stats import chisquare\n",
            "\n",
            "# 1. SRM Check (Sample Ratio Mismatch)\n",
            "n_control = len(df_target[df_target['treatment_rand'] == 0])\n",
            "n_treatment = len(df_target[df_target['treatment_rand'] == 1])\n",
            "total_users = n_control + n_treatment\n",
            "\n",
            "expected = [total_users / 2, total_users / 2]\n",
            "observed = [n_control, n_treatment]\n",
            "chi2_stat, p_val_srm = chisquare(f_obs=observed, f_exp=expected)\n",
            "\n",
            "print(\"=== SRM CHECK (Kiểm tra phân bổ mẫu) ===\")\n",
            "print(f\"Control: {n_control} | Treatment: {n_treatment}\")\n",
            "print(f\"Chi-Square P-value: {p_val_srm:.4f}\")\n",
            "if p_val_srm > 0.05:\n",
            "    print(\"✅ Không phát hiện SRM (Hệ thống chia ngẫu nhiên hoạt động tốt).\")\n",
            "else:\n",
            "    print(\"❌ LỖI SRM: Phân bổ mẫu có vấn đề!\")\n",
            "\n",
            "# 2. Covariate Balance Check\n",
            "def check_balance(df, feature):\n",
            "    control = df[df['treatment_rand'] == 0][feature]\n",
            "    treatment = df[df['treatment_rand'] == 1][feature]\n",
            "    t_stat, p_val = stats.ttest_ind(control, treatment, equal_var=False)\n",
            "    return p_val\n",
            "\n",
            "features_to_check = ['age', 'monthly_rides_history', 'recency_days', 'fare_obs']\n",
            "p_values = [check_balance(df_target, f) for f in features_to_check]\n",
            "\n",
            "plt.figure(figsize=(8, 4))\n",
            "sns.barplot(x=features_to_check, y=p_values, color='skyblue')\n",
            "plt.axhline(0.05, color='red', linestyle='--', label='Ngưỡng 0.05')\n",
            "plt.title('Covariate Balance Check (P-values)')\n",
            "plt.ylabel('P-value (Càng cao càng tốt)')\n",
            "plt.legend()\n",
            "plt.show()\n",
            "\n",
            "print(\"✅ Nếu tất cả cột đều cao hơn đường đỏ -> Covariate Balance Đạt!\")\n"
        ]
    }
    
    nb['cells'][target_idx] = srm_cell

with open('notebooks/week4_ab_testing/1_ab_test_analysis.ipynb', 'w', encoding='utf-8') as f:
    json.dump(nb, f, indent=1, ensure_ascii=False)
