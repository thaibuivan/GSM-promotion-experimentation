import os
import numpy as np
import pandas as pd
from scipy.stats import nbinom as NB, ttest_ind
from scipy.optimize import brentq
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from xgboost import XGBRegressor
import warnings
warnings.filterwarnings('ignore')

# ============================================================
# CONSTANTS
# ============================================================
N_USERS        = 20000
SEED           = 42

# --- Y0 Baseline (Negative Binomial) ---
BASELINE_MEAN  = 8.0   # E[Y0] muc tieu: 8 chuyen / 30 ngay
NB_DISPERSION  = 4.0   # Dispersion r cua NB; nho -> duoi day hon
ZERO_TARGET    = 0.20  # Ty le rider ngu dong (Y0 = 0)
WAKE_RATE      = 0.25  # Voucher danh thuc 25% nguoi ngu dong

# --- Y0 baseline conditional log-linear weights ---
B_HISTORY = 0.35   # Rider co lich su di nhieu -> Y0 cao
B_URBAN   = 0.20   # Rider noi thanh -> Y0 cao hon
B_RECENCY = -0.10  # Lau khong dung App -> Y0 thap hon

# --- ITE / CATE (Tac dong ca nhan cua Voucher) ---
TAU_BASE      = 1.5    # Tac dong co ban
D_LEISURE     = 1.2    # Urban leisure (thoi gian ranh) -> de kich cau
D_SUBURBAN    = 0.8    # Ngoai o -> nhay cam gia, de kich cau
D_RAIN        = 0.4    # Mua -> tang nhe
P_AIRPORT     = 1.5    # San bay -> voucher gan nhu vo dung (tru)
P_RUSH        = 0.8    # Gio cao diem -> phai di lam, khong can voucher (tru)
P_CASH        = 0.9    # Tra tien mat -> it nhay cam voucher (tru)
TAU_NOISE     = 0.3

# --- Observational Confounding ---
TARGETING = {"history": 0.85, "urban": 0.60, "recency": 0.40}

# --- Fare / Unit Economics ---
# avg_fare_per_trip ~ LogNormal(mu, sigma) theo nhom
FARE_URBAN_MU     = 2.7    # exp(2.7) ~ 14.9 USD/trip
FARE_URBAN_SIGMA  = 0.45
FARE_SUBURB_MU    = 3.1    # exp(3.1) ~ 22.2 USD/trip
FARE_SUBURB_SIGMA = 0.55
FARE_AIRPORT_MU   = 4.0    # exp(4.0) ~ 54.6 USD/trip
FARE_AIRPORT_SIGMA= 0.3

import json
try:
    with open(os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), 'config.json'), 'r') as f:
        _cfg = json.load(f)
    VOUCHER_DISCOUNT_RATE = _cfg['economics'].get('voucher_rate', 0.15)
except:
    VOUCHER_DISCOUNT_RATE = 0.15

VOUCHER_CAP_PER_TRIP  = 3.0

# Demographics
AGE_MEAN    = 30
AGE_STD     = 8
URBAN_RATIO = 0.60
HOUR_DEMAND_MULTIPLIER = [
    0.3, 0.2, 0.2, 0.15, 0.15, 0.2,
    0.5, 1.0, 1.5, 1.5,
    1.0, 0.8, 0.7, 0.7,
    0.8, 0.9, 1.0, 1.5, 1.5,
    1.3, 1.2, 1.0, 0.8, 0.5
]


# ============================================================
# HELPER: Zero-Inflated Negative Binomial draw
# ============================================================
def _zinb_draw(mu, pi_zero, dispersion, rng, size=None):
    """Sinh so nguyen duong theo Zero-Inflated Negative Binomial.
    mu co the la scalar hoac array. Neu la scalar, can truyen size.
    """
    mu_arr = np.broadcast_to(np.asarray(mu, float), (size,) if size is not None else np.asarray(mu, float).shape)
    p = dispersion / (dispersion + mu_arr)
    y = NB.rvs(dispersion, p, random_state=rng.integers(int(1e9)))
    n = len(np.atleast_1d(y))
    return np.where(rng.random(n) < pi_zero, 0, y).astype(np.int32)


