import scipy.stats as stats
import pandas as pd
import numpy as np

print("Running Data Generator...")
from notebooks.week2_synthetic_data.data_simulator import RideSharingDataGenerator
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

print("\n" + "="*50)
print("PHÂN TÍCH HIỆU ỨNG DỊ THỂ (HETEROGENEOUS TREATMENT EFFECTS)")
print("="*50 + "\n")

for target_persona in ['Suburban Commuters', 'Urban Leisure']:
    print(f"--- ĐÁNH GIÁ NHÓM: {target_persona.upper()} ---")
    df_target = df[df['persona'] == target_persona].copy()

    control = df_target[df_target['treatment_rand'] == 0]['y_rand']
    treatment = df_target[df_target['treatment_rand'] == 1]['y_rand']
    t_stat, p_val = stats.ttest_ind(control, treatment, equal_var=False)
    
    mean_control = control.mean()
    mean_treatment = treatment.mean()
    ate = mean_treatment - mean_control
    
    print(f"Incremental Rides (ATE): +{ate:.2f} chuyến/user")
    print(f"P-Value: {p_val:.6f}")

    control_fare = df_target[df_target['treatment_rand'] == 0]['fare_rand']
    treatment_fare = df_target[df_target['treatment_rand'] == 1]['fare_rand']

    mean_fare_control = control_fare.mean()
    mean_fare_treatment = treatment_fare.mean()

    incremental_gross_revenue = mean_fare_treatment - mean_fare_control
    voucher_cost = mean_fare_treatment * 0.25 
    incremental_net_revenue = incremental_gross_revenue - voucher_cost
    roi = incremental_net_revenue / voucher_cost if voucher_cost > 0 else 0

    print(f"Doanh thu thuần tăng thêm (Net Revenue): ${incremental_net_revenue:.2f}/user")
    print(f"ROI (Return on Investment): {roi*100:.1f}%\n")