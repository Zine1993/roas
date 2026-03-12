import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from scipy.optimize import curve_fit

st.set_page_config(page_title="App 回收精细化预估", layout="wide")

# --- 核心数学模型：幂律分布 ---
def retention_model(t, a, b):
    return a * np.power(t, b)

# --- 自定义 CSS 优化视觉 ---
st.markdown("""
    <style>
    .main { background-color: #f5f7f9; }
    .stMetric { background-color: #ffffff; padding: 15px; border-radius: 10px; box-shadow: 0 2px 4px rgba(0,0,0,0.05); }
    </style>
    """, unsafe_allow_html=True)

st.title("🎯 App 买量回收精细化预估工具")
st.caption("基于 Cohort 群组分析，通过多点拟合与折损修正，科学预估 Payback Period。")

# --- 分页逻辑 ---
tab_ret, tab_mon, tab_roi = st.tabs(["👥 1. 用户留存拟合", "💰 2. 变现指标修正", "📊 3. 最终回收报告"])

# --- TAB 1: 留存拟合 ---
with tab_ret:
    st.header("用户留存模型")
    col_input, col_chart = st.columns([1, 2])
    
    with col_input:
        st.write("请输入实测留存点 (2-10个):")
        init_df = pd.DataFrame([
            {"Day": 1, "Rate%": 35.0},
            {"Day": 7, "Rate%": 12.0},
            {"Day": 30, "Rate%": 4.5}
        ])
        ret_data = st.data_editor(init_df, num_rows="dynamic", hide_index=True)
        
        # 数据清洗与拟合
        clean_df = ret_data.dropna().sort_values("Day")
        x_obs = clean_df["Day"].values
        y_obs = clean_df["Rate%"].values / 100
        
        if len(clean_df) >= 2:
            popt, _ = curve_fit(retention_model, x_obs, y_obs, p0=[y_obs[0], -0.5])
            a_fit, b_fit = popt
            days_180 = np.arange(1, 181)
            y_fit = retention_model(days_180, a_fit, b_fit)
        else:
            st.warning("请至少输入两个点位。")

    with col_chart:
        if len(clean_df) >= 2:
            fig_ret = go.Figure()
            fig_ret.add_trace(go.Scatter(x=days_180, y=y_fit, name="拟合曲线", line=dict(color='#1f77b4', width=2)))
            fig_ret.add_trace(go.Scatter(x=x_obs, y=y_obs, mode='markers', name="实测点", marker=dict(size=10, color='red')))
            fig_ret.update_layout(title="180天留存衰减预估", xaxis_title="天数", yaxis_title="留存率", height=400)
            st.plotly_chart(fig_ret, use_container_width=True)

# --- TAB 2: 变现修正 ---
with tab_mon:
    st.header("新用户变现效率")
    c1, c2 = st.columns(2)
    
    with c1:
        st.subheader("大盘活跃数据 (参考)")
        act_pay_rate = st.number_input("活跃用户付费率 (%)", value=5.0) / 100
        act_arppu = st.number_input("活跃用户 ARPPU ($)", value=50.0)
    
    with c2:
        st.subheader("新增用户折损 (修正)")
        # 针对你提到的折损极大的情况
        pay_discount = st.slider("付费率折损系数", 0.05, 1.0, 0.5, step=0.01)
        arppu_discount = st.slider("ARPPU 折损系数", 0.5, 1.0, 0.8)

    # 实际参与计算的指标
    real_pay_rate = act_pay_rate * pay_discount
    real_arppu = act_arppu * arppu_discount
    st.info(f"💡 修正后：新用户首周预估付费率为 {real_pay_rate*100:.2f}%，ARPPU 为 ${real_arppu:.2f}")

# --- TAB 3: 回收报告 ---
with tab_roi:
    st.header("核心回收预估")
    
    c_cost, c_organic, c_margin = st.columns(3)
    with c_cost:
        cpi = st.number_input("买量成本 CPI ($)", value=3.0)
    with c_organic:
        organic_lift = st.slider("自然量补偿 (Organic Lift %)", 0, 100, 20, help="买量带来的额外自然量占比")
    with c_margin:
        platform_cut = st.slider("渠道分成折损 (%)", 15, 35, 30)

    # 计算最终 eCPI (考虑自然量)
    # 逻辑：如果自然量是20%，意味着买1个人实际进1.2个人
    ecpi = cpi / (1 + (organic_lift / 100))
    
    # 计算累计 LTV
    net_daily_revenue = real_pay_rate * real_arppu * (1 - (platform_cut / 100))
    cum_ltv = np.cumsum(y_fit * net_daily_revenue)
    
    # 结果指标
    payback_idx = np.where(cum_ltv >= ecpi)[0]
    payback_day = f"{payback_idx[0] + 1} 天" if len(payback_idx) > 0 else "180天+"
    roi_180 = (cum_ltv[-1] / ecpi) * 100

    # 看板展示
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("有效 eCPI", f"${ecpi:.2f}", help="考虑自然量后的实际单人获客成本")
    m2.metric("回本周期", payback_day)
    m3.metric("180日预测 ROI", f"{roi_180:.1f}%")
    m4.metric("D180 累计 LTV", f"${cum_ltv[-1]:.2f}")

    # 回收图表
    fig_roi = go.Figure()
    fig_roi.add_trace(go.Scatter(x=days_180, y=cum_ltv, name="累计 LTV", fill='tozeroy', line=dict(color='green')))
    fig_roi.add_hline(y=ecpi, line_dash="dash", line_color="red", annotation_text="回本线 (eCPI)")
    fig_roi.update_layout(title="LTV 回收趋势图", xaxis_title="天数", yaxis_title="金额 ($)", height=500)
    st.plotly_chart(fig_roi, use_container_width=True)
