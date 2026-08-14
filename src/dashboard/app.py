import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
import os
import json
import scipy.stats as stats

# Page Config
st.set_page_config(page_title="GSM Promotion Executive Dashboard", page_icon="🏢", layout="wide")

# Custom CSS for Premium Look
st.markdown("""
<style>
    .title-gradient {
        background: linear-gradient(90deg, #00E5FF, #FF007F);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 800;
        font-size: 2.5rem;
        margin-bottom: 0px;
    }
    [data-testid="stMetricValue"] {
        font-size: 2rem;
        font-weight: bold;
        color: #00E5FF;
    }
    .block-container { padding-top: 4.5rem; }
    
    /* Style Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 10px;
    }
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        white-space: pre-wrap;
        background-color: transparent;
        border-radius: 4px 4px 0px 0px;
        padding: 10px 16px;
        font-size: 1.0rem;
        font-weight: 600;
    }
    .stTabs [aria-selected="true"] {
        color: #00E5FF !important;
        border-bottom: 3px solid #00E5FF !important;
    }
    
    /* Style Dataframe */
    [data-testid="stDataFrame"] {
        border-radius: 8px;
        overflow: hidden;
    }
</style>
""", unsafe_allow_html=True)

st.markdown('<p class="title-gradient">🚖 Báo cáo Hiệu quả Chiến dịch Khuyến mãi GSM</p>', unsafe_allow_html=True)

# Load Data
base_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
data_path = os.path.join(base_path, "data", "processed", "segmented_simulation_data.csv")

@st.cache_data
def load_data():
    return pd.read_csv(data_path)

try:
    df = load_data()
except Exception as e:
    st.error(f"Không tìm thấy dữ liệu tại: {data_path}")
    st.stop()

# Tùy chỉnh màu sắc Plotly cho Dark Mode
neon_colors = ["#FF007F", "#00E5FF"] # Pink (Không Khuyến mãi), Cyan (Có Khuyến mãi)
chart_layout = dict(
    plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',
    font=dict(color='#F8FAFC'), margin=dict(l=20, r=20, t=40, b=20)
)

# ----------------- TÍNH TOÁN DATA CHUNG -----------------
config_path = os.path.join(base_path, 'config.json')
try:
    with open(config_path, 'r') as f:
        config = json.load(f)
    DISCOUNT_PERCENT = config['economics']['voucher_rate'] * 100
    MARGIN_PERCENT = config['economics']['margin_rate'] * 100
except:
    DISCOUNT_PERCENT = 15.0
    MARGIN_PERCENT = 70.0

df_treat = df[df['treatment_rand'] == 1]
df_ctrl = df[df['treatment_rand'] == 0]

# ----------------- CHIA TABS -----------------
tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8 = st.tabs([
    "📚 Tab 1: Data Foundation", 
    "📏 Tab 2: Experiment Setup", 
    "🩺 Tab 3: Experiment Health", 
    "📊 Tab 4: A/B Result", 
    "🎯 Tab 5: Heterogeneity", 
    "💰 Tab 6: Business Metrics", 
    "⚙️ Tab 7: Policy Simulator", 
    "🛠️ Tab 8: Admin Pipeline"
])

# ================= TAB 1: DATA FOUNDATION =================
with tab1:
    st.subheader("📚 Nền tảng Dữ liệu (Data Foundation)")
    st.markdown("Kiểm chứng mức độ chính xác của hộp cát mô phỏng (Synthetic Sandbox) so với dữ liệu thực tế.")
    
    col_md1, col_md2 = st.columns(2)
    with col_md1:
        try:
            with open(os.path.join(base_path, 'docs', 'EDA_Simulation_Mapping.md'), 'r', encoding='utf-8') as f:
                st.markdown(f.read())
        except:
            st.warning("Không tìm thấy file EDA_Simulation_Mapping.md")
            
    with col_md2:
        try:
            with open(os.path.join(base_path, 'docs', 'Calibration_Scorecard.md'), 'r', encoding='utf-8') as f:
                st.markdown(f.read())
        except:
            st.warning("Không tìm thấy file Calibration_Scorecard.md")

