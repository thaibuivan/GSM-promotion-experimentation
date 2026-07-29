import json

with open('notebooks/week7_uplift_modeling/1_uplift_modeling_tlearner.ipynb', 'r', encoding='utf-8') as f:
    nb = json.load(f)

# The cell to update is the training cell
for cell in nb['cells']:
    if cell['cell_type'] == 'code':
        source = "".join(cell['source'])
        if 'eval_set' in source:
            # Re-write the source code to fix the XGBoost API
            new_source = """# Lọc dữ liệu Train và Val theo nhóm Treatment và Control
X_train_0, y_train_0 = X_train[T_train == 0], y_train[T_train == 0]
X_train_1, y_train_1 = X_train[T_train == 1], y_train[T_train == 1]

X_val_0, y_val_0 = X_val[T_val == 0], y_val[T_val == 0]
X_val_1, y_val_1 = X_val[T_val == 1], y_val[T_val == 1]

# Khởi tạo 2 mô hình XGBoost (XGBoost API mới yêu cầu early_stopping_rounds nằm ở lúc khởi tạo)
model_0 = XGBRegressor(n_estimators=100, max_depth=3, learning_rate=0.1, random_state=42, early_stopping_rounds=10)
model_1 = XGBRegressor(n_estimators=100, max_depth=3, learning_rate=0.1, random_state=42, early_stopping_rounds=10)

# Huấn luyện có sử dụng Early Stopping trên tập Validation để chống Overfitting
model_0.fit(X_train_0, y_train_0, eval_set=[(X_val_0, y_val_0)], verbose=False)
model_1.fit(X_train_1, y_train_1, eval_set=[(X_val_1, y_val_1)], verbose=False)

print("Hoàn tất quá trình huấn luyện mô hình XGBoost cho nhóm Control và Treatment (đã có Validation & Early Stopping).")
"""
            cell['source'] = [line + '\n' for line in new_source.split('\n')][:-1]
            break

with open('notebooks/week7_uplift_modeling/1_uplift_modeling_tlearner.ipynb', 'w', encoding='utf-8') as f:
    json.dump(nb, f, indent=1, ensure_ascii=False)
