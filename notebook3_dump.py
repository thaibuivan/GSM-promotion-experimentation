import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
import warnings
warnings.filterwarnings('ignore')

sns.set_theme(style='whitegrid')
print('Libraries loaded.')

# Tải dữ liệu
df = pd.read_csv('../../data/processed/complex_simulation_data.csv')

# Feature Engineering:
# Thuật toán K-Means hoạt động trên không gian khoảng cách (Euclidean).
# Biến preferred_hour mang tính chu kỳ (0-23h), dùng trực tiếp sẽ không chính xác.
# Do đó, ta chuyển thành biến nhị phân: is_rush_hour (1 nếu là giờ cao điểm, 0 nếu không).
rush_hours = [7, 8, 9, 17, 18, 19]
df['is_rush_hour'] = df['preferred_hour'].apply(lambda x: 1 if x in rush_hours else 0)

print(f'Dataset shape: {df.shape}')
display(df.head())

# Chọn các đặc trưng để phân cụm
features = ['age', 'is_urban', 'monthly_rides_history', 'recency_days', 'is_rush_hour']
X = df[features]

# Chuẩn hóa
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

print('Dữ liệu đã được chuẩn hóa.')

inertias = []
sil_scores = []
K_range = range(2, 8)

for k in K_range:
    kmeans = KMeans(n_clusters=k, random_state=42, n_init=10)
    labels = kmeans.fit_predict(X_scaled)
    inertias.append(kmeans.inertia_)
    # Sample để tính silhouette cho nhanh (vì dữ liệu 20k rows)
    sil_scores.append(silhouette_score(X_scaled, labels, sample_size=5000, random_state=42))

fig, ax1 = plt.subplots(figsize=(10, 5))

ax1.plot(K_range, inertias, 'bo-', label='Inertia (Elbow)')
ax1.set_xlabel('Số lượng cụm (K)')
ax1.set_ylabel('Inertia (WCSS)', color='b')
ax1.tick_params('y', colors='b')

ax2 = ax1.twinx()
ax2.plot(K_range, sil_scores, 'rs-', label='Silhouette Score')
ax2.set_ylabel('Silhouette Score', color='r')
ax2.tick_params('y', colors='r')

plt.title('Tìm K tối ưu bằng phương pháp Elbow & Silhouette')
plt.show()

from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans

# 1. Chuẩn bị tính năng (Bao gồm 5 tính năng mới của Phase 2)
features = ['is_urban', 'monthly_rides_history', 'preferred_hour', 'recency_days', 
            'is_weekend_rider', 'is_rain_rider', 'is_airport_trip', 'payment_type', 'passenger_count']
X = df[features]

# 2. Chuẩn hóa dữ liệu
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# 3. K-Means (K=5 cho Phase 2)
kmeans = KMeans(n_clusters=5, random_state=42, n_init=10)
df['cluster_id'] = kmeans.fit_predict(X_scaled)

centroids = pd.DataFrame(scaler.inverse_transform(kmeans.cluster_centers_), columns=features)
print("Tọa độ trọng tâm (Centroids) của 5 Cụm:")
display(centroids.round(2))

def auto_label(row):
    if row['is_airport_trip'] > 0.4: return 'Airport Business'
    if row['payment_type'] > 1.5: return 'Cash Traditional'
    if row['is_weekend_rider'] > 0.6 and row['is_urban'] > 0.5: return 'Urban Weekend Party'
    if row['is_urban'] > 0.5: return 'Urban Regulars'
    return 'Suburban Occasionals'

persona_map = {i: auto_label(row) for i, row in centroids.iterrows()}
df['persona'] = df['cluster_id'].map(persona_map)

print("\nSố lượng khách hàng mỗi nhóm:")
print(df['persona'].value_counts())

profile = df.groupby('cluster_id')[features].mean().round(2)
profile['size'] = df['cluster_id'].value_counts()
profile['percentage'] = (profile['size'] / len(df) * 100).round(1).astype(str) + '%'
display(profile)

from math import pi

def make_radar_chart(df_profile, features):
    # Normalize the profile values between 0 and 1 for the radar chart
    df_norm = (df_profile[features] - df_profile[features].min()) / (df_profile[features].max() - df_profile[features].min() + 1e-9)
    
    categories = features
    N = len(categories)
    angles = [n / float(N) * 2 * pi for n in range(N)]
    angles += angles[:1]
    
    plt.figure(figsize=(8, 8))
    ax = plt.subplot(111, polar=True)
    ax.set_theta_offset(pi / 2)
    ax.set_theta_direction(-1)
    plt.xticks(angles[:-1], categories, color='grey', size=11)
    ax.set_rlabel_position(0)
    plt.yticks([0.25, 0.5, 0.75], ["0.25","0.50","0.75"], color="grey", size=8)
    plt.ylim(0, 1)

    colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd']
    
    for i, (idx, row) in enumerate(df_norm.iterrows()):
        values = row.values.flatten().tolist()
        values += values[:1]
        ax.plot(angles, values, linewidth=2, linestyle='solid', label=f'Cluster {idx}', color=colors[i])
        ax.fill(angles, values, colors[i], alpha=0.1)
        
    plt.legend(loc='upper right', bbox_to_anchor=(0.1, 0.1))
    plt.title('Radar Chart của 5 Personas (Normalized)')
    plt.tight_layout()
    plt.show()

make_radar_chart(profile, features)

# Gán nhãn Persona chuẩn theo góc nhìn Business
persona_names = {
    0: 'Suburban Commuters',
    1: 'Urban Commuters',
    2: 'Urban Leisure',
    3: 'Suburban Occasionals'
}
df['persona'] = df['cluster_id'].map(persona_names)

# Lưu lại bộ dữ liệu có chứa nhãn Persona để dùng cho các tuần sau
df.to_csv('../../data/processed/segmented_simulation_data.csv', index=False)
print('Đã cập nhật nhãn Persona và lưu file segmented_simulation_data.csv thành công!')

