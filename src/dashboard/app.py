import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
import os
import json
import statsmodels.api as sm
from scipy.stats import binomtest

# Page Config
st.set_page_config(page_title="Khung thử nghiệm khuyến mãi", layout="wide")

# Custom CSS
st.markdown("""
<style>
    .stApp {
        background-color: #F6F8FB;
    }
    h1, h2, h3, h4, h5, h6 {
        color: #0F172A;
    }
    .stMarkdown .executive-title,
    .executive-title {
        color: #0F172A;
        font-weight: 800;
        font-size: 2.45rem !important;
        line-height: 1.18;
        margin-bottom: 6px;
    }
    [data-testid="metric-container"] {
        background-color: #F9FAFB;
        border: 1px solid #E5E7EB;
        border-radius: 8px;
        padding: 16px 18px;
        box-shadow: 0 6px 16px rgba(15, 23, 42, 0.05);
        min-height: 124px;
    }
    [data-testid="metric-container"] label,
    [data-testid="metric-container"] [data-testid="stMetricLabel"] {
        color: #334155;
        font-weight: 700;
    }
    [data-testid="stMetricValue"] {
        font-size: 2rem;
        font-weight: bold;
    }
    .kpi-card {
        background-color: #FFFFFF;
        border: 1px solid #E5E7EB;
        border-radius: 8px;
        padding: 16px 18px;
        box-shadow: 0 6px 16px rgba(15, 23, 42, 0.05);
        min-height: 138px;
    }
    .kpi-label {
        color: #334155;
        font-size: 0.86rem;
        font-weight: 750;
        line-height: 1.25;
        min-height: 42px;
    }
    .kpi-value {
        color: #0F172A;
        font-size: 2rem;
        font-weight: 850;
        line-height: 1.15;
        margin: 8px 0 10px;
    }
    .kpi-delta {
        display: inline-flex;
        align-items: center;
        border-radius: 999px;
        padding: 4px 8px;
        font-size: 0.78rem;
        font-weight: 700;
        line-height: 1.2;
        white-space: normal;
    }
    .kpi-delta.positive {
        background-color: #DCFCE7;
        color: #15803D;
    }
    .kpi-delta.negative {
        background-color: #FEE2E2;
        color: #B91C1C;
    }
    .block-container { padding-top: 3.5rem; }
    
    .stTabs [data-baseweb="tab-list"],
    div[data-testid="stTabs"] div[data-baseweb="tab-list"],
    div[role="tablist"] {
        gap: 8px;
        border-bottom: 1px solid rgba(15, 23, 42, 0.14);
        margin-bottom: 24px;
    }
    .stTabs [data-baseweb="tab"],
    div[data-testid="stTabs"] button[data-baseweb="tab"],
    button[role="tab"],
    div[role="tab"] {
        height: 66px !important;
        min-height: 66px !important;
        white-space: nowrap !important;
        background-color: transparent !important;
        border-radius: 4px 4px 0px 0px;
        padding: 16px 22px !important;
        font-size: 22px !important;
        font-weight: 800 !important;
    }
    .stTabs [data-baseweb="tab"] p,
    .stTabs [data-baseweb="tab"] div[data-testid="stMarkdownContainer"] p,
    div[data-testid="stTabs"] button[data-baseweb="tab"] p,
    div[data-testid="stTabs"] button[data-baseweb="tab"] div[data-testid="stMarkdownContainer"] p,
    button[role="tab"] *,
    div[role="tab"] * {
        font-size: 22px !important;
        font-weight: 800 !important;
        line-height: 1.15 !important;
    }
    .stTabs [data-baseweb="tab"][aria-selected="true"],
    div[data-testid="stTabs"] button[data-baseweb="tab"][aria-selected="true"],
    button[role="tab"][aria-selected="true"],
    div[role="tab"][aria-selected="true"] {
        color: #0EA5A4 !important;
        background-color: rgba(14, 165, 164, 0.10) !important;
        border-bottom: 4px solid #0EA5A4 !important;
    }
    div[data-testid="stTabs"] button[data-baseweb="tab"][aria-selected="true"] p,
    button[role="tab"][aria-selected="true"] *,
    div[role="tab"][aria-selected="true"] * {
        color: #0EA5A4 !important;
    }
    
    .roadmap-card {
        padding: 20px;
        border-radius: 8px;
        background-color: #FFFFFF;
        border: 1px solid #D8E2EA;
        box-shadow: 0 8px 22px rgba(15, 23, 42, 0.06);
        text-align: center;
        height: 100%;
    }
    .roadmap-title {
        font-size: 1.2rem;
        font-weight: 700;
        color: #0EA5A4;
        margin-bottom: 5px;
    }
    .roadmap-subtitle {
        font-size: 1rem;
        font-weight: 600;
        color: #64748B;
        margin-bottom: 10px;
    }
    
    .flow-card {
        padding: 10px 20px;
        border-radius: 6px;
        background-color: #FFFFFF;
        border: 1px solid #D8E2EA;
        border-left: 4px solid #0EA5A4;
        box-shadow: 0 8px 22px rgba(15, 23, 42, 0.06);
        margin-bottom: 15px;
    }
</style>
""", unsafe_allow_html=True)

st.markdown('<p class="executive-title">Framework hỗ trợ quyết định khuyến mãi dựa trên dữ liệu</p>', unsafe_allow_html=True)
st.info("Xây dựng quy trình end-to-end từ đo lường tác động voucher, xác định khách hàng có khả năng tạo giá trị tăng thêm, đến mô phỏng chính sách khuyến mãi phù hợp.")
st.caption("**Phạm vi:** Prototype trên synthetic sandbox nhằm kiểm chứng phương pháp; chưa đại diện cho chính sách vận hành thực tế.")

base_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
data_path = os.path.join(base_path, "data", "processed", "segmented_simulation_data.csv")
pred_path = os.path.join(base_path, 'data', 'processed', 'test_predictions.csv')

@st.cache_data
def load_data(path, file_signature):
    return pd.read_csv(path)

def get_file_signature(path):
    stat = os.stat(path)
    return f"{stat.st_size}:{stat.st_mtime_ns}"

try:
    df = load_data(data_path, get_file_signature(data_path))
    preds_df = load_data(pred_path, get_file_signature(pred_path))
except Exception as e:
    st.error(f"Không thể tải dữ liệu. Chi tiết lỗi: {str(e)}")
    st.stop()

chart_layout = dict(
    plot_bgcolor='rgba(255,255,255,0)', paper_bgcolor='rgba(255,255,255,0)',
    font=dict(color='#0F172A'), margin=dict(l=20, r=20, t=40, b=20)
)

config_path = os.path.join(base_path, 'config.json')
try:
    with open(config_path, 'r') as f:
        config = json.load(f)
    DISCOUNT_PERCENT = config['economics'].get('voucher_rate', 0.15) * 100
    MARGIN_PERCENT = config['economics'].get('margin_rate', 0.7) * 100
    VOUCHER_CAP = config['economics'].get('voucher_cap')
