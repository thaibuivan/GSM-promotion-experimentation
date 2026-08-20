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
    .executive-title {
        color: #1E1E1E;
        font-weight: 800;
        font-size: 2.2rem;
        margin-bottom: 0px;
    }
    @media (prefers-color-scheme: dark) {
        .executive-title { color: #F8FAFC; }
    }
    [data-testid="stMetricValue"] {
        font-size: 2rem;
        font-weight: bold;
    }
    .block-container { padding-top: 3.5rem; }
    
    .stTabs [data-baseweb="tab-list"] { gap: 10px; }
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        white-space: pre-wrap;
        background-color: transparent;
        border-radius: 4px 4px 0px 0px;
        padding: 10px 16px;
        font-size: 1.1rem;
        font-weight: 600;
    }
    
    .breadcrumb {
        font-size: 1.1rem;
        color: #888;
        margin-bottom: 20px;
        padding: 10px 0px;
        border-bottom: 1px solid #444;
    }
    .breadcrumb span.active {
        color: #00E5FF;
        font-weight: bold;
    }
    
    .roadmap-card {
        padding: 20px;
        border-radius: 8px;
        background-color: #222222;
        border: 1px solid #444;
        text-align: center;
        height: 100%;
    }
    .roadmap-title {
        font-size: 1.2rem;
        font-weight: 700;
        color: #00E5FF;
        margin-bottom: 5px;
    }
    .roadmap-subtitle {
        font-size: 1rem;
        font-weight: 600;
        color: #aaa;
        margin-bottom: 10px;
    }
    
    .flow-card {
        padding: 10px 20px;
        border-radius: 6px;
        background-color: #2E2E2E;
        border-left: 4px solid #00E5FF;
        margin-bottom: 15px;
    }