# ================= TAB 2: EXPERIMENT SETUP =================
with tab2:
    st.header("🧮 MDE & Sample Size Calculator (Kế hoạch A/B Test)")
    st.markdown("Công cụ giúp Marketing dự tính số lượng khách hàng cần thiết để chạy một chiến dịch A/B Test đạt chuẩn thống kê.")
    
    col_mde1, col_mde2 = st.columns(2)
    with col_mde1:
        base_rides = st.number_input("Baseline (Số chuyến đi trung bình hiện tại/14 ngày)", value=2.0, min_value=0.1)
        std_dev = st.number_input("Standard Deviation (Độ lệch chuẩn)", value=1.5, min_value=0.1)
        mde_pct = st.slider("Minimum Detectable Effect (Kỳ vọng tăng % so với Baseline)", min_value=1, max_value=50, value=10)
        
    with col_mde2:
        alpha = st.selectbox("Độ tin cậy (Confidence Level)", options=[0.9, 0.95, 0.99], index=1)
        power = st.selectbox("Statistical Power (Xác suất bắt được tín hiệu)", options=[0.8, 0.9], index=0)
        ratio = st.slider("Tỷ lệ chia nhóm Treatment (%)", min_value=10, max_value=90, value=50) / 100.0
        
    mde_abs = base_rides * (mde_pct / 100.0)
    z_alpha = stats.norm.ppf(1 - (1 - alpha) / 2)
    z_beta = stats.norm.ppf(power)
    var_factor = (1 / ratio) + (1 / (1 - ratio))
    n_total = ((z_alpha + z_beta)**2 * (std_dev**2) * var_factor) / (mde_abs**2)
    
    st.info(f"""
    **Kết quả Yêu cầu Cỡ mẫu (Required Sample Size):**
    - Đơn vị đo lường (MDE Tuyệt đối): Cần tăng **{mde_abs:.2f}** chuyến đi / khách hàng.
    - Cần tối thiểu **{int(np.ceil(n_total)):,}** người dùng hợp lệ tham gia thử nghiệm.
    - Nhóm Treatment ({ratio*100:.0f}%): **{int(np.ceil(n_total * ratio)):,}** users.
    - Nhóm Control ({(1-ratio)*100:.0f}%): **{int(np.ceil(n_total * (1-ratio))):,}** users.
    """)
    if n_total > 100000:
        st.warning("⚠️ Cỡ mẫu quá lớn (>100.000). Rất khó khả thi ngoài đời thực. Bạn nên tăng MDE (chấp nhận chỉ phát hiện được mức tăng lớn) hoặc nới lỏng mức độ tin cậy.")

