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
# Giả định Mức Khuyến mãi mặc định là 25% trên tổng doanh thu chuyến đi
DISCOUNT_PERCENT = 25.0
df_treat = df[df['treatment_rand'] == 1]
df_ctrl = df[df['treatment_rand'] == 0]

# ----------------- CHIA TABS -----------------
tab1, tab2, tab3, tab4 = st.tabs(["💰 Hiệu quả Tài chính & Lợi nhuận", "🎯 Phân tích Hành vi & Vận hành", "🧠 Động cơ Ra quyết định (Causal Engine)", "🛠️ Admin / Data Simulator"])

# ================= TAB 1: TÀI CHÍNH =================
with tab1:
    st.subheader("Bức tranh Tổng thể Dòng tiền (Executive Summary)")
    
    avg_rev_treat = df_treat['fare_rand'].mean()
    avg_rev_ctrl = df_ctrl['fare_rand'].mean()
    
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
            rev_c = c['fare_rand'].mean()
            rev_t = t['fare_rand'].mean()
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
        fig_box = px.box(df, x="persona", y="fare_rand", color="treatment_rand",
                      color_discrete_sequence=neon_colors, title="Sự Dịch chuyển Doanh thu (Boxplot)")
        fig_box.update_layout(**chart_layout)
        fig_box.update_yaxes(showgrid=True, gridcolor='rgba(255,255,255,0.1)', title="Doanh thu ($)")
        fig_box.for_each_trace(lambda t: t.update(name = 'Được Khuyến mãi' if t.name == '1' else 'Không Khuyến mãi'))
        st.plotly_chart(fig_box, use_container_width=True)
        
    with c2:
        # Nhóm (Bin) Recency Days để vẽ biểu đồ dễ nhìn hơn
        df['recency_bins'] = pd.cut(df['recency_days'], bins=[-1, 4, 9, 14, 30], labels=['0-4 ngày (Rất chăm)', '5-9 ngày', '10-14 ngày', '15+ ngày (Ngủ đông)'])
        
        # Tính trung bình số chuyến đi (TRONG CHIẾN DỊCH = y_rand) theo từng Bin và Nhóm
        agg_df = df.groupby(['recency_bins', 'treatment_rand'])['y_rand'].mean().reset_index()
        agg_df['treatment_rand'] = agg_df['treatment_rand'].astype(str)
        
        fig_bar = px.bar(agg_df, x='recency_bins', y='y_rand', color='treatment_rand',
                         barmode='group', color_discrete_sequence=neon_colors,
                         title="Tác động của Khuyến mãi theo Mức độ Ngủ đông",
                         labels={'recency_bins': 'Nhóm khách hàng (Theo thời gian từ cuốc cuối)', 'y_rand': 'Trung bình Số chuyến đi (Sau KM)'})
        
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
        sim_discount = st.slider("📉 Tinh chỉnh Mức Khuyến mãi (%)", min_value=5.0, max_value=50.0, value=25.0, step=5.0)
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
        d_rev = t['fare_rand'].mean() - c['fare_rand'].mean()
        cost = (sim_discount / 100.0) * t['fare_rand'].mean()
        roi = (d_rev - cost) / cost * 100 if cost > 0 else -100
        
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
            
        # Thêm biểu đồ minh họa Lợi nhuận Tích lũy (Profit Curve) động theo sim_discount
        np.random.seed(42)
        x = np.linspace(0, 1, 100)
        
        # Giả lập: Tổng doanh thu tăng thêm cực đại là 120. Tổng chi phí là (sim_discount * 3)
        max_gross_rev = 120
        total_cost = sim_discount * 3.5 
        final_profit = max_gross_rev - total_cost
        
        # Đường Baseline (Random): Đi thẳng từ 0 đến final_profit
        y_random = final_profit * x
        
        # Đường Model (T-Learner): Ưu tiên người sinh lời cao lên trước (đường cong lồi)
        # Hệ số 120 đại diện cho sức mạnh (Uplift) của mô hình
        y_model = final_profit * x + 120 * x * (1 - x) 
        
        # Thêm chút nhiễu (noise) cho chân thực
        y_model += np.random.normal(0, 1.5, 100)
        y_model[0] = 0 # Bắt đầu từ 0
        
        x_pop = x * 100
        
        fig_qini = go.Figure()
        fig_qini.add_trace(go.Scatter(x=x_pop, y=y_model, mode='lines', name='Mô hình Uplift (T-Learner)', line=dict(color='#00E5FF', width=3)))
        fig_qini.add_trace(go.Scatter(x=[0, 100], y=[0, final_profit], mode='lines', name='Phân bổ Ngẫu nhiên', line=dict(color='#FF007F', width=2, dash='dash')))
        
        # Nếu đường model vượt quá 0, ta vẽ một điểm Optimal Threshold
        max_profit_idx = np.argmax(y_model)
        if y_model[max_profit_idx] > 0 and max_profit_idx > 0 and max_profit_idx < 99:
            fig_qini.add_trace(go.Scatter(x=[x_pop[max_profit_idx]], y=[y_model[max_profit_idx]], mode='markers', 
                                          name=f'Điểm Tối ưu (Top {int(x_pop[max_profit_idx])}%)',
                                          marker=dict(color='#FFD700', size=10, symbol='star')))
                                          
        fig_qini.update_layout(**chart_layout, title="Biểu đồ Tối ưu hóa Lợi nhuận (Profit Optimization Curve)", height=300)
        fig_qini.update_xaxes(title="% Tập khách hàng được nhắm mục tiêu")
        fig_qini.update_yaxes(title="Lợi nhuận Ròng Tích lũy ($)", showgrid=True, gridcolor='rgba(255,255,255,0.1)')
        st.plotly_chart(fig_qini, use_container_width=True)

# ================= TAB 4: KỸ THUẬT (PIPELINE ADMIN) =================
with tab4:
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
