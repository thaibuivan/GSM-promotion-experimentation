import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
import os
import json
import statsmodels.api as sm

# Page Config
st.set_page_config(page_title="Promotion Experimentation Framework", layout="wide")

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

st.markdown('<p class="executive-title">Promotion Experimentation & Personalization Framework</p>', unsafe_allow_html=True)
st.markdown("### Customer-Level Prototype for Causal Targeting and Policy Evaluation")
st.info("Project này đóng gói một workflow đi từ causal evidence đến customer-level policy decision. Current prototype giải quyết WHO ở cấp customer; production evolution là session-aware WHO + WHEN và sau đó voucher-level WHO + WHEN + HOW MUCH.")
st.caption("🎯 **Evaluation Population:** Dữ liệu mô phỏng tập trung vào 30 ngày (Synthetic Causal Benchmark). Không dùng để so sánh số tiền tuyệt đối trực tiếp giữa các quần thể khác nhau.")

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
    st.error(f"Không tìm thấy dữ liệu. Lỗi: {str(e)}")
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
    VOUCHER_CAP = config['economics'].get('voucher_cap', 3.0)
except:
    DISCOUNT_PERCENT = 15.0
    MARGIN_PERCENT = 70.0
    VOUCHER_CAP = 3.0

df_treat = df[df['treatment_rand'] == 1]
df_ctrl = df[df['treatment_rand'] == 0]

def calc_cost(fare, rate_pct):
    raw_cost = fare * (rate_pct / 100.0)
    return np.minimum(raw_cost, VOUCHER_CAP)

def render_breadcrumb(active_step):
    steps = [
        ("Business Problem", "1. Business Problem"),
        ("Causal Evidence", "2. Causal Evidence"),
        ("User Heterogeneity", "3. User Heterogeneity"),
        ("Policy", "4. Policy Simulator"),
        ("Robustness", "5. Robustness")
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
    "1. Business Problem", 
    "2. Causal Evidence", 
    "3. User Heterogeneity", 
    "4. Policy Simulator", 
    "5. Robustness"
])

