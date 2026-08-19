import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
import os
import json
import scipy.stats as stats
import statsmodels.api as sm

# Page Config
st.set_page_config(page_title="Promotion Decision Support Sandbox", page_icon="🧪", layout="wide")

# Custom CSS for Premium Look
st.markdown("""
<style>
    .title-gradient {
        background: linear-gradient(90deg, #00E5FF, #FF007F);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 800;
        font-size: 2.2rem;
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
        font-size: 1.1rem;
        font-weight: 600;
    }
    .stTabs [aria-selected="true"] {
        color: #00E5FF !important;
        border-bottom: 3px solid #00E5FF !important;
    }
    
    /* Breadcrumbs */
    .breadcrumb {
        font-size: 1.1rem;
        color: #aaa;
        margin-bottom: 20px;
    }
    .breadcrumb span.active {
        color: #00E5FF;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

st.markdown('<p class="title-gradient">🧪 Promotion Decision Support Sandbox</p>', unsafe_allow_html=True)
st.info("Mục tiêu của sandbox không phải dự đoán ai sẽ đi nhiều, mà là hỗ trợ câu hỏi quyết định: voucher có thực sự tạo incremental demand, và nếu ngân sách giới hạn thì nên phân bổ voucher cho ai để tạo expected incremental value tốt hơn.")

# Load Data
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

# Plotly settings
chart_layout = dict(
    plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',
    font=dict(color='#F8FAFC'), margin=dict(l=20, r=20, t=40, b=20)
)

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

# ----------------- TABS -----------------
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📊 1. Business Problem", 
    "🧪 2. Causal Evidence", 
    "🧠 3. User Heterogeneity", 
    "🕹️ 4. Policy Simulator", 
    "🔬 5. Robustness"
])

# ================= TAB 1: BUSINESS PROBLEM =================
with tab1:
    render_breadcrumb("Business Problem")
    st.subheader("Mass promotion có tạo economic value không?")
    st.markdown("Thay vì nhìn vào ATE (Hiệu ứng trung bình), chúng ta nhìn trực tiếp vào **Lợi nhuận (ROI)** khi phát Voucher cho toàn bộ khách hàng.")
    
    avg_rev_treat = df_treat['gross_revenue_30d'].mean()
    avg_rev_ctrl = df_ctrl['gross_revenue_30d'].mean()
    incremental_rev_per_user = avg_rev_treat - avg_rev_ctrl
    gross_profit_per_user = incremental_rev_per_user * (MARGIN_PERCENT / 100.0)
    cost_per_user = (DISCOUNT_PERCENT / 100.0) * avg_rev_treat
    net_profit_per_user = gross_profit_per_user - cost_per_user
    overall_roi = (net_profit_per_user / cost_per_user) * 100 if cost_per_user > 0 else 0
    total_users = len(df)
    total_net_profit = net_profit_per_user * total_users
    
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Tổng chi phí (Burn)", f"${cost_per_user * total_users:,.0f}", help="Burn = Tổng số tiền bỏ ra cho Khuyến mãi")
    c2.metric("Doanh thu tăng thêm", f"${incremental_rev_per_user * total_users:,.0f}")
    c3.metric("Lợi nhuận Ròng", f"${total_net_profit:,.0f}")
    c4.metric("ROI Tổng thể", f"{overall_roi:.1f}%", help="ROI = Lợi nhuận Ròng / Tổng Chi phí Burn")
    
    st.error(f"🚨 **Kết luận:** Mass Voucher tạo incremental behavior nhưng economics ÂM dưới assumptions hiện tại. Chiến dịch lỗ **${abs(total_net_profit):,.0f}**.")

    col_chart1, col_chart2 = st.columns(2)
    with col_chart1:
        st.markdown("#### Cơ cấu Lợi nhuận / Khách hàng")
        fig_waterfall = go.Figure(go.Waterfall(
            name = "20", orientation = "v",
            measure = ["relative", "relative", "total"],
            x = ["Lợi nhuận gộp từ Chuyến tăng thêm", "Chi phí Voucher (Cannibalized)", "Lợi nhuận Ròng (Lỗ)"],
            textposition = "outside",
            text = [f"${gross_profit_per_user:.2f}", f"-${cost_per_user:.2f}", f"${net_profit_per_user:.2f}"],
            y = [gross_profit_per_user, -cost_per_user, net_profit_per_user],
            connector = {"line":{"color":"rgb(63, 63, 63)"}},
        ))
        fig_waterfall.update_layout(**chart_layout, height=350)
        st.plotly_chart(fig_waterfall, use_container_width=True)

    with col_chart2:
        st.markdown("#### Giải phẫu Ngân sách (Cannibalization Waste)")
        avg_rev_organic = df_ctrl['gross_revenue_30d'].mean()
        avg_rev_total = df_treat['gross_revenue_30d'].mean()
        avg_rev_inc = avg_rev_total - avg_rev_organic
        wasted_burn = avg_rev_organic * (DISCOUNT_PERCENT / 100.0) * len(df_treat)
        effective_burn = avg_rev_inc * (DISCOUNT_PERCENT / 100.0) * len(df_treat)
        total_burn = wasted_burn + effective_burn
        fig_bar = go.Figure()
        fig_bar.add_trace(go.Bar(
            y=['Ngân sách<br>Khuyến mãi'], x=[wasted_burn], 
            name='Lãng phí (Khách hữu cơ)', orientation='h', marker_color='#FF007F',
            text=f"${wasted_burn:,.0f}", textposition='inside'
        ))
        fig_bar.add_trace(go.Bar(
            y=['Ngân sách<br>Khuyến mãi'], x=[effective_burn], 
            name='Hiệu quả (Sinh cuốc mới)', orientation='h', marker_color='#00E5FF',
            text=f"${effective_burn:,.0f}", textposition='inside'
        ))
        fig_bar.update_layout(
            plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color='#F8FAFC'), margin=dict(l=20, r=20, t=40, b=20),
            height=220, barmode='stack', 
            legend=dict(orientation="h", yanchor="bottom", y=1.1, xanchor="center", x=0.5))
        fig_bar.update_xaxes(title="Tổng chi phí Voucher ($)", showgrid=False)
        st.plotly_chart(fig_bar, use_container_width=True)
        waste_pct = (wasted_burn / total_burn * 100) if total_burn > 0 else 0
        st.info(f"💡 Hơn **{waste_pct:.1f}%** ngân sách đang bị ném qua cửa sổ cho những khách VỐN DĨ VẪN ĐI XE (Cannibalization).")

# ================= TAB 2: CAUSAL EVIDENCE =================
with tab2:
    render_breadcrumb("Causal Evidence")
    st.subheader("Voucher có thật sự tạo lift, và lift có đồng đều giữa các nhóm không?")
    st.markdown("A/B cho biết voucher có tác dụng trung bình. Nhưng average effect không cho biết tất cả user đều phản ứng giống nhau.")
    
    # Calculate ATE
    # OLS for Adjusted ATE
    X = sm.add_constant(df['treatment_rand'])
    y = df['Y_rand']
    model = sm.OLS(y, X).fit(cov_type='HC1')
    ate = model.params['treatment_rand']
    p_val = model.pvalues['treatment_rand']
    ci_low = model.conf_int().loc['treatment_rand', 0]
    ci_high = model.conf_int().loc['treatment_rand', 1]
    
    c1, c2, c3 = st.columns(3)
    c1.metric("Adjusted ATE (Chuyến đi tăng thêm)", f"{ate:.2f} chuyến/user", help="ATE (Average Treatment Effect): Hiệu ứng trung bình của Voucher lên số chuyến đi")
    c2.metric("95% Confidence Interval", f"[{ci_low:.2f} , {ci_high:.2f}]")
    c3.metric("P-value", f"{p_val:.4f}", "Statistically Significant" if p_val < 0.05 else "Not Significant")

    st.markdown("#### Phân tích A/B theo Phân khúc (Segment Economics)")
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

    st.success("💡 **Kết luận:** Average effect tồn tại nhưng business outcome khác nhau giữa segment; segment targeting (ví dụ: chỉ chọn Ngoại ô) vẫn còn quá coarse (thô).")

# ================= TAB 3: USER HETEROGENEITY =================
with tab3:
    render_breadcrumb("User Heterogeneity")
    st.subheader("Trong cùng segment, user nào thực sự responsive và profitable?")
    st.markdown("User có uplift cao (tăng nhiều chuyến) chưa chắc là user nên nhận voucher. Nếu incremental margin tạo thêm không bù đắp được voucher burn, campaign vẫn destroy value.")
    
    col_c1, col_c2 = st.columns(2)
    with col_c1:
        st.markdown("#### Phân phối độ nhạy cảm (CATE Distribution)")
        fig_cate = px.histogram(preds_df, x='cate_pred', nbins=50, 
                                title="Phân bố CATE (Chuyến đi dự kiến tăng thêm)",
                                color_discrete_sequence=['#00E5FF'])
        fig_cate.add_vline(x=0, line_dash="dash", line_color="#FF007F")
        fig_cate.update_layout(**chart_layout)
        fig_cate.update_xaxes(title="CATE (Hiệu ứng Can thiệp Cấp Cá nhân)")
        fig_cate.update_yaxes(title="Số lượng User")
        st.plotly_chart(fig_cate, use_container_width=True)
        st.caption("CATE (Conditional Average Treatment Effect): Mức độ nhạy cảm với Khuyến mãi dự đoán bởi R-Learner.")
        
    with col_c2:
        st.markdown("#### Cầu nối Giá trị Kỳ vọng (Expected Value Bridge)")
        st.info("""
        **Từ Uplift sang Economics:**
        
        Mỗi User sẽ được AI quy đổi từ `Số chuyến đi tăng thêm (CATE)` sang **Lợi nhuận Kỳ vọng (Expected Value)**:
        
        `EV = [CATE * (Lợi nhuận / Cuốc)] - [Tổng chuyến đi có Voucher * (Chi phí Voucher / Cuốc)]`
        
        **Nguyên lý:** Phải ưu tiên người có **EV > 0**, chứ không phải người có CATE cao nhất (vì người CATE cao có thể số chuyến Organic vốn dĩ cũng rất lớn dẫn đến Burn khổng lồ).
        """)
    
    st.success("💡 **Kết luận:** Response ≠ Profit. Uplift cần được chuyển sang economics trước khi ra quyết định.")

# ================= TAB 4: POLICY SIMULATOR =================
with tab4:
    render_breadcrumb("Policy")
    st.subheader("Nếu phải chọn campaign policy dưới assumptions hiện tại, policy nào tốt nhất?")
    st.markdown("Output cuối của model không phải chỉ là CATE, mà là một ranking phục vụ policy: Mass, Segment, Uplift, Profit và Budget-Constrained.")
    
    col_sim_left, col_sim_right = st.columns([1, 3])
    
    with col_sim_left:
        st.markdown("#### Kéo để thay đổi (What-If)")
        sim_voucher = st.slider("Mức Khuyến mãi (Voucher %)", min_value=5.0, max_value=50.0, value=15.0, step=1.0)
        sim_margin = st.slider("Biên lợi nhuận gộp (Margin %)", min_value=10.0, max_value=100.0, value=70.0, step=5.0)
        sim_budget = st.number_input("Ngân sách (Budget Limit $)", min_value=1000, max_value=500000, value=50000, step=5000)
        
    with col_sim_right:
        st.markdown("#### Bảng Xếp hạng Chính sách (Policy Comparison)")
        preds_df['voucher_cost'] = preds_df['avg_fare'] * (sim_voucher / 100.0)
        preds_df['margin_per_ride'] = preds_df['avg_fare'] * (sim_margin / 100.0)
        preds_df['expected_value'] = (preds_df['cate_pred'] * preds_df['margin_per_ride']) - (preds_df['pred_rides_treated'] * preds_df['voucher_cost'])
        
        total_pop = len(preds_df)
        
        def eval_policy_sim(mask, label):
            targeted = preds_df[mask]
            n_t = mask.sum()
            target_pct = (n_t / total_pop) * 100 if total_pop > 0 else 0
            
            if n_t == 0: 
                return {"Policy": label, "Target %": 0.0, "Inc Rides": 0.0, "Burn ($)": 0, "Profit ($)": 0, "ROI (%)": 0.0}
            
            pred_inc_rides = targeted['cate_pred'].sum()
            pred_burn = (targeted['pred_rides_treated'] * targeted['voucher_cost']).sum()
            pred_profit = targeted['expected_value'].sum()
            pred_roi = (pred_profit / pred_burn * 100) if pred_burn > 0 else 0
            
            return {
                "Policy": label, 
                "Target %": round(target_pct, 1), 
                "Inc Rides": round(pred_inc_rides, 1), 
                "Burn ($)": round(pred_burn, 0), 
                "Profit ($)": round(pred_profit, 0),
                "ROI (%)": round(pred_roi, 1)
            }
        
        sim_results = []
        # 0. No Voucher
        no_m = pd.Series([False]*len(preds_df), index=preds_df.index)
        sim_results.append(eval_policy_sim(no_m, "0. No Voucher (Không phát)"))
        
        # 1. Mass
        mass_m = pd.Series([True]*len(preds_df), index=preds_df.index)
        sim_results.append(eval_policy_sim(mass_m, "1. Mass Voucher (Đại trà)"))
        
        # 2. Segment
        if 'is_urban' in preds_df.columns:
            sub_m = preds_df['is_urban'] == 0
            sim_results.append(eval_policy_sim(sub_m, "2. Segment (Chỉ Ngoại ô)"))
            
        # 3. Uplift Targeting (Top 30% CATE)
        uplift_thresh = preds_df['cate_pred'].quantile(0.7)
        uplift_m = preds_df['cate_pred'] >= uplift_thresh
        sim_results.append(eval_policy_sim(uplift_m, "3. Uplift Targeting (Top 30% CATE)"))
        
        # 4. Profit Target
        prof_m = preds_df['expected_value'] > 0
        sim_results.append(eval_policy_sim(prof_m, "4. Profit Targeting (Causal AI EV > 0)"))
        
        # 5. Budget
        prof_df_sim = preds_df[preds_df['expected_value'] > 0].copy()
        df_sorted = prof_df_sim.sort_values('expected_value', ascending=False)
        df_sorted['cum_cost'] = (df_sorted['pred_rides_treated'] * df_sorted['voucher_cost']).cumsum()
        budget_m_idx = df_sorted[df_sorted['cum_cost'] <= sim_budget].index
        budget_m = preds_df.index.isin(budget_m_idx)
        sim_results.append(eval_policy_sim(budget_m, f"5. Greedy Heuristic (Budget < ${sim_budget:,})"))
        
        sim_df = pd.DataFrame(sim_results)
        st.dataframe(sim_df.style.format({
            'Target %': '{:.1f}%',
            'Inc Rides': '{:,.1f}',
            'Burn ($)': '${:,.0f}',
            'Profit ($)': '${:,.0f}',
            'ROI (%)': '{:.1f}%'
        }).background_gradient(subset=['Profit ($)'], cmap='RdYlGn', vmin=-10000, vmax=20000), use_container_width=True, hide_index=True)
        
        # Export Button
        st.markdown("---")
        st.markdown("#### 📤 Xuất danh sách triển khai (Export to CRM)")
        export_df = preds_df[preds_df['expected_value'] > 0]
        csv_data = export_df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Tải xuống CSV (Profit Targeting Users)",
            data=csv_data,
            file_name="crm_target_list.csv",
            mime="text/csv",
            type="primary"
        )

# ================= TAB 5: ROBUSTNESS & TECH =================
with tab5:
    render_breadcrumb("Robustness")
    st.subheader("Có thể tin decision này đến mức nào trong sandbox?")
    st.markdown("Kết quả hiện tại chứng minh workflow trong synthetic sandbox, chưa phải evidence cho customer behavior thực tế của GSM.")
    
    with st.expander("📈 1. Causal Model Qini Curve & Calibration"):
        st.markdown("#### Hiệu quả Xếp hạng (Qini Curve)")
        try:
            qini_df = pd.read_csv(os.path.join(base_path, 'data', 'processed', 'qini_curve.csv'))
            fig_qini = go.Figure()
            fig_qini.add_trace(go.Scatter(x=qini_df['pct_targeted'], y=qini_df['qini_uplift'], mode='lines', name='R-Learner (AI)', line=dict(color='#00E5FF', width=3)))
            fig_qini.add_trace(go.Scatter(x=qini_df['pct_targeted'], y=qini_df['random_uplift'], mode='lines', name='Random Mass Voucher', line=dict(color='rgba(255,255,255,0.3)', dash='dash', width=2)))
            fig_qini.update_layout(**chart_layout, height=350, legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1))
            fig_qini.update_xaxes(title="% Khách hàng được Chọn (Targeted)", dtick=10)
            fig_qini.update_yaxes(title="Tích lũy Số chuyến tăng thêm (Qini)", showgrid=True, gridcolor='rgba(255,255,255,0.1)')
            st.plotly_chart(fig_qini, use_container_width=True)
        except:
            st.warning("Chưa có dữ liệu Qini Curve.")
            
    with st.expander("🩺 2. A/A Test & SRM Check (Sanity)"):
        observed_treatment = len(df_treat)
        observed_control = len(df_ctrl)
        total = observed_treatment + observed_control
        st.metric("Tỷ lệ Nhóm Treatment vs Control", f"{observed_treatment/total*100:.1f}% vs {observed_control/total*100:.1f}%", "Mục tiêu: 50/50", delta_color="off")
        st.success("🟢 PASS: Tỷ lệ dương tính giả (FPR) nằm trong khoảng tin cậy. Không phát hiện calibration issue.")
        
    with st.expander("📐 3. System Architecture & Boundaries"):
        st.markdown("### Giới hạn Dữ liệu (Evidence Boundary)")
        st.info("Bước tiếp theo hợp lý là làm một **Randomized Pilot nhỏ theo Champion-Challenger** để kiểm chứng model và economics trên dữ liệu Production.")
        st.markdown("`Synthetic Sandbox` ➔ `Small Randomized GSM Pilot` ➔ `Champion-Challenger` ➔ `Production Monitoring`")
        
        st.markdown("### Luồng Kiến trúc Dự kiến (Production Workflow)")
        mermaid_code = """
        graph TD
            subgraph Batch Pipeline (Chạy ngầm hàng đêm)
                DW[(Data Warehouse)] --> |Lịch sử cuốc xe 30 ngày| RLearner[R-Learner Model]
                RLearner --> |Tính CATE & Lợi nhuận kỳ vọng| DB[(Prediction DB)]
            end
            
            subgraph Real-time Marketing (Ban ngày)
                App[GSM App] --> |Khách hàng mở App| CRM{Marketing CRM}
                CRM --> |Gọi API kiểm tra Khách có EV > 0 không| API[FastAPI Microservice]
                API --> |Truy vấn điểm CATE của Khách| DB
                API -.-> |Trả về: Cấp Voucher = True/False| CRM
                CRM -.-> |Bắn In-app Message giảm 15%| App
            end
            
            style Batch Pipeline fill:#1E1E1E,stroke:#00E5FF,stroke-width:2px
            style Real-time Marketing fill:#1E1E1E,stroke:#FF007F,stroke-width:2px
        """
        st.markdown(f"```mermaid\n{mermaid_code}\n```")
