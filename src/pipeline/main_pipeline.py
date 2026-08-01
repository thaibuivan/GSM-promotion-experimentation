import os
import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from xgboost import XGBRegressor
import warnings
warnings.filterwarnings('ignore')

# Constants
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

def run_pipeline(n_users=N_USERS, progress_callback=None):
    if progress_callback: progress_callback(10, "Đang sinh dữ liệu nhân khẩu học (Demographics)...")
    
    # 1. Base Demographics
    is_urban = np.random.binomial(n=1, p=URBAN_RATIO, size=n_users)
    age = np.clip(np.random.normal(AGE_MEAN, AGE_STD, n_users), 18, 60).astype(int)
    
    is_weekend_rider = np.random.binomial(n=1, p=0.30, size=n_users)
    is_rain_rider = np.random.binomial(n=1, p=0.15, size=n_users)
    prob_airport = np.where(is_urban == 1, 0.08, 0.02)
    is_airport_trip = np.random.binomial(n=1, p=prob_airport)
    payment_type = np.random.choice([1, 2], size=n_users, p=[0.8, 0.2])
    passenger_count = np.random.choice([1, 2, 3, 4], size=n_users, p=[0.7, 0.2, 0.08, 0.02])

    if progress_callback: progress_callback(30, "Đang thiết lập hành vi người dùng (User Behavior)...")
    
    monthly_rides = np.random.poisson(lam=RIDES_LAMBDA, size=n_users)
    recency_mean = np.where(is_urban == 1, 4, 10)
    recency_days = np.clip(np.random.poisson(lam=recency_mean), 0, 30).astype(int)
    
    hour_weights = np.array(HOUR_DEMAND_MULTIPLIER)
    hour_probs = hour_weights / hour_weights.sum()
    preferred_hour = np.random.choice(range(24), size=n_users, p=hour_probs)

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
    noise = np.random.normal(0, 1.2, n_users)
    y0_rides = np.clip(base + noise, 0, None)

    if progress_callback: progress_callback(50, "Đang cấu hình hệ thống A/B Testing và mô phỏng Causal Effect...")
    
    t_rand = np.random.binomial(1, p=0.5, size=n_users)
    is_leisure = ((preferred_hour >= 10) & (preferred_hour <= 15)) | (preferred_hour >= 20)
    is_urban_leisure = (is_urban == 1) & is_leisure

    ate_multiplier = np.where(is_urban_leisure, 2.5/TRUE_ATE, 1.0)
    ate_multiplier = np.where(is_airport_trip == 1, 0.0, ate_multiplier)
    ate_multiplier = np.where(payment_type == 2, 0.1, ate_multiplier)
    ate_multiplier = np.where(is_rain_rider == 1, ate_multiplier * 0.5, ate_multiplier)
    ate_multiplier = np.where((is_weekend_rider == 1) & (is_airport_trip == 0), ate_multiplier * 1.5, ate_multiplier)

    treatment_effect = TRUE_ATE * ate_multiplier
    y1_rides = y0_rides + treatment_effect
    y_rand = np.where(t_rand == 1, y1_rides, y0_rides)

    avg_distance = np.where(is_urban == 1, np.random.normal(3.0, 1.0, n_users), np.random.normal(5.5, 2.0, n_users))
    avg_distance = np.clip(avg_distance, 0.5, 25)
    avg_distance = np.where(is_airport_trip == 1, np.random.normal(15.0, 3.0, n_users), avg_distance)
    fare = y_rand * (5.0 * avg_distance + np.random.normal(0, 2.5, n_users))
    fare_rand = np.clip(fare, 0, None).round(2)

    df = pd.DataFrame({
        'user_id': range(1, n_users + 1),
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

    if progress_callback: progress_callback(70, "Đang huấn luyện mô hình K-Means 5 Cụm...")
    
    features = ['is_urban', 'monthly_rides_history', 'preferred_hour', 'recency_days', 
                'is_weekend_rider', 'is_rain_rider', 'is_airport_trip', 'payment_type', 'passenger_count']
    X = df[features]
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    kmeans = KMeans(n_clusters=5, random_state=42, n_init=10)
    df['cluster_id'] = kmeans.fit_predict(X_scaled)
    centroids = pd.DataFrame(scaler.inverse_transform(kmeans.cluster_centers_), columns=features)

    def auto_label(row):
        if row['is_airport_trip'] > 0.4: return 'Airport Business'
        if row['payment_type'] > 1.5: return 'Cash Traditional'
        if row['is_weekend_rider'] > 0.6 and row['is_urban'] > 0.5: return 'Urban Weekend'
        if row['is_urban'] > 0.5: return 'Urban Regulars'
        return 'Suburban Occasionals'

    persona_map = {i: auto_label(row) for i, row in centroids.iterrows()}
    df['persona'] = df['cluster_id'].map(persona_map)

    if progress_callback: progress_callback(85, "Đang huấn luyện Uplift Model (T-Learner XGBoost)...")
    
    # Train T-Learner
    df_train = df.copy()
    model_0 = XGBRegressor(n_estimators=100, max_depth=4, learning_rate=0.1, random_state=42)
    model_1 = XGBRegressor(n_estimators=100, max_depth=4, learning_rate=0.1, random_state=42)
    
    df_t0 = df_train[df_train['treatment_rand'] == 0]
    df_t1 = df_train[df_train['treatment_rand'] == 1]
    
    model_0.fit(df_t0[features], df_t0['y_rand'])
    model_1.fit(df_t1[features], df_t1['y_rand'])
    
    # Predict CATE
    pred_0 = model_0.predict(df_train[features])
    pred_1 = model_1.predict(df_train[features])
    df['cate_score'] = pred_1 - pred_0

    if progress_callback: progress_callback(95, "Đang lưu cấu trúc Dữ liệu vào Database...")
    
    # Save to processed folder
    base_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    save_dir = os.path.join(base_path, 'data', 'processed')
    os.makedirs(save_dir, exist_ok=True)
    df.to_csv(os.path.join(save_dir, 'segmented_simulation_data.csv'), index=False)
    
    if progress_callback: progress_callback(100, "Hoàn tất Toàn bộ Pipeline!")
    return df

if __name__ == "__main__":
    def print_prog(pct, msg):
        print(f"[{pct}%] {msg}")
    run_pipeline(progress_callback=print_prog)