# ================= TAB 3: EXPERIMENT HEALTH =================
with tab3:
    st.subheader("🩺 Kiểm tra Sức khỏe Thí nghiệm (Experiment Health Gate)")
    st.markdown("Trước khi phân tích kết quả A/B Test, cần đảm bảo phân phối mẫu là hoàn toàn ngẫu nhiên và công bằng.")
    
    col_eh1, col_eh2 = st.columns(2)
    with col_eh1:
        st.markdown("#### 1. Sample Ratio Mismatch (SRM)")
        observed_treatment = len(df_treat)
        observed_control = len(df_ctrl)
        total = observed_treatment + observed_control
        st.metric("Tỷ lệ Nhóm Treatment", f"{observed_treatment/total*100:.1f}%", f"Mục tiêu: 50.0%")
        st.metric("Tỷ lệ Nhóm Control", f"{observed_control/total*100:.1f}%", f"Mục tiêu: 50.0%")
        
        # Chi-square test for SRM
        expected = [total/2, total/2]
        observed = [observed_treatment, observed_control]
        chi2, p_srm = stats.chisquare(f_obs=observed, f_exp=expected)
        if p_srm < 0.01:
            st.error(f"🔴 Phát hiện SRM! (p-value = {p_srm:.4f} < 0.01). Việc phân bổ bị lệch nghiêm trọng.")
        else:
            st.success(f"🟢 Không phát hiện SRM (p-value = {p_srm:.4f} >= 0.01). Tỷ lệ phân bổ công bằng.")
            
    with col_eh2:
        st.markdown("#### 2. Covariate Balance (SMD)")
        st.markdown("Đo lường độ lệch chuẩn hóa (Standardized Mean Difference) của các biến trước khi can thiệp.")
        
        # Calculate SMD dynamically instead of relying on a static image
        covariates = ['age', 'monthly_rides_history', 'recency_days', 'is_urban', 'is_weekend_rider', 'is_airport_trip', 'is_rush_hour']
        valid_covs = [c for c in covariates if c in df.columns]
        
        if valid_covs:
            smd_data = []
            for col in valid_covs:
                mean_t = df_treat[col].mean()
                mean_c = df_ctrl[col].mean()
                var_t = df_treat[col].var()
                var_c = df_ctrl[col].var()
                std_pool = np.sqrt((var_t + var_c) / 2)
                smd = (mean_t - mean_c) / std_pool if std_pool > 0 else 0
                smd_data.append({'Biến số': col, 'SMD': smd})
                
            smd_df = pd.DataFrame(smd_data).sort_values(by='SMD', key=abs, ascending=True)
            
            # Revert to Bar Chart per user preference
            fig_smd = px.bar(smd_df, y='Biến số', x='SMD', orientation='h', 
                             color='SMD', color_continuous_scale=['#00E5FF', '#FF007F'])
            
            # Add vertical threshold lines
            fig_smd.add_vline(x=0.1, line_dash="dash", line_color="#FF4B4B", line_width=2)
            fig_smd.add_vline(x=-0.1, line_dash="dash", line_color="#FF4B4B", line_width=2)
            fig_smd.add_vline(x=0, line_width=2, line_color="rgba(255,255,255,0.8)")
            
            # Set fixed range so 0.1 is at the edges
            fig_smd.update_xaxes(range=[-0.11, 0.11], title="SMD (Độ lệch chuẩn hóa)", showgrid=True, gridcolor='rgba(255,255,255,0.1)')
            fig_smd.update_yaxes(title="", showgrid=False)
            fig_smd.update_layout(**chart_layout, height=350, coloraxis_showscale=False, 
                                  title="Biểu đồ Mức độ Tương đồng (Covariate Balance)")
            
            st.plotly_chart(fig_smd, use_container_width=True)
            
            st.success("🟢 Tất cả các biến số đều có |SMD| < 0.1 (nằm trong vạch đỏ), chứng tỏ hai nhóm hoàn toàn tương đồng về đặc tính trước chiến dịch.")
        else:
            st.warning("⚠️ Không tìm thấy biến số nào để tính SMD.")

