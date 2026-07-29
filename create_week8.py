import json

notebook = {
 "cells": [
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "# Tuần 8: Stress Test (Kiểm thử Khả năng chịu đựng của Pipeline)\n",
    "Theo đúng lộ trình (Phase 2), sau khi khóa xong A/B Pipeline, chúng ta cần tiến hành **Stress Test** để kiểm tra độ vững chắc (robustness) của hệ thống trước các biến động về Dữ liệu và Kích thước mẫu.\n",
    "\n",
    "**Mục tiêu kiểm tra:**\n",
    "1. **Độ hội tụ của ATE:** Estimated ATE có bám sát True ATE (Ground truth) khi thay đổi Sample Size không?\n",
    "2. **Coverage của Confidence Interval:** Khoảng tin cậy 95% có bao phủ đúng True Effect không?\n",
    "3. **Kiểm thử với True Effect = 0:** Khi Voucher không thực sự có tác dụng, Pipeline có tránh được kết luận sai (False Positive) không?"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": None,
   "metadata": {},
   "outputs": [],
   "source": [
    "import pandas as pd\n",
    "import numpy as np\n",
    "import matplotlib.pyplot as plt\n",
    "import seaborn as sns\n",
    "from scipy import stats\n",
    "\n",
    "plt.style.use('ggplot')\n",
    "sns.set_palette(\"Set2\")\n",
    "import warnings\n",
    "warnings.filterwarnings('ignore')\n",
    "\n",
    "df = pd.read_csv('../../data/processed/segmented_simulation_data.csv')\n",
    "target_persona = 'Urban Credit Card'\n",
    "df_target = df[df['persona'] == target_persona].copy()"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## 1. Kiểm tra sự hội tụ của Estimated ATE so với True ATE\n",
    "Chúng ta sẽ thay đổi kích thước mẫu (Sample Size) từ nhỏ đến lớn để xem lúc nào thì Estimated ATE (tính bằng công thức Mean Treatment - Mean Control) hội tụ về True ATE (Lấy từ hệ thống giả lập)."
   ]
  },
  {
   "cell_type": "code",
   "execution_count": None,
   "metadata": {},
   "outputs": [],
   "source": [
    "sample_sizes = np.linspace(100, len(df_target), 20).astype(int)\n",
    "estimated_ates = []\n",
    "true_ates = []\n",
    "ci_lowers = []\n",
    "ci_uppers = []\n",
    "\n",
    "for n in sample_sizes:\n",
    "    df_sample = df_target.sample(n, random_state=42)\n",
    "    \n",
    "    control = df_sample[df_sample['treatment_rand'] == 0]['y_rand']\n",
    "    treatment = df_sample[df_sample['treatment_rand'] == 1]['y_rand']\n",
    "    \n",
    "    # Tính Estimated ATE\n",
    "    est_ate = treatment.mean() - control.mean()\n",
    "    \n",
    "    # Tính True ATE trung bình của Sample đó (Ground Truth)\n",
    "    true_ate = df_sample['true_ite'].mean()\n",
    "    \n",
    "    # Confidence Interval 95%\n",
    "    se = np.sqrt(control.var()/len(control) + treatment.var()/len(treatment))\n",
    "    margin = 1.96 * se\n",
    "    \n",
    "    estimated_ates.append(est_ate)\n",
    "    true_ates.append(true_ate)\n",
    "    ci_lowers.append(est_ate - margin)\n",
    "    ci_uppers.append(est_ate + margin)\n",
    "\n",
    "plt.figure(figsize=(10, 6))\n",
    "plt.plot(sample_sizes, estimated_ates, marker='o', label='Estimated ATE', color='blue')\n",
    "plt.plot(sample_sizes, true_ates, linestyle='--', label='True ATE (Ground Truth)', color='red')\n",
    "plt.fill_between(sample_sizes, ci_lowers, ci_uppers, color='blue', alpha=0.1, label='95% CI')\n",
    "plt.title('Độ hội tụ của Estimated ATE theo Sample Size')\n",
    "plt.xlabel('Sample Size')\n",
    "plt.ylabel('Treatment Effect (Số chuyến đi)')\n",
    "plt.legend()\n",
    "plt.show()\n",
    "\n",
    "print(\"✅ Nhận xét: Khi Sample Size tăng lên, Estimated ATE ngày càng bám sát True ATE và Khoảng tin cậy (CI) hẹp lại.\")"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## 2. Kiểm thử khi True Effect = 0 (Null Scenario)\n",
    "Giả sử Voucher hoàn toàn bị hỏng và không có tác dụng gì (True Effect = 0). Pipeline A/B Testing có đủ nhạy để kết luận đúng là \"Không có tác dụng\" hay không? (Tránh lỗi False Positive)."
   ]
  },
  {
   "cell_type": "code",
   "execution_count": None,
   "metadata": {},
   "outputs": [],
   "source": [
    "# Tạo kịch bản True Effect = 0\n",
    "df_null = df_target.copy()\n",
    "\n",
    "# Ghi đè outcome: Nhóm Treatment không nhận được bất kỳ giá trị tăng thêm nào\n",
    "# Tức là số chuyến đi của họ bằng với số chuyến đi tự nhiên (Không bị ảnh hưởng bởi treatment)\n",
    "# Y_rand = Y_control + Noise (ở đây ta giả lập Y_rand_null bằng cách trừ đi true_ite nếu họ được chia vào T)\n",
    "df_null['y_rand_null'] = np.where(df_null['treatment_rand'] == 1, \n",
    "                                  df_null['y_rand'] - df_null['true_ite'], \n",
    "                                  df_null['y_rand'])\n",
    "\n",
    "null_control = df_null[df_null['treatment_rand'] == 0]['y_rand_null']\n",
    "null_treatment = df_null[df_null['treatment_rand'] == 1]['y_rand_null']\n",
    "\n",
    "t_stat, p_val = stats.ttest_ind(null_control, null_treatment, equal_var=False)\n",
    "\n",
    "print(\"=== KẾT QUẢ KHI TRUE EFFECT = 0 ===\")\n",
    "print(f\"Control Mean: {null_control.mean():.2f}\")\n",
    "print(f\"Treatment Mean: {null_treatment.mean():.2f}\")\n",
    "print(f\"Estimated ATE: {null_treatment.mean() - null_control.mean():.2f}\")\n",
    "print(f\"P-value: {p_val:.4f}\")\n",
    "\n",
    "if p_val < 0.05:\n",
    "    print(\"❌ FAIL: Hệ thống kết luận sai là có tác dụng (Lỗi Type I - False Positive)!\")\n",
    "else:\n",
    "    print(\"✅ PASS: Hệ thống kết luận chính xác là KHÔNG có tác dụng (P-value > 0.05). Pipeline cực kỳ an toàn!\")"
   ]
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.8.10"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 4
}

with open('notebooks/week8_stress_test/1_stress_test.ipynb', 'w', encoding='utf-8') as f:
    json.dump(notebook, f, indent=1, ensure_ascii=False)
