"""
Sprint 1B: 5-Policy Comparison Script
Compares 6 policies on the same test set and exports results for Streamlit dashboard.
"""
import pandas as pd
import numpy as np
import xgboost as xgb
from sklearn.model_selection import train_test_split
import os
import json

base_path = r"D:\Intern VSF\GSM-promotion-experimentation"
data_path = os.path.join(base_path, 'data', 'processed', 'segmented_simulation_data.csv')

print("=" * 60)
print("Sprint 1B: 5-Policy Comparison")
print("=" * 60)

# ─── 1. LOAD DATA ─────────────────────────────────────────
print("\n[1/5] Loading data...")
df = pd.read_csv(data_path)
print(f"  Total users: {len(df):,}")

# Economics parameters from config
config_path = os.path.join(base_path, 'config.json')
with open(config_path, 'r') as f:
    config = json.load(f)

VOUCHER_RATE = config['economics']['voucher_rate']
MARGIN_RATE  = config['economics']['margin_rate']
CAMPAIGN_BUDGET = config['economics']['budget_limit']

features = ['age', 'is_urban', 'preferred_hour', 'is_rush_hour', 'is_airport_trip',
            'is_rain_rider', 'is_weekend_rider', 'is_credit_card', 'passenger_count',
            'monthly_rides_history', 'recency_days']

X = df[features]
y = df['Y_rand']
T = df['treatment_rand']

X_tv, X_test, y_tv, y_test, T_tv, T_test = train_test_split(X, y, T, test_size=0.2, random_state=42)
X_train, X_val, y_train, y_val, T_train, T_val = train_test_split(X_tv, y_tv, T_tv, test_size=0.25, random_state=42)

test_idx = X_test.index
df_test = df.loc[test_idx].copy()
df_test['avg_fare'] = df_test['avg_fare_per_trip']

print(f"  Test set size: {len(df_test):,}")

# ─── 2. TRAIN X-LEARNER ───────────────────────────────────
print("\n[2/5] Training X-Learner...")
params = dict(random_state=42, min_child_weight=5, reg_lambda=1.0, n_estimators=200, learning_rate=0.05, max_depth=4)

m0 = xgb.XGBRegressor(**params)
m1 = xgb.XGBRegressor(**params)
m0.fit(X_train[T_train == 0], y_train[T_train == 0])
m1.fit(X_train[T_train == 1], y_train[T_train == 1])

pseudo0 = m1.predict(X_train[T_train == 0]) - y_train[T_train == 0]
pseudo1 = y_train[T_train == 1] - m0.predict(X_train[T_train == 1])

tau0 = xgb.XGBRegressor(**params); tau0.fit(X_train[T_train == 0], pseudo0)
tau1 = xgb.XGBRegressor(**params); tau1.fit(X_train[T_train == 1], pseudo1)

cate = 0.5 * tau0.predict(X_test) + 0.5 * tau1.predict(X_test)
pred1 = m1.predict(X_test)
print(f"  Mean predicted CATE: {cate.mean():.4f}")

# ─── 3. COMPUTE EXPECTED VALUE PER USER ───────────────────
print("\n[3/5] Computing Expected Incremental Value per user...")
df_test['cate_pred'] = cate
df_test['pred_rides_treated'] = pred1
df_test['voucher_cost'] = df_test['avg_fare'] * VOUCHER_RATE
df_test['margin_per_ride'] = df_test['avg_fare'] * MARGIN_RATE
# EV_i = CATE_i × margin_per_ride − pred_rides_treated × voucher_cost
df_test['expected_value'] = (df_test['cate_pred'] * df_test['margin_per_ride']) - \
                            (df_test['pred_rides_treated'] * df_test['voucher_cost'])

