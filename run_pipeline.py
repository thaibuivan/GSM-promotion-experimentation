import numpy as np
import pandas as pd
from scipy import stats

np.random.seed(42)

N_USERS = 20000
TRUE_ATE = 0.5  # <--- HẠ XUỐNG 0.5 (Đã thay đổi)

RIDES_LAMBDA = 5
AGE_MEAN = 30
AGE_STD = 8
GENDER_PROBS = [0.55, 0.40, 0.05]

AVG_FARE_USD = 17.60
MEDIAN_FARE_USD = 13.50
AVG_FARE_PER_MILE = 8.43

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
        age = np.clip(np.random.normal(AGE_MEAN, AGE_STD, self.n), 18, 60).astype(int)
        gender = np.random.choice(['Male', 'Female', 'Other'], size=self.n, p=GENDER_PROBS)
        is_urban = np.random.binomial(n=1, p=URBAN_RATIO, size=self.n)
        
        monthly_rides = np.random.poisson(lam=RIDES_LAMBDA, size=self.n)
        segment = np.where(monthly_rides < 4, 'Occasional', np.where(monthly_rides <= 8, 'Regular', 'Heavy'))
        
        recency_mean = np.where(is_urban == 1, 4, 10)
        recency_days = np.clip(np.random.poisson(lam=recency_mean), 0, 30).astype(int)
        
        hour_weights = np.array(HOUR_DEMAND_MULTIPLIER)
        hour_probs = hour_weights / hour_weights.sum()
        preferred_hour = np.random.choice(range(24), size=self.n, p=hour_probs)
        
        hour_effect = np.array([HOUR_DEMAND_MULTIPLIER[h] for h in preferred_hour])
        base = (monthly_rides * 0.5 - recency_days * 0.15 + is_urban * 1.5 + (hour_effect - 0.7) * 0.5)
        noise = np.random.normal(0, 1.2, self.n)
        base = np.clip(base + noise, 0, None)
        
        prob_t = np.clip(0.1 + (is_urban * 0.35) + (monthly_rides * 0.04), 0.05, 0.90)
        t_obs = np.random.binomial(1, p=prob_t)
        t_rand = np.random.binomial(1, p=0.5, size=self.n)
        
        y_obs = np.clip(base + (self.true_ate * t_obs) + np.random.normal(0, 0.8, self.n), 0, None).round().astype(int)
        y_rand = np.clip(base + (self.true_ate * t_rand) + np.random.normal(0, 0.8, self.n), 0, None).round().astype(int)
        
        FARE_PER_KM = 5.0
        avg_distance_obs = np.clip(np.where(is_urban == 1, np.random.normal(3.0, 1.0, self.n), np.random.normal(5.5, 2.0, self.n)), 0.5, 25)
        avg_distance_rand = np.clip(np.where(is_urban == 1, np.random.normal(3.0, 1.0, self.n), np.random.normal(5.5, 2.0, self.n)), 0.5, 25)
        
        fare_obs = np.clip(y_obs * (FARE_PER_KM * avg_distance_obs + np.random.normal(0, 2.5, self.n)), 0, None).round(2)
        fare_rand = np.clip(y_rand * (FARE_PER_KM * avg_distance_rand + np.random.normal(0, 2.5, self.n)), 0, None).round(2)
        
        return pd.DataFrame({
            'user_id': range(1, self.n + 1),
            'age': age, 'gender': gender, 'is_urban': is_urban,
            'customer_segment': segment, 'monthly_rides_history': monthly_rides,
            'recency_days': recency_days, 'preferred_hour': preferred_hour,
            'base_rides': base.round(1),
            'treatment_obs': t_obs, 'y_obs': y_obs, 'fare_obs': fare_obs,
            'treatment_rand': t_rand, 'y_rand': y_rand, 'fare_rand': fare_rand,
        })

print("Running Data Generator...")
df = RideSharingDataGenerator().run()
df.to_csv('data/processed/complex_simulation_data.csv', index=False)

from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
print("Running Segmentation...")
X = df[['is_urban', 'monthly_rides_history', 'preferred_hour', 'recency_days']]
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)
kmeans = KMeans(n_clusters=4, random_state=42, n_init=10)
df['cluster_id'] = kmeans.fit_predict(X_scaled)

persona_names = {0: 'Suburban Commuters', 1: 'Urban Commuters', 2: 'Urban Leisure', 3: 'Suburban Occasionals'}
df['persona'] = df['cluster_id'].map(persona_names)
df.to_csv('data/processed/segmented_simulation_data.csv', index=False)

print("Running A/B Test Analysis...")
df_target = df[df['persona'] == 'Suburban Commuters'].copy()

control = df_target[df_target['treatment_rand'] == 0]['y_rand']
treatment = df_target[df_target['treatment_rand'] == 1]['y_rand']
t_stat, p_val = stats.ttest_ind(control, treatment, equal_var=False)
print(f"Incremental Rides P-Value: {p_val}")

control_fare = df_target[df_target['treatment_rand'] == 0]['fare_rand']
treatment_fare = df_target[df_target['treatment_rand'] == 1]['fare_rand']

mean_fare_control = control_fare.mean()
mean_fare_treatment = treatment_fare.mean()

incremental_gross_revenue = mean_fare_treatment - mean_fare_control
voucher_cost = mean_fare_treatment * 0.25 
incremental_net_revenue = incremental_gross_revenue - voucher_cost
roi = incremental_net_revenue / voucher_cost

print(f"Mean Fare Control: ${mean_fare_control:.2f}")
print(f"Mean Fare Treatment: ${mean_fare_treatment:.2f}")
print(f"Incremental Gross Revenue: ${incremental_gross_revenue:.2f}")
print(f"Voucher Cost: ${voucher_cost:.2f}")
print(f"Net Revenue: ${incremental_net_revenue:.2f}")
print(f"ROI: {roi*100:.1f}%")