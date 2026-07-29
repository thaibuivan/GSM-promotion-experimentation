import json

with open('notebooks/week7_uplift_modeling/1_uplift_modeling_tlearner.ipynb', 'r', encoding='utf-8') as f:
    nb = json.load(f)

# Update Cell 4 (Data Split)
cell_4_new = """df = pd.read_csv('../../data/processed/segmented_simulation_data.csv')

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

# Chia dữ liệu thành Train (60%), Validation (20%), Test (20%)
X_temp, X_test, T_temp, T_test, y_temp, y_test = train_test_split(
    X, T, y, test_size=0.2, random_state=42
)

X_train, X_val, T_train, T_val, y_train, y_val = train_test_split(
    X_temp, T_temp, y_temp, test_size=0.25, random_state=42
)

print(f"Kích thước tập Train (60%): {len(X_train)}")
print(f"Kích thước tập Validation (20%): {len(X_val)}")
print(f"Kích thước tập Test (20%): {len(X_test)}")
"""
nb['cells'][4]['source'] = [line + '\n' for line in cell_4_new.split('\n')]

# Update Cell 6 (Model Training)
cell_6_new = """# Lọc dữ liệu Train và Val theo nhóm Treatment và Control
X_train_0, y_train_0 = X_train[T_train == 0], y_train[T_train == 0]
X_train_1, y_train_1 = X_train[T_train == 1], y_train[T_train == 1]

X_val_0, y_val_0 = X_val[T_val == 0], y_val[T_val == 0]
X_val_1, y_val_1 = X_val[T_val == 1], y_val[T_val == 1]

# Khởi tạo 2 mô hình XGBoost
model_0 = XGBRegressor(n_estimators=100, max_depth=3, learning_rate=0.1, random_state=42)
model_1 = XGBRegressor(n_estimators=100, max_depth=3, learning_rate=0.1, random_state=42)

# Huấn luyện có sử dụng Early Stopping trên tập Validation để chống Overfitting
model_0.fit(X_train_0, y_train_0, eval_set=[(X_val_0, y_val_0)], early_stopping_rounds=10, verbose=False)
model_1.fit(X_train_1, y_train_1, eval_set=[(X_val_1, y_val_1)], early_stopping_rounds=10, verbose=False)

print("Hoàn tất quá trình huấn luyện mô hình XGBoost cho nhóm Control và Treatment (đã có Validation & Early Stopping).")
"""
nb['cells'][6]['source'] = [line + '\n' for line in cell_6_new.split('\n')]

with open('notebooks/week7_uplift_modeling/1_uplift_modeling_tlearner.ipynb', 'w', encoding='utf-8') as f:
    json.dump(nb, f, indent=1, ensure_ascii=False)
