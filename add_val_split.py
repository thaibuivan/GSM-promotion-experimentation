import json

with open('notebooks/week7_uplift_modeling/1_uplift_modeling_tlearner.ipynb', 'r', encoding='utf-8') as f:
    nb = json.load(f)

# Find the cell that does the splitting
for cell in nb['cells']:
    if cell['cell_type'] == 'code':
        source = "".join(cell['source'])
        if 'train_test_split(' in source:
            new_source = """X_temp, X_test, T_temp, T_test, y_temp, y_test = train_test_split(
    X, T, y, test_size=0.2, random_state=42
)

# Chia tiếp tập Temp thành Train (75% của temp -> 60% tổng) và Val (25% của temp -> 20% tổng)
X_train, X_val, T_train, T_val, y_train, y_val = train_test_split(
    X_temp, T_temp, y_temp, test_size=0.25, random_state=42
)

print(f"Kích thước tập Train (60%): {len(X_train)}")
print(f"Kích thước tập Validation (20%): {len(X_val)}")
print(f"Kích thước tập Test (20%): {len(X_test)}")

# Lọc dữ liệu Train và Validation theo nhóm Treatment và Control
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
            # Replace lines from train_test_split to print("✅ Đã huấn luyện xong...")
            # Actually it's better to just reconstruct the cell source.
            
            # Find start and end indices of the old split and train block
            lines = cell['source']
            start_idx = -1
            end_idx = -1
            for i, line in enumerate(lines):
                if 'train_test_split(' in line:
                    start_idx = i
                if 'Hoàn tất quá trình huấn luyện' in line or 'Đã huấn luyện xong' in line:
                    end_idx = i
                    
            if start_idx != -1 and end_idx != -1:
                # Replace the block
                new_lines = [line + '\n' for line in new_source.split('\n')][:-1] # avoid extra newline
                cell['source'] = lines[:start_idx] + new_lines + lines[end_idx+1:]
            break

with open('notebooks/week7_uplift_modeling/1_uplift_modeling_tlearner.ipynb', 'w', encoding='utf-8') as f:
    json.dump(nb, f, indent=1, ensure_ascii=False)