</style>
""", unsafe_allow_html=True)

st.markdown('<p class="executive-title">Khung thử nghiệm khuyến mãi và cá nhân hóa</p>', unsafe_allow_html=True)
st.markdown("### Mô hình thử nghiệm ở cấp khách hàng cho nhắm chọn nhân quả và đánh giá chính sách")
st.info("Dự án xây dựng một quy trình xuyên suốt từ bằng chứng nhân quả đến quyết định phát voucher ở cấp khách hàng. Phiên bản hiện tại trả lời KHÁCH HÀNG NÀO nên nhận voucher; hướng phát triển tiếp theo là KHÁCH HÀNG NÀO + KHI NÀO ở cấp phiên, rồi KHÁCH HÀNG NÀO + KHI NÀO + MỨC BAO NHIÊU ở cấp voucher.")
st.caption("**Phạm vi:** Synthetic sandbox cấp khách hàng trong chu kỳ 30 ngày. Economics mặc định dùng voucher 15% giá mỗi chuyến, không cap; đây không phải chính sách GSM thực tế.")

base_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
data_path = os.path.join(base_path, "data", "processed", "segmented_simulation_data.csv")
pred_path = os.path.join(base_path, 'data', 'processed', 'test_predictions.csv')

@st.cache_data
def load_data(path):
    return pd.read_csv(path)

try:
    df = load_data(data_path)
    preds_df = load_data(pred_path)
except Exception as e:
    st.error(f"Không thể tải dữ liệu. Chi tiết lỗi: {str(e)}")
    st.stop()

chart_layout = dict(
    plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',
    font=dict(color='#F8FAFC'), margin=dict(l=20, r=20, t=40, b=20)
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

def standardized_mean_difference(treated, control):
    pooled_variance = (treated.var(ddof=1) + control.var(ddof=1)) / 2.0
    if pd.isna(pooled_variance) or pooled_variance <= 0:
        return 0.0
    return (treated.mean() - control.mean()) / np.sqrt(pooled_variance)

def render_breadcrumb(active_step):
    steps = [
        ("Business Problem", "1. Bài toán kinh doanh"),
        ("Causal Evidence", "2. Bằng chứng nhân quả"),
        ("User Heterogeneity", "3. Ai nhạy với voucher?"),
        ("Policy", "4. Mô phỏng chính sách"),
        ("Robustness", "5. Kiểm tra độ vững")
    ]
    html = '<div class="breadcrumb">'
    for i, (key, label) in enumerate(steps):
        if key == active_step:
            html += f'<span class="active">{label}</span>'
        else:
            html += f'<span>{label}</span>'
        if i < len(steps) - 1:
            html += ' ➔ '
    html += '</div>'
    st.markdown(html, unsafe_allow_html=True)

tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "1. Bài toán kinh doanh",
    "2. Bằng chứng nhân quả",
    "3. Ai nhạy với voucher?",
    "4. Mô phỏng chính sách",
    "5. Kiểm tra độ vững"
])

# ================= TAB 1: BUSINESS PROBLEM =================
with tab1:
    render_breadcrumb("Business Problem")
    st.subheader("Phát voucher đại trà có tạo thêm lợi nhuận không?")
    st.markdown("Thay vì chỉ nhìn vào tỷ lệ mở ứng dụng hoặc số chuyến tăng, ta đánh giá trực tiếp **lợi nhuận tăng thêm** khi phát voucher đại trà theo các giả định của môi trường mô phỏng.")
    
    avg_rev_treat = df_treat['gross_revenue_30d'].mean()
    avg_rev_ctrl = df_ctrl['gross_revenue_30d'].mean()
    incremental_rev_per_user = avg_rev_treat - avg_rev_ctrl
    gross_profit_per_user = incremental_rev_per_user * (MARGIN_PERCENT / 100.0)
    cost_per_user = df_treat['discount_cost_30d'].mean()
    net_profit_per_user = gross_profit_per_user - cost_per_user
    overall_roi = (net_profit_per_user / cost_per_user) * 100 if cost_per_user > 0 else 0
    total_users = len(df)
    total_net_profit = net_profit_per_user * total_users
    
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Tổng chi phí voucher", f"${cost_per_user * total_users:,.0f}")
    c2.metric("Doanh thu tăng thêm", f"${incremental_rev_per_user * total_users:,.0f}")
    c3.metric("Lợi nhuận ròng", f"${total_net_profit:,.0f}")
    c4.metric("ROI tổng thể", f"{overall_roi:.1f}%")
    
    st.error("**Kết luận:** Phát voucher đại trà tạo thêm nhu cầu nhưng lợi nhuận vẫn âm theo các giả định hiện tại. Vì vậy, đây không phải chính sách ứng viên phù hợp.")

    col_chart1, col_chart2 = st.columns(2)
    with col_chart1:
        st.markdown("#### Cơ cấu lợi nhuận trên mỗi khách hàng")
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
        fig_waterfall.update_layout(**chart_layout, height=350)
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
        
        fig_bar = go.Figure()
        fig_bar.add_trace(go.Bar(
            y=['Ngân sách khuyến mãi'], x=[wasted_burn],
            name='Chi phí trên chuyến nền', orientation='h', marker_color='#FF4B4B',
            text=f"${wasted_burn:,.0f}", textposition='inside'
        ))
        fig_bar.add_trace(go.Bar(
            y=['Ngân sách khuyến mãi'], x=[effective_burn],
            name='Chi phí trên chuyến tăng thêm', orientation='h', marker_color='#00CC96',
            text=f"${effective_burn:,.0f}", textposition='inside'
        ))
        fig_bar.update_layout(
            plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color='#F8FAFC'), margin=dict(l=20, r=20, t=40, b=20),
            height=200, barmode='stack',
            legend=dict(orientation="h", yanchor="bottom", y=1.1, xanchor="center", x=0.5))
        fig_bar.update_xaxes(title="Tổng chi phí voucher ($)", showgrid=False)
        st.plotly_chart(fig_bar, use_container_width=True)
        st.info("Khuyến mãi đại trà tạo thêm chuyến xe, nhưng phần lớn chi phí có thể rơi vào các chuyến nền vốn vẫn có khả năng phát sinh dù không phát voucher.")

# ================= TAB 2: CAUSAL EVIDENCE =================
with tab2:
    render_breadcrumb("Causal Evidence")
    
    st.markdown("#### Cổng kiểm tra chất lượng thí nghiệm")
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

    with st.expander("Số liệu kiểm định và nguồn tính"):
        h1, h2, h3, h4 = st.columns(4)
        h1.metric(
            "Số lần mô phỏng A/A",
            f"{health['aa_monte_carlo_runs']:,}" if health is not None else "N/A"
        )
        h2.metric(
            "False Positive Rate",
            f"{health['false_positive_rate']:.2%}" if health is not None else "N/A"
        )
        h3.metric("SRM p-value hiện tại", f"{srm_p_value:.4f}")
        h4.metric(
            "Max |SMD| hiện tại",
            f"{max_abs_smd:.3f}" if pd.notna(max_abs_smd) else "N/A",
            help=f"Biến có |SMD| lớn nhất: {max_smd_feature}" if max_smd_feature else "Không có biến phù hợp"
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
    c2.metric("ATE đã hiệu chỉnh", f"{adj_ate:.2f} chuyến", help="Ước lượng đã điều chỉnh theo hành vi nền để tăng độ chính xác.")
    c3.metric("Khoảng tin cậy 95%", f"[{ci_low:.2f} , {ci_high:.2f}]")
    c4.metric("P-value", f"{p_val:.4f}", "Có ý nghĩa thống kê" if p_val < 0.05 else "Chưa có ý nghĩa thống kê")

    with st.expander("Phương pháp kỹ thuật - Ước lượng nhân quả"):
        st.markdown("""
        **Mô hình hồi quy nhân quả:**
        `Y_i = β₀ + β₁T_i + β₂X_nền,i + ε_i`
        
        > **Việc phân nhóm ngẫu nhiên tạo khả năng nhận diện tác động nhân quả. Điều chỉnh theo đặc trưng nền nhằm tăng độ chính xác, không phải để sửa sai lệch do nhiễu.**
        """)

    st.markdown("#### Hiệu quả kinh tế theo phân khúc")
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
                'ATE': round(ate, 2),
                'GMV nền ($)': round(base_gmv, 2),
                'GMV tăng thêm ($)': round(d_rev, 2),
                'Chi phí voucher ($)': round(cost, 2),
                'Lợi nhuận ròng ($)': round(gross_profit - cost, 2),
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
                    'ATE': round(ate, 2),
                    'GMV nền ($)': round(rev_c, 2),
                    'GMV tăng thêm ($)': round(d_rev, 2),
                    'Chi phí voucher ($)': round(cost, 2),
                    'Lợi nhuận ròng ($)': round(gross_profit - cost, 2),
                    'ROI (%)': round(roi, 1)
                })
    roi_df = pd.DataFrame(roi_data).sort_values(by='ROI (%)', ascending=False)
    
    st.dataframe(roi_df.style.format(precision=1)
             .background_gradient(subset=['ROI (%)'], cmap='RdYlGn', vmin=-100, vmax=50), 
             use_container_width=True, hide_index=True)
    if use_synthetic_segment_benchmark:
        st.caption("Hiệu quả theo phân khúc sử dụng hai kết quả tiềm năng tổng hợp Y0/Y1 làm chuẩn đối chiếu ổn định; không diễn giải đây là ROI thực tế trên môi trường vận hành.")

    st.info("**Kết luận:** Tác động trung bình tồn tại nhưng hiệu quả kinh doanh khác nhau giữa các nhóm. Phát voucher theo phân khúc đơn thuần vẫn chưa tối ưu được lợi nhuận.")

# ================= TAB 3: USER HETEROGENEITY =================
with tab3:
    render_breadcrumb("User Heterogeneity")
    st.subheader("Ai thực sự nhạy với voucher?")
    st.markdown("Tín hiệu uplift giúp phân biệt khách hàng theo mức phản ứng với voucher, nhưng phản ứng cao chưa đồng nghĩa với lợi nhuận cao.")
    
    col_c1, col_c2 = st.columns(2)
    with col_c1:
        st.markdown("#### Phân phối tác động cá nhân (CATE)")
        q_low = preds_df['cate_pred'].quantile(0.01)
        q_high = preds_df['cate_pred'].quantile(0.99)
        fig_cate = px.histogram(preds_df, x='cate_pred', nbins=100, 
                                title="Phân bố CATE (Chuyến đi dự kiến tăng thêm)",
                                color_discrete_sequence=['#00E5FF'], opacity=0.75,
                                marginal="box", range_x=[q_low, q_high])
        fig_cate.add_vline(x=0, line_dash="dash", line_color="#FF4B4B", 
                           annotation_text="CATE=0", annotation_position="top left", annotation_font_color="#FF4B4B")
        fig_cate.update_layout(
            plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color='#F8FAFC'), margin=dict(l=20, r=20, t=40, b=20),
            bargap=0.05
        )
        fig_cate.update_xaxes(title="CATE (Tác động nhân quả)", showgrid=True, gridcolor='#333333')
        fig_cate.update_yaxes(title="Số khách hàng", showgrid=True, gridcolor='#333333')
        st.plotly_chart(fig_cate, use_container_width=True)
        st.caption("Mô hình theo phong cách R-Learner đơn giản hóa dự báo độ nhạy với voucher ở cấp khách hàng.")
        qini_summary = load_or_build_qini_curve()
        qini_coef = compute_qini_coef(qini_summary)
        if pd.notna(qini_coef):
            st.metric("Hệ số Qini", f"{qini_coef:.3f}", "Xếp hạng tốt hơn ngẫu nhiên" if qini_coef > 0 else "Cần xem xét lại")
        else:
            st.caption("Chưa tính được hệ số Qini. Cần chạy lại quy trình xuất kết quả chính sách.")
        
    with col_c2:
        st.markdown("#### Từ CATE đến lợi nhuận kỳ vọng")
        st.info("""
        **Chuyển tín hiệu mô hình thành quyết định:**
        
        `Lợi nhuận kỳ vọng = [CATE × Lợi nhuận mỗi chuyến] - [Tổng chuyến dự kiến × Chi phí voucher mỗi chuyến]`
        
        **Nguyên tắc nhắm chọn:** Chỉ phát voucher cho khách hàng có **lợi nhuận tăng thêm kỳ vọng > 0**. Nếu CATE cao nhưng số chuyến nền quá lớn, chi phí khuyến mãi vẫn có thể lớn hơn phần lợi nhuận tăng thêm.
        """)
        

        preds_df['voucher_cost'] = calc_cost(preds_df['avg_fare'], DISCOUNT_PERCENT)
        preds_df['margin_per_ride'] = preds_df['avg_fare'] * (MARGIN_PERCENT / 100.0)
        preds_df['expected_value'] = (preds_df['cate_pred'] * preds_df['margin_per_ride']) - (preds_df['pred_rides_treated'] * preds_df['voucher_cost'])
        
        fig_scatter = px.scatter(preds_df.sample(min(2000, len(preds_df)), random_state=42), 
                                 x='cate_pred', y='expected_value', 
                                 color='expected_value', color_continuous_scale='RdYlGn',
                                 title="CATE và lợi nhuận kỳ vọng - mẫu 2.000 khách hàng",
                                 opacity=0.6)
        fig_scatter.add_hline(y=0, line_dash="dash", line_color="#FF4B4B")
        fig_scatter.add_vline(x=0, line_dash="dash", line_color="#00CC96")
        fig_scatter.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', font=dict(color='#F8FAFC'), coloraxis_showscale=False, height=350)
        fig_scatter.update_xaxes(title="CATE (số chuyến tăng thêm)")
        fig_scatter.update_yaxes(title="Lợi nhuận kỳ vọng ($)")
        st.plotly_chart(fig_scatter, use_container_width=True)

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
    render_breadcrumb("Policy")
    st.subheader("Lựa chọn chính sách phát voucher trong giới hạn kinh tế")
    
    st.markdown("""
    <div style='display: flex; justify-content: space-between; align-items: center; background-color: #2E2E2E; padding: 15px; border-radius: 6px; margin-bottom: 20px;'>
        <div style='text-align: center; flex: 1;'><b>TẦNG MÔ HÌNH</b><br><span style='color:#ccc; font-size: 0.9em;'>CATE dự báo</span></div>
        <div style='font-size: 1.5rem; color: #00E5FF;'>➔</div>
        <div style='text-align: center; flex: 1;'><b>TẦNG KINH TẾ</b><br><span style='color:#ccc; font-size: 0.9em;'>Lợi nhuận tăng thêm - Chi phí voucher</span></div>
        <div style='font-size: 1.5rem; color: #00E5FF;'>➔</div>
        <div style='text-align: center; flex: 1;'><b>TẦNG CHÍNH SÁCH</b><br><span style='color:#ccc; font-size: 0.9em;'>Phát / Không phát / Ràng buộc ngân sách</span></div>
    </div>
    """, unsafe_allow_html=True)
    
    st.caption("**Đầu ra mô hình chưa phải quyết định cuối cùng; điều kiện kinh tế và ràng buộc chính sách mới chuyển dự báo thành hành động.**")
    st.latex(r"EV_i = CATE_i \times L_i - \widehat{Y_i(1)} \times C_i")
    st.caption("Trong đó, Lᵢ là lợi nhuận trên mỗi chuyến; Ŷᵢ(1) là tổng số chuyến dự kiến khi phát voucher; Cᵢ là chi phí voucher trên mỗi chuyến.")
    
    col_sim_left, col_sim_right = st.columns([1, 3])
    
    with col_sim_left:
        st.markdown("#### Các giả định")
        sim_voucher = st.slider("Mức giảm giá (%)", min_value=5.0, max_value=50.0, value=15.0, step=1.0)
        sim_margin = st.slider("Biên lợi nhuận (%)", min_value=10.0, max_value=100.0, value=70.0, step=5.0)
        sim_budget = st.number_input("Ngân sách ($)", min_value=1000, max_value=500000, value=50000, step=5000)
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
                return {"Chính sách ứng viên": label, "Tỷ lệ nhắm chọn": 0.0, "Chuyến tăng thêm": 0.0, "Chi phí voucher ($)": 0, "Lợi nhuận ($)": 0, "ROI (%)": 0.0}
            
            pred_inc_rides = targeted['cate_pred'].sum()
            pred_burn = (targeted['pred_rides_treated'] * targeted['voucher_cost']).sum()
            pred_profit = targeted['expected_value'].sum()
            pred_roi = (pred_profit / pred_burn * 100) if pred_burn > 0 else 0
            
            return {
                "Chính sách ứng viên": label,
                "Tỷ lệ nhắm chọn": round(target_pct, 1),
                "Chuyến tăng thêm": round(pred_inc_rides, 1),
                "Chi phí voucher ($)": round(pred_burn, 0),
                "Lợi nhuận ($)": round(pred_profit, 0),
                "ROI (%)": round(pred_roi, 1)
            }
        
        sim_results = []
        no_m = pd.Series([False]*len(preds_df), index=preds_df.index)
        sim_results.append(eval_policy_sim(no_m, "0. Không phát voucher"))
        
        mass_m = pd.Series([True]*len(preds_df), index=preds_df.index)
        sim_results.append(eval_policy_sim(mass_m, "1. Phát voucher đại trà"))
        
        if 'persona' in preds_df.columns:
            sub_m = preds_df['persona'].str.contains('Suburban', case=False, na=False)
            sim_results.append(eval_policy_sim(sub_m, "2. Phát theo phân khúc ngoại thành"))
            
        uplift_thresh = preds_df['cate_pred'].quantile(0.7)
        uplift_m = preds_df['cate_pred'] >= uplift_thresh
        sim_results.append(eval_policy_sim(uplift_m, "3. Phát theo uplift (30% CATE cao nhất)"))
        
        prof_m = preds_df['expected_value'] > 0
        sim_results.append(eval_policy_sim(prof_m, "4. Phát theo lợi nhuận kỳ vọng"))
        
        prof_df_sim = preds_df[preds_df['expected_value'] > 0].copy()
        df_sorted = prof_df_sim.sort_values('expected_value', ascending=False)
        df_sorted['cum_cost'] = (df_sorted['pred_rides_treated'] * df_sorted['voucher_cost']).cumsum()
        budget_m_idx = df_sorted[df_sorted['cum_cost'] <= sim_budget].index
        budget_m = preds_df.index.isin(budget_m_idx)
        sim_results.append(eval_policy_sim(budget_m, "5. Phân bổ theo ngân sách"))
        
        sim_df = pd.DataFrame(sim_results)
        # Handle tooltip column if needed (Streamlit dataframe tooltip isn't native for single cells easily without extra code, we will just use a helper icon or text).
        
        st.dataframe(sim_df.drop(columns=['tooltip'], errors='ignore').style.format({
            'Tỷ lệ nhắm chọn': '{:.1f}%',
            'Chuyến tăng thêm': '{:,.1f}',
            'Chi phí voucher ($)': '${:,.0f}',
            'Lợi nhuận ($)': '${:,.0f}',
            'ROI (%)': '{:.1f}%'
        }).background_gradient(subset=['Lợi nhuận ($)'], cmap='RdYlGn', vmin=-5000, vmax=15000), use_container_width=True, hide_index=True)

        st.download_button(
            "Tải bảng chính sách (CSV)",
            data=sim_df.to_csv(index=False).encode('utf-8-sig'),
            file_name="policy_simulation.csv",
            mime="text/csv"
        )
        
        st.caption("*5. Phân bổ theo ngân sách: Thuật toán tham lam xếp khách hàng có EV dương theo EV từ cao xuống thấp. Nếu ngân sách lớn hơn tổng chi phí của toàn bộ khách hàng EV dương, kết quả sẽ giống chính sách phát theo lợi nhuận kỳ vọng. Đây không phải nghiệm tối ưu tổ hợp chính xác.*")
        
        best_profit = sim_df['Lợi nhuận ($)'].max()
        if best_profit > 0:
            best_policy = sim_df.loc[sim_df['Lợi nhuận ($)'].idxmax(), 'Chính sách ứng viên']
            st.success(f"**Chính sách ứng viên được đề xuất theo các giả định hiện tại:** {best_policy}")
        else:
            st.error("**Phương án được đề xuất:** Không phát voucher")

# ================= TAB 5: ROBUSTNESS =================
with tab5:
    render_breadcrumb("Robustness")
    st.subheader("Cổng kiểm định trước triển khai và lộ trình phát triển")
    st.markdown("Mọi chính sách ứng viên đều phải vượt qua các kiểm tra độ vững trước khi được đưa vào thử nghiệm thực tế.")
    
    st.markdown("#### 1. Các cổng kiểm tra độ vững")
    g1, g2, g3, g4 = st.columns(4)
    g1.success("**Tăng quy mô mẫu**\n\nATE duy trì ổn định và khoảng tin cậy hẹp dần khi N tăng từ 10 nghìn lên 50 nghìn và 100 nghìn.")
    g2.success("**Kiểm tra tác động bằng 0**\n\nKhi tác động thật bằng 0, ước lượng vẫn tập trung quanh 0 và tỷ lệ dương tính giả gần mức sai lầm loại I đã thiết kế trong mô phỏng.")
    g3.warning("**Mất cân bằng giữa hai nhóm**\n\nVới tỷ lệ phân bổ nhóm nhận voucher/đối chứng là 90/10, ước lượng có thể dao động đáng kể trong một lần chạy; rủi ro chính là độ bất định lớn hơn và lực thống kê thấp hơn.")
    g4.info("**Bổ sung nhiễu**\n\nNhiễu ngoại sinh làm tín hiệu yếu đi và tăng độ bất định, nhưng về kỳ vọng không tạo sai lệch có hướng một cách hệ thống.")
    
    st.caption("**Các kiểm tra độ vững trên dữ liệu tổng hợp giúp kiểm tra logic đo lường, nhưng chưa chứng minh hệ thống đã đủ vững trên môi trường vận hành thực tế hoặc sẵn sàng tự động triển khai.**")
    st.caption("Nguồn: `notebooks/week6_stress_test/1_stress_test.ipynb`. Dashboard tóm tắt kết quả đã chạy, không tự chạy lại stress tests khi tải trang.")
    st.info("**Cổng Champion–Challenger:** Phát theo lợi nhuận kỳ vọng mới là chính sách ứng viên, chưa phải quyết định triển khai cuối cùng. Thử nghiệm thực tế cần so sánh chính sách này với phát theo phân khúc và chỉ mở rộng khi lợi nhuận tăng thêm cao hơn với bằng chứng thống kê.")
    
    with st.expander("Cách diễn giải kiểm tra độ vững"):
        st.markdown("""
        | Kiểm tra | Biến được thay đổi | Hành vi thống kê kỳ vọng |
        |---|---|---|
        | Quy mô mẫu | N | Khoảng tin cậy hẹp dần |
        | Tác động bằng 0 | ATE thật | Ước lượng tập trung quanh 0 |
        | Chia nhóm 90/10 | Tỷ lệ phân bổ treatment | Sai số chuẩn tăng |
        | Bổ sung nhiễu | Phương sai outcome | Tín hiệu yếu đi |
        
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
            <div style='color: #fff; font-size: 1.2rem; margin: 10px 0;'>KHÁCH HÀNG NÀO?</div>
            <p>Khách hàng nào nên nhận voucher?</p>
        </div>
        """, unsafe_allow_html=True)
    with c2:
        st.markdown("""
        <div class='roadmap-card'>
            <div class='roadmap-title' style='color:#ccc;'>TIẾP THEO</div>
            <div class='roadmap-subtitle'>Cấp phiên</div>
            <div style='color: #fff; font-size: 1.2rem; margin: 10px 0;'>KHÁCH HÀNG NÀO + KHI NÀO?</div>
            <p>Khách hàng nào nên nhận voucher và trong phiên hoặc bối cảnh nào?</p>
        </div>
        """, unsafe_allow_html=True)
    with c3:
        st.markdown("""
        <div class='roadmap-card'>
            <div class='roadmap-title' style='color:#ccc;'>TƯƠNG LAI</div>
            <div class='roadmap-subtitle'>Cá nhân hóa voucher</div>
            <div style='color: #fff; font-size: 1.2rem; margin: 10px 0;'>KHÁCH HÀNG NÀO + KHI NÀO + MỨC BAO NHIÊU?</div>
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
    
    with st.expander("Chi tiết đánh giá mô hình: Qini và Calibration"):
        model_snapshot = load_model_snapshot()
        if model_snapshot:
            st.caption(
                f"Qini, calibration và policy cùng dùng snapshot đã khóa trên "
                f"test set {model_snapshot['test_rows']:,} khách hàng (seed {model_snapshot['split_seed']})."
            )
        col_qini, col_calib = st.columns(2)
        with col_qini:
            st.markdown("#### Đường Qini - đánh giá khả năng xếp hạng")
            st.caption("Câu hỏi: Mô hình có đưa những khách hàng phản ứng tốt lên đầu danh sách tốt hơn cách chọn ngẫu nhiên không?")
            qini_df = load_or_build_qini_curve()
            if qini_df is not None and not qini_df.empty:
                fig_qini = go.Figure()
                fig_qini.add_trace(go.Scatter(x=qini_df['pct_targeted'], y=qini_df['qini_uplift'], mode='lines', name='Mô hình', line=dict(color='#00E5FF', width=3)))
                fig_qini.add_trace(go.Scatter(x=qini_df['pct_targeted'], y=qini_df['random_uplift'], mode='lines', name='Mốc ngẫu nhiên', line=dict(color='rgba(255,255,255,0.3)', dash='dash', width=2)))
                fig_qini.update_layout(**chart_layout, height=350, legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1))
                fig_qini.update_xaxes(title="Tỷ lệ khách hàng được nhắm chọn (%)", dtick=10)
                fig_qini.update_yaxes(title="Số chuyến tăng thêm tích lũy (Qini)")
                st.plotly_chart(fig_qini, use_container_width=True)
            else:
                st.warning("Chưa có dữ liệu để vẽ đường Qini.")
                
        with col_calib:
            st.markdown("#### Biểu đồ Calibration - đánh giá độ lớn dự báo")
            st.caption("Câu hỏi: Độ lớn CATE dự báo có gần với uplift quan sát theo từng nhóm thập phân vị (decile) không?")
            try:
                calib_df = pd.read_csv(os.path.join(base_path, 'data', 'processed', 'uplift_calibration.csv'))
                fig_cal = go.Figure()
                fig_cal.add_trace(go.Scatter(name='CATE dự báo', x=calib_df['Decile'], y=calib_df['Predicted_CATE'], mode='lines+markers', line=dict(color='#FF4B4B', width=3)))
                fig_cal.add_trace(go.Scatter(name='Uplift quan sát', x=calib_df['Decile'], y=calib_df['Observed_Uplift'], mode='lines+markers', line=dict(color='#00CC96', width=2)))
                fig_cal.add_trace(go.Scatter(name='Giá trị thật tổng hợp', x=calib_df['Decile'], y=calib_df['Ground_Truth_CATE'], mode='lines', line=dict(color='rgba(255,255,255,0.4)', dash='dash', width=2)))
                fig_cal.update_layout(**chart_layout, height=350, legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1))
                fig_cal.update_xaxes(title="Các nhóm decile (tốt nhất đến kém nhất)")
                fig_cal.update_yaxes(title="Uplift trung bình")
                st.plotly_chart(fig_cal, use_container_width=True)
            except:
                st.warning("Chưa có dữ liệu Calibration.")
                
        st.info("**Mô hình có tín hiệu xếp hạng hữu ích, nhưng độ lớn CATE dự báo vẫn chưa được hiệu chỉnh hoàn hảo.**")