# ============================================================
# HELPER: Z-score chuan hoa
# ============================================================
def _zs(x):
    x = np.asarray(x, float)
    s = x.std()
    return (x - x.mean()) / s if s > 0 else np.zeros_like(x)


# ============================================================
# MAIN PIPELINE
# ============================================================
def run_pipeline(n_users=N_USERS, progress_callback=None):
    np.random.seed(SEED)
    rng = np.random.default_rng(SEED)

    if progress_callback: progress_callback(10, "Dang sinh du lieu Nhan khau hoc (Demographics)...")

    # ----------------------------------------------------------
    # BLOCK 1: Demographics
    # ----------------------------------------------------------
    is_urban         = rng.binomial(1, URBAN_RATIO, n_users)

    # [FIX 1] age: Noi thanh tre hon (mean=28), ngoai o lon hon (mean=34)
    # Dung Shifted Gamma distribution (Base=18) de fix loi Spike o moc 18 tuoi
    # Gamma mean can cong them: Noi thanh = 28-18=10, Ngoai o = 34-18=16
    gamma_mean = np.where(is_urban == 1, 10, 16).astype(float)
    age_shape = 5.0  # Chon shape=5 de do thi thoai hon 
    age_scale = gamma_mean / age_shape
    age = 18 + rng.gamma(shape=age_shape, scale=age_scale)
    age = np.clip(age, 18, 70).astype(int)

    is_weekend_rider = rng.binomial(1, 0.30, n_users)

    # [FIX 2] is_rain_rider: Noi thanh hay goi xe luc mua (22%) hon ngoai o (8%)
    # Vi noi thanh khong co cho tru mua, kho di xe may
    prob_rain    = np.where(is_urban == 1, 0.22, 0.08)
    is_rain_rider = rng.binomial(1, prob_rain)

    prob_airport     = np.where(is_urban == 1, 0.08, 0.02)
    is_airport_trip  = rng.binomial(1, prob_airport)

    # [FIX 3] payment_type: Noi thanh + tre tuoi -> dung the/vi dien tu nhieu hon
    # Noi thanh: 90% the, Ngoai o: 65% the; Nguoi tre (< 35) tang them 5%
    prob_card    = np.where(is_urban == 1, 0.90, 0.65)
    prob_card    = np.clip(prob_card + np.where(age < 35, 0.05, -0.05), 0.5, 0.98)
    payment_type = (rng.random(n_users) < prob_card).astype(int) + 1  # 1=Card, 2=Cash

    # [FIX 4] passenger_count: Gio cao diem -> di mot minh; Cuoi tuan -> di nhom
    # Base: [70%, 20%, 8%, 2%] nhung dieu chinh theo context
    p_solo    = np.clip(0.70 + 0.15 * is_rush_hour if 'is_rush_hour' in dir() else np.full(n_users, 0.70), 0.5, 0.90)
    passenger_count = np.ones(n_users, dtype=int)  # Default: di mot minh
    # Sinh ngau nhien cho nhung nguoi khong di mot minh
    not_solo_mask = rng.random(n_users) >= 0.70
    passenger_count[not_solo_mask] = rng.choice([2, 3, 4], size=not_solo_mask.sum(), p=[0.70, 0.25, 0.05])

    hour_weights   = np.array(HOUR_DEMAND_MULTIPLIER)
    hour_probs     = hour_weights / hour_weights.sum()
    preferred_hour = rng.choice(range(24), size=n_users, p=hour_probs)

    # [FIX 4.5] Lich su cuoc xe: Nâng cấp tương quan nhân quả
    # - Tỷ lệ ngủ đông (pi_zero) phụ thuộc Nội thành (10%) / Ngoại ô (35%)
    # - Số cuốc xe (mu) phụ thuộc Nội thành (+2) và Dùng thẻ (+1.5)
    pi_zero_history = np.where(is_urban == 1, 0.10, 0.35)
    mu_history = 3.0 + 2.0 * is_urban + 1.5 * (payment_type == 1).astype(int)
    monthly_rides_history = _zinb_draw(mu=mu_history, pi_zero=pi_zero_history, dispersion=4.0, rng=rng, size=n_users)

    # Recency (Poisson, don vi ngay) - Conditional tren is_urban
    recency_mean = np.where(is_urban == 1, 4, 12)
    recency_days = np.clip(rng.poisson(lam=recency_mean), 0, 90).astype(int)

    # Derived behavior flags
    is_rush_hour     = np.isin(preferred_hour, [7, 8, 9, 17, 18, 19]).astype(int)
    is_leisure       = (((preferred_hour >= 10) & (preferred_hour <= 15)) | (preferred_hour >= 20)).astype(int)
    is_urban_leisure = ((is_urban == 1) & (is_leisure == 1)).astype(int)

    # [FIX 4 complete] Ap dung is_rush_hour vao passenger_count
    # Gio cao diem: tang xac suat di mot minh them 15%
    solo_upgrade = (rng.random(n_users) < 0.15 * is_rush_hour)
    passenger_count = np.where(solo_upgrade, 1, passenger_count)

    if progress_callback: progress_callback(30, "Dang sinh Y0 (Potential Outcome khi khong co Voucher)...")

    # ----------------------------------------------------------
    # BLOCK 2: Potential Outcome Y0 --- Zero-Inflated Negative Binomial
    # Yeu cau ky thuat: dung ZINB de mo phong duoi dai va ngu dong, calibrate E[Y0] ~ BASELINE_MEAN
    # ----------------------------------------------------------
    z_history = _zs(np.log1p(monthly_rides_history))
    z_urban   = _zs(is_urban)
    z_recency = _zs(recency_days)

    # mu0: Muc ky vong tu nhien cua Y0 theo dac diem ca nhan
    mu0 = BASELINE_MEAN * np.exp(
        B_HISTORY * z_history
        + B_URBAN   * z_urban
        + B_RECENCY * z_recency
    )

    # [FIX 5] lin0: Them recency_days vao mo hinh ngu dong
    # Nguoi lau khong dung App (recency cao) -> xac suat ngu dong TANG manh
    # Phan tich kinh doanh: recency la predictor manh nhat cua churn, can dua vao dormancy model
    lin0 = -(0.90 * z_history + 0.30 * z_urban - 0.50 * z_recency)

    def _p_zero(c):
        pi    = 1 / (1 + np.exp(-(c + lin0)))
        p_nb0 = (NB_DISPERSION / (NB_DISPERSION + mu0)) ** NB_DISPERSION
        return (pi + (1 - pi) * p_nb0).mean()

    c0  = brentq(lambda c: _p_zero(c) - ZERO_TARGET, -20, 20)
    pi0 = 1 / (1 + np.exp(-(c0 + lin0)))   # Xac suat rider ngu dong (tu nhien)
    pi1 = pi0 * (1 - WAKE_RATE)            # Voucher danh thuc bot nguoi ngu dong

    Y0 = _zinb_draw(mu0, pi0, NB_DISPERSION, rng)

    if progress_callback: progress_callback(45, "Dang thiet lap CATE (Tac dong ca nhan cua Voucher)...")

    # ----------------------------------------------------------
    # BLOCK 3: Individual Treatment Effect (ITE / CATE)
    # Dinh nghia tau_true (CATE) la expected treatment effect: E[Y1 - Y0]
    # ----------------------------------------------------------
    # [FIX 6] TAU_NOISE ca nhan hoa theo tuoi:
    # Nguoi tre (18-30) nhanh nhay voi khuyen mai hon nguoi lon tuoi
    # age_sensitivity: 1.5 cho nguoi tre, giam dan xuong 0.5 cho nguoi gia
    age_norm        = (age - 18) / (60 - 18)          # Chuan hoa ve [0, 1]
    age_sensitivity = 1.5 - age_norm                   # 1.5 (tre) -> 0.5 (gia)
    # 1. Diminishing Returns (Khach di nhieu roi thi khong tang may)
    history_penalty = 1.0 / np.sqrt(monthly_rides_history + 1.0)
    
    # 2. Tuoi tac tuong tac voi Troi mua (Tre nhay cam hon voi voucher khi mua)
    rain_age_interaction = is_rain_rider * (age_sensitivity - 1.0)
    
    # 3. Ngoai o + Cuoi tuan -> Cực kỳ nhạy cảm
    suburban_leisure = (1 - is_urban) * is_weekend_rider
    
    # 4. Hieu ung Win-back: Bo app cang lau, voucher cang co tac dung
    recency_boost = np.log1p(recency_days) / 5.0 

    tau_raw = (
        TAU_BASE
        + D_LEISURE   * is_urban_leisure
        + D_SUBURBAN  * suburban_leisure    # Da tuong tac phi tuyen
        + D_RAIN      * rain_age_interaction # Da tuong tac phi tuyen
        - P_AIRPORT   * is_airport_trip
        - P_RUSH      * is_rush_hour
        - P_CASH      * (payment_type == 2).astype(int)
        + recency_boost                      # Insight moi
        + TAU_NOISE   * age_sensitivity * rng.standard_normal(n_users)
    )
    
    # Ap dung luat Hieu suat giam dan
    tau_raw = tau_raw * history_penalty
    tau_raw = np.clip(tau_raw, 0, None)

    # mu1 truoc khi calibrate
    mu1_raw = mu0 + tau_raw

    # cate_true (dang ky vong) truoc calibrate
    cate_raw = (1 - pi1) * mu1_raw - (1 - pi0) * mu0

    # Calibrate: dung brentq tim scale sao cho E[cate_true] = TARGET_ATE tren mau huu han
    TARGET_ATE = 0.8

    def _ate_at_scale(s):
        mu1_s     = mu0 + tau_raw * s
        cate_s    = (1 - pi1) * mu1_s - (1 - pi0) * mu0
        return cate_s.mean() - TARGET_ATE

    # Kiem tra xem ATE co the dat duoc khong (tau_raw > 0)
    if tau_raw.sum() > 0:
        scale_factor = brentq(_ate_at_scale, 0.01, 20.0)
    else:
        scale_factor = 1.0

    tau_calibrated = tau_raw * scale_factor
    mu1            = mu0 + tau_calibrated

    # cate_true sau calibrate: expected incremental rides (ly thuyet)
    # cate_true[i] = E[Y1_i] - E[Y0_i] = (1-pi1)*mu1 - (1-pi0)*mu0
    cate_true    = (1 - pi1) * mu1 - (1 - pi0) * mu0
    ATE_EXPECTED = cate_true.mean()  # Phai gan dung = 0.8

    # Sinh Y1 (realized potential outcome khi co Voucher)
    Y1 = np.maximum(_zinb_draw(mu1, pi1, NB_DISPERSION, rng), 0)

    # Realized ATE tren mau huu han (dung de khao sat hieu qua thuc te)
    ATE_REALIZED = (Y1 - Y0).mean()


    if progress_callback: progress_callback(55, "Dang gan Treatment (RCT + Observational)...")

    # ----------------------------------------------------------
    # BLOCK 4: Treatment Assignment
    # ----------------------------------------------------------
    # 4a. T_rand: Stratified Randomization (fix SRM vinh vien)
    blk_rides   = pd.qcut(monthly_rides_history, 5, labels=False, duplicates='drop')
    blk_recency = pd.qcut(recency_days,          3, labels=False, duplicates='drop')
    block_id    = blk_rides.astype(str) + '_' + blk_recency.astype(str)

    t_rand = np.zeros(n_users, dtype=np.int8)
    for _, idx_g in pd.Series(block_id).groupby(block_id).groups.items():
        idx_arr = np.array(idx_g)
        k       = int(round(len(idx_arr) * 0.5))
        chosen  = rng.choice(idx_arr, k, replace=False)
        t_rand[chosen] = 1

    # 4b. T_obs: Observational (co confounding)
    # [FIX 7] Them age vao confounding: AI hay target nguoi tre (quen dung app, de bi khuyen mai)
    z_age   = _zs(age)
    lin_obs = (
        TARGETING["history"]  * z_history
        + TARGETING["urban"]  * z_urban
        - TARGETING["recency"]* z_recency   # Lau khong dung -> it duoc target
        - 0.40 * z_age                      # Nguoi gia -> it duoc he thong target hon
        - 1.5 * is_rush_hour                # Gio cao diem -> he thong tat voucher
        - 1.2 * is_rain_rider               # Mua -> tat voucher de bao ve margin
    ).astype(float)

    # Calibrate c1 sao cho tong T_obs xap xi tong T_rand
    n_treated = int(t_rand.sum())
    c1 = brentq(lambda c: (1 / (1 + np.exp(-(c + lin_obs)))).sum() - n_treated, -20, 20)
    propensity_true = 1 / (1 + np.exp(-(c1 + lin_obs)))
    t_obs = (rng.random(n_users) < propensity_true).astype(np.int8)

    # 4c. Observed outcomes
    Y_rand = np.where(t_rand == 1, Y1, Y0).astype(np.int32)
    Y_obs  = np.where(t_obs  == 1, Y1, Y0).astype(np.int32)

    if progress_callback: progress_callback(65, "Dang sinh Gia cuoc (Log-Normal Fare Distribution)...")

    # ----------------------------------------------------------
    # BLOCK 5: Unit Economics
    # avg_fare_per_trip ~ LogNormal (khac theo nhom)
    # ----------------------------------------------------------
    base_fare = np.where(
        is_airport_trip == 1,
        rng.lognormal(FARE_AIRPORT_MU, FARE_AIRPORT_SIGMA, n_users),
        np.where(
            is_urban == 1,
            rng.lognormal(FARE_URBAN_MU,  FARE_URBAN_SIGMA,  n_users),
            rng.lognormal(FARE_SUBURB_MU, FARE_SUBURB_SIGMA, n_users)
        )
    )
    # [FIX 8] Surge Pricing: Gio cao diem gia tang 1.4x (giong Grab/Gojek thuc te)
    # Nguon tham khao: Grab surge pricing 1.3x-1.8x trong peak hours
    surge_multiplier  = np.where(is_rush_hour == 1, 1.40, 1.0)
    avg_fare_per_trip = (base_fare * surge_multiplier).round(2)

    # Doanh thu thang (dung Y_rand cho nhanh RCT)
    gross_revenue_30d = (Y_rand * avg_fare_per_trip).round(2)

    # Chi phi voucher: giam 20%, cap 3 USD/chuyen, CHI ap dung cho T_rand=1
    discount_per_trip = np.minimum(avg_fare_per_trip * VOUCHER_DISCOUNT_RATE, VOUCHER_CAP_PER_TRIP)
    discount_cost_30d = (t_rand * Y_rand * discount_per_trip).round(2)

    # Doanh thu thuan
    try:
        MARGIN_RATE = _cfg['economics'].get('margin_rate', 0.70)
    except:
        MARGIN_RATE = 0.70
    net_contribution  = (gross_revenue_30d * MARGIN_RATE - discount_cost_30d).round(2)

    if progress_callback: progress_callback(75, "Dang huan luyen mo hinh K-Means 5 Cum...")

    # ----------------------------------------------------------
    # BLOCK 6: Build DataFrame + Segmentation
    # ----------------------------------------------------------
    persona = np.full(n_users, "Urban Regulars", dtype=object)
    
    # 1. Suburban Cash
    mask_sub_cash = (is_urban == 0) & (payment_type == 2)
    persona[mask_sub_cash] = "Suburban Cash"
    
    # 2. Suburban Card
    mask_sub_card = (is_urban == 0) & (payment_type == 1)
    persona[mask_sub_card] = "Suburban Card"
    
    # 3. Rain Riders
    mask_rain = (is_urban == 1) & (is_rain_rider == 1)
    persona[mask_rain] = "Rain Riders"
    
    # 4. Airport Business
    mask_airport = (is_urban == 1) & (is_airport_trip == 1) & ~mask_rain
    persona[mask_airport] = "Airport Business"
    
    df = pd.DataFrame({
        'persona'              : persona,
        'user_id'              : range(1, n_users + 1),
        'age'                  : age,
        'is_urban'             : is_urban,
        'is_weekend_rider'     : is_weekend_rider,
        'is_rain_rider'        : is_rain_rider,
        'is_airport_trip'      : is_airport_trip,
        'is_rush_hour'         : is_rush_hour,
        'payment_type'         : payment_type,
        'passenger_count'      : passenger_count,
        'monthly_rides_history': monthly_rides_history,
        'recency_days'         : recency_days,
        'preferred_hour'       : preferred_hour,
        # Potential Outcomes & Realized ITE
        'Y0'                   : Y0,
        'Y1'                   : Y1,
        'ite_realized'         : (Y1 - Y0),               # Realized ITE = Y1 - Y0 (God-mode ground truth)
        'cate_true'            : cate_true.round(4),       # Expected CATE = E[Y1-Y0 | X]
        # RCT branch
        'treatment_rand'       : t_rand,
        'Y_rand'               : Y_rand,
        # Observational branch
        'treatment_obs'        : t_obs,
        'propensity_true'      : propensity_true.round(6),
        'Y_obs'                : Y_obs,
        # Unit Economics
        'avg_fare_per_trip'    : avg_fare_per_trip,
        'gross_revenue_30d'    : gross_revenue_30d,
        'discount_cost_30d'    : discount_cost_30d,
        'net_contribution'     : net_contribution,
        # Legacy backward compat (Tuan 4 notebook dung y_obs, fare_rand)
        'y_obs'                : Y_rand,
        'fare_rand'            : gross_revenue_30d,
    })


    # ----------------------------------------------------------
    # BLOCK 7: T-Learner REMOVED
    # Ly do: (1) Data Leakage - model predict tren chinh data no da hoc
    #        (2) Trung lap voi Week 7 notebook - da co phan tich day du hon
    #        (3) Pipeline nen chi lam Data Generation, khong lam Modeling
    # cate_true da co san o Block 3 de dung lam Benchmark cho Week 7
    # ----------------------------------------------------------
    if progress_callback: progress_callback(88, "Hoan tat sinh du lieu, dang luu...")

    if progress_callback: progress_callback(96, "Dang luu du lieu vao Database...")

    # ----------------------------------------------------------
    # BLOCK 8: Save
    # ----------------------------------------------------------
    try:
        base_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    except NameError:
        # Neu chay trong Jupyter Notebook, __file__ khong ton tai
        # Jupyter hien tai dang o thư muc notebooks/week2_synthetic_data
        base_path = os.path.abspath(os.path.join(os.getcwd(), '..', '..'))
    save_dir  = os.path.join(base_path, 'data', 'processed')
    os.makedirs(save_dir, exist_ok=True)
    df.to_csv(os.path.join(save_dir, 'segmented_simulation_data.csv'), index=False)

    if progress_callback: progress_callback(100, "Hoan tat Toan bo Pipeline!")

    print("[DGP Summary]")
    print(f"  E[Y0]          = {Y0.mean():.3f}  (target: {BASELINE_MEAN})")
    print(f"  P(Y0=0)        = {(Y0==0).mean():.3f}  (target: {ZERO_TARGET})")
    print(f"  ATE expected   = {ATE_EXPECTED:.4f} (target: {TARGET_ATE})")
    print(f"  ATE realized   = {ATE_REALIZED:.4f} (realized Y1-Y0 mean)")
    print(f"  T_rand rate    = {t_rand.mean():.3f} (target: 0.500)")
    print(f"  T_obs rate     = {t_obs.mean():.3f}")
    print(f"  avg_fare       = {avg_fare_per_trip.mean():.2f} USD/trip")
    print(f"  avg_revenue    = {gross_revenue_30d.mean():.2f} USD/user-month")
    print(f"  avg_discount   = {discount_cost_30d[t_rand==1].mean():.2f} USD/user-month (treated only)")
    print(f"  avg_net_contr  = {net_contribution.mean():.2f} USD/user-month")

    return df