# ================= TAB 1: BUSINESS PROBLEM =================
with tab1:
    render_breadcrumb("Business Problem")
    st.subheader("Mass promotion có tạo expected incremental profit không?")
    st.markdown("Thay vì nhìn vào tỷ lệ mở app, chúng ta nhìn trực tiếp vào **Lợi nhuận Biên (Incremental Profit)** khi phát Voucher đại trà dưới sandbox assumptions.")
    
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
    c1.metric("Tổng chi phí (Burn)", f"${cost_per_user * total_users:,.0f}")
    c2.metric("Doanh thu tăng thêm", f"${incremental_rev_per_user * total_users:,.0f}")
    c3.metric("Lợi nhuận Ròng", f"${total_net_profit:,.0f}")
    c4.metric("ROI Tổng thể", f"{overall_roi:.1f}%")
    
    st.error("**Kết luận:** Mass Voucher tạo incremental demand nhưng economics âm dưới assumptions hiện tại. Mass deployment không phải candidate policy phù hợp.")

    col_chart1, col_chart2 = st.columns(2)
    with col_chart1:
        st.markdown("#### Cơ cấu Lợi nhuận / Khách hàng")
        fig_waterfall = go.Figure(go.Waterfall(
            name = "20", orientation = "v",
            measure = ["relative", "relative", "total"],
            x = ["Lợi nhuận gộp sinh thêm", "Chi phí Voucher (Cannibalized)", "Lợi nhuận Ròng"],
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
        st.markdown("#### Phân rã Chi phí Trợ giá (Minh họa)")
        st.caption("Đây là mô phỏng phân rã trên sandbox, không phải ước lượng cannibalization chính thức trên production.")
        
        organic_cost_per_ride = calc_cost(df_ctrl['avg_fare_per_trip'], DISCOUNT_PERCENT)
        avg_burn_organic = (df_ctrl['Y_rand'] * organic_cost_per_ride).mean()
        avg_burn_total = df_treat['discount_cost_30d'].mean()
        avg_burn_inc = max(avg_burn_total - avg_burn_organic, 0)
        
        wasted_burn = avg_burn_organic * total_users
        effective_burn = avg_burn_inc * total_users
        total_burn = wasted_burn + effective_burn
        
        fig_bar = go.Figure()
        fig_bar.add_trace(go.Bar(
            y=['Ngân sách Khuyến mãi'], x=[wasted_burn],
            name='Burn trên rides nền', orientation='h', marker_color='#FF4B4B',
            text=f"${wasted_burn:,.0f}", textposition='inside'
        ))
        fig_bar.add_trace(go.Bar(
            y=['Ngân sách Khuyến mãi'], x=[effective_burn],
            name='Burn trên incremental rides', orientation='h', marker_color='#00CC96',
            text=f"${effective_burn:,.0f}", textposition='inside'
        ))
        fig_bar.update_layout(
            plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color='#F8FAFC'), margin=dict(l=20, r=20, t=40, b=20),
            height=200, barmode='stack',
            legend=dict(orientation="h", yanchor="bottom", y=1.1, xanchor="center", x=0.5))
        fig_bar.update_xaxes(title="Tổng chi phí Voucher ($)", showgrid=False)
        st.plotly_chart(fig_bar, use_container_width=True)
        st.info("Khuyến mãi đại trà tạo thêm cuốc xe, nhưng phần lớn burn có thể rơi vào rides nền vốn đã có khả năng phát sinh nếu không phát voucher.")

# ================= TAB 2: CAUSAL EVIDENCE =================
with tab2:
    render_breadcrumb("Causal Evidence")
    
    st.markdown("#### Experiment Health Gate")
    observed_treatment = len(df_treat)
    observed_control = len(df_ctrl)
    total = observed_treatment + observed_control
    st.success("**Prior Experiment Validation Summary: PASS**\n\nBased on Week 4 A/A Monte Carlo, SRM and covariate-balance checks.")
    
    st.markdown("---")
    st.subheader("Voucher có thật sự tạo Causal Effect, và lift có đồng đều không?")
    st.markdown("Trước khi cá nhân hóa, ta cần chứng minh Voucher thực sự tạo ra lượng cầu tăng thêm mang tính nhân quả.")
    
    raw_ate = df_treat['Y_rand'].mean() - df_ctrl['Y_rand'].mean()
    
    X = sm.add_constant(df[['treatment_rand', 'monthly_rides_history']])
    y = df['Y_rand']
    model = sm.OLS(y, X).fit(cov_type='HC1')
    adj_ate = model.params['treatment_rand']
    p_val = model.pvalues['treatment_rand']
    ci_low = model.conf_int().loc['treatment_rand', 0]
    ci_high = model.conf_int().loc['treatment_rand', 1]
    
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Raw ATE", f"{raw_ate:.2f} chuyến", help="Chênh lệch trung bình đơn thuần")
    c2.metric("Adjusted ATE", f"{adj_ate:.2f} chuyến", help="Baseline-adjusted estimator for improved precision.")
    c3.metric("95% CI (Adjusted)", f"[{ci_low:.2f} , {ci_high:.2f}]")
    c4.metric("P-value", f"{p_val:.4f}", "Statistically Significant" if p_val < 0.05 else "Not Significant")

    with st.expander("Technical Method - Causal Estimation"):
        st.markdown("""
        **Causal Regression Model:**
        `Y_i = β₀ + β₁T_i + β₂Baseline_i + ε_i`
        
        > **Randomization is the identification strategy. Baseline adjustment is used to improve precision, not to repair confounding.**
        """)

    st.markdown("#### Phân tích theo Phân khúc (Segment Economics)")
    roi_data = []
    for p in df['persona'].unique():
        t = df[(df['persona'] == p) & (df['treatment_rand'] == 1)]
        c = df[(df['persona'] == p) & (df['treatment_rand'] == 0)]
        if len(t) > 0 and len(c) > 0:
            rev_c = c['gross_revenue_30d'].mean()
            rev_t = t['gross_revenue_30d'].mean()
            d_rev = rev_t - rev_c
            gross_profit = d_rev * (MARGIN_PERCENT / 100.0)
            cost = t['discount_cost_30d'].mean()
            roi = (gross_profit - cost) / cost * 100 if cost > 0 else 0
            roi_data.append({
                'Phân khúc (Persona)': p, 
                'Base GMV ($)': round(rev_c, 2),
                'Inc GMV ($)': round(d_rev, 2),
                'Burn ($)': round(cost, 2),
                'Net Profit ($)': round(gross_profit - cost, 2),
                'ROI (%)': round(roi, 1)
            })
    roi_df = pd.DataFrame(roi_data).sort_values(by='ROI (%)', ascending=False)
    
    st.dataframe(roi_df.style.format(precision=1)
             .background_gradient(subset=['ROI (%)'], cmap='RdYlGn', vmin=-100, vmax=50), 
             use_container_width=True, hide_index=True)

    st.info("**Kết luận:** Average effect tồn tại nhưng business outcome khác nhau giữa các nhóm; segment targeting cơ bản vẫn chưa tối ưu được Lợi nhuận.")

# ================= TAB 3: USER HETEROGENEITY =================
with tab3:
    render_breadcrumb("User Heterogeneity")
    st.subheader("Bóc tách độ nhạy cảm (Responsiveness)")
    st.markdown("Tín hiệu Uplift phân tách người dùng dựa trên phản ứng thực tế, nhưng Response chưa đồng nghĩa với Profit.")
    
    col_c1, col_c2 = st.columns(2)
    with col_c1:
        st.markdown("#### Phân phối độ nhạy cảm (CATE Distribution)")
        fig_cate = px.histogram(preds_df, x='cate_pred', nbins=50, 
                                title="Phân bố CATE (Chuyến đi dự kiến tăng thêm)",
                                color_discrete_sequence=['#555555'])
        fig_cate.add_vline(x=0, line_dash="dash", line_color="#FF4B4B")
        fig_cate.update_layout(**chart_layout)
        fig_cate.update_xaxes(title="CATE (Causal Effect)")
        fig_cate.update_yaxes(title="Số lượng User")
        st.plotly_chart(fig_cate, use_container_width=True)
        st.caption("Simplified R-Learner-style Model dự báo độ nhạy cảm tại cấp độ khách hàng.")
        try:
            qini_summary = pd.read_csv(os.path.join(base_path, 'data', 'processed', 'qini_curve.csv'))
            area_model = np.trapz(qini_summary['qini_uplift'], qini_summary['pct_targeted'])
            area_random = np.trapz(qini_summary['random_uplift'], qini_summary['pct_targeted'])
            qini_coef = (area_model - area_random) / abs(area_random) if abs(area_random) > 1e-9 else np.nan
            st.metric("Qini Coef", f"{qini_coef:.3f}", "Ranking > random" if qini_coef > 0 else "Needs review")
        except Exception:
            st.caption("Qini Coef chưa khả dụng. Hãy chạy lại policy export pipeline nếu cần.")
        
    with col_c2:
        st.markdown("#### Cầu nối Lợi nhuận (Expected Value Bridge)")
        st.info("""
        **Chuyển đổi Signal thành Decision:**
        
        `Expected Profit = [CATE * (Lợi nhuận/Cuốc)] - [Tổng chuyến dự kiến * (Chi phí Voucher/Cuốc)]`
        
        **Nguyên lý Targeting:** Chỉ giữ lại tập khách hàng có **Expected Incremental Profit > 0**. Nếu CATE cao nhưng baseline trips quá lớn, chi phí khuyến mãi sẽ nuốt chửng lợi nhuận biên.
        """)
        
    with st.expander("Technical Method - Heterogeneous Treatment Estimation"):
        st.markdown("""
        **Quy trình Mô hình hóa (Residualization Flow):**
        `X + T + Y` ➔ `Outcome Residualization` ➔ `Treatment Residualization` ➔ `R-Learner-style Effect Model` ➔ `CATE Ranking`
        
        **Technical Equations:**
        `m(X) = E[Y|X]`
        `e(X) = P(T=1|X)`
        `Y_tilde = Y - m(X)`
        `T_tilde = T - e(X)`
        
        > **Current implementation does not use cross-fitting, so it is described as a simplified R-Learner-style residual learner rather than full DML.**
        """)

# ================= TAB 4: POLICY SIMULATOR =================
with tab4:
    render_breadcrumb("Policy")
    st.subheader("Lựa chọn Candidate Policy dưới Giới hạn Kinh tế")
    
    st.markdown("""
    <div style='display: flex; justify-content: space-between; align-items: center; background-color: #2E2E2E; padding: 15px; border-radius: 6px; margin-bottom: 20px;'>
        <div style='text-align: center; flex: 1;'><b>MODEL LAYER</b><br><span style='color:#ccc; font-size: 0.9em;'>Predicted CATE</span></div>
        <div style='font-size: 1.5rem; color: #00E5FF;'>➔</div>
        <div style='text-align: center; flex: 1;'><b>ECONOMICS LAYER</b><br><span style='color:#ccc; font-size: 0.9em;'>Incremental Margin - Voucher Cost</span></div>
        <div style='font-size: 1.5rem; color: #00E5FF;'>➔</div>
        <div style='text-align: center; flex: 1;'><b>POLICY LAYER</b><br><span style='color:#ccc; font-size: 0.9em;'>Target / Do Not Target / Budget Rule</span></div>
    </div>
    """, unsafe_allow_html=True)
    
    st.caption("**Model output is not the final decision; economics and policy constraints translate prediction into action.**")
    st.latex(r"EV_i = CATE_i \times AvgFare_i \times MarginRate - PredictedTreatedRides_i \times VoucherCostPerRide_i")
    
    col_sim_left, col_sim_right = st.columns([1, 3])
    
    with col_sim_left:
        st.markdown("#### Assumptions")
        sim_voucher = st.slider("Mức Khuyến mãi (%)", min_value=5.0, max_value=50.0, value=15.0, step=1.0)
        sim_margin = st.slider("Biên lợi nhuận (%)", min_value=10.0, max_value=100.0, value=70.0, step=5.0)
        sim_budget = st.number_input("Ngân sách (Budget $)", min_value=1000, max_value=500000, value=50000, step=5000)
        
    with col_sim_right:
        st.markdown("#### Bảng Quyết định Chính sách (Policy Decision)")
        preds_df['voucher_cost'] = calc_cost(preds_df['avg_fare'], sim_voucher)
        preds_df['margin_per_ride'] = preds_df['avg_fare'] * (sim_margin / 100.0)
        preds_df['expected_value'] = (preds_df['cate_pred'] * preds_df['margin_per_ride']) - (preds_df['pred_rides_treated'] * preds_df['voucher_cost'])
        
        total_pop = len(preds_df)
        
        def eval_policy_sim(mask, label):
            targeted = preds_df[mask]
            n_t = mask.sum()
            target_pct = (n_t / total_pop) * 100 if total_pop > 0 else 0
            
            if n_t == 0: 
                return {"Candidate Policy": label, "Target %": 0.0, "Inc Rides": 0.0, "Burn ($)": 0, "Profit ($)": 0, "ROI (%)": 0.0}
            
            pred_inc_rides = targeted['cate_pred'].sum()
            pred_burn = (targeted['pred_rides_treated'] * targeted['voucher_cost']).sum()
            pred_profit = targeted['expected_value'].sum()
            pred_roi = (pred_profit / pred_burn * 100) if pred_burn > 0 else 0
            
            return {
                "Candidate Policy": label, 
                "Target %": round(target_pct, 1), 
                "Inc Rides": round(pred_inc_rides, 1), 
                "Burn ($)": round(pred_burn, 0), 
                "Profit ($)": round(pred_profit, 0),
                "ROI (%)": round(pred_roi, 1)
            }
        
        sim_results = []
        no_m = pd.Series([False]*len(preds_df), index=preds_df.index)
        sim_results.append(eval_policy_sim(no_m, "0. No Voucher"))
        
        mass_m = pd.Series([True]*len(preds_df), index=preds_df.index)
        sim_results.append(eval_policy_sim(mass_m, "1. Mass Voucher"))
        
        if 'persona' in preds_df.columns:
            sub_m = preds_df['persona'].str.contains('Suburban', case=False, na=False)
            sim_results.append(eval_policy_sim(sub_m, "2. Segment Targeting (Suburban)"))
            
        uplift_thresh = preds_df['cate_pred'].quantile(0.7)
        uplift_m = preds_df['cate_pred'] >= uplift_thresh
        sim_results.append(eval_policy_sim(uplift_m, "3. Uplift Targeting (Top 30% CATE)"))
        
        prof_m = preds_df['expected_value'] > 0
        sim_results.append(eval_policy_sim(prof_m, "4. Profit Targeting"))
        
        prof_df_sim = preds_df[preds_df['expected_value'] > 0].copy()
        df_sorted = prof_df_sim.sort_values('expected_value', ascending=False)
        df_sorted['cum_cost'] = (df_sorted['pred_rides_treated'] * df_sorted['voucher_cost']).cumsum()
        budget_m_idx = df_sorted[df_sorted['cum_cost'] <= sim_budget].index
        budget_m = preds_df.index.isin(budget_m_idx)
        sim_results.append(eval_policy_sim(budget_m, "5. Budget Greedy"))
        
        sim_df = pd.DataFrame(sim_results)
        # Handle tooltip column if needed (Streamlit dataframe tooltip isn't native for single cells easily without extra code, we will just use a helper icon or text).
        
        st.dataframe(sim_df.drop(columns=['tooltip'], errors='ignore').style.format({
            'Target %': '{:.1f}%',
            'Inc Rides': '{:,.1f}',
            'Burn ($)': '${:,.0f}',
            'Profit ($)': '${:,.0f}',
            'ROI (%)': '{:.1f}%'
        }).background_gradient(subset=['Profit ($)'], cmap='RdYlGn', vmin=-5000, vmax=15000), use_container_width=True, hide_index=True)
        
        st.caption("ℹ️ *5. Budget Greedy: Current budget allocation is a greedy heuristic that ranks positive-EV users; it is not an exact combinatorial optimum.*")
        
        best_profit = sim_df['Profit ($)'].max()
        if best_profit > 0:
            best_policy = sim_df.loc[sim_df['Profit ($)'].idxmax(), 'Candidate Policy']
            st.success(f"**Recommended Candidate under Current Sandbox Assumptions:** {best_policy}")
        else:
            st.error("**Recommended Outside Option:** No Voucher")

# ================= TAB 5: ROBUSTNESS =================
with tab5:
    render_breadcrumb("Robustness")
    st.subheader("Deployment Gates & Enterprise Roadmap")
    st.markdown("Bất kỳ Candidate Policy nào cũng cần vượt qua rào cản Robustness trước khi triển khai Pilot thực tế.")
    
    st.markdown("#### 1. Deployment Stress Gates")
    g1, g2, g3, g4 = st.columns(4)
    g1.success("✅ **Sample Scale-Up**\n\nATE remains stable; confidence intervals narrow as N increases (10k ➔ 50k ➔ 100k).")
    g2.success("✅ **Null Effect Test**\n\nWhen true effect = 0, estimates remain centered near zero and false-positive behavior stays around the designed Type-I error in simulation.")
    g3.warning("⚠️ **Treatment Imbalance**\n\nPoint estimates remain broadly stable; uncertainty increases because one arm contains fewer observations.")
    g4.info("ℹ️ **Noise Injection**\n\nAdditional exogenous noise weakens signal and increases uncertainty without systematic directional bias in expectation.")
    
    st.caption("**Stable under the synthetic scenarios tested — not evidence of production robustness.**")
    
    with st.expander("Stress Test Interpretation"):
        st.markdown("""
        | Stress | Changed Variable | Expected Statistical Behavior |
        |---|---|---|
        | Sample Scale | N | CI narrows |
        | Null Effect | True ATE | Estimate centered near 0 |
        | 90/10 Split | Treatment allocation | SE increases |
        | Noise | Outcome variance | Signal weakens |
        
        > **Stress testing here checks whether the pipeline behaves as statistical theory suggests, not whether it is already production-robust.**
        """)
    
    st.markdown("---")
    st.markdown("#### 2. Enterprise Maturity Roadmap")
    
    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown("""
        <div class='roadmap-card'>
            <div class='roadmap-title'>CURRENT</div>
            <div class='roadmap-subtitle'>Customer-Level</div>
            <div style='color: #fff; font-size: 1.2rem; margin: 10px 0;'>WHO?</div>
            <p>Who should receive a voucher?</p>
        </div>
        """, unsafe_allow_html=True)
    with c2:
        st.markdown("""
        <div class='roadmap-card'>
            <div class='roadmap-title' style='color:#ccc;'>NEXT</div>
            <div class='roadmap-subtitle'>Session-Level</div>
            <div style='color: #fff; font-size: 1.2rem; margin: 10px 0;'>WHO + WHEN?</div>
            <p>Who should receive it, and in which context/session?</p>
        </div>
        """, unsafe_allow_html=True)
    with c3:
        st.markdown("""
        <div class='roadmap-card'>
            <div class='roadmap-title' style='color:#ccc;'>FUTURE</div>
            <div class='roadmap-subtitle'>Voucher Personalization</div>
            <div style='color: #fff; font-size: 1.2rem; margin: 10px 0;'>WHO + WHEN + HOW MUCH?</div>
            <p>What voucher amount maximizes expected incremental value?</p>
        </div>
        """, unsafe_allow_html=True)
        
    with st.expander("Lightweight Technical Architecture"):
        st.markdown("""
        `Data Layer` ➔ `Experiment Validation` ➔ `Causal Estimation` ➔ `Economics Engine` ➔ `Policy Engine` ➔ `Decision Interface`
        
        **CURRENT:** Offline / Customer-Level / Synthetic
        **NEXT:** Session/Event Features / Session-Level
        **FUTURE:** Voucher Amount Decision / Monitoring
        
        > **Illustrative framework evolution - not the current GSM production architecture.**
        """)
    
    with st.expander("Model Technical Detail (Qini vs Calibration)"):
        col_qini, col_calib = st.columns(2)
        with col_qini:
            st.markdown("#### Qini Curve (Ranking Metric)")
            st.caption("Hỏi: Model có đưa responsive users lên top tốt hơn random không?")
            try:
                qini_df = pd.read_csv(os.path.join(base_path, 'data', 'processed', 'qini_curve.csv'))
                fig_qini = go.Figure()
                fig_qini.add_trace(go.Scatter(x=qini_df['pct_targeted'], y=qini_df['qini_uplift'], mode='lines', name='Model', line=dict(color='#00E5FF', width=3)))
                fig_qini.add_trace(go.Scatter(x=qini_df['pct_targeted'], y=qini_df['random_uplift'], mode='lines', name='Random Baseline', line=dict(color='rgba(255,255,255,0.3)', dash='dash', width=2)))
                fig_qini.update_layout(**chart_layout, height=350, legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1))
                fig_qini.update_xaxes(title="% Khách hàng (Targeted)", dtick=10)
                fig_qini.update_yaxes(title="Tích lũy Số chuyến (Qini)")
                st.plotly_chart(fig_qini, use_container_width=True)
            except:
                st.warning("Chưa có dữ liệu Qini Curve.")
                
        with col_calib:
            st.markdown("#### Calibration Chart (Magnitude Diagnostic)")
            st.caption("Hỏi: Predicted CATE magnitude có sát observed benchmark theo decile không?")
            try:
                calib_df = pd.read_csv(os.path.join(base_path, 'data', 'processed', 'uplift_calibration.csv'))
                fig_cal = go.Figure()
                fig_cal.add_trace(go.Scatter(name='Predicted CATE', x=calib_df['Decile'], y=calib_df['Predicted_CATE'], mode='lines+markers', line=dict(color='#FF4B4B', width=3)))
                fig_cal.add_trace(go.Scatter(name='Observed Uplift', x=calib_df['Decile'], y=calib_df['Observed_Uplift'], mode='lines+markers', line=dict(color='#00CC96', width=2)))
                fig_cal.add_trace(go.Scatter(name='Synthetic Ground Truth', x=calib_df['Decile'], y=calib_df['Ground_Truth_CATE'], mode='lines', line=dict(color='rgba(255,255,255,0.4)', dash='dash', width=2)))
                fig_cal.update_layout(**chart_layout, height=350, legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1))
                fig_cal.update_xaxes(title="Deciles (Tốt nhất đến Kém nhất)")
                fig_cal.update_yaxes(title="Uplift trung bình")
                st.plotly_chart(fig_cal, use_container_width=True)
            except:
                st.warning("Chưa có dữ liệu Calibration.")
                
        st.info("**Useful ranking signal; magnitude calibration remains imperfect.**")