# Observed uplift on test set (for policy outcome evaluation)
# We use the actual Y_rand and treatment assignment in test set
# For each policy, "profit" = ATE_for_targeted × margin − voucher_cost_for_targeted
def evaluate_policy(target_mask, df_eval, label):
    targeted = df_eval[target_mask]
    not_targeted = df_eval[~target_mask]
    n_targeted = target_mask.sum()
    
    if n_targeted == 0:
        return {"Policy": label, "N_Targeted": 0, "Pct_Targeted": 0.0,
                "Expected_Incremental_Rides": 0, "Expected_GMV": 0, "Incremental_GMV": 0,
                "Burn": 0, "CPIR": 0, "Burn_per_GMV_pct": 0, "Burn_per_Inc_GMV_pct": 0,
                "Expected_Incremental_Profit": 0,
                "EV_Lower_95": 0, "EV_Upper_95": 0,
                "Est_ROI_pct": 0}

    # Among targeted: use model's expected value as proxy
    total_ev = targeted['expected_value'].sum()
    total_burn = (targeted['pred_rides_treated'] * targeted['voucher_cost']).sum()
    
    total_inc_rides = targeted['cate_pred'].sum()
    total_gmv = (targeted['pred_rides_treated'] * targeted['avg_fare']).sum()
    total_inc_gmv = (targeted['cate_pred'] * targeted['avg_fare']).sum()
    
    roi = (total_ev / total_burn * 100) if total_burn > 0 else 0
    cpir = (total_burn / total_inc_rides) if total_inc_rides > 0 else 0
    burn_per_gmv = (total_burn / total_gmv * 100) if total_gmv > 0 else 0
    burn_per_inc_gmv = (total_burn / total_inc_gmv * 100) if total_inc_gmv > 0 else 0
    
    if n_targeted > 1:
        std_ev = targeted['expected_value'].std()
        moe = 1.96 * std_ev * np.sqrt(n_targeted)
    else:
        moe = 0

    return {
        "Policy": label,
        "N_Targeted": int(n_targeted),
        "Pct_Targeted": round(n_targeted / len(df_eval) * 100, 1),
        "Expected_Incremental_Rides": round(total_inc_rides, 0),
        "Expected_GMV": round(total_gmv, 0),
        "Incremental_GMV": round(total_inc_gmv, 0),
        "Burn": round(total_burn, 0),
        "CPIR": round(cpir, 0),
        "Burn_per_GMV_pct": round(burn_per_gmv, 1),
        "Burn_per_Inc_GMV_pct": round(burn_per_inc_gmv, 1),
        "Expected_Incremental_Profit": round(total_ev, 0),
        "EV_Lower_95": round(total_ev - moe, 0),
        "EV_Upper_95": round(total_ev + moe, 0),
        "Est_ROI_pct": round(roi, 1)
    }

# ─── 4. DEFINE AND EVALUATE 6 POLICIES ────────────────────
print("\n[4/5] Evaluating 6 policies...")

results = []

# Policy 0: No Voucher
results.append({
    "Policy": "0. No Voucher",
    "N_Targeted": 0,
    "Pct_Targeted": 0.0,
    "Total_Voucher_Cost": 0,
    "Expected_Incremental_Profit": 0,
    "EV_Lower_95": 0,
    "EV_Upper_95": 0,
    "Est_ROI_pct": 0.0
})

# Policy 1: Mass Voucher (all users)
mass_mask = pd.Series([True] * len(df_test), index=df_test.index)
results.append(evaluate_policy(mass_mask, df_test, "1. Mass Voucher (All Users)"))

# Policy 2: Segment Targeting (Suburban personas from K-Means)
suburban_mask = df_test['persona'].str.contains('Suburban', case=False, na=False)
results.append(evaluate_policy(suburban_mask, df_test, "2. Segment Targeting (Suburban)"))

# Policy 3: Uplift Targeting (Top 30% by predicted CATE)
cate_threshold = df_test['cate_pred'].quantile(0.70)
uplift_mask = df_test['cate_pred'] >= cate_threshold
results.append(evaluate_policy(uplift_mask, df_test, "3. Uplift Targeting (Top 30% CATE)"))

# Policy 4: Profit Targeting (EV > 0)
profit_mask = df_test['expected_value'] > 0
results.append(evaluate_policy(profit_mask, df_test, "4. Profit Targeting (EV > 0)"))

# Policy 5: Budget-Constrained Profit Targeting
df_sorted_ev = df_test.sort_values('expected_value', ascending=False).copy()
df_sorted_ev['cumulative_cost'] = (df_sorted_ev['pred_rides_treated'] * df_sorted_ev['voucher_cost']).cumsum()
budget_mask_idx = df_sorted_ev[df_sorted_ev['cumulative_cost'] <= CAMPAIGN_BUDGET].index
budget_mask = df_test.index.isin(budget_mask_idx)
results.append(evaluate_policy(budget_mask, df_test, f"5. Budget-Constrained (${CAMPAIGN_BUDGET:,})"))