# ============================================================
# MONTE CARLO VALIDATION
# Cau hoi: "Estimator RCT co recover dung ATE = 0.8 khong?"
# Phuong phap: Dung Y0, Y1 co san, random lai assignment 500 lan.
# Khong can chay lai toan bo DGP -> nhanh va dung muc dich.
# ============================================================
def run_monte_carlo_validation(df, n_trials=500, seed=42):
    """
    Validate rang RCT estimator la unbiased va 95% CI coverage dung.

    Quy trinh:
        - Fixed: Y0, Y1 tu df (potential outcomes, God-mode ground truth)
        - Variable: Random treatment assignment moi trial
        - Estimator: Simple difference-in-means (Y_obs[T=1].mean - Y_obs[T=0].mean)

    Bao cao:
        - Bias         = mean(ATE_hat) - true_ATE   (tuong duong 0 neu unbiased)
        - SE           = std(ATE_hat) qua cac trial
        - Coverage     = P(true_ATE in 95% CI)       (ky vong ~0.95)
        - Power        = P(p-value < 0.05 | ATE > 0) (ky vong > 0.8)
    """
    rng_mc = np.random.default_rng(seed)
    n      = len(df)
    Y0     = df['Y0'].values
    Y1     = df['Y1'].values

    # True ATE: Finite-population realized ATE (dung Y1-Y0 thuc te, khong phai ky vong)
    # Ly do: MC dung fixed Y0, Y1 nen true_ate = mean(Y1-Y0) tren tap nay
    true_ate = df['ite_realized'].mean()

    ate_estimates = []
    ci_covered    = []
    p_values      = []

    for _ in range(n_trials):
        t      = rng_mc.binomial(1, 0.5, n)
        Y_obs  = np.where(t == 1, Y1, Y0)

        y1_grp = Y_obs[t == 1]
        y0_grp = Y_obs[t == 0]

        ate_est       = y1_grp.mean() - y0_grp.mean()
        _, p_val      = ttest_ind(y1_grp, y0_grp, equal_var=False)
        se            = np.sqrt(y1_grp.var() / len(y1_grp) + y0_grp.var() / len(y0_grp))
        ci_lo, ci_hi  = ate_est - 1.96 * se, ate_est + 1.96 * se

        ate_estimates.append(ate_est)
        ci_covered.append(int(ci_lo <= true_ate <= ci_hi))
        p_values.append(p_val)

    ate_estimates = np.array(ate_estimates)
    p_values      = np.array(p_values)
    bias          = ate_estimates.mean() - true_ate
    se_mc         = ate_estimates.std()

    results = {
        'n_trials'      : n_trials,
        'true_ate'      : round(true_ate, 4),
        'mean_ate_est'  : round(ate_estimates.mean(), 4),
        'bias'          : round(bias, 4),
        'bias_pct'      : round(abs(bias) / true_ate * 100, 2),
        'se'            : round(se_mc, 4),
        'rmse'          : round(np.sqrt(bias**2 + se_mc**2), 4),
        'coverage_95ci' : round(np.mean(ci_covered), 4),
        'power'         : round(np.mean(p_values < 0.05), 4),
        'ate_estimates' : ate_estimates,
        'p_values'      : p_values,
    }
    return results


