import json

with open('notebooks/week8_stress_test/1_stress_test.ipynb', 'r', encoding='utf-8') as f:
    nb = json.load(f)

new_cells = [
    {
        "cell_type": "markdown",
        "metadata": {},
        "source": [
            "## 3. Stress Test: Tỷ lệ chia mẫu (Treatment Ratio) không đều\n",
            "Đôi khi do ngân sách Marketing eo hẹp, chúng ta không thể chia 50/50 mà phải chia 90% Control / 10% Treatment. Liệu ATE có còn chính xác?"
        ]
    },
    {
        "cell_type": "code",
        "metadata": {},
        "outputs": [],
        "execution_count": None,
        "source": [
            "print(\"=== KỊCH BẢN CHIA MẪU 90/10 ===\")\n",
            "df_imbalanced = df.copy()\n",
            "# Randomize lại với tỷ lệ 10% nhận Voucher\n",
            "np.random.seed(42)\n",
            "df_imbalanced['treatment_imbalanced'] = np.random.choice([0, 1], size=len(df), p=[0.9, 0.1])\n",
            "\n",
            "y_t_imb = df_imbalanced[df_imbalanced['treatment_imbalanced'] == 1]['y_rand'].mean()\n",
            "y_c_imb = df_imbalanced[df_imbalanced['treatment_imbalanced'] == 0]['y_rand'].mean()\n",
            "ate_imb = y_t_imb - y_c_imb\n",
            "\n",
            "print(f\"Tỷ lệ tập T thực tế: {df_imbalanced['treatment_imbalanced'].mean():.2%}\")\n",
            "print(f\"ATE đo được (Sample Size: {len(df)}): {ate_imb:.4f} chuyến (So với gốc 0.1740)\")\n",
            "print(\"-> Kết luận: ATE sẽ dao động mạnh hơn và khoảng tin cậy sẽ rộng hơn do mẫu nhóm T quá ít.\")\n"
        ]
    },
    {
        "cell_type": "markdown",
        "metadata": {},
        "source": [
            "## 4. Stress Test: Thêm Nhiễu ngẫu nhiên (Gaussian Noise)\n",
            "Trong thực tế, số chuyến đi có thể bị nhiễu do thời tiết, ngày nghỉ lễ. Hãy bơm thêm nhiễu ngẫu nhiên vào dữ liệu để xem ATE có bị phá vỡ không."
        ]
    },
    {
        "cell_type": "code",
        "metadata": {},
        "outputs": [],
        "execution_count": None,
        "source": [
            "print(\"=== KỊCH BẢN BƠM NHIỄU (NOISE INJECTION) ===\")\n",
            "df_noisy = df.copy()\n",
            "# Thêm nhiễu phân phối chuẩn (Mean = 0, Std = 1)\n",
            "np.random.seed(99)\n",
            "noise = np.random.normal(0, 1, size=len(df))\n",
            "df_noisy['y_noisy'] = df_noisy['y_rand'] + noise\n",
            "\n",
            "y_t_noisy = df_noisy[df_noisy['treatment_rand'] == 1]['y_noisy'].mean()\n",
            "y_c_noisy = df_noisy[df_noisy['treatment_rand'] == 0]['y_noisy'].mean()\n",
            "ate_noisy = y_t_noisy - y_c_noisy\n",
            "\n",
            "print(f\"ATE đo được (có nhiễu): {ate_noisy:.4f} chuyến\")\n",
            "print(f\"Sai số tuyệt đối so với ATE gốc (0.1740): {abs(ate_noisy - 0.1740):.4f} chuyến\")\n",
            "print(\"-> Kết luận: Thử nghiệm ngẫu nhiên hóa (A/B Test) vẫn duy trì được ATE cực kỳ vững chắc (Robust) bất chấp dữ liệu bị bơm nhiễu mạnh, bởi vì nhiễu được triệt tiêu đều ở cả 2 nhóm!\")\n"
        ]
    }
]

nb['cells'].extend(new_cells)

with open('notebooks/week8_stress_test/1_stress_test.ipynb', 'w', encoding='utf-8') as f:
    json.dump(nb, f, indent=1, ensure_ascii=False)
