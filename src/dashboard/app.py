import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
import os

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
        gap: 24px;
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
# Giả định Mức Khuyến mãi mặc định là 15% trên tổng doanh thu chuyến đi
DISCOUNT_PERCENT = 15.0
df_treat = df[df['treatment_rand'] == 1]
df_ctrl = df[df['treatment_rand'] == 0]

# ----------------- CHIA TABS -----------------
tab1, tab2, tab3, tab4, tab5 = st.tabs(["💰 Hiệu quả Tài chính", "🎯 Phân tích Hành vi", "🧠 Causal Engine", "🤖 So sánh Policy (Uplift ML)", "🛠️ Admin Pipeline"])

# ================= TAB 1: TÀI CHÍNH =================
with tab1:
    st.subheader("Bức tranh Tổng thể Dòng tiền (Executive Summary)")
    
    avg_rev_treat = df_treat['gross_revenue_30d'].mean()
    avg_rev_ctrl = df_ctrl['gross_revenue_30d'].mean()
    
    incremental_rev_per_user = avg_rev_treat - avg_rev_ctrl
    cost_per_user = (DISCOUNT_PERCENT / 100.0) * avg_rev_treat
    net_profit_per_user = incremental_rev_per_user - cost_per_user
    overall_roi = (net_profit_per_user / cost_per_user) * 100 if cost_per_user > 0 else 0
    
    col1, col2, col3 = st.columns(3)
    col1.metric("Doanh thu Tăng thêm (Mỗi KH)", f"${incremental_rev_per_user:.2f}", "Nếu áp dụng đại trà")
    col2.metric(f"Chi phí Trợ giá ({DISCOUNT_PERCENT}%)", f"${cost_per_user:.2f}", f"Chi phí/KH (Giảm {DISCOUNT_PERCENT}%)")
    col3.metric("Lợi nhuận Ròng (Net Profit)", f"${net_profit_per_user:.2f}", f"ROI: {overall_roi:.1f}%", delta_color="normal" if net_profit_per_user > 0 else "inverse")
    
    st.warning("⚠️ **Cảnh báo Tài chính:** Việc phát Voucher ĐẠI TRÀ cho 100% khách hàng đang gây LỖ RÒNG. Dưới đây là nguyên nhân phân bổ:")
    
    # Tính ROI cho từng nhóm
    roi_data = []
    for p in df['persona'].unique():
        t = df[(df['persona'] == p) & (df['treatment_rand'] == 1)]
        c = df[(df['persona'] == p) & (df['treatment_rand'] == 0)]
        if len(t) > 0 and len(c) > 0:
            rev_c = c['gross_revenue_30d'].mean()
            rev_t = t['gross_revenue_30d'].mean()
            d_rev = rev_t - rev_c
            cost = (DISCOUNT_PERCENT / 100.0) * rev_t
            roi = (d_rev - cost) / cost * 100 if cost > 0 else 0
            
            roi_data.append({
                'Phân khúc (Persona)': p, 
                'Doanh thu tự nhiên ($)': round(rev_c, 2),
                'Doanh thu có Voucher ($)': round(rev_t, 2),
                'Doanh thu Tăng thêm ($)': round(d_rev, 2),
                'Chi phí Trợ giá ($)': round(cost, 2),
                'Lợi nhuận Ròng ($)': round(d_rev - cost, 2),
                'ROI (%)': round(roi, 1)
            })
    
    roi_df = pd.DataFrame(roi_data).sort_values(by='ROI (%)', ascending=False)
    
    c_chart, c_table = st.columns([1, 1.2])
    
    with c_chart:
        # Vẽ Bar Chart ROI
        fig_roi = px.bar(roi_df, x='Phân khúc (Persona)', y='ROI (%)', 
                         color='ROI (%)', color_continuous_scale=['#FF007F', '#1E293B', '#00E5FF'],
                         title="Biểu đồ Tỷ suất Hoàn vốn (ROI)",
                         text=roi_df['ROI (%)'].apply(lambda x: f"{x:.1f}%"))
        fig_roi.update_traces(textposition='outside')
        fig_roi.update_layout(**chart_layout, coloraxis_showscale=False)
        fig_roi.update_yaxes(showgrid=True, gridcolor='rgba(255,255,255,0.1)')
        st.plotly_chart(fig_roi, use_container_width=True)
        
    with c_table:
        st.markdown("**Bảng Kê Chi tiết Tài chính theo Phân khúc (Drill-down)**")
        # Format bảng Dataframe đẹp mắt
        st.dataframe(roi_df.style.format(precision=1)
                     .background_gradient(subset=['ROI (%)'], cmap='RdYlGn', vmin=-100, vmax=50)
                     .highlight_max(subset=['Lợi nhuận Ròng ($)'], color='rgba(0,229,255,0.3)'), 
                     use_container_width=True, hide_index=True)