except:
    DISCOUNT_PERCENT = 15.0
    MARGIN_PERCENT = 70.0
    VOUCHER_CAP = None

df_treat = df[df['treatment_rand'] == 1]
df_ctrl = df[df['treatment_rand'] == 0]

def calc_cost(fare, rate_pct):
    raw_cost = fare * (rate_pct / 100.0)
    return raw_cost if VOUCHER_CAP is None else np.minimum(raw_cost, VOUCHER_CAP)

def render_kpi_card(label, value, delta, tone="positive"):
    st.markdown(
        f"""
        <div class="kpi-card">
            <div class="kpi-label">{label}</div>
            <div class="kpi-value">{value}</div>
            <div class="kpi-delta {tone}">{delta}</div>
        </div>
        """,
        unsafe_allow_html=True
    )

def trapezoid_area(y, x):
    if hasattr(np, 'trapezoid'):
        return np.trapezoid(y, x)
    return np.trapz(y, x)

def load_or_build_qini_curve():
    qini_path = os.path.join(base_path, 'data', 'processed', 'qini_curve.csv')
    if os.path.exists(qini_path):
        qini_df = pd.read_csv(qini_path)
        required_cols = {'pct_targeted', 'qini_uplift', 'random_uplift'}
        if required_cols.issubset(qini_df.columns):
            return qini_df

    if {'cate_pred', 'cate_true'}.issubset(preds_df.columns):
        qini_df = preds_df.sort_values('cate_pred', ascending=False).copy()
        qini_df['pct_targeted'] = np.arange(1, len(qini_df) + 1) / len(qini_df) * 100
        qini_df['qini_uplift'] = qini_df['cate_true'].cumsum()
        total_uplift = qini_df['cate_true'].sum()
        qini_df['random_uplift'] = qini_df['pct_targeted'] / 100 * total_uplift
        zero_row = pd.DataFrame([{'pct_targeted': 0.0, 'qini_uplift': 0.0, 'random_uplift': 0.0}])
        return pd.concat([zero_row, qini_df[['pct_targeted', 'qini_uplift', 'random_uplift']]], ignore_index=True)

    return None

def compute_qini_coef(qini_df):
    if qini_df is None or qini_df.empty:
        return np.nan
    area_model = trapezoid_area(qini_df['qini_uplift'], qini_df['pct_targeted'])
    area_random = trapezoid_area(qini_df['random_uplift'], qini_df['pct_targeted'])
    return (area_model - area_random) / abs(area_random) if abs(area_random) > 1e-9 else np.nan

@st.cache_data
def load_experiment_health():
    health_path = os.path.join(base_path, 'data', 'processed', 'experiment_health.json')
    if not os.path.exists(health_path):
        return None
    with open(health_path, 'r', encoding='utf-8') as f:
        return json.load(f)

@st.cache_data
def load_model_snapshot():
    snapshot_path = os.path.join(base_path, 'data', 'processed', 'model_snapshot_manifest.json')
    if not os.path.exists(snapshot_path):
        return None
    with open(snapshot_path, 'r', encoding='utf-8') as f:
        return json.load(f)

def load_uplift_model_comparison():
    return pd.DataFrame([
        {'Mô hình': 'R-Learner-style', 'Qini Coef': 0.188, 'Vai trò': 'Được chọn'},
        {'Mô hình': 'S-Learner', 'Qini Coef': 0.153, 'Vai trò': 'Benchmark'},
        {'Mô hình': 'DR-Learner', 'Qini Coef': 0.138, 'Vai trò': 'Challenger'},
        {'Mô hình': 'X-Learner', 'Qini Coef': 0.038, 'Vai trò': 'Benchmark'},
        {'Mô hình': 'T-Learner', 'Qini Coef': -0.320, 'Vai trò': 'Baseline'}
    ])

def render_model_evaluation():
    st.markdown("---")
    st.subheader("Đánh giá sâu model được chọn: Qini và calibration")
    model_snapshot = load_model_snapshot()
    if model_snapshot:
        st.caption(
            f"Qini curve, calibration và policy cùng dùng snapshot đã khóa trên "
            f"test set {model_snapshot['test_rows']:,} khách hàng (seed {model_snapshot['split_seed']})."
        )

    col_qini, col_calib = st.columns(2)
    with col_qini:
        st.markdown("#### Qini curve - ranking uplift")
        st.caption("Mô hình có đưa khách hàng phản ứng tốt lên đầu danh sách tốt hơn cách chọn ngẫu nhiên không?")
        qini_df = load_or_build_qini_curve()
        if qini_df is not None and not qini_df.empty:
            fig_qini = go.Figure()
            fig_qini.add_trace(go.Scatter(
                x=qini_df['pct_targeted'], y=qini_df['qini_uplift'], mode='lines',
                name='Mô hình', line=dict(color='#0EA5A4', width=3)
            ))
            fig_qini.add_trace(go.Scatter(
                x=qini_df['pct_targeted'], y=qini_df['random_uplift'], mode='lines',
                name='Mốc ngẫu nhiên', line=dict(color='rgba(15,23,42,0.30)', dash='dash', width=2)
            ))
            fig_qini.update_layout(
                **chart_layout, height=350,
                legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
            )
            fig_qini.update_xaxes(title="Tỷ lệ khách hàng được nhắm chọn (%)", dtick=10)
            fig_qini.update_yaxes(title="Số chuyến tăng thêm tích lũy (Qini)")
            st.plotly_chart(fig_qini, use_container_width=True)
        else:
            st.warning("Chưa có dữ liệu để vẽ đường Qini.")

    with col_calib:
        st.markdown("#### Calibration - độ lớn CATE")
        st.caption("CATE dự báo có gần với uplift quan sát theo từng nhóm thập phân vị không?")
        try:
            calib_df = pd.read_csv(os.path.join(base_path, 'data', 'processed', 'uplift_calibration.csv'))
            fig_cal = go.Figure()
            fig_cal.add_trace(go.Scatter(
                name='CATE dự báo', x=calib_df['Decile'], y=calib_df['Predicted_CATE'],
                mode='lines+markers', line=dict(color='#FF4B4B', width=3)
            ))
            fig_cal.add_trace(go.Scatter(
                name='Uplift quan sát', x=calib_df['Decile'], y=calib_df['Observed_Uplift'],
                mode='lines+markers', line=dict(color='#00CC96', width=2)
            ))
            fig_cal.add_trace(go.Scatter(
                name='CATE ground truth (synthetic)', x=calib_df['Decile'], y=calib_df['Ground_Truth_CATE'],
                mode='lines', line=dict(color='rgba(15,23,42,0.38)', dash='dash', width=2)
            ))
            fig_cal.update_layout(
                **chart_layout, height=350,
                legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
            )
            fig_cal.update_xaxes(title="Các nhóm thập phân vị (tốt nhất đến kém nhất)")
            fig_cal.update_yaxes(title="Uplift trung bình")
            st.plotly_chart(fig_cal, use_container_width=True)
        except (FileNotFoundError, KeyError, pd.errors.EmptyDataError):
            st.warning("Chưa có dữ liệu hiệu chỉnh.")

    st.info("**Qini kiểm tra khả năng ranking; calibration kiểm tra độ lớn CATE. Model có ranking signal hữu ích, nhưng magnitude vẫn cần theo dõi.**")

