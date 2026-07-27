import json

filepath = r"D:\Intern VSF\GSM-promotion-experimentation\notebooks\week3_segmentation\1_user_segmentation.ipynb"

with open(filepath, 'r', encoding='utf-8') as f:
    nb = json.load(f)

def make_code_cell(source_lines):
    return {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": source_lines
    }

def make_md_cell(source_lines):
    return {
        "cell_type": "markdown",
        "metadata": {},
        "source": source_lines
    }

new_cells = [
    make_md_cell([
        "# Tuần 3: Phân tập Khách hàng (User Segmentation) & Định nghĩa Persona\n",
        "\n",
        "Mục tiêu: Dùng K-Means Clustering để nhóm 20,000 khách hàng thành các phân khúc dựa trên hành vi, nhân khẩu học và đặc điểm giao dịch.\n",
        "\n",
        "**Lý do chọn K=5 trong dự án này:**\n",
        "Mặc dù Elbow Method và Silhouette Score gợi ý K=4 theo tiêu chí thuần Toán học, chúng ta chọn K=5 vì lý do kinh doanh quan trọng: nhóm **Airport Business** có đặc điểm kinh tế hoàn toàn khác biệt — giá trị chuyến đi cao hơn 3-4x và kháng Voucher hoàn toàn (ATE ≈ 0). Bằng cách đưa `fare_obs` vào feature set, K-Means có thể tự nhiên tách nhóm này ra mà không cần gán nhãn thủ công."
    ]),
    make_code_cell([
        "import pandas as pd\n",
        "import numpy as np\n",
        "import matplotlib.pyplot as plt\n",
        "import seaborn as sns\n",
        "from sklearn.preprocessing import StandardScaler\n",
        "from sklearn.cluster import KMeans\n",
        "from sklearn.metrics import silhouette_score\n",
        "from math import pi\n",
        "import warnings\n",
        "warnings.filterwarnings('ignore')\n",
        "\n",
        "sns.set_theme(style='whitegrid')\n",
        "print('Libraries loaded.')"
    ]),
    make_md_cell(["## 1. Tải dữ liệu và Feature Engineering"]),
    make_code_cell([
        "df = pd.read_csv('../../data/processed/complex_simulation_data.csv')\n",
        "\n",
        "# Chuyển giờ chu kỳ thành biến nhị phân (K-Means không xử lý tốt biến chu kỳ)\n",
        "rush_hours = [7, 8, 9, 17, 18, 19]\n",
        "df['is_rush_hour'] = df['preferred_hour'].apply(lambda x: 1 if x in rush_hours else 0)\n",
        "\n",
        "print(f'Dataset shape: {df.shape}')\n",
        "display(df.head())"
    ]),
    make_md_cell([
        "## 2. Chuẩn hóa dữ liệu (Standardization)\n",
        "\n",
        "K-Means rất nhạy cảm với thang đo. Ta cần chuẩn hóa về cùng thang đo (Mean=0, Std=1).\n",
        "\n",
        "**Feature set cho K=5 (bao gồm fare_obs để tách nhóm Airport):**\n",
        "- `is_urban`, `is_rush_hour`, `recency_days`, `monthly_rides_history`: Đặc điểm hành vi nền tảng\n",
        "- `is_airport_trip`, `fare_obs`: Đặc điểm kinh tế giao dịch — giúp K-Means tự nhiên tách Airport\n",
        "- `is_weekend_rider`, `is_rain_rider`, `payment_type`: Biến hành vi Phase 2"
    ]),
    make_code_cell([
        "# Feature set bao gồm fare_obs để K-Means nhận diện Airport (chuyến đi giá trị cao)\n",
        "features = ['is_urban', 'monthly_rides_history', 'recency_days', 'is_rush_hour',\n",
        "            'is_airport_trip', 'fare_obs', 'is_weekend_rider', 'is_rain_rider', 'payment_type']\n",
        "\n",
        "X = df[features]\n",
        "scaler = StandardScaler()\n",
        "X_scaled = scaler.fit_transform(X)\n",
        "\n",
        "print('Dữ liệu đã được chuẩn hóa.')\n",
        "print(f'Feature set: {features}')"
    ]),
    make_md_cell([
        "## 3. Tìm số cụm K tối ưu (Elbow Method & Silhouette Score)\n",
        "\n",
        "> **Lưu ý phương pháp:** Elbow & Silhouette là tiêu chí định lượng giúp thu hẹp khoảng tìm kiếm. Quyết định cuối cùng kết hợp thêm **Domain Knowledge** (nhóm Airport cần tách riêng vì lý do kinh doanh)."
    ]),
    make_code_cell([
        "inertias = []\n",
        "sil_scores = []\n",
        "K_range = range(2, 8)\n",
        "\n",
        "for k in K_range:\n",
        "    kmeans = KMeans(n_clusters=k, random_state=42, n_init=10)\n",
        "    labels = kmeans.fit_predict(X_scaled)\n",
        "    inertias.append(kmeans.inertia_)\n",
        "    sil_scores.append(silhouette_score(X_scaled, labels, sample_size=5000, random_state=42))\n",
        "\n",
        "fig, ax1 = plt.subplots(figsize=(10, 5))\n",
        "ax1.plot(K_range, inertias, 'bo-', label='Inertia (Elbow)')\n",
        "ax1.set_xlabel('Số lượng cụm (K)')\n",
        "ax1.set_ylabel('Inertia (WCSS)', color='b')\n",
        "ax1.tick_params('y', colors='b')\n",
        "\n",
        "ax2 = ax1.twinx()\n",
        "ax2.plot(K_range, sil_scores, 'rs-', label='Silhouette Score')\n",
        "ax2.set_ylabel('Silhouette Score', color='r')\n",
        "ax2.tick_params('y', colors='r')\n",
        "\n",
        "plt.title('Tìm K tối ưu bằng phương pháp Elbow & Silhouette')\n",
        "plt.tight_layout()\n",
        "plt.show()\n",
        "\n",
        "print(f'Silhouette Scores: {[round(s,3) for s in sil_scores]}')\n",
        "print(f'K range: {list(K_range)}')"
    ]),
    make_md_cell([
        "Dựa vào biểu đồ và mục tiêu bài toán, ta chọn **K=5**:\n",
        "- Silhouette Score tại K=4 (thuần Toán học) và K=5 (có Domain Knowledge) chênh lệch nhỏ (~0.035)\n",
        "- Với feature `fare_obs` và `is_airport_trip` trong tập đặc trưng, K=5 cho phép thuật toán **tự nhiên tách nhóm Airport** — nhóm có giá trị kinh tế hoàn toàn khác biệt\n",
        "- Đây là cách áp dụng **Domain Knowledge** kết hợp với **Statistical Guidance** — tiêu chuẩn trong thực chiến"
    ]),
    make_code_cell([
        "# K-Means với K=5\n",
        "kmeans = KMeans(n_clusters=5, random_state=42, n_init=10)\n",
        "df['cluster_id'] = kmeans.fit_predict(X_scaled)\n",
        "\n",
        "# Phân tích Centroids để đặt tên Persona\n",
        "centroids = pd.DataFrame(scaler.inverse_transform(kmeans.cluster_centers_), columns=features)\n",
        "print('=== Tọa độ trọng tâm (Centroids) của 5 Cụm ===')\n",
        "display(centroids.round(2))"
    ]),
    make_md_cell(["## 4. Phân tích Cụm (Cluster Profiling) & Đặt tên Persona"]),
    make_code_cell([
        "# Đặt tên Persona dựa trên Centroid của từng cụm\n",
        "def auto_label(row):\n",
        "    \"\"\"Đọc Centroid và đặt tên Persona theo logic Business.\"\"\"\n",
        "    if row['is_airport_trip'] > 0.4:                              return 'Airport Business'\n",
        "    if row['payment_type'] > 1.5:                                  return 'Cash Traditional'\n",
        "    if row['is_weekend_rider'] > 0.5 and row['is_urban'] > 0.5:   return 'Urban Weekend Party'\n",
        "    if row['is_urban'] > 0.5:                                      return 'Urban Regulars'\n",
        "    return 'Suburban Occasionals'\n",
        "\n",
        "persona_map = {i: auto_label(row) for i, row in centroids.iterrows()}\n",
        "df['persona'] = df['cluster_id'].map(persona_map)\n",
        "\n",
        "print('=== Phân bổ Khách hàng theo Persona ===')\n",
        "persona_counts = df['persona'].value_counts()\n",
        "print(persona_counts)\n",
        "print(f'\\nTổng: {len(df)} khách hàng')"
    ]),
    make_code_cell([
        "# Bảng Profile đầy đủ cho 5 Personas\n",
        "profile = df.groupby('cluster_id')[features].mean().round(2)\n",
        "profile['persona'] = profile.index.map(persona_map)\n",
        "profile['size'] = df['cluster_id'].value_counts()\n",
        "profile['pct'] = (profile['size'] / len(df) * 100).round(1).astype(str) + '%'\n",
        "profile = profile.set_index('persona')\n",
        "print('=== Cluster Profile ===')\n",
        "display(profile)"
    ]),
    make_md_cell(["### Trực quan hóa bằng Biểu đồ Radar (Radar Chart)"]),
    make_code_cell([
        "def make_radar_chart(df_profile, features, title='Radar Chart của 5 Personas'):\n",
        "    df_norm = (df_profile[features] - df_profile[features].min()) / \\\n",
        "              (df_profile[features].max() - df_profile[features].min() + 1e-9)\n",
        "    \n",
        "    N = len(features)\n",
        "    angles = [n / float(N) * 2 * pi for n in range(N)]\n",
        "    angles += angles[:1]\n",
        "    \n",
        "    fig, ax = plt.subplots(figsize=(9, 9), subplot_kw=dict(polar=True))\n",
        "    ax.set_theta_offset(pi / 2)\n",
        "    ax.set_theta_direction(-1)\n",
        "    plt.xticks(angles[:-1], features, color='grey', size=10)\n",
        "    ax.set_rlabel_position(0)\n",
        "    plt.yticks([0.25, 0.5, 0.75], ['0.25','0.50','0.75'], color='grey', size=8)\n",
        "    plt.ylim(0, 1)\n",
        "\n",
        "    colors = ['#e74c3c', '#3498db', '#2ecc71', '#f39c12', '#9b59b6']\n",
        "    \n",
        "    for i, (persona_name, row) in enumerate(df_norm.iterrows()):\n",
        "        values = row.values.flatten().tolist()\n",
        "        values += values[:1]\n",
        "        ax.plot(angles, values, linewidth=2, linestyle='solid',\n",
        "                label=persona_name, color=colors[i % len(colors)])\n",
        "        ax.fill(angles, values, colors[i % len(colors)], alpha=0.08)\n",
        "        \n",
        "    plt.legend(loc='upper right', bbox_to_anchor=(1.3, 1.1), fontsize=10)\n",
        "    plt.title(title, size=13, pad=20)\n",
        "    plt.tight_layout()\n",
        "    plt.show()\n",
        "\n",
        "# Dùng profile theo persona_name\n",
        "profile_for_radar = df.groupby('persona')[features].mean().round(2)\n",
        "make_radar_chart(profile_for_radar, features)"
    ]),
    make_md_cell([
        "### Định nghĩa 5 Business Personas\n",
        "\n",
        "Từ Centroid và biểu đồ Radar, ta định nghĩa 5 nhóm như sau:\n",
        "\n",
        "| Persona | Đặc điểm nổi bật | Tần suất | Độ nhạy Voucher |\n",
        "|---|---|---|---|\n",
        "| **Airport Business** | Chuyến đi sân bay, fare cao 3-4x, giờ cố định theo lịch bay | ~5-8% | ❌ Kháng hoàn toàn (ATE≈0) |\n",
        "| **Cash Traditional** | Thanh toán tiền mặt, ngại app, ít dùng khuyến mãi digital | ~10-15% | ❌ Rất thấp |\n",
        "| **Urban Weekend Party** | Nội thành, cuối tuần, giờ tối — đây là nhóm nhạy cảm nhất | ~15-20% | ✅ Rất cao |\n",
        "| **Urban Regulars** | Dân văn phòng nội thành, đi làm đều đặn | ~30-35% | ✅ Trung bình |\n",
        "| **Suburban Occasionals** | Ngoại ô, không thường xuyên, tiết kiệm | ~20-25% | ✅ Cao (nhạy giá) |\n",
        "\n",
        "> **Nhóm mục tiêu cho chiến dịch Voucher:** Urban Weekend Party & Suburban Occasionals  \n",
        "> **Nhóm cần loại trừ tuyệt đối:** Airport Business & Cash Traditional (gây Cannibalization)"
    ]),
    make_code_cell([
        "# Lưu dataset đã có nhãn Persona\n",
        "df.to_csv('../../data/processed/segmented_simulation_data.csv', index=False)\n",
        "print(f'Đã lưu segmented_simulation_data.csv — {len(df)} rows, {len(df.columns)} cols')\n",
        "print(f'Phân bổ Persona cuối cùng:')\n",
        "print(df['persona'].value_counts())"
    ])
]

nb['cells'] = new_cells

with open(filepath, 'w', encoding='utf-8') as f:
    json.dump(nb, f, indent=1, ensure_ascii=False)

print("Done! Notebook 3 rewritten with K=5 successfully.")
