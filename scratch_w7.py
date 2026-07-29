import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from xgboost import XGBRegressor
from sklearn.model_selection import train_test_split

plt.style.use('ggplot')
sns.set_palette("Set2")
import warnings
warnings.filterwarnings('ignore')

df = pd.read_csv('../../data/processed/segmented_simulation_data.csv')

# Chọn nhóm khách hàng cần tối ưu (ví dụ: Urban Cash đang bị lỗ do Sure Things quá nhiều)
target_persona = 'Urban Cash'
df_target = df[df['persona'] == target_persona].copy()

# Các biến Features (Covariates)
features = ['age', 'is_urban', 'fare_obs', 'preferred_hour', 
            'is_rush_hour', 'is_airport_trip', 'is_rain_rider', 
            'is_weekend_rider', 'is_credit_card', 'is_frequent_tipper', 
            'avg_trip_distance', 'typical_passenger_count', 
            'monthly_rides_history', 'recency_days']

X = df_target[features]
T = df_target['treatment_rand'] # Biến can thiệp (Voucher ngẫu nhiên)
y = df_target['y_rand']         # Outcome (Số chuyến đi)

X_train, X_test, T_train, T_test, y_train, y_test = train_test_split(
    X, T, y, test_size=0.3, random_state=42
)

print(f"Kích thước tập Train: {len(X_train)}")
print(f"Kích thước tập Test: {len(X_test)}")

# Lọc dữ liệu Train theo nhóm Treatment và Control
X_train_0 = X_train[T_train == 0]
y_train_0 = y_train[T_train == 0]

X_train_1 = X_train[T_train == 1]
y_train_1 = y_train[T_train == 1]

# Khởi tạo 2 mô hình XGBoost
model_0 = XGBRegressor(n_estimators=100, max_depth=3, learning_rate=0.1, random_state=42)
model_1 = XGBRegressor(n_estimators=100, max_depth=3, learning_rate=0.1, random_state=42)

# Huấn luyện
model_0.fit(X_train_0, y_train_0)
model_1.fit(X_train_1, y_train_1)

print("✅ Đã huấn luyện xong 2 mô hình XGBoost cho T-Learner.")

# Dự đoán trên tập Test
pred_0 = model_0.predict(X_test)
pred_1 = model_1.predict(X_test)

# Tính CATE (Uplift Score)
cate_pred = pred_1 - pred_0

df_res = pd.DataFrame({
    'y_true': y_test,
    'T': T_test,
    'pred_0': pred_0,
    'pred_1': pred_1,
    'CATE_pred': cate_pred
})

plt.figure(figsize=(10, 5))
sns.histplot(df_res['CATE_pred'], bins=30, kde=True, color='teal')
plt.title('Phân phối Uplift Score (CATE) trên tập Test')
plt.xlabel('Số chuyến đi tăng thêm nhờ Voucher')
plt.ylabel('Số lượng KH')
plt.axvline(x=0, color='red', linestyle='--')
plt.show()

print("Nhận xét: Có khách hàng CATE > 0 (Tăng chuyến), nhưng cũng có người CATE < 0 hoặc = 0 (Không đổi hoặc giảm).")

profit_per_ride = 20000
voucher_cost = 15000

df_res['Expected_Profit'] = (df_res['CATE_pred'] * profit_per_ride) - voucher_cost

# Quyết định phát Voucher (Policy)
df_res['Action'] = np.where(df_res['Expected_Profit'] > 0, 'Send Voucher', 'No Voucher')

print(df_res['Action'].value_counts())

action_counts = df_res['Action'].value_counts()
plt.figure(figsize=(6, 6))
plt.pie(action_counts, labels=action_counts.index, autopct='%1.1f%%', colors=['#ff9999','#66b3ff'])
plt.title('Tỷ lệ phát Voucher theo Mô hình T-Learner')
plt.show()

# Tính toán lợi nhuận thực tế trên tập Test để đánh giá (nếu áp dụng chiến lược)
# Để đơn giản, ta tính Lợi nhuận = T_test * (y_test * 20k - 15k) 

df_res = df_res.sort_values(by='CATE_pred', ascending=False).reset_index(drop=True)

df_res['Actual_Profit'] = np.where(df_res['T'] == 1, (df_res['y_true'] * profit_per_ride) - voucher_cost, df_res['y_true'] * profit_per_ride)
df_res['Control_Profit'] = np.where(df_res['T'] == 0, df_res['y_true'] * profit_per_ride, 0)

print("T-Learner Pipeline Hoàn Tất!")