def standardized_mean_difference(treated, control):
    pooled_variance = (treated.var(ddof=1) + control.var(ddof=1)) / 2.0
    if pd.isna(pooled_variance) or pooled_variance <= 0:
        return 0.0
    return (treated.mean() - control.mean()) / np.sqrt(pooled_variance)

tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "1. Bài toán kinh doanh",
    "2. Bằng chứng nhân quả",
    "3. Ai nhạy với voucher?",
    "4. Mô phỏng chính sách",
    "5. Kiểm tra độ vững"
])

# ================= TAB 1: BUSINESS PROBLEM =================
with tab1:
    st.subheader("Phát voucher đại trà có tạo thêm lợi nhuận không?")
    st.markdown("Thay vì chỉ nhìn vào tỷ lệ mở ứng dụng hoặc số chuyến tăng, ta đánh giá trực tiếp **lợi nhuận tăng thêm** khi phát voucher đại trà theo các giả định của môi trường mô phỏng.")
    
    avg_trips_treat = df_treat['Y_rand'].mean()
    avg_trips_ctrl = df_ctrl['Y_rand'].mean()
    incremental_trips_per_user = avg_trips_treat - avg_trips_ctrl
    avg_rev_treat = df_treat['gross_revenue_30d'].mean()
    avg_rev_ctrl = df_ctrl['gross_revenue_30d'].mean()
    incremental_rev_per_user = avg_rev_treat - avg_rev_ctrl
    gross_profit_per_user = incremental_rev_per_user * (MARGIN_PERCENT / 100.0)
    cost_per_user = df_treat['discount_cost_30d'].mean()
    net_profit_per_user = gross_profit_per_user - cost_per_user
    overall_roi = (net_profit_per_user / cost_per_user) * 100 if cost_per_user > 0 else 0
    total_users = len(df)
    total_incremental_trips = incremental_trips_per_user * total_users
    total_incremental_revenue = incremental_rev_per_user * total_users
    total_voucher_cost = cost_per_user * total_users
    total_net_profit = net_profit_per_user * total_users

    population_label = f"{total_users:,}".replace(",", ".")
    st.caption(
        f"Quy mô ngoại suy: **{population_label} khách hàng trong 30 ngày** · "
        f"voucher **{DISCOUNT_PERCENT:.0f}% không cap**."
    )
    
    c1, c2, c3, c4, c5 = st.columns(5)
    with c1:
        render_kpi_card(
            "Chuyến xe tăng thêm (30 ngày)",
            f"{total_incremental_trips:,.0f}",
            f"↑ {total_incremental_trips:,.0f} so với không phát"
        )
    with c2:
        render_kpi_card(
            "Doanh thu tăng thêm (30 ngày)",
            f"${total_incremental_revenue:,.0f}",
            f"↑ ${total_incremental_revenue:,.0f} tăng thêm"
        )
    with c3:
        render_kpi_card(
            "Tổng chi phí voucher (30 ngày)",
            f"${total_voucher_cost:,.0f}",
            f"↑ ${total_voucher_cost:,.0f} chi phí",
            "negative"
        )
    with c4:
        net_delta = (
            f"↓ ${abs(total_net_profit):,.0f} so với không phát"
            if total_net_profit < 0 else
            f"↑ ${total_net_profit:,.0f} so với không phát"
        )
        render_kpi_card(
            "Lợi nhuận ròng (30 ngày)",
            f"${total_net_profit:,.0f}",
            net_delta,
            "negative" if total_net_profit < 0 else "positive"
        )
    with c5:
        render_kpi_card(
            "ROI tổng thể",
            f"{overall_roi:.1f}%",
            f"↓ {abs(overall_roi):.1f} điểm dưới hòa vốn" if overall_roi < 0 else f"↑ {overall_roi:.1f} điểm trên hòa vốn",
            "negative" if overall_roi < 0 else "positive"
        )

    col_chart1, col_chart2 = st.columns(2)
    with col_chart1:
        st.markdown("#### Cơ cấu lợi nhuận trên mỗi khách hàng")
        waterfall_points = [
            0,
            gross_profit_per_user,
            gross_profit_per_user - cost_per_user,
            net_profit_per_user
        ]
        waterfall_min = min(waterfall_points)
        waterfall_max = max(waterfall_points)
        waterfall_padding = max((waterfall_max - waterfall_min) * 0.28, 8)
        fig_waterfall = go.Figure(go.Waterfall(
            name = "20", orientation = "v",
            measure = ["relative", "relative", "total"],
            x = ["Lợi nhuận gộp tăng thêm", "Chi phí voucher", "Lợi nhuận ròng"],
            textposition = "outside",
            text = [f"${gross_profit_per_user:.2f}", f"-${cost_per_user:.2f}", f"${net_profit_per_user:.2f}"],
            y = [gross_profit_per_user, -cost_per_user, net_profit_per_user],
            decreasing = {"marker":{"color":"#FF4B4B"}},
            increasing = {"marker":{"color":"#00CC96"}},
            totals = {"marker":{"color":"#FF4B4B"}}
        ))
        fig_waterfall.update_layout(**{**chart_layout, "height": 390, "margin": dict(l=20, r=20, t=72, b=96)})
        fig_waterfall.update_xaxes(automargin=True)
        fig_waterfall.update_yaxes(
            range=[waterfall_min - waterfall_padding, waterfall_max + waterfall_padding],
            automargin=True
        )
        st.plotly_chart(fig_waterfall, use_container_width=True)

    with col_chart2:
        st.markdown("#### Phân rã chi phí trợ giá (minh họa)")
        st.caption("Đây là phân rã minh họa trong môi trường mô phỏng, không phải ước lượng chính thức về mức độ chi trả cho các chuyến vốn đã tự phát sinh trên dữ liệu vận hành thực tế.")
        
        organic_cost_per_ride = calc_cost(df_ctrl['avg_fare_per_trip'], DISCOUNT_PERCENT)
        avg_burn_organic = (df_ctrl['Y_rand'] * organic_cost_per_ride).mean()
        avg_burn_total = df_treat['discount_cost_30d'].mean()
        avg_burn_inc = max(avg_burn_total - avg_burn_organic, 0)
        
        wasted_burn = avg_burn_organic * total_users
        effective_burn = avg_burn_inc * total_users
        total_burn = wasted_burn + effective_burn
        
        fig_burn = go.Figure(go.Pie(
            labels=['Chi phí trên chuyến nền', 'Chi phí trên chuyến tăng thêm'],
            values=[wasted_burn, effective_burn],
            hole=0.58,
            marker=dict(colors=['#FF4B4B', '#00CC96'], line=dict(color='#FFFFFF', width=2)),
            textinfo='percent',
            sort=False,
            hovertemplate="%{label}<br>$%{value:,.0f}<br>%{percent}<extra></extra>"
        ))
        fig_burn.update_layout(
            **{**chart_layout, "height": 370, "margin": dict(l=20, r=20, t=40, b=46)},
            annotations=[dict(
                text=f"Tổng burn<br>${total_burn:,.0f}",
                x=0.5,
                y=0.5,
                font=dict(size=16, color='#0F172A'),
                showarrow=False
            )],
            legend=dict(orientation="h", yanchor="bottom", y=-0.02, xanchor="center", x=0.5)
        )
        st.plotly_chart(fig_burn, use_container_width=True)
        st.info("Khuyến mãi đại trà tạo thêm chuyến xe, nhưng phần lớn chi phí có thể rơi vào các chuyến nền vốn vẫn có khả năng phát sinh dù không phát voucher.")

    st.error("**Kết luận:** Phát voucher đại trà tạo thêm nhu cầu nhưng lợi nhuận vẫn âm theo các giả định hiện tại. Vì vậy, đây không phải chính sách ứng viên phù hợp.")