def print_mc_summary(mc):
    """In ket qua Monte Carlo vao terminal."""
    print("\n[Monte Carlo Validation Summary]")
    print(f"  Trials           = {mc['n_trials']}")
    print(f"  True ATE         = {mc['true_ate']:.4f}")
    print(f"  Mean ATE Est.    = {mc['mean_ate_est']:.4f}")
    print(f"  Bias             = {mc['bias']:+.4f}  ({mc['bias_pct']:.2f}% of true ATE)")
    print(f"  SE               = {mc['se']:.4f}")
    print(f"  RMSE             = {mc['rmse']:.4f}")
    print(f"  95% CI Coverage  = {mc['coverage_95ci']:.3f}  (target: 0.950)")
    print(f"  Power (alpha=5%) = {mc['power']:.3f}  (target: > 0.80)")
    ok = all([
        abs(mc['bias_pct']) < 5,
        abs(mc['coverage_95ci'] - 0.95) < 0.05,
        mc['power'] > 0.80,
    ])
    print(f"  [{'PASS' if ok else 'WARN'}] Sanity check {'passed' if ok else 'needs review'}.")


if __name__ == "__main__":
    def _print_prog(pct, msg):
        print(f"[{pct}%] {msg}")
    df = run_pipeline(progress_callback=_print_prog)
    mc = run_monte_carlo_validation(df, n_trials=500)
    print_mc_summary(mc)