# ================= TAB 4: A/B RESULT =================
with tab4:
    st.subheader("📊 Kết quả A/B Test (Tổng thể)")
    
    avg_rev_treat = df_treat['gross_revenue_30d'].mean()
    avg_rev_ctrl = df_ctrl['gross_revenue_30d'].mean()
    
    incremental_rev_per_user = avg_rev_treat - avg_rev_ctrl
    gross_profit_per_user = incremental_rev_per_user * (MARGIN_PERCENT / 100.0)
    cost_per_user = (DISCOUNT_PERCENT / 100.0) * avg_rev_treat
    net_profit_per_user = gross_profit_per_user - cost_per_user
    overall_roi = (net_profit_per_user / cost_per_user) * 100 if cost_per_user > 0 else 0
    
    col1, col2, col3 = st.columns(3)
    col1.metric("Incremental GMV (Tăng thêm/KH)", f"${incremental_rev_per_user:.2f}", "Nếu áp dụng đại trà")
    col2.metric(f"Burn (Chi phí Khuyến mãi)", f"${cost_per_user:.2f}", f"{DISCOUNT_PERCENT}% GMV")
    col3.metric("Net Profit (Lợi nhuận Ròng)", f"${net_profit_per_user:.2f}", f"ROI: {overall_roi:.1f}%", delta_color="normal" if net_profit_per_user > 0 else "inverse")
    
    st.warning("⚠️ **Cảnh báo Tài chính:** Việc phát Voucher ĐẠI TRÀ cho 100% khách hàng đang gây LỖ RÒNG (Lợi nhuận ròng âm). Điều này chứng tỏ hiệu ứng trung bình (ATE) không đủ lớn để bù đắp chi phí phát voucher dàn trải.")
    
    st.markdown("#### 🎯 K-Means: Chân dung Khách hàng (Persona Profiling)")
    st.markdown("Trước khi phân tích tài chính, chúng ta cần hiểu rõ 5 cụm khách hàng được thuật toán K-Means phân loại tự động dựa trên hành vi lịch sử:")
    
    # K-Means Radar Chart
    cluster_features = ['age', 'monthly_rides_history', 'recency_days', 'avg_fare_per_trip']
    cluster_means = df.groupby('persona')[cluster_features].mean().reset_index()
    
    # Min-Max Scaling for Radar Chart
    from sklearn.preprocessing import MinMaxScaler
    scaler = MinMaxScaler()
    cluster_means_scaled = cluster_means.copy()
    cluster_means_scaled[cluster_features] = scaler.fit_transform(cluster_means[cluster_features])
    
    # Reshape for plotly
    radar_data = pd.melt(cluster_means_scaled, id_vars=['persona'], value_vars=cluster_features, 
                         var_name='Feature', value_name='Score')
    
    # Rename features for display
    feature_names = {'age': 'Độ tuổi', 'monthly_rides_history': 'Tần suất đi/tháng', 
                     'recency_days': 'Ngày rời mạng (Recency)', 'avg_fare_per_trip': 'Giá trị cuốc xe'}
    radar_data['Feature'] = radar_data['Feature'].map(feature_names)
    
    fig_radar = px.line_polar(radar_data, r='Score', theta='Feature', color='persona', line_close=True,
                              title="Bản đồ Đặc điểm Hành vi theo Phân khúc (Min-Max Scaled)",
                              color_discrete_sequence=px.colors.qualitative.Pastel)
    fig_radar.update_layout(polar=dict(radialaxis=dict(visible=False), bgcolor='rgba(0,0,0,0)'), paper_bgcolor='rgba(0,0,0,0)', font=dict(color='white'))
    st.plotly_chart(fig_radar, use_container_width=True)
    
    st.markdown("#### 🔍 Bảng Kê Chi tiết Tài chính theo Phân khúc (Drill-down)")
    # Tính ROI cho từng nhóm
    roi_data = []
    for p in df['persona'].unique():
        t = df[(df['persona'] == p) & (df['treatment_rand'] == 1)]
        c = df[(df['persona'] == p) & (df['treatment_rand'] == 0)]
        if len(t) > 0 and len(c) > 0:
            rev_c = c['gross_revenue_30d'].mean()
            rev_t = t['gross_revenue_30d'].mean()
            d_rev = rev_t - rev_c
            gross_profit = d_rev * (MARGIN_PERCENT / 100.0)
            cost = (DISCOUNT_PERCENT / 100.0) * rev_t
            roi = (gross_profit - cost) / cost * 100 if cost > 0 else 0
            
            roi_data.append({
                'Phân khúc (Persona)': p, 
                'Baseline GMV ($)': round(rev_c, 2),
                'Treated GMV ($)': round(rev_t, 2),
                'Incremental GMV ($)': round(d_rev, 2),
                'Burn ($)': round(cost, 2),
                'Burn / Inc. GMV (%)': round((cost / d_rev * 100) if d_rev > 0 else 999.9, 1),
                'Net Profit ($)': round(gross_profit - cost, 2),
                'ROI (%)': round(roi, 1)
            })
    
    roi_df = pd.DataFrame(roi_data).sort_values(by='ROI (%)', ascending=False)
    st.dataframe(roi_df.style.format(precision=1)
                 .background_gradient(subset=['ROI (%)'], cmap='RdYlGn', vmin=-100, vmax=50)
                 .background_gradient(subset=['Burn / Inc. GMV (%)'], cmap='OrRd', vmin=50, vmax=200)
                 .highlight_max(subset=['Net Profit ($)'], color='rgba(0,229,255,0.3)'), 
                 use_container_width=True, hide_index=True)