# ================= TAB 2: CAUSAL EVIDENCE =================
with tab2:
    
    st.markdown("#### Chất lượng thí nghiệm")
    observed_treatment = len(df_treat)
    observed_control = len(df_ctrl)
    total = observed_treatment + observed_control

    health = load_experiment_health()
    srm_p_value = binomtest(k=observed_treatment, n=total, p=0.5).pvalue
    balance_features = [
        col for col in ['age', 'monthly_rides_history', 'recency_days', 'avg_fare_per_trip', 'is_urban']
        if col in df.columns
    ]
    smd_by_feature = {
        col: standardized_mean_difference(df_treat[col], df_ctrl[col])
        for col in balance_features
    }
    max_smd_feature = max(smd_by_feature, key=lambda col: abs(smd_by_feature[col])) if smd_by_feature else None
    max_abs_smd = abs(smd_by_feature[max_smd_feature]) if max_smd_feature else np.nan

    if health is not None:
        fpr = health['false_positive_rate']
        fpr_ok = health['fpr_acceptance_low'] <= fpr <= health['fpr_acceptance_high']
        srm_ok = srm_p_value >= health['alpha']
        balance_ok = pd.notna(max_abs_smd) and max_abs_smd < health['balance_smd_threshold']
        health_pass = fpr_ok and srm_ok and balance_ok
        health_message = (
            "Không phát hiện vấn đề đáng kể trong các kiểm tra A/A, SRM và cân bằng biến nền."
            if health_pass else
            "Có ít nhất một chỉ số vượt ngưỡng; cần xem chi tiết trước khi diễn giải ATE."
        )
        (st.success if health_pass else st.warning)(
            f"**Kết quả kiểm định: {'ĐẠT' if health_pass else 'CẦN XEM XÉT'}**\n\n{health_message}"
        )
    else:
        st.warning("Chưa có artifact kiểm định thí nghiệm; dashboard không tự gán trạng thái ĐẠT.")

    with st.expander("Chi tiết kiểm định"):
        h1, h2, h3, h4 = st.columns(4)
        h1.metric(
            "Số lần mô phỏng A/A",
            f"{health['aa_monte_carlo_runs']:,}" if health is not None else "N/A",
            help="Số lần chạy thử nghiệm ngẫu nhiên để test xem hệ thống chia nhóm có bị thiên vị (bias) hay không."
        )
        h2.metric(
            "False Positive Rate",
            f"{health['false_positive_rate']:.2%}" if health is not None else "N/A",
            help="Tỷ lệ báo động giả. Hệ thống chuẩn phải có FPR xoay quanh 5% (Mức Alpha). Nếu quá cao nghĩa là hệ thống chia nhóm đang bị lỗi và thường xuyên báo kết quả ảo."
        )
        h3.metric("SRM p-value hiện tại", f"{srm_p_value:.4f}", help="Kiểm định Sample Ratio Mismatch. Nếu p-value < 0.05, số lượng khách 2 nhóm (Treatment/Control) đang bị lệch nghiêm trọng so với tỷ lệ 50/50, cần dừng thí nghiệm ngay.")
        h4.metric(
            "Max |SMD| hiện tại",
            f"{max_abs_smd:.3f}" if pd.notna(max_abs_smd) else "N/A",
            help=f"Độ lệch chuẩn hóa lớn nhất (Biến lệch nhất: {max_smd_feature}). Nếu |SMD| < 0.1 chứng tỏ 2 nhóm cực kỳ cân bằng về mặt đặc điểm khách hàng (tuổi, lịch sử đi xe...)." if max_smd_feature else "Không có biến phù hợp"
        )
        st.caption(
            f"Phân bổ hiện tại: {observed_treatment:,} nhận voucher / {observed_control:,} đối chứng. "
            + (
                f"Trong {health['aa_monte_carlo_runs']:,} lần mô phỏng, tỷ lệ cảnh báo SRM là "
                f"{health['srm_simulation_rate']:.2%} với Binomial p-value = "
                f"{health['srm_binomial_p_value']:.4f}. Nguồn: {health['source']}."
                if health is not None else
                "SRM p-value và SMD được tính trực tiếp từ dữ liệu hiện tại."
            )
        )
        if smd_by_feature:
            smd_labels = {
                'age': 'Tuổi',
                'monthly_rides_history': 'Lịch sử chuyến',
                'recency_days': 'Số ngày từ lần gần nhất',
                'avg_fare_per_trip': 'Giá vé trung bình',
                'is_urban': 'Nội thành'
            }
            smd_threshold = health['balance_smd_threshold'] if health is not None else 0.1
            smd_df = pd.DataFrame([
                {
                    'Biến': smd_labels.get(feature, feature),
                    'SMD': value,
                    '|SMD|': abs(value)
                }
                for feature, value in smd_by_feature.items()
            ]).sort_values('|SMD|', ascending=False)

            fig_smd = go.Figure(go.Bar(
                x=smd_df['|SMD|'],
                y=smd_df['Biến'],
                orientation='h',
                marker_color=np.where(smd_df['|SMD|'] < smd_threshold, '#00CC96', '#FF4B4B'),
                customdata=np.round(smd_df['SMD'], 3),
                hovertemplate="Biến: %{y}<br>|SMD|: %{x:.3f}<br>SMD: %{customdata:.3f}<extra></extra>"
            ))
            fig_smd.add_vline(
                x=smd_threshold,
                line_dash="dash",
                line_color="#0F172A",
                annotation_text=f"Ngưỡng {smd_threshold:.1f}",
                annotation_position="top right"
            )
            fig_smd.update_layout(
                **chart_layout,
                height=max(260, 58 * len(smd_df) + 110),
                title="Cân bằng biến nền theo |SMD|",
                showlegend=False
            )
            fig_smd.update_xaxes(title="|SMD|", range=[0, max(smd_threshold * 1.4, smd_df['|SMD|'].max() * 1.2)])
            fig_smd.update_yaxes(title="", autorange="reversed")
            st.plotly_chart(fig_smd, use_container_width=True)
        st.info(
            "**💡 Giải thích nhanh cho Mentor:**\n"
            "- **FPR (False Positive Rate):** Hệ thống chia nhóm chuẩn phải có tỷ lệ báo động giả ~5%. Nếu quá cao là hệ thống đang có lỗi.\n"
            "- **SRM p-value:** Nếu < 0.05, số lượng khách 2 nhóm đang bị lệch nghiêm trọng so với tỷ lệ 50/50.\n"
            "- **Max |SMD|:** Độ lệch đặc điểm khách hàng. |SMD| < 0.1 chứng tỏ 2 nhóm cực kỳ cân bằng."
        )
    
    st.markdown("---")
    st.subheader("Voucher có thật sự tạo tác động nhân quả và mức tăng có đồng đều không?")
    st.markdown("Trước khi cá nhân hóa, ta cần chứng minh voucher thực sự tạo ra lượng cầu tăng thêm mang tính nhân quả.")
    
    raw_ate = df_treat['Y_rand'].mean() - df_ctrl['Y_rand'].mean()
    
    X = sm.add_constant(df[['treatment_rand', 'monthly_rides_history']])
    y = df['Y_rand']
    model = sm.OLS(y, X).fit(cov_type='HC1')
    adj_ate = model.params['treatment_rand']
    p_val = model.pvalues['treatment_rand']
    ci_low = model.conf_int().loc['treatment_rand', 0]
    ci_high = model.conf_int().loc['treatment_rand', 1]
    
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("ATE thô", f"{raw_ate:.2f} chuyến", help="Chênh lệch trung bình đơn thuần giữa nhóm nhận voucher và nhóm đối chứng.")
    c2.metric("Adjusted ATE", f"{adj_ate:.2f} chuyến", help="Ước lượng đã điều chỉnh theo hành vi nền để tăng độ chính xác.")
    c3.metric("CI 95%", f"[{ci_low:.2f} , {ci_high:.2f}]", help="Nếu lặp lại thí nghiệm 100 lần, thì 95 lần mức tăng thực tế sẽ rơi vào khoảng này. Khoảng này KHÔNG chứa số 0 chứng tỏ việc tăng chuyến đi là có thật.")
    c4.metric("P-value", f"{p_val:.4f}", "Có ý nghĩa thống kê" if p_val < 0.05 else "Chưa có ý nghĩa thống kê", help="Xác suất mà kết quả tăng trưởng này chỉ là do 'ăn may'. P-value < 0.05 (nhỏ hơn 5%) nghĩa là chắc chắn có tác dụng thực sự.")
    st.info(
        "**💡 Giải thích nhanh cho Mentor:**\n"
        "- **Khoảng tin cậy 95%:** Khoảng này KHÔNG chứa số 0 chứng tỏ việc tăng chuyến đi là có thật, không phải ngẫu nhiên.\n"
        "- **P-value:** Nhỏ hơn 0.05 (5%) nghĩa là tỷ lệ kết quả này do 'ăn may' là cực kỳ thấp. Chắc chắn voucher có tác dụng."
    )

    with st.expander("Phương pháp kỹ thuật - Ước lượng nhân quả"):
        st.markdown("""
        **Mô hình hồi quy nhân quả:**
        `Y_i = β₀ + β₁T_i + β₂X_nền,i + ε_i`
        
        > **Việc phân nhóm ngẫu nhiên tạo khả năng nhận diện tác động nhân quả. Điều chỉnh theo đặc trưng nền nhằm tăng độ chính xác, không phải để sửa sai lệch do nhiễu.**
        """)

    st.markdown("#### Targeting theo phân khúc")
    roi_data = []
    use_synthetic_segment_benchmark = {'Y0', 'Y1', 'avg_fare_per_trip'}.issubset(df.columns)
    for p in df['persona'].unique():
        segment = df[df['persona'] == p]
        if use_synthetic_segment_benchmark:
            base_gmv = (segment['Y0'] * segment['avg_fare_per_trip']).mean()
            d_rev = ((segment['Y1'] - segment['Y0']) * segment['avg_fare_per_trip']).mean()
            ate = (segment['Y1'] - segment['Y0']).mean()
            cost = (segment['Y1'] * calc_cost(segment['avg_fare_per_trip'], DISCOUNT_PERCENT)).mean()
            gross_profit = d_rev * (MARGIN_PERCENT / 100.0)
            roi = (gross_profit - cost) / cost * 100 if cost > 0 else 0
            roi_data.append({
                'Phân khúc': p,
                'Số khách hàng': len(segment),
                'ATE (chuyến/KH)': round(ate, 2),
                'GMV nền / KH ($)': round(base_gmv, 2),
                'GMV tăng thêm / KH ($)': round(d_rev, 2),
                'Chi phí voucher / KH ($)': round(cost, 2),
                'Lợi nhuận ròng / KH ($)': round(gross_profit - cost, 2),
                'ROI (%)': round(roi, 1)
            })
        else:
            t = segment[segment['treatment_rand'] == 1]
            c = segment[segment['treatment_rand'] == 0]
            if len(t) > 0 and len(c) > 0:
                rev_c = c['gross_revenue_30d'].mean()
                rev_t = t['gross_revenue_30d'].mean()
                d_rev = rev_t - rev_c
                ate = t['Y_rand'].mean() - c['Y_rand'].mean()
                gross_profit = d_rev * (MARGIN_PERCENT / 100.0)
                cost = t['discount_cost_30d'].mean()
                roi = (gross_profit - cost) / cost * 100 if cost > 0 else 0
                roi_data.append({
                    'Phân khúc': p,
                    'Số khách hàng': len(segment),
                    'ATE (chuyến/KH)': round(ate, 2),
                    'GMV nền / KH ($)': round(rev_c, 2),
                    'GMV tăng thêm / KH ($)': round(d_rev, 2),
                    'Chi phí voucher / KH ($)': round(cost, 2),
                    'Lợi nhuận ròng / KH ($)': round(gross_profit - cost, 2),
                    'ROI (%)': round(roi, 1)
                })
    roi_df = pd.DataFrame(roi_data).sort_values(by='ROI (%)', ascending=False)
    
    st.dataframe(roi_df.style.format(precision=1)
             .background_gradient(subset=['ROI (%)'], cmap='RdYlGn', vmin=-100, vmax=50), 
             use_container_width=True, hide_index=True)
    st.caption("Các chỉ số tiền trong bảng là **trung bình trên mỗi khách hàng trong phân khúc**, không phải tổng toàn segment. Đơn vị `$` là currency giả lập của synthetic sandbox.")
    st.info("Targeting theo phân khúc cải thiện hiệu quả so với mass voucher, nhưng vẫn chưa đủ để tạo ROI dương.")
    if use_synthetic_segment_benchmark:
        st.caption("Hiệu quả theo phân khúc sử dụng hai kết quả tiềm năng tổng hợp Y0/Y1 làm chuẩn đối chiếu ổn định; không diễn giải đây là ROI thực tế trên môi trường vận hành.")

    st.markdown("→ Cần chuyển từ targeting theo nhóm sang ước lượng tác động ở cấp từng khách hàng.")

