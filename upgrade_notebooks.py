import json
import os

def update_notebook(filepath, target_str, new_code):
    with open(filepath, 'r', encoding='utf-8') as f:
        nb = json.load(f)
        
    for cell in nb.get('cells', []):
        if cell.get('cell_type') == 'code':
            source = "".join(cell.get('source', []))
            if target_str in source:
                # Prepare new code as list of lines with newlines
                lines = [line + '\n' for line in new_code.split('\n')]
                if lines:
                    lines[-1] = lines[-1].rstrip('\n') # Remove last newline
                cell['source'] = lines
                
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(nb, f, indent=1, ensure_ascii=False)
        
# 1. Update 2_complex_data_generation.ipynb
gen_notebook = r"D:\Intern VSF\GSM-promotion-experimentation\notebooks\week2_synthetic_data\2_complex_data_generation.ipynb"
new_gen_code = """import numpy as np
import pandas as pd

# --- HẰNG SỐ NỀN TẢNG TỪ EDA TUẦN 1 ---
N_USERS = 20000
TRUE_ATE = 0.8
RIDES_LAMBDA = 5
AGE_MEAN = 30
AGE_STD = 8
HOUR_DEMAND_MULTIPLIER = [
    0.3, 0.2, 0.2, 0.15, 0.15, 0.2,
    0.5, 1.0, 1.5,
    1.5,
    1.0, 0.8, 0.7, 0.7,
    0.8, 0.9,
    1.0, 1.5, 1.5,
    1.3, 1.2, 1.0,
    0.8, 0.5
]
URBAN_RATIO = 0.60

class RideSharingDataGenerator:
    def __init__(self, n_users=N_USERS, true_ate=TRUE_ATE):
        self.n = n_users
        self.true_ate = true_ate

    def run(self):
        # 1. Base Demographics
        is_urban = np.random.binomial(n=1, p=URBAN_RATIO, size=self.n)
        age = np.clip(np.random.normal(AGE_MEAN, AGE_STD, self.n), 18, 60).astype(int)
        
        # 2. PHASE 2 FEATURES
        is_weekend_rider = np.random.binomial(n=1, p=0.30, size=self.n)
        is_rain_rider = np.random.binomial(n=1, p=0.15, size=self.n)
        prob_airport = np.where(is_urban == 1, 0.08, 0.02)
        is_airport_trip = np.random.binomial(n=1, p=prob_airport)
        payment_type = np.random.choice([1, 2], size=self.n, p=[0.8, 0.2])
        passenger_count = np.random.choice([1, 2, 3, 4], size=self.n, p=[0.7, 0.2, 0.08, 0.02])

        # 3. Behavior
        monthly_rides = np.random.poisson(lam=RIDES_LAMBDA, size=self.n)
        recency_mean = np.where(is_urban == 1, 4, 10)
        recency_days = np.clip(np.random.poisson(lam=recency_mean), 0, 30).astype(int)
        
        hour_weights = np.array(HOUR_DEMAND_MULTIPLIER)
        hour_probs = hour_weights / hour_weights.sum()
        preferred_hour = np.random.choice(range(24), size=self.n, p=hour_probs)

        # 4. Base Rides
        hour_effect = np.array([HOUR_DEMAND_MULTIPLIER[h] for h in preferred_hour])
        base = (
            monthly_rides * 0.5 
            - recency_days * 0.15 
            + is_urban * 1.5 
            + (hour_effect - 0.7) * 0.5
            + is_weekend_rider * 1.0
            + is_rain_rider * 0.5
            + is_airport_trip * 2.0
        )
        noise = np.random.normal(0, 1.2, self.n)
        y0_rides = np.clip(base + noise, 0, None)

        # 5. Treatment Randomization
        t_rand = np.random.binomial(1, p=0.5, size=self.n)

        # 6. HTE Injection
        is_leisure = ((preferred_hour >= 10) & (preferred_hour <= 15)) | (preferred_hour >= 20)
        is_urban_leisure = (is_urban == 1) & is_leisure

        ate_multiplier = np.where(is_urban_leisure, 2.5/self.true_ate, 1.0)
        ate_multiplier = np.where(is_airport_trip == 1, 0.0, ate_multiplier)
        ate_multiplier = np.where(payment_type == 2, 0.1, ate_multiplier)
        ate_multiplier = np.where(is_rain_rider == 1, ate_multiplier * 0.5, ate_multiplier)
        ate_multiplier = np.where((is_weekend_rider == 1) & (is_airport_trip == 0), ate_multiplier * 1.5, ate_multiplier)

        treatment_effect = self.true_ate * ate_multiplier
        y1_rides = y0_rides + treatment_effect
        y_rand = np.where(t_rand == 1, y1_rides, y0_rides)

        # 7. Fare
        avg_distance = np.where(is_urban == 1, np.random.normal(3.0, 1.0, self.n), np.random.normal(5.5, 2.0, self.n))
        avg_distance = np.clip(avg_distance, 0.5, 25)
        avg_distance = np.where(is_airport_trip == 1, np.random.normal(15.0, 3.0, self.n), avg_distance)
        
        fare = y_rand * (5.0 * avg_distance + np.random.normal(0, 2.5, self.n))
        fare_rand = np.clip(fare, 0, None).round(2)

        df = pd.DataFrame({
            'user_id': range(1, self.n + 1),
            'age': age,
            'is_urban': is_urban,
            'is_weekend_rider': is_weekend_rider,
            'is_rain_rider': is_rain_rider,
            'is_airport_trip': is_airport_trip,
            'payment_type': payment_type,
            'passenger_count': passenger_count,
            'monthly_rides_history': monthly_rides,
            'recency_days': recency_days,
            'preferred_hour': preferred_hour,
            'treatment_rand': t_rand,
            'y_rand': y_rand,
            'fare_rand': fare_rand
        })
        return df

print("Đang khởi tạo Data Generator V2...")"""
update_notebook(gen_notebook, "class RideSharingDataGenerator", new_gen_code)

# 2. Update 1_user_segmentation.ipynb
seg_notebook = r"D:\Intern VSF\GSM-promotion-experimentation\notebooks\week3_segmentation\1_user_segmentation.ipynb"
new_seg_code = """from sklearn.preprocessing import StandardScaler
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

print("\\nSố lượng khách hàng mỗi nhóm:")
print(df['persona'].value_counts())"""
update_notebook(seg_notebook, "KMeans(n_clusters=4", new_seg_code)

print("Đã nâng cấp xong Notebooks!")
