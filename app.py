import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go

st.set_page_config(page_title="App ROI 模拟器", layout="wide")

st.title("🚀 移动应用回本周期 (ROI) 预估模型")

# --- 侧边栏：输入参数 ---
with st.sidebar:
    st.header("1. 获客成本")
    cpi = st.number_input("CPI (单个下载成本 $)", value=2.0)
    
    st.header("2. 留存曲线 (输入关键点)")
    d1 = st.slider("次留 (D1 %)", 0, 100, 40) / 100
    d7 = st.slider("七留 (D7 %)", 0, 100, 15) / 100
    d30 = st.slider("三十留 (D30 %)", 0, 100, 5) / 100
    
    st.header("3. 变现与财务")
    pay_rate = st.slider("付费率 (%)", 0.0, 20.0, 2.0) / 100
    arppu = st.number_input("ARPPU (付费用户平均贡献 $)", value=50.0)
    tax_rate = st.slider("渠道分成+税收 (%)", 0, 50, 30) / 100

# --- 计算逻辑 ---
# 简单的留存拟合 (Power Law: y = a * x^b)
days = np.arange(1, 181) # 预估半年
# 简易拟合：这里可以用更复杂的曲线拟合，此处为演示逻辑
daily_arpu = pay_rate * arppu * (1 - tax_rate)

# 模拟留存衰减 (这里使用简化的衰减逻辑)
def get_retention(day):
    if day == 1: return 1.0
    if day <= 7: return d1 * (day**np.log2(d7/d1)/np.log2(7))
    return d7 * (day/7)**(np.log(d30/d7)/np.log(30/7))

retention_series = np.array([get_retention(d) for d in days])
daily_revenue = retention_series * daily_arpu
cum_ltv = np.cumsum(daily_revenue)

# 寻找回本天数
payback_day = np.where(cum_ltv >= cpi)[0]
payback_day = payback_day[0] + 1 if len(payback_day) > 0 else "180+"

# --- 结果展示 ---
col1, col2, col3 = st.columns(3)
col1.metric("6个月预测 LTV", f"${cum_ltv[-1]:.2f}")
col2.metric("回本周期 (Payback)", f"{payback_day} 天")
col3.metric("最终 ROI", f"{(cum_ltv[-1]/cpi)*100:.1f}%")

# 绘制回收曲线
fig = go.Figure()
fig.add_trace(go.Scatter(x=days, y=cum_ltv, name="累计 LTV", line=dict(color='green', width=3)))
fig.add_hline(y=cpi, line_dash="dash", line_color="red", annotation_text="CPI 成本线")
fig.update_layout(title="LTV 回收趋势图", xaxis_title="天数", yaxis_title="金额 ($)")
st.plotly_chart(fig, use_container_width=True)
