import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
import scipy.stats as stats
import warnings
warnings.filterwarnings('ignore')

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

class AdvancedRideSharingDataGenerator:
    def __init__(self, n_users=N_USERS, true_ate=TRUE_ATE):
        self.n = n_users
        self.true_ate = true_ate

    def run(self):
        # 1. Base Demographics
        is_urban = np.random.binomial(n=1, p=URBAN_RATIO, size=self.n)
        age = np.clip(np.random.normal(AGE_MEAN, AGE_STD, self.n), 18, 60).astype(int)
        
        # 2. PHASE 2 FEATURES (Từ Data Dictionary & Causal DAG)
        # Khách cuối tuần: 30%
        is_weekend_rider = np.random.binomial(n=1, p=0.30, size=self.n)
        # Khách đi mưa (Sẵn sàng gọi xe lúc Surge Pricing): 15%
        is_rain_rider = np.random.binomial(n=1, p=0.15, size=self.n)
        # Khách đi sân bay (JFK/LaGuardia): 5% tập trung ở Urban
        prob_airport = np.where(is_urban == 1, 0.08, 0.02)
        is_airport_trip = np.random.binomial(n=1, p=prob_airport)
        # Hình thức thanh toán: 1=Thẻ (80%), 2=Tiền mặt (20%)
        payment_type = np.random.choice([1, 2], size=self.n, p=[0.8, 0.2])
        # Số lượng khách (Đi ghép chia tiền cước): 1-4 người
        passenger_count = np.random.choice([1, 2, 3, 4], size=self.n, p=[0.7, 0.2, 0.08, 0.02])

        # 3. Behavior
        monthly_rides = np.random.poisson(lam=RIDES_LAMBDA, size=self.n)
        recency_mean = np.where(is_urban == 1, 4, 10)
        recency_days = np.clip(np.random.poisson(lam=recency_mean), 0, 30).astype(int)
        
        hour_weights = np.array(HOUR_DEMAND_MULTIPLIER)
        hour_probs = hour_weights / hour_weights.sum()
        preferred_hour = np.random.choice(range(24), size=self.n, p=hour_probs)

        # 4. Base Rides (Y0 - Không có Voucher)
        hour_effect = np.array([HOUR_DEMAND_MULTIPLIER[h] for h in preferred_hour])
        base = (
            monthly_rides * 0.5 
            - recency_days * 0.15 
            + is_urban * 1.5 
            + (hour_effect - 0.7) * 0.5
            + is_weekend_rider * 1.0 # Đi cuối tuần -> Tổng chuyến đi nhiều hơn
            + is_rain_rider * 0.5 # Hay đi mưa -> Đi taxi thay vì xe máy
            + is_airport_trip * 2.0 # Khách sân bay thường có lịch trình ổn định
        )
        noise = np.random.normal(0, 1.2, self.n)
        y0_rides = np.clip(base + noise, 0, None)

        # 5. Phân bổ Voucher ngẫu nhiên (A/B Test)
        t_rand = np.random.binomial(1, p=0.5, size=self.n)

        # 6. HTE Injection (Logic Nhân quả nâng cao)
        is_leisure = ((preferred_hour >= 10) & (preferred_hour <= 15)) | (preferred_hour >= 20)
        is_urban_leisure = (is_urban == 1) & is_leisure

        # Base multiplier: Nhóm Urban Leisure rất co giãn với Voucher
        ate_multiplier = np.where(is_urban_leisure, 2.5/self.true_ate, 1.0)
        
        # Bổ sung Luật Cản trở (Blockers) từ Phase 2:
        # Khách Sân bay có cầu cứng (Inelastic), không cần mã giảm giá vẫn đi => ATE = 0
        ate_multiplier = np.where(is_airport_trip == 1, 0.0, ate_multiplier)
        # Khách Tiền mặt mù công nghệ, không biết xài Voucher => ATE cực thấp
        ate_multiplier = np.where(payment_type == 2, 0.1, ate_multiplier)
        # Khách Đi mưa lúc đó giá Surge Pricing x3 x4, Voucher 25% không thấm tháp gì => ATE giảm một nửa
        ate_multiplier = np.where(is_rain_rider == 1, ate_multiplier * 0.5, ate_multiplier)
        
        # Bổ sung Lực đẩy (Accelerators):
        # Khách Cuối tuần cực kỳ co giãn, đi nhậu đi chơi siêu nhiều nếu có mã => ATE x1.5
        ate_multiplier = np.where((is_weekend_rider == 1) & (is_airport_trip == 0), ate_multiplier * 1.5, ate_multiplier)

        treatment_effect = self.true_ate * ate_multiplier
        y1_rides = y0_rides + treatment_effect

        y_rand = np.where(t_rand == 1, y1_rides, y0_rides)

        # 7. Tính Toán Cước phí (Fare)
        avg_distance = np.where(is_urban == 1, np.random.normal(3.0, 1.0, self.n), np.random.normal(5.5, 2.0, self.n))
        avg_distance = np.clip(avg_distance, 0.5, 25)
        # Sân bay thường ở rất xa (Quãng đường dài, cước cao)
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