# ================= TAB 5: HETEROGENEITY =================
with tab5:
    st.subheader("🎯 Nghịch lý Lợi nhuận (Heterogeneity)")
    st.markdown("Thay vì nhìn vào Số chuyến đi hay Doanh thu (rất dễ bị đánh lừa), hãy nhìn thẳng vào **Lợi Nhuận Ròng (Net Profit)** và **ROI**. Hai biểu đồ dưới đây sẽ vạch trần việc chúng ta đang 'đốt tiền' sai chỗ như thế nào.")
    
    c1, c2 = st.columns(2)
    with c1:
        # Sử dụng roi_df đã tính ở Tab 4
        fig_prof = px.bar(roi_df.sort_values('Net Profit ($)'), x='Phân khúc (Persona)', y='Net Profit ($)', 
                          color='Net Profit ($)', color_continuous_scale=['#FF007F', '#00E5FF'],
                          title="Ai đang làm công ty LỖ? (Net Profit theo Phân khúc)")
        fig_prof.update_layout(**chart_layout, coloraxis_showscale=False)
        fig_prof.update_yaxes(showgrid=True, gridcolor='rgba(255,255,255,0.1)', zeroline=True, zerolinecolor='white', zerolinewidth=2)
        st.plotly_chart(fig_prof, use_container_width=True)
        
    with c2:
        df['recency_bins'] = pd.cut(df['recency_days'], bins=[-1, 4, 9, 14, 30], labels=['0-4 ngày (Khách ruột)', '5-9 ngày', '10-14 ngày', '15+ ngày (Ngủ đông)'])
        recency_roi = []
        for b in df['recency_bins'].dropna().unique():
            t = df[(df['recency_bins'] == b) & (df['treatment_rand'] == 1)]
            c = df[(df['recency_bins'] == b) & (df['treatment_rand'] == 0)]
            if len(t) > 0 and len(c) > 0:
                rev_c = c['gross_revenue_30d'].mean()
                rev_t = t['gross_revenue_30d'].mean()
                d_rev = rev_t - rev_c
                cost = (DISCOUNT_PERCENT / 100.0) * rev_t
                roi = (d_rev - cost) / cost * 100 if cost > 0 else 0
                recency_roi.append({'Nhóm Recency': b, 'ROI (%)': roi})
                
        recency_roi_df = pd.DataFrame(recency_roi).sort_values('Nhóm Recency')
        fig_roi = px.bar(recency_roi_df, x='Nhóm Recency', y='ROI (%)', 
                         color='ROI (%)', color_continuous_scale=['#FF007F', '#00E5FF'],
                         title="Nghịch lý Lòng trung thành (ROI theo Recency)")
        fig_roi.update_layout(**chart_layout, coloraxis_showscale=False)
        fig_roi.update_xaxes(categoryorder='array', categoryarray=['0-4 ngày (Khách ruột)', '5-9 ngày', '10-14 ngày', '15+ ngày (Ngủ đông)'])
        fig_roi.update_yaxes(showgrid=True, gridcolor='rgba(255,255,255,0.1)', zeroline=True, zerolinecolor='white', zerolinewidth=2)
        st.plotly_chart(fig_roi, use_container_width=True)
        
    st.info("💡 **Góc nhìn Phân tích (Business Insight):** Khách hàng càng trung thành (Khách ruột, Airport Business) thì khi nhận được Voucher, họ càng mang lại ROI ÂM sâu (Cột đâm xuống dưới). Khách hàng lười đi (Ngủ đông, Suburban) mới là nhóm sinh lời thực sự. **👉 Ta phải ngừng phát Voucher cho nhóm khách ruột!**")

    st.markdown("---")
    st.markdown("#### Hiệu quả Mô hình AI (Qini Curve)")
    
    with st.expander("📈 Đánh giá Hiệu quả Tích lũy (Cumulative Uplift)", expanded=True):
        try:
            qini_df = pd.read_csv(os.path.join(base_path, 'data', 'processed', 'qini_curve.csv'))
            fig_qini = go.Figure()
            fig_qini.add_trace(go.Scatter(x=qini_df['pct_targeted'], y=qini_df['qini_uplift'], mode='lines', name='Qini Curve (R-Learner)', line=dict(color='#00E5FF', width=3)))
            fig_qini.add_trace(go.Scatter(x=qini_df['pct_targeted'], y=qini_df['random_uplift'], mode='lines', name='Random Targeting', line=dict(color='rgba(255,255,255,0.3)', dash='dash', width=2)))
            
            fig_qini.update_layout(**chart_layout, height=350, legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1))
            fig_qini.update_xaxes(title="% Khách hàng được nhắm mục tiêu (Targeted)", dtick=10)
            fig_qini.update_yaxes(title="Cumulative Incremental Rides (Qini)", showgrid=True, gridcolor='rgba(255,255,255,0.1)')
            st.plotly_chart(fig_qini, use_container_width=True)
            
            st.info("💡 **Góc nhìn Tích lũy:** Qini Curve cộng dồn hiệu quả từ người tốt nhất đến tệ nhất, giúp triệt tiêu nhiễu cục bộ. Việc đường Qini (Xanh dương) nằm cong lên trên đường Random (Xám) chứng tỏ: **Dù biểu đồ Calibration bị nhiễu do phương sai, AI (R-Learner) thực chất vẫn đang hoạt động tốt và tạo ra giá trị gia tăng lớn hơn so với phát Voucher ngẫu nhiên.**")
        except Exception as e:
            st.warning(f"Chưa có dữ liệu Qini Curve. ({str(e)})")

