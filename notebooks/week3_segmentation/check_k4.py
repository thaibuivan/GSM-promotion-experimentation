import pandas as pd
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

df = pd.read_csv('../../data/processed/complex_simulation_data.csv')
rush_hours = [7, 8, 9, 17, 18, 19]
df['is_rush_hour'] = df['preferred_hour'].apply(lambda x: 1 if x in rush_hours else 0)
df['is_credit_card'] = df['preferred_payment'].apply(lambda x: 1 if x == 'Credit Card' else 0)

features = ['is_urban', 'monthly_rides_history', 'recency_days', 'is_rush_hour', 
            'is_airport_trip', 'fare_obs', 'is_weekend_rider', 'is_rain_rider', 
            'is_credit_card', 'is_frequent_tipper', 'avg_trip_distance', 'typical_passenger_count']

X = df[features]
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Chạy thử K=4
kmeans_4 = KMeans(n_clusters=4, random_state=42, n_init=10)
kmeans_4.fit(X_scaled)
centroids_4 = pd.DataFrame(scaler.inverse_transform(kmeans_4.cluster_centers_), columns=features)

pd.set_option('display.max_columns', None)
print("=== TRỌNG TÂM CÁC CỤM KHI K=4 ===")
print(centroids_4.round(2))