# ================= TAB 3: USER HETEROGENEITY =================
with tab3:
    st.subheader("Ai nhạy với voucher?")
    st.markdown("Phân phối CATE dự báo cho thấy response không đồng đều giữa khách hàng; vì vậy cần model uplift để xếp hạng ai nên được ưu tiên nhận voucher.")
    
    col_c1, col_c2 = st.columns(2)
    with col_c1:
        st.markdown("#### Phân phối CATE dự báo")
        q_low = preds_df['cate_pred'].quantile(0.01)
        q_high = preds_df['cate_pred'].quantile(0.99)
        fig_cate = px.histogram(preds_df, x='cate_pred', nbins=100, 
                                title="Phân bố CATE dự báo (số chuyến tăng thêm kỳ vọng)",
                                color_discrete_sequence=['#0EA5A4'], opacity=0.75,
                                marginal="box", range_x=[q_low, q_high])
        fig_cate.add_vline(x=0, line_dash="dash", line_color="#FF4B4B", 
                           annotation_text="CATE=0", annotation_position="top left", annotation_font_color="#FF4B4B")
        fig_cate.update_layout(
            plot_bgcolor='rgba(255,255,255,0)', paper_bgcolor='rgba(255,255,255,0)',
            font=dict(color='#0F172A'), margin=dict(l=20, r=20, t=40, b=20),
            bargap=0.05
        )
        fig_cate.update_xaxes(title="CATE dự báo (số chuyến tăng thêm)", showgrid=True, gridcolor='#E2E8F0')
        fig_cate.update_yaxes(title="Số khách hàng", showgrid=True, gridcolor='#E2E8F0')
        st.plotly_chart(fig_cate, use_container_width=True)
        st.caption("Đây là CATE dự báo từ representative model, không phải individual treatment effect tuyệt đối trên production.")
        
    with col_c2:
        st.markdown("#### So sánh mô hình uplift")
        model_snapshot = load_model_snapshot()
        model_comparison = load_uplift_model_comparison()

        def highlight_selected(row):
            return ['background-color: rgba(14, 165, 164, 0.14); font-weight: 700' if row['Vai trò'] == 'Được chọn' else '' for _ in row]

        st.dataframe(
            model_comparison.style
                .format({'Qini Coef': '{:.3f}'})
                .apply(highlight_selected, axis=1),
            use_container_width=True,
            hide_index=True
        )
        if model_snapshot:
            st.success(
                f"Chọn **{model_snapshot['model_name']}** làm representative model vì Qini cao nhất "
                f"trên held-out test set {model_snapshot['test_rows']:,} khách hàng."
            )
        else:
            st.success("Chọn **simplified R-Learner-style residual model** vì Qini cao nhất trong các model đã thử.")
        st.caption("Theo Week 5 report, các Qini coefficients này được so sánh trên cùng held-out test set 4.000 khách hàng và cùng cách tính; dashboard hiện chỉ recompute/render Qini curve cho snapshot R-Learner-style đã khóa.")

    render_model_evaluation()

    st.markdown("---")
    st.markdown("#### Từ CATE đến giá trị kinh tế")
    st.info("""
    **Expected Value = Incremental Margin − Expected Voucher Cost**

    `EV = [CATE × margin_per_ride] - [predicted_rides_treated × voucher_cost_per_ride]`

    **Điểm cần nhớ:** CATE cao không đồng nghĩa Expected Value dương. Nếu số chuyến nền hoặc chi phí voucher lớn, promotion burn vẫn có thể vượt phần margin tăng thêm.
    """)

    preds_df['voucher_cost'] = calc_cost(preds_df['avg_fare'], DISCOUNT_PERCENT)
    preds_df['margin_per_ride'] = preds_df['avg_fare'] * (MARGIN_PERCENT / 100.0)
    preds_df['expected_value'] = (preds_df['cate_pred'] * preds_df['margin_per_ride']) - (preds_df['pred_rides_treated'] * preds_df['voucher_cost'])

    fig_scatter = px.scatter(preds_df.sample(min(2000, len(preds_df)), random_state=42),
                             x='cate_pred', y='expected_value',
                             color='expected_value', color_continuous_scale='RdYlGn',
                             title="CATE dự báo và Expected Value - mẫu 2.000 khách hàng",
                             opacity=0.6)
    fig_scatter.add_hline(y=0, line_dash="dash", line_color="#FF4B4B")
    fig_scatter.add_vline(x=0, line_dash="dash", line_color="#00CC96")
    fig_scatter.update_layout(plot_bgcolor='rgba(255,255,255,0)', paper_bgcolor='rgba(255,255,255,0)', font=dict(color='#0F172A'), coloraxis_showscale=False, height=350)
    fig_scatter.update_xaxes(title="CATE dự báo (số chuyến tăng thêm)")
    fig_scatter.update_yaxes(title="Expected Value ($)")
    st.plotly_chart(fig_scatter, use_container_width=True)
    st.markdown("→ Sang Tab 4: dùng Expected Value để so sánh mass, segment, uplift và profit targeting trong policy simulator.")

    with st.expander("Phương pháp kỹ thuật - Ước lượng tác động khác biệt"):
        st.markdown("""
        **Quy trình Mô hình hóa (Residualization Flow):**
        `X + T + Y` ➔ `Trừ mức nền của kết quả` ➔ `Trừ xác suất nhận voucher` ➔ `Mô hình tác động kiểu R-Learner` ➔ `Xếp hạng CATE`
        
        **Các công thức chính:**
        `m(X) = E[Y|X]`
        `e(X) = P(T=1|X)`
        `Y_tilde = Y - m(X)`
        `T_tilde = T - e(X)`
        
        > **Phiên bản hiện tại chưa dùng cross-fitting, vì vậy được mô tả là mô hình residual đơn giản hóa theo phong cách R-Learner, chưa phải DML đầy đủ.**
        """)