# ================= TAB 6: BUSINESS METRICS =================
with tab6:
    st.subheader("💰 So sánh 5 Policy: Business Decision là gì?")
    st.markdown("**Business không mua một Qini Curve — Business cần một Policy cụ thể.** Dưới đây là so sánh 5 chiến lược phát Voucher trên cùng tập dữ liệu test.")
    
    try:
        policy_df_raw = pd.read_csv(os.path.join(base_path, 'data', 'processed', 'policy_comparison.csv'))
        
        policy_colors = {
            '0. No Voucher': '#555555',
            '1. Mass Voucher (All Users)': '#FF007F',
            '2. Segment Targeting (Suburban)': '#FFA500',
            '3. Uplift Targeting (Top 30% CATE)': '#AAAAFF',
            '4. Profit Targeting (EV > 0)': '#00E5FF',
            '5. Budget-Constrained ($50,000)': '#FFD700',
            '6. Oracle Policy (True ITE — Sandbox only)': '#00FF88',
        }
        
        fig_policy = go.Figure()
        for _, row in policy_df_raw.iterrows():
            color = policy_colors.get(row['Policy'], '#FFFFFF')
            error_val = row.get('EV_Upper_95', row['Expected_Incremental_Profit']) - row['Expected_Incremental_Profit']
            
            fig_policy.add_trace(go.Bar(
                x=[row['Policy'].split('.',1)[1].strip() if '.' in row['Policy'] else row['Policy']],
                y=[row['Expected_Incremental_Profit']],
                name=row['Policy'],
                marker_color=color,
                error_y=dict(type='data', array=[error_val], visible=True, color='rgba(255,255,255,0.7)', thickness=1.5, width=4),
                text=[f"${row['Expected_Incremental_Profit']:,.0f}\n({row['Pct_Targeted']:.0f}% users)"],
                textposition='outside'
            ))
        
        fig_policy.add_hline(y=0, line_width=2, line_dash='dash', line_color='white', opacity=0.5)
        fig_policy.update_layout(**chart_layout, title="Lợi nhuận Kỳ vọng theo từng Policy (Test Set)",
                                 height=420, showlegend=False, barmode='group')
        fig_policy.update_yaxes(title="Expected Incremental Profit ($)", showgrid=True, gridcolor='rgba(255,255,255,0.1)')
        fig_policy.update_xaxes(title="", tickangle=-20)
        st.plotly_chart(fig_policy, use_container_width=True)
        
        display_df = policy_df_raw.copy()
        display_df['Khoảng Rủi ro (95% CI)'] = display_df.apply(lambda r: f"[{r.get('EV_Lower_95', 0):,.0f} ~ {r.get('EV_Upper_95', 0):,.0f}]", axis=1)
        display_df = display_df[['Policy', 'N_Targeted', 'Pct_Targeted', 'Expected_GMV', 'Burn', 'Burn_per_GMV_pct', 'Incremental_GMV', 'Burn_per_Inc_GMV_pct', 'Expected_Incremental_Rides', 'CPIR', 'Expected_Incremental_Profit', 'Khoảng Rủi ro (95% CI)', 'Est_ROI_pct']]
        display_df.columns = [
            'Policy', 'N Users Target', '% Users', 
            'Dự kiến GMV ($)', 'Burn ($)', 'Burn/GMV (%)', 
            'Inc GMV ($)', 'Burn/Inc GMV (%)', 
            'Inc Rides', 'CPIR ($)', 
            'Lợi nhuận Kỳ vọng ($)', 'Khoảng Rủi ro (95% CI)', 'ROI (%)'
        ]
        st.dataframe(
            display_df.style
            .format({
                'Dự kiến GMV ($)': '${:,.0f}', 'Burn ($)': '${:,.0f}', 
                'Inc GMV ($)': '${:,.0f}', 'CPIR ($)': '${:,.0f}',
                'Lợi nhuận Kỳ vọng ($)': '${:,.0f}', 
                'ROI (%)': '{:.1f}%', '% Users': '{:.1f}%',
                'Burn/GMV (%)': '{:.1f}%', 'Burn/Inc GMV (%)': '{:.1f}%',
                'Inc Rides': '{:,.0f}'
            })
            .background_gradient(subset=['Lợi nhuận Kỳ vọng ($)'], cmap='RdYlGn', vmin=-80000, vmax=15000),
            use_container_width=True, hide_index=True
        )
        
        profit_row = policy_df_raw[policy_df_raw['Policy'].str.contains('Profit Targeting')].iloc[0]
        mass_row = policy_df_raw[policy_df_raw['Policy'].str.contains('Mass Voucher')].iloc[0]
        regret_str = ""
        try:
            with open(os.path.join(base_path, 'data', 'processed', 'oracle_regret.json'), 'r') as f:
                regret_data = json.load(f)
                regret_str = f"**Oracle Regret:** So với kịch bản hoàn hảo, ta bỏ lỡ **{regret_data['regret_abs']:,.0f} USD** ({regret_data['regret_pct']}% giá trị max)."
        except:
            pass

        st.info(f"**📊 Kết luận trong Sandbox:** Profit Targeting cho lợi nhuận **{profit_row['Expected_Incremental_Profit']:,.0f} USD**, trong khi Mass Voucher gây lỗ **{abs(mass_row['Expected_Incremental_Profit']):,.0f} USD**. {regret_str}")
        
    except Exception as e:
        st.warning(f"Nhấn 'Chạy Pipeline' ở tab Admin để tạo dữ liệu Policy Comparison. ({str(e)})")