print("\n[1/3] DANG SINH DU LIEU PHA 2 VOI CAC BIEN NHIEU VI MO...")
df = AdvancedRideSharingDataGenerator().run()
df.to_csv('data/processed/phase2_data.csv', index=False)
print(f"Da tao {len(df):,} dong du lieu voi cac bien moi (Thoi tiet, Cuoi tuan, San bay, Tien mat).")

print("\n[2/3] DANG CHAY LAI K-MEANS CLUSTERING (TIM PERSONAS NGACH)...")
features = ['is_urban', 'monthly_rides_history', 'preferred_hour', 'recency_days', 
            'is_weekend_rider', 'is_rain_rider', 'is_airport_trip', 'payment_type', 'passenger_count']
X = df[features]
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Nâng số cụm lên 5 để đón bắt các tệp khách hàng đặc thù
kmeans = KMeans(n_clusters=5, random_state=42, n_init=10)
df['cluster_id'] = kmeans.fit_predict(X_scaled)

centroids = pd.DataFrame(scaler.inverse_transform(kmeans.cluster_centers_), columns=features)

def auto_label(row):
    if row['is_airport_trip'] > 0.4: return 'Airport Business'
    if row['payment_type'] > 1.5: return 'Cash Traditional'
    if row['is_weekend_rider'] > 0.6 and row['is_urban'] > 0.5: return 'Urban Weekend Party'
    if row['is_urban'] > 0.5: return 'Urban Regulars'
    return 'Suburban Occasionals'

persona_map = {i: auto_label(row) for i, row in centroids.iterrows()}
df['persona'] = df['cluster_id'].map(persona_map)
df.to_csv('data/processed/phase2_segmented_data.csv', index=False)
print("\nPersonas moi duoc K-Means tim thay:")
print(df['persona'].value_counts())

print("\n" + "="*60)
print("PHAN TICH ROI DE VACH TRAN BAY LOI NHUAN (CANNIBALIZATION)")
print("="*60)

for target_persona in df['persona'].unique():
    print(f"\n--- NHOM: {target_persona.upper()} ---")
    df_target = df[df['persona'] == target_persona].copy()
    
    if len(df_target) < 100:
        continue

    control = df_target[df_target['treatment_rand'] == 0]['y_rand']
    treatment = df_target[df_target['treatment_rand'] == 1]['y_rand']
    
    mean_control = control.mean()
    mean_treatment = treatment.mean()
    ate = mean_treatment - mean_control
    
    print(f"- Base Rides (So chuyen tu nhien): {mean_control:.2f}")
    print(f"- Incremental Rides (Hieu ung ATE): +{ate:.2f} chuyen/user")
    
    control_fare = df_target[df_target['treatment_rand'] == 0]['fare_rand']
    treatment_fare = df_target[df_target['treatment_rand'] == 1]['fare_rand']
    
    incremental_gross = treatment_fare.mean() - control_fare.mean()
    voucher_cost = treatment_fare.mean() * 0.25 
    incremental_net = incremental_gross - voucher_cost
    roi = incremental_net / voucher_cost if voucher_cost > 0 else 0

    print(f"- Tac dong Loi nhuan Rong: ${incremental_net:.2f}/user")
    
    if roi < 0:
        print(f"- Ty suat Dau tu (ROI): {roi*100:.1f}% (Bao dong Do: Lo Nang)")
    elif roi < 0.5:
        print(f"- Ty suat Dau tu (ROI): {roi*100:.1f}% (Chap nhan duoc)")
    else:
        print(f"- Ty suat Dau tu (ROI): {roi*100:.1f}% (Mo Vang)")
    print("-" * 30)

print("\nHOAN THANH PHASE 2!")
