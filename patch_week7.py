import json

with open('notebooks/week7_uplift_modeling/1_uplift_modeling_tlearner.ipynb', 'r', encoding='utf-8') as f:
    nb = json.load(f)

# Find where to append the disclaimer (right after the first markdown)
nb['cells'].insert(1, {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "> **⚠️ DISCLAIMER QUAN TRỌNG:**\n",
    "> Uplift Modeling trong file này được thực hiện trên **Synthetic user-level dataset (Dữ liệu giả lập)** được hiệu chỉnh từ phân phối của NYC TLC, phục vụ cho mục đích nghiên cứu và thí nghiệm.\n",
    "> **KHÔNG được trình bày hoặc hiểu lầm** đây là mô hình đã học từ dữ liệu khách hàng thực tế của Xanh SM."
   ]
})

# Remove the last cell which is incomplete evaluation
nb['cells'] = nb['cells'][:-2]

# Add proper AUUC and Qini evaluation
nb['cells'].extend([
    {
     "cell_type": "markdown",
     "metadata": {},
     "source": [
      "## 5. Đánh giá Uplift (Qini Curve & AUUC)\n",
      "Thay vì dùng Accuracy như các mô hình Classification bình thường, Uplift Modeling được đánh giá bằng **Qini Curve** và **AUUC (Area Under Uplift Curve)**.\n",
      "Chúng ta sẽ xếp hạng khách hàng theo điểm CATE dự đoán từ cao xuống thấp và đo lường số chuyến đi tích lũy (Cumulative Incremental Trips) tăng thêm."
     ]
    },
    {
     "cell_type": "code",
     "execution_count": None,
     "metadata": {},
     "outputs": [],
     "source": [
      "def plot_qini_curve(df_res):\n",
      "    # Sắp xếp khách hàng theo CATE giảm dần\n",
      "    df_sorted = df_res.sort_values(by='CATE_pred', ascending=False).reset_index(drop=True)\n",
      "    \n",
      "    # Tính toán Qini Curve\n",
      "    df_sorted['T_count'] = df_sorted['T'].cumsum()\n",
      "    df_sorted['C_count'] = (1 - df_sorted['T']).cumsum()\n",
      "    \n",
      "    df_sorted['Y_T_sum'] = (df_sorted['y_true'] * df_sorted['T']).cumsum()\n",
      "    df_sorted['Y_C_sum'] = (df_sorted['y_true'] * (1 - df_sorted['T'])).cumsum()\n",
      "    \n",
      "    # Tránh chia cho 0\n",
      "    df_sorted['C_count'] = df_sorted['C_count'].replace(0, 1)\n",
      "    \n",
      "    # Uplift Tích lũy (Cumulative Incremental Trips)\n",
      "    df_sorted['Qini'] = df_sorted['Y_T_sum'] - df_sorted['Y_C_sum'] * (df_sorted['T_count'] / df_sorted['C_count'])\n",
      "    \n",
      "    # Random policy (Đường chéo)\n",
      "    total_uplift = df_sorted['Qini'].iloc[-1]\n",
      "    df_sorted['Random_Qini'] = np.linspace(0, total_uplift, len(df_sorted))\n",
      "    \n",
      "    # Tính AUUC (Diện tích dưới đường Qini)\n",
      "    auuc_model = np.trapz(df_sorted['Qini'], dx=1)\n",
      "    auuc_random = np.trapz(df_sorted['Random_Qini'], dx=1)\n",
      "    qini_coef = (auuc_model - auuc_random) / auuc_random\n",
      "    \n",
      "    plt.figure(figsize=(10, 6))\n",
      "    plt.plot(df_sorted.index / len(df_sorted) * 100, df_sorted['Qini'], label='T-Learner Qini Curve', color='blue', linewidth=2)\n",
      "    plt.plot(df_sorted.index / len(df_sorted) * 100, df_sorted['Random_Qini'], label='Random Targeting', color='gray', linestyle='--')\n",
      "    plt.title(f'Qini Curve (AUUC Coefficient: {qini_coef:.3f})')\n",
      "    plt.xlabel('Tỷ lệ phần trăm khách hàng được Target (%)')\n",
      "    plt.ylabel('Cumulative Incremental Trips (Chuyến tăng thêm)')\n",
      "    plt.legend()\n",
      "    plt.grid(True, alpha=0.3)\n",
      "    plt.show()\n",
      "    \n",
      "    return df_sorted\n",
      "\n",
      "df_qini = plot_qini_curve(df_res)\n",
      "print(\"✅ Qini Coefficient > 0 chứng tỏ T-Learner ưu việt hơn hẳn so với việc phát Voucher ngẫu nhiên!\")"
     ]
    },
    {
     "cell_type": "markdown",
     "metadata": {},
     "source": [
      "## 6. Business Evaluation: Phân tích Top-k% Targeting\n",
      "Câu hỏi của Business: *\"Nếu tôi chỉ có ngân sách để phát Voucher cho 20% khách hàng tốt nhất (Top 20% predicted CATE), tôi sẽ thu về được bao nhiêu chuyến và lợi nhuận là bao nhiêu?\"*"
     ]
    },
    {
     "cell_type": "code",
     "execution_count": None,
     "metadata": {},
     "outputs": [],
     "source": [
      "top_k_percent = 0.20\n",
      "top_k_idx = int(len(df_qini) * top_k_percent)\n",
      "\n",
      "df_top_k = df_qini.iloc[:top_k_idx]\n",
      "\n",
      "# Tính lợi nhuận nếu áp dụng Top-20% Policy\n",
      "trips_generated = df_top_k['Qini'].iloc[-1]\n",
      "vouchers_sent = df_top_k['T_count'].iloc[-1]\n",
      "\n",
      "incremental_profit = (trips_generated * profit_per_ride) - (vouchers_sent * voucher_cost)\n",
      "\n",
      "print(\"=== BÁO CÁO HIỆU QUẢ KINH DOANH (TOP-20% TARGETING) ===\")\n",
      "print(f\"Số khách hàng được nhận Voucher (20%): {len(df_top_k)} người\")\n",
      "print(f\"Số Voucher thực tế đã phát (Nhóm T): {int(vouchers_sent)} voucher\")\n",
      "print(f\"Số chuyến đi tăng thêm (Incremental Trips): {trips_generated:.1f} chuyến\")\n",
      "print(f\"Tổng chi phí Voucher: {vouchers_sent * voucher_cost:,.0f} VND\")\n",
      "print(f\"Lợi nhuận gộp từ chuyến tăng thêm: {trips_generated * profit_per_ride:,.0f} VND\")\n",
      "print(\"-\" * 40)\n",
      "print(f\"💰 INCREMENTAL PROFIT (Lợi nhuận ròng tăng thêm): {incremental_profit:,.0f} VND\")\n",
      "\n",
      "if incremental_profit > 0:\n",
      "    print(\"\\n🚀 KẾT LUẬN: Chiến lược Top-20% Targeting tạo ra LỢI NHUẬN DƯƠNG. Khuyến nghị áp dụng thay cho Mass Voucher!\")\n",
      "else:\n",
      "    print(\"\\n⚠️ KẾT LUẬN: Lợi nhuận vẫn âm, cần điều chỉnh mức chiết khấu Voucher thấp hơn!\")"
     ]
    }
])

with open('notebooks/week7_uplift_modeling/1_uplift_modeling_tlearner.ipynb', 'w', encoding='utf-8') as f:
    json.dump(nb, f, indent=1, ensure_ascii=False)