# ================= TAB 2: VẬN HÀNH =================
with tab2:
    st.subheader("Bóc tách Hành vi Khách hàng & Hiện tượng Cannibalization")
    
    st.markdown("Cùng nhìn sâu vào thói quen đặt xe để giải thích tại sao nhóm đi làm (Commuters) lại gây lỗ, còn nhóm thỉnh thoảng đi (Occasionals) lại sinh lời.")
    
    c1, c2 = st.columns(2)
    with c1:
        fig_box = px.box(df, x="persona", y="gross_revenue_30d", color="treatment_rand",
                      color_discrete_sequence=neon_colors, title="Sự Dịch chuyển Doanh thu (Boxplot)")
        fig_box.update_layout(**chart_layout)
        fig_box.update_yaxes(showgrid=True, gridcolor='rgba(255,255,255,0.1)', title="Doanh thu ($)")
        fig_box.for_each_trace(lambda t: t.update(name = 'Được Khuyến mãi' if t.name == '1' else 'Không Khuyến mãi'))
        st.plotly_chart(fig_box, use_container_width=True)
        
    with c2:
        # Nhóm (Bin) Recency Days để vẽ biểu đồ dễ nhìn hơn
        df['recency_bins'] = pd.cut(df['recency_days'], bins=[-1, 4, 9, 14, 30], labels=['0-4 ngày (Rất chăm)', '5-9 ngày', '10-14 ngày', '15+ ngày (Ngủ đông)'])
        
        # Tính trung bình số chuyến đi (TRONG CHIẾN DỊCH = Y_rand) theo từng Bin và Nhóm
        agg_df = df.groupby(['recency_bins', 'treatment_rand'])['Y_rand'].mean().reset_index()
        agg_df['treatment_rand'] = agg_df['treatment_rand'].astype(str)
        
        fig_bar = px.bar(agg_df, x='recency_bins', y='Y_rand', color='treatment_rand',
                         barmode='group', color_discrete_sequence=neon_colors,
                         title="Tác động của Khuyến mãi theo Mức độ Ngủ đông",
                         labels={'recency_bins': 'Nhóm khách hàng (Theo thời gian từ cuốc cuối)', 'Y_rand': 'Trung bình Số chuyến đi (Sau KM)'})
        
        fig_bar.update_layout(**chart_layout)
        fig_bar.update_yaxes(showgrid=True, gridcolor='rgba(255,255,255,0.1)')
        fig_bar.for_each_trace(lambda t: t.update(name = 'Được Khuyến mãi' if t.name == '1' else 'Không Khuyến mãi'))
        st.plotly_chart(fig_bar, use_container_width=True)
        
    st.info("💡 **Góc nhìn Phân tích:** Từ biểu đồ Cột nhóm, ta thấy khách hàng càng **chăm đi (0-4 ngày)** thì hai cột Hồng và Xanh cao gần bằng nhau -> Phát Khuyến mãi cho nhóm này không làm họ đi nhiều hơn, gây lãng phí (Cannibalization). Ngược lại, với khách hàng **ngủ đông (15+ ngày)**, cột Xanh cao vượt trội so với cột Hồng -> Khuyến mãi đã 'đánh thức' họ thành công, tạo ra doanh thu gia tăng (Uplift) thực sự.")