# ================= TAB 4: POLICY SIMULATOR =================
with tab4:
    st.subheader("Lựa chọn chính sách phát voucher trong giới hạn kinh tế")
    
    st.markdown("""
    <div style='display: flex; justify-content: space-between; align-items: center; background-color: #FFFFFF; color: #0F172A; border: 1px solid #D8E2EA; box-shadow: 0 8px 22px rgba(15, 23, 42, 0.06); padding: 15px; border-radius: 6px; margin-bottom: 20px;'>
        <div style='text-align: center; flex: 1;'><b>TẦNG MÔ HÌNH</b><br><span style='color:#64748B; font-size: 0.9em;'>CATE dự báo</span></div>
        <div style='font-size: 1.5rem; color: #0EA5A4;'>➔</div>
        <div style='text-align: center; flex: 1;'><b>TẦNG KINH TẾ</b><br><span style='color:#64748B; font-size: 0.9em;'>Incremental Margin - Expected Voucher Cost</span></div>
        <div style='font-size: 1.5rem; color: #0EA5A4;'>➔</div>
        <div style='text-align: center; flex: 1;'><b>TẦNG CHÍNH SÁCH</b><br><span style='color:#64748B; font-size: 0.9em;'>Phát / Không phát / Ràng buộc ngân sách</span></div>
    </div>
    """, unsafe_allow_html=True)
    
    st.caption("**Đầu ra mô hình chưa phải quyết định cuối cùng; điều kiện kinh tế và ràng buộc chính sách mới chuyển dự báo thành hành động.**")
    st.latex(r"EV_i = CATE_i \times L_i - \widehat{Y_i(1)} \times C_i")
    st.caption("Trong đó, Lᵢ là lợi nhuận trên mỗi chuyến; Ŷᵢ(1) là tổng số chuyến dự kiến khi phát voucher; Cᵢ là chi phí voucher trên mỗi chuyến. Một khách hàng chỉ đáng nhận voucher khi incremental margin kỳ vọng đủ bù promotion burn.")
    
    col_sim_left, col_sim_right = st.columns([1, 3])
    
    with col_sim_left:
        st.markdown("#### Các giả định")
        sim_voucher = st.slider("Mức giảm giá (%)", min_value=5.0, max_value=50.0, value=15.0, step=1.0)
        st.warning("Uplift/CATE hiện được ước lượng dưới treatment voucher 15%. Thay đổi mức voucher trong simulator chỉ là economic sensitivity analysis; CATE được giữ cố định và không được diễn giải là causal effect đã estimate cho mức voucher mới.")
        sim_margin = st.slider("Biên lợi nhuận (%)", min_value=10.0, max_value=100.0, value=70.0, step=5.0)
        sim_budget = st.number_input("Ngân sách cho policy phân bổ ($)", min_value=1000, max_value=500000, value=50000, step=5000)
        st.caption("Ngân sách chỉ áp dụng cho Budget-Constrained Greedy; các policy còn lại được giữ nguyên để làm benchmark.")
        st.caption("Chi phí voucher mỗi chuyến = mức giảm giá × giá cước; simulator không áp dụng cap trong synthetic sandbox.")
        
    with col_sim_right:
        st.markdown("#### Bảng so sánh chính sách")
        preds_df['voucher_cost'] = calc_cost(preds_df['avg_fare'], sim_voucher)
        preds_df['margin_per_ride'] = preds_df['avg_fare'] * (sim_margin / 100.0)
        preds_df['expected_value'] = (preds_df['cate_pred'] * preds_df['margin_per_ride']) - (preds_df['pred_rides_treated'] * preds_df['voucher_cost'])
        
        total_pop = len(preds_df)
        
        def eval_policy_sim(mask, label):
            targeted = preds_df[mask]
            n_t = mask.sum()
            target_pct = (n_t / total_pop) * 100 if total_pop > 0 else 0
            
            if n_t == 0: 
                return {"Chính sách so sánh": label, "Tỷ lệ khách hàng được nhận (%)": 0.0, "Chuyến tăng thêm": 0.0, "Chi phí voucher ($)": 0, "Lợi nhuận kỳ vọng ($)": 0, "ROI (%)": 0.0}
            
            pred_inc_rides = targeted['cate_pred'].sum()
            pred_burn = (targeted['pred_rides_treated'] * targeted['voucher_cost']).sum()
            pred_profit = targeted['expected_value'].sum()
            pred_roi = (pred_profit / pred_burn * 100) if pred_burn > 0 else 0
            
            return {
                "Chính sách so sánh": label,
                "Tỷ lệ khách hàng được nhận (%)": round(target_pct, 1),
                "Chuyến tăng thêm": round(pred_inc_rides, 1),
                "Chi phí voucher ($)": round(pred_burn, 0),
                "Lợi nhuận kỳ vọng ($)": round(pred_profit, 0),
                "ROI (%)": round(pred_roi, 1)
            }
        
        sim_results = []
        no_m = pd.Series([False]*len(preds_df), index=preds_df.index)
        sim_results.append(eval_policy_sim(no_m, "0. No Voucher"))
        
        mass_m = pd.Series([True]*len(preds_df), index=preds_df.index)
        sim_results.append(eval_policy_sim(mass_m, "1. Mass Voucher"))
        
        if 'persona' in preds_df.columns:
            sub_m = preds_df['persona'].str.contains('Suburban', case=False, na=False)
            sim_results.append(eval_policy_sim(sub_m, "2. Segment Targeting"))
            
        uplift_thresh = preds_df['cate_pred'].quantile(0.7)
        uplift_m = preds_df['cate_pred'] >= uplift_thresh
        sim_results.append(eval_policy_sim(uplift_m, "3. Uplift Targeting"))
        
        prof_m = preds_df['expected_value'] > 0
        sim_results.append(eval_policy_sim(prof_m, "4. EV/Profit Targeting"))
        
        prof_df_sim = preds_df[preds_df['expected_value'] > 0].copy()
        df_sorted = prof_df_sim.sort_values('expected_value', ascending=False)
        df_sorted['cum_cost'] = (df_sorted['pred_rides_treated'] * df_sorted['voucher_cost']).cumsum()
        budget_m_idx = df_sorted[df_sorted['cum_cost'] <= sim_budget].index
        budget_m = preds_df.index.isin(budget_m_idx)
        sim_results.append(eval_policy_sim(budget_m, "5. Budget-Constrained Greedy"))
        
        sim_df = pd.DataFrame(sim_results)
        # Handle tooltip column if needed (Streamlit dataframe tooltip isn't native for single cells easily without extra code, we will just use a helper icon or text).
        
        st.dataframe(sim_df.drop(columns=['tooltip'], errors='ignore').style.format({
            'Tỷ lệ khách hàng được nhận (%)': '{:.1f}%',
            'Chuyến tăng thêm': '{:,.1f}',
            'Chi phí voucher ($)': '${:,.0f}',
            'Lợi nhuận kỳ vọng ($)': '${:,.0f}',
            'ROI (%)': '{:.1f}%'
        }).background_gradient(subset=['Lợi nhuận kỳ vọng ($)'], cmap='RdYlGn', vmin=-5000, vmax=15000), use_container_width=True, hide_index=True)

        st.caption("*5. Budget-Constrained Greedy: greedy heuristic chỉ xét khách hàng có EV dương, xếp theo EV từ cao xuống thấp, rồi lấy theo cumulative voucher cost tới ngân sách. Nếu ngân sách lớn hơn tổng chi phí của toàn bộ khách hàng EV dương, kết quả sẽ giống EV/Profit Targeting. Đây không phải nghiệm tối ưu tổ hợp chính xác.*")
        
        best_profit = sim_df['Lợi nhuận kỳ vọng ($)'].max()
        if best_profit > 0:
            best_policy = sim_df.loc[sim_df['Lợi nhuận kỳ vọng ($)'].idxmax(), 'Chính sách so sánh']
            st.success(f"**Chiến lược có lợi nhuận kỳ vọng cao nhất trong mô phỏng:** {best_policy}")
        else:
            st.error("**Chiến lược có lợi nhuận kỳ vọng cao nhất trong mô phỏng:** 0. No Voucher")

        budget_row = sim_df[sim_df['Chính sách so sánh'] == "5. Budget-Constrained Greedy"].iloc[0]
        st.info(
            f"Với ngân sách hiện tại, Budget-Constrained Greedy target "
            f"{budget_row['Tỷ lệ khách hàng được nhận (%)']:.1f}% khách hàng và tạo "
            f"${budget_row['Lợi nhuận kỳ vọng ($)']:,.0f} Expected Profit. Đây là scenario result, không phải recommendation thứ hai."
        )

        st.download_button(
            "Tải bảng chính sách (CSV)",
            data=sim_df.to_csv(index=False).encode('utf-8-sig'),
            file_name="policy_simulation.csv",
            mime="text/csv"
        )