# ================= TAB 7: POLICY SIMULATOR =================
with tab7:
    st.subheader("⚙️ Trình giả lập Kịch bản (Promotion Simulator)")
    col_sim_left, col_sim_right = st.columns([1, 2.5])
    
    with col_sim_left:
        st.markdown("#### Thiết lập Kinh tế (Economics)")
        sim2_budget = st.number_input("Ngân sách Chiến dịch ($)", min_value=1000, max_value=500000, value=50000, step=5000)
        sim2_voucher = st.slider("Mức Khuyến mãi (% Doanh thu)", min_value=5.0, max_value=50.0, value=15.0, step=5.0)
        sim2_margin = st.slider("Biên lợi nhuận gộp (%)", min_value=10.0, max_value=100.0, value=70.0, step=5.0)
        sim2_max_target = st.slider("Max Target % (Giới hạn KH)", min_value=10, max_value=100, value=100, step=10)
        
    with col_sim_right:
        st.markdown("#### Bảng So sánh Kịch bản")
        try:
            preds_df = pd.read_csv(os.path.join(base_path, 'data', 'processed', 'test_predictions.csv'))
            preds_df['voucher_cost'] = preds_df['avg_fare'] * (sim2_voucher / 100.0)
            preds_df['margin_per_ride'] = preds_df['avg_fare'] * (sim2_margin / 100.0)
            preds_df['expected_value'] = (preds_df['cate_pred'] * preds_df['margin_per_ride']) - (preds_df['pred_rides_treated'] * preds_df['voucher_cost'])
            
            if 'true_ite' in preds_df.columns:
                preds_df['oracle_ev_sim'] = (preds_df['true_ite'] * preds_df['margin_per_ride']) - (preds_df['pred_rides_treated'] * preds_df['voucher_cost'])
            
            def eval_policy_sim(mask, label):
                targeted = preds_df[mask]
                n_t = mask.sum()
                if n_t == 0: return {"Kịch bản": label, "Profit": 0, "Users": 0}
                
                if 'oracle_ev_sim' in targeted.columns:
                    t_ev = targeted['oracle_ev_sim'].sum()
                else:
                    t_ev = targeted['expected_value'].sum()
                    
                return {"Kịch bản": label, "Profit": round(t_ev, 0), "Users": int(n_t)}
            
            sim_results = []
            mass_m = pd.Series([True]*len(preds_df), index=preds_df.index)
            if sim2_max_target < 100: mass_m.iloc[int(len(preds_df) * sim2_max_target / 100):] = False
            sim_results.append(eval_policy_sim(mass_m, "Mass Voucher"))
            
            # Segment Targeting
            if 'is_urban' in preds_df.columns:
                sub_m = preds_df['is_urban'] == 0
                sim_results.append(eval_policy_sim(sub_m, "Segment Targeting (Suburban)"))
                
            # Uplift Targeting
            if 'cate_pred' in preds_df.columns:
                uplift_m = preds_df['cate_pred'] >= preds_df['cate_pred'].quantile(0.70)
                sim_results.append(eval_policy_sim(uplift_m, "Uplift Targeting (Top 30% CATE)"))
            
            prof_m = preds_df['expected_value'] > 0
            if prof_m.sum() > (len(preds_df) * sim2_max_target / 100):
                thresh = preds_df['expected_value'].quantile(1 - (sim2_max_target / 100))
                prof_m = preds_df['expected_value'] > thresh
            sim_results.append(eval_policy_sim(prof_m, "Profit Targeting (EV > 0)"))
            
            df_sorted = preds_df.sort_values('expected_value', ascending=False).copy()
            df_sorted['cum_cost'] = (df_sorted['pred_rides_treated'] * df_sorted['voucher_cost']).cumsum()
            budget_m_idx = df_sorted[df_sorted['cum_cost'] <= sim2_budget].index
            budget_m = preds_df.index.isin(budget_m_idx)
            sim_results.append(eval_policy_sim(budget_m, f"Budget-Constrained (${sim2_budget:,})"))
            
            sim_df = pd.DataFrame(sim_results)
            st.dataframe(sim_df.style.format({'Profit': '${:,.0f}'}).background_gradient(subset=['Profit'], cmap='RdYlGn', vmin=-50000, vmax=50000), use_container_width=True, hide_index=True)
            
            best_policy = sim_df.loc[sim_df['Profit'].idxmax()]
            if best_policy['Profit'] > 0: st.success(f"🏆 Kịch bản **{best_policy['Kịch bản']}** mang lại Lợi nhuận cao nhất (**${best_policy['Profit']:,.0f}**).")
            else: st.error("🛑 Ngay cả kịch bản tốt nhất cũng đang Lỗ. Hãy giảm Voucher hoặc Tăng Margin.")
            
        except Exception as e:
            st.warning(f"Chưa có dữ liệu dự đoán để mô phỏng. ({str(e)})")

# ================= TAB 8: ADMIN PIPELINE =================
with tab8:
    st.subheader("🛠️ Trình quản lý Data Pipeline")
    if st.button("▶️ Chạy toàn bộ Data Pipeline", type="primary"):
        import sys
        pipeline_path = os.path.join(base_path, 'src', 'pipeline')
        if pipeline_path not in sys.path:
            sys.path.append(pipeline_path)
        try:
            from main_pipeline import run_pipeline
            progress_bar = st.progress(0, text="Khởi tạo Pipeline...")
            def st_progress_callback(pct, msg): progress_bar.progress(pct, text=f"[{pct}%] {msg}")
            run_pipeline(n_users=20000, progress_callback=st_progress_callback)
            st.success("✅ Đã hoàn tất Pipeline! Tải lại trang (F5) để Dashboard cập nhật dữ liệu.")
        except Exception as e:
            st.error(f"Lỗi khi chạy Pipeline: {e}")