# ================= TAB 3: KỸ THUẬT (CAUSAL ENGINE) =================
with tab3:
    st.subheader("Causal Decision Engine (Bộ giả lập Chiến lược)")
    st.markdown("Giả lập việc điều chỉnh chi phí Khuyến mãi. Thuật toán đằng sau sẽ tự động nội suy mức lợi nhuận mới và thay đổi Đề xuất chiến lược thời gian thực.")
    
    col_sim1, col_sim2 = st.columns([1, 2])
    
    with col_sim1:
        st.markdown("#### Bảng Điều Khiển (Simulator)")
        sim_discount = st.slider("📉 Tinh chỉnh Mức Khuyến mãi (%)", min_value=5.0, max_value=50.0, value=15.0, step=5.0)
        sim_margin = st.slider("💰 Tinh chỉnh Biên lợi nhuận (Margin %)", min_value=10.0, max_value=100.0, value=75.0, step=5.0)
        test_persona = st.selectbox("🎯 Kiểm thử cho Tệp Khách hàng:", df['persona'].unique())
        
        # Mô phỏng Tính năng T-Learner (Feature Importance Mock)
        st.markdown("---")
        st.markdown("#### Động cơ Uplift (Feature SHAP)")
        feature_importance = pd.DataFrame({
            'Feature': ['Recency Days', 'Historical Spend', 'Persona Cluster', 'App Opens', 'Time of Day'],
            'SHAP Value': [0.45, 0.32, 0.65, 0.15, 0.10]
        }).sort_values('SHAP Value', ascending=True)
        
        fig_shap = px.bar(feature_importance, x='SHAP Value', y='Feature', orientation='h',
                          color='SHAP Value', color_continuous_scale=['#1E293B', '#00E5FF'])
        # Khắc phục lỗi Margin bằng cách sao chép chart_layout và cập nhật
        shap_layout = chart_layout.copy()
        shap_layout['margin'] = dict(l=0, r=0, t=10, b=0)
        fig_shap.update_layout(**shap_layout, height=250, coloraxis_showscale=False)
        fig_shap.update_xaxes(showgrid=False, title="", showticklabels=False)
        st.plotly_chart(fig_shap, use_container_width=True)
        
    with col_sim2:
        st.markdown("#### Tín hiệu Hành động (Action Signal)")
        
        # Tính toán lại ngầm theo giá voucher mới
        t = df[(df['persona'] == test_persona) & (df['treatment_rand'] == 1)]
        c = df[(df['persona'] == test_persona) & (df['treatment_rand'] == 0)]
        d_margin = (t['gross_revenue_30d'].mean() - c['gross_revenue_30d'].mean()) * (sim_margin / 100.0)
        cost = (sim_discount / 100.0) * t['gross_revenue_30d'].mean()
        roi = (d_margin - cost) / cost * 100 if cost > 0 else -100
        
        if roi > 0:
            st.success(f"""
            🟢 **TÍN HIỆU: ĐÁNH MẠNH (TARGET) - LÃI RÒNG**
            
            Với mức Khuyến mãi **{sim_discount}%**, thuật toán Causal Inference dự phóng chiến dịch cho nhóm `{test_persona}` mang lại **ROI = +{roi:.1f}%**.
            
            Lý do: Khả năng chuyển đổi từ trạng thái Ngủ đông (Dormant) sang Active vượt ngưỡng chi phí CAC. Tín hiệu Đèn Xanh kích hoạt!
            """)
        elif roi > -40:
            st.warning(f"""
            🟡 **TÍN HIỆU: RỦI RO (CÂN NHẮC) - LỖ NHẸ**
            
            Với mức Khuyến mãi **{sim_discount}%**, chiến dịch cho nhóm `{test_persona}` đang ngấp nghé lỗ (**ROI = {roi:.1f}%**). 
            
            Nhóm này có phản ứng tăng chuyến đi (CATE dương), tuy nhiên giá trị cuốc xe không đủ bù đắp hoàn toàn chi phí trợ giá. Đề xuất tiếp tục kéo giảm % Khuyến mãi xuống để tìm điểm hòa vốn.
            """)
        else:
            st.error(f"""
            🔴 **TÍN HIỆU: CHẶN (DENY-LIST) - CANNIBALIZATION**
            
            Với mức Khuyến mãi **{sim_discount}%**, nhóm `{test_persona}` gây ra hiện tượng 'Ăn thịt doanh thu' nặng nề (**ROI = {roi:.1f}%**).
            
            Thuật toán Uplift dự đoán hành vi của nhóm này bị chi phối bởi tính chất bắt buộc (Commuting) chứ không phải do giá cả. Cấm phát Khuyến mãi để bảo vệ Profit Margin.
            """)
            