# ================= TAB 5: ROBUSTNESS =================
with tab5:
    st.subheader("Kiểm tra độ vững & lộ trình phát triển")
    st.markdown("Tab này kiểm tra framework phản ứng thế nào khi bị stress, rồi nối sang bước kiểm chứng policy ngoài thực tế và roadmap mở rộng sản phẩm.")
    
    st.markdown("#### 1. Stress tests")
    g1, g2 = st.columns(2)
    g1.success("**Sample Size**\n\nATE ổn định, CI hẹp dần khi N tăng.")
    g2.success("**Null Effect**\n\nEstimate tập trung quanh 0, FPR gần mức thiết kế.")
    g3, g4 = st.columns(2)
    g3.warning("**Phân bổ Treatment 90/10**\n\nUncertainty/SE tăng.")
    g4.info("**Noise Injection**\n\nSignal yếu đi, uncertainty tăng.")
    
    st.caption("Các stress test này kiểm tra statistical behavior trong synthetic sandbox, chưa chứng minh production robustness; kết quả được tổng hợp từ Week 6 stress-test notebook và không rerun khi dashboard load.")
    st.info("**Champion–Challenger:** Policy được lựa chọn từ simulator mới chỉ là candidate/challenger. Trước khi rollout cần thử nghiệm trực tiếp với baseline/champion hiện hành và chỉ mở rộng khi incremental profit cải thiện với bằng chứng thống kê.")
    
    with st.expander("Cách diễn giải kiểm tra độ vững"):
        st.markdown("""
        | Kiểm tra | Biến được thay đổi | Hành vi thống kê kỳ vọng |
        |---|---|---|
        | Sample Size | N | ATE ổn định hơn, khoảng tin cậy hẹp dần |
        | Null Effect | ATE thật | Ước lượng tập trung quanh 0, FPR gần mức thiết kế |
        | Treatment Allocation 90/10 | Tỷ lệ phân bổ treatment | Sai số chuẩn và độ bất định tăng |
        | Noise Injection | Phương sai outcome | Tín hiệu yếu đi, độ bất định tăng |
        
        > **Các phép kiểm tra ở đây xác nhận quy trình có phản ứng đúng như lý thuyết thống kê hay không, chưa khẳng định quy trình đã đủ vững để vận hành thực tế.**
        """)
    
    st.markdown("---")
    st.markdown("#### 2. Lộ trình trưởng thành của hệ thống")
    
    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown("""
        <div class='roadmap-card'>
            <div class='roadmap-title'>HIỆN TẠI</div>
            <div class='roadmap-subtitle'>Cấp khách hàng</div>
            <div style='color: #0F172A; font-size: 1.2rem; margin: 10px 0;'>KHÁCH HÀNG NÀO?</div>
            <p>Khách hàng nào nên nhận voucher?</p>
        </div>
        """, unsafe_allow_html=True)
    with c2:
        st.markdown("""
        <div class='roadmap-card'>
            <div class='roadmap-title' style='color:#64748B;'>TIẾP THEO</div>
            <div class='roadmap-subtitle'>Cấp phiên</div>
            <div style='color: #0F172A; font-size: 1.2rem; margin: 10px 0;'>KHÁCH HÀNG NÀO + KHI NÀO?</div>
            <p>Khách hàng nào nên nhận voucher và trong phiên hoặc bối cảnh nào?</p>
        </div>
        """, unsafe_allow_html=True)
    with c3:
        st.markdown("""
        <div class='roadmap-card'>
            <div class='roadmap-title' style='color:#64748B;'>TƯƠNG LAI</div>
            <div class='roadmap-subtitle'>Cá nhân hóa voucher</div>
            <div style='color: #0F172A; font-size: 1.2rem; margin: 10px 0;'>KHÁCH HÀNG NÀO + KHI NÀO + MỨC BAO NHIÊU?</div>
            <p>Mức voucher nào tối đa hóa giá trị tăng thêm kỳ vọng?</p>
        </div>
        """, unsafe_allow_html=True)
        
    with st.expander("Kiến trúc kỹ thuật khái quát"):
        st.markdown("""
        `Tầng dữ liệu` ➔ `Kiểm định thí nghiệm` ➔ `Ước lượng nhân quả` ➔ `Bộ máy kinh tế` ➔ `Bộ máy chính sách` ➔ `Giao diện quyết định`
        
        **HIỆN TẠI:** Ngoại tuyến / Cấp khách hàng / Dữ liệu tổng hợp<br>
        **TIẾP THEO:** Đặc trưng phiên và sự kiện / Cấp phiên<br>
        **TƯƠNG LAI:** Quyết định mức voucher / Giám sát
        
        > **Đây là lộ trình minh họa cho sự phát triển của khung giải pháp, không phải kiến trúc vận hành thực tế hiện tại của GSM.**
        """)

    st.caption("Từ prototype đến production: kiểm chứng policy ngoài thực tế trước, sau đó mới mở rộng từ WHO sang WHEN và HOW MUCH.")