# Oracle Policy (using true_ite if available)
if 'true_ite' in df_test.columns:
    df_test['oracle_ev'] = (df_test['true_ite'] * df_test['margin_per_ride']) - \
                           (df_test['pred_rides_treated'] * df_test['voucher_cost'])
    oracle_mask = df_test['oracle_ev'] > 0
    oracle_ev = df_test[oracle_mask]['oracle_ev'].sum()
    oracle_cost = (df_test[oracle_mask]['pred_rides_treated'] * df_test[oracle_mask]['voucher_cost']).sum()
    oracle_roi = (oracle_ev / oracle_cost * 100) if oracle_cost > 0 else 0
    
    n_oracle = oracle_mask.sum()
    if n_oracle > 1:
        oracle_std = df_test[oracle_mask]['oracle_ev'].std()
        oracle_moe = 1.96 * oracle_std * np.sqrt(n_oracle)
    else:
        oracle_moe = 0

    results.append({
        "Policy": "6. Oracle Policy (True ITE — Sandbox only)",
        "N_Targeted": int(n_oracle),
        "Pct_Targeted": round(n_oracle / len(df_test) * 100, 1),
        "Total_Voucher_Cost": round(oracle_cost, 0),
        "Expected_Incremental_Profit": round(oracle_ev, 0),
        "EV_Lower_95": round(oracle_ev - oracle_moe, 0),
        "EV_Upper_95": round(oracle_ev + oracle_moe, 0),
        "Est_ROI_pct": round(oracle_roi, 1)
    })

    # Compute Regret
    profit_policy_ev = df_test[profit_mask]['expected_value'].sum()
    regret = oracle_ev - profit_policy_ev
    regret_pct = (regret / oracle_ev * 100) if oracle_ev > 0 else 0
    print(f"\n  Oracle Profit: ${oracle_ev:,.0f}")
    print(f"  Profit Targeting: ${profit_policy_ev:,.0f}")
    print(f"  Regret: ${regret:,.0f} ({regret_pct:.1f}% of oracle)")

# ─── 5. SAVE RESULTS ──────────────────────────────────────
print("\n[5/5] Saving results...")
policy_df = pd.DataFrame(results)
print("\n" + policy_df.to_string(index=False))

out_path = os.path.join(base_path, 'data', 'processed', 'policy_comparison.csv')
policy_df.to_csv(out_path, index=False)

# Save user-level predictions for interactive Streamlit simulator
cols_to_save = ['persona', 'avg_fare', 'cate_pred', 'pred_rides_treated', 'Y_rand', 'treatment_rand']
if 'true_ite' in df_test.columns:
    cols_to_save.append('true_ite')
df_test_preds = df_test[cols_to_save].copy()
preds_path = os.path.join(base_path, 'data', 'processed', 'test_predictions.csv')
df_test_preds.to_csv(preds_path, index=False)
print(f"  User-level predictions saved to: test_predictions.csv")

# Compute and save Uplift Calibration (Deciles)
df_calib = df_test.copy()
df_calib['decile'] = pd.qcut(df_calib['cate_pred'], q=10, labels=False, duplicates='drop')
# Reverse decile so Decile 1 is the highest CATE
df_calib['decile'] = 9 - df_calib['decile'] + 1 

calib_results = []
for d in sorted(df_calib['decile'].unique()):
    subset = df_calib[df_calib['decile'] == d]
    t = subset[subset['treatment_rand'] == 1]
    c = subset[subset['treatment_rand'] == 0]
    obs_uplift = t['Y_rand'].mean() - c['Y_rand'].mean()
    true_uplift = subset['true_ite'].mean() if 'true_ite' in subset.columns else None
    pred_uplift = subset['cate_pred'].mean()
    
    calib_results.append({
        'Decile': d,
        'Predicted_CATE': pred_uplift,
        'Observed_Uplift': obs_uplift,
        'True_ITE': true_uplift
    })

calib_df = pd.DataFrame(calib_results)
calib_path = os.path.join(base_path, 'data', 'processed', 'uplift_calibration.csv')
calib_df.to_csv(calib_path, index=False)
print(f"  Calibration data saved to: uplift_calibration.csv")

# Save regret info if oracle is available
if 'true_ite' in df_test.columns:
    regret_info = {
        "oracle_profit": round(oracle_ev, 0),
        "profit_targeting_profit": round(profit_policy_ev, 0),
        "regret_abs": round(regret, 0),
        "regret_pct": round(regret_pct, 1)
    }
    regret_path = os.path.join(base_path, 'data', 'processed', 'oracle_regret.json')
    with open(regret_path, 'w') as f:
        json.dump(regret_info, f)
    print(f"\n  Oracle Regret saved to: oracle_regret.json")

print(f"\n  Policy comparison saved to: {out_path}")
print("\n" + "=" * 60)
print("Sprint 1B/2A: Export complete!")
print("=" * 60)