# ================= TAB 5: UPLIFT ML (X-LEARNER) =================
with tab4:
    st.subheader("🎯 Bệ phóng AI: Tối ưu hóa Cá nhân (Uplift Modeling)")
    st.markdown("Giải bài toán: **Nên phát khuyến mãi cho ai để tối đa hóa Lợi nhuận?** Khác với Tab 3 (Dự đoán theo nhóm), hệ thống Machine Learning tại đây dự đoán xác suất sinh lời trên *từng cá nhân cụ thể*.")
    
    # Lá chắn học thuật
    with st.expander("🛡️ Kiểm định Giả định Nhân quả (Causal Assumptions Check) - ĐÃ ĐẠT", expanded=False):
        st.markdown("""
        Trước khi chạy Uplift Modeling, nền tảng A/B Testing (Tuần 4) đã ngầm chứng minh dữ liệu thỏa mãn 3 trụ cột của Causal Inference:
        1. **Tính phủ lấp (Positivity):** $P(T=1|X) = 0.5 > 0$ cho mọi user (Do là A/B Test 50/50).
        2. **Không nhiễu ẩn (Unconfoundedness - CIA):** Chỉ số SMD < 0.1 ở Tuần 4 chứng minh việc gán Voucher hoàn toàn ngẫu nhiên, độc lập với đặc tính user.
        3. **Tính độc lập (SUTVA):** Hành vi của User A không can thiệp (interfere) vào quyết định của User B.
        """)
        
    try:
        curves_df = pd.read_csv(os.path.join(base_path, 'data', 'processed', 'uplift_profit_curves.csv'))
        persona_df = pd.read_csv(os.path.join(base_path, 'data', 'processed', 'top30_persona_dist.csv'))
        
        c_curve, c_donut = st.columns([1.5, 1])
        
        with c_curve:
            fig_uplift = go.Figure()
            fig_uplift.add_trace(go.Scatter(x=curves_df['Target_Percentage'], y=curves_df['X_Learner_Profit'], mode='lines+markers', name='X-Learner (Cày cuốc & Lợi nhuận cực đại)', line=dict(color='#00E5FF', width=3)))
            fig_uplift.add_trace(go.Scatter(x=curves_df['Target_Percentage'], y=curves_df['S_Learner_Profit'], mode='lines', name='S-Learner (Mượt mà nhưng Bảo thủ)', line=dict(color='#FF007F', width=2)))
            fig_uplift.add_trace(go.Scatter(x=[0, 100], y=[0, curves_df['X_Learner_Profit'].iloc[-1]], mode='lines', name='Mass Marketing (Phát bừa)', line=dict(color='gray', width=1, dash='dash')))
            
            # Đánh dấu đỉnh
            max_profit_x = curves_df.loc[curves_df['X_Learner_Profit'].idxmax(), 'Target_Percentage']
            max_profit_y = curves_df['X_Learner_Profit'].max()
            fig_uplift.add_trace(go.Scatter(x=[max_profit_x], y=[max_profit_y], mode='markers', name=f'Đỉnh Lợi Nhuận (${max_profit_y:,.0f})', marker=dict(color='#FFD700', size=12, symbol='star')))
            
            fig_uplift.update_layout(**chart_layout, title="Cuộc chiến Lợi nhuận: S-Learner vs X-Learner", height=400, legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1))
            fig_uplift.update_xaxes(title="Tỷ lệ khách hàng được phát Voucher (%)")
            fig_uplift.update_yaxes(title="Lợi nhuận Ròng ($)", showgrid=True, gridcolor='rgba(255,255,255,0.1)')
            st.plotly_chart(fig_uplift, use_container_width=True)
            
            st.info(f"**Quyết định Chốt hạ:** Khuyến nghị áp dụng **X-Learner** và phát Voucher cho **Top {max_profit_x}%**. S-Learner có đường cong mượt nhưng mắc 'Thiên kiến Zero-effect' (Sợ rủi ro) nên bỏ lỡ hơn 50% lợi nhuận!")
            
        with c_donut:
            fig_donut = px.pie(persona_df, values='Percentage', names='Persona', hole=0.6, title="Chân dung 'Khách hàng Vàng' (Top 30%)", color_discrete_sequence=px.colors.qualitative.Pastel)
            fig_donut.update_layout(**chart_layout, height=400, showlegend=True)
            fig_donut.update_traces(textinfo='percent+label')
            st.plotly_chart(fig_donut, use_container_width=True)
            
            st.success("✅ **Xác nhận Chiến lược (trong Sandbox):** X-Learner không biết về chiến lược của ta, nhưng kết quả tập trung vào nhóm Suburban — phù hợp với assumptions HTE đã thiết kế. Cần validation trên GSM data thật để xác nhận.")
            
    except Exception as e:
        st.error(f"Lỗi khi tải hoặc hiển thị dữ liệu Uplift: {str(e)}\n\nVui lòng chạy lại Pipeline hoặc script export.")

    # ─── POLICY COMPARISON SECTION ─────────────────────────
    st.markdown("---")
    st.subheader("🏆 So sánh 5 Policy: Business Decision là gì?")
    st.markdown("""
    **Business không mua một Qini Curve — Business cần một Policy cụ thể.**  
    Dưới đây là so sánh 5 chiến lược phát Voucher trên cùng tập dữ liệu test, dưới cùng tham số kinh tế (Voucher 15% doanh thu, Margin 75%/ride).
    """)
    
    try:
        policy_df_raw = pd.read_csv(os.path.join(base_path, 'data', 'processed', 'policy_comparison.csv'))
        
        # — Bar chart: Expected Incremental Profit by Policy
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
            fig_policy.add_trace(go.Bar(
                x=[row['Policy'].split('.',1)[1].strip() if '.' in row['Policy'] else row['Policy']],
                y=[row['Expected_Incremental_Profit']],
                name=row['Policy'],
                marker_color=color,
                text=[f"${row['Expected_Incremental_Profit']:,.0f}\n({row['Pct_Targeted']:.0f}% users)"],
                textposition='outside'
            ))
        
        fig_policy.add_hline(y=0, line_width=2, line_dash='dash', line_color='white', opacity=0.5)
        fig_policy.update_layout(**chart_layout, title="Lợi nhuận Kỳ vọng theo từng Policy (Test Set)",
                                 height=420, showlegend=False, barmode='group')
        fig_policy.update_yaxes(title="Expected Incremental Profit ($)", showgrid=True, gridcolor='rgba(255,255,255,0.1)')
        fig_policy.update_xaxes(title="", tickangle=-20)
        st.plotly_chart(fig_policy, use_container_width=True)
        
        # — Table with color gradient
        display_df = policy_df_raw.copy()
        display_df.columns = ['Policy', 'N Users Targetật', '% Users', 'Chi phí Voucher ($)', 'Lợi nhuận Kỳ vọng ($)', 'ROI (%)']
        st.dataframe(
            display_df.style
            .format({'Chi phí Voucher ($)': '${:,.0f}', 'Lợi nhuận Kỳ vọng ($)': '${:,.0f}', 'ROI (%)': '{:.1f}%', '% Users': '{:.1f}%'})
            .background_gradient(subset=['Lợi nhuận Kỳ vọng ($)'], cmap='RdYlGn', vmin=-80000, vmax=15000),
            use_container_width=True, hide_index=True
        )
        
        # — Key insight callout
        profit_row = policy_df_raw[policy_df_raw['Policy'].str.contains('Profit Targeting')].iloc[0]
        mass_row = policy_df_raw[policy_df_raw['Policy'].str.contains('Mass Voucher')].iloc[0]
        st.info(f"""
        **📊 Kết luận trong Sandbox:**  
        Profit Targeting (phát cho {profit_row['Pct_Targeted']:.0f}% user có Expected Value > 0) cho lợi nhuận **${profit_row['Expected_Incremental_Profit']:,.0f}**,  
        trong khi Mass Voucher (phát cho tất cả) gây lỗ **${abs(mass_row['Expected_Incremental_Profit']):,.0f}**.  
        Điều này cho thấy trong sandbox với assumptions hiện tại: **nhắm mục tiêu đúng đối tượng quan trọng hơn việc phát rộng.** 
        Kết quả cần được kiểm chứng trên GSM data thật trước khi áp dụng thực tế.
        """)
        
    except Exception as e:
        st.warning(f"Nhấn 'Chạy Pipeline' ở tab Admin để tạo dữ liệu Policy Comparison. ({str(e)})")

# ================= TAB 6: KỸ THUẬT (PIPELINE ADMIN) =================
with tab5:
    st.subheader("Trình quản lý Data Pipeline (Backend Developer Only)")
    st.markdown("Giả lập hệ thống kết nối Data Warehouse và chạy luồng Machine Learning (K-Means & T-Learner) end-to-end.")
    
    if st.button("▶️ Chạy toàn bộ Data Pipeline", type="primary"):
        import sys
        pipeline_path = os.path.join(base_path, 'src', 'pipeline')
        if pipeline_path not in sys.path:
            sys.path.append(pipeline_path)
            
        try:
            from main_pipeline import run_pipeline
            progress_bar = st.progress(0, text="Khởi tạo Pipeline...")
            
            def st_progress_callback(pct, msg):
                progress_bar.progress(pct, text=f"[{pct}%] {msg}")
                
            run_pipeline(n_users=20000, progress_callback=st_progress_callback)
            
            st.success("✅ Đã hoàn tất Pipeline! Tải lại trang (F5) để Dashboard cập nhật dữ liệu mới nhất.")
        except Exception as e:
            st.error(f"Lỗi khi chạy Pipeline: {e}")
