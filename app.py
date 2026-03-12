import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go

# 页面配置
st.set_page_config(page_title="App ROI 科学预估模型", layout="wide")

st.title("📊 移动应用回本周期 (Payback) 科学预估模型")
st.markdown("""
本模型通过**幂律分布**拟合留存曲线，并引入**折损系数**修正活跃用户与新增买量用户之间的数据偏差。
""")

# --- 1. 侧边栏：参数输入 ---
with st.sidebar:
    st.header("🎯 核心指标输入")
    st.subheader("活跃大盘数据 (基准)")
    base_pay_rate = st.number_input("活跃用户付费率 (%)", value=5.0, step=0.1) / 100
    base_arppu = st.number_input("活跃用户 ARPPU ($)", value=50.0, step=1.0)
    
    st.divider()
    
    st.subheader("⚠️ 新增买量折损")
    pay_discount = st.slider("付费率折损 (新用户/活跃用户)", 0.1, 1.0, 0.7)
    arppu_discount = st.slider("ARPPU 折损 (新用户/活跃用户)", 0.1, 1.0, 0.9)
    
    st.divider()
    
    st.subheader("📈 留存曲线设置 (买量实测)")
    d1 = st.slider("D1 留存 (%)", 10, 80, 35) / 100
    d30 = st.slider("D30 留存 (%)", 1, 30, 4) / 100
    
    st.divider()
    
    st.subheader("💰 财务与成本")
    cpi = st.number_input("预计 CPI ($)", value=3.0, step=0.1)
    platform_fee = st.slider("渠道分成+税收 (%)", 0, 50, 30) / 100

# --- 2. 核心计算逻辑 ---

# 2.1 留存曲线拟合 (Power Law: R = d1 * t^b)
days = np.arange(1, 181) # 预估180天
# 求解幂律系数 b = log(d30/d1) / log(30/1)
b_slope = np.log(d30/d1) / np.log(30)
retention_curve = d1 * (days**b_slope)

# 2.2 修正后的变现指标
adj_pay_rate = base_pay_rate * pay_discount
adj_arppu = base_arppu * arppu_discount
daily_net_arpu = adj_pay_rate * adj_arppu * (1 - platform_fee)

# 2.3 累计 LTV 计算
daily_ltv_contrib = retention_curve * daily_net_arpu
# 第一天单独处理或简化处理（通常第0天即下载日也有收入）
cum_ltv = np.cumsum(daily_ltv_contrib)

# 2.4 回本计算
payback_day_idx = np.where(cum_ltv >= cpi)[0]
payback_result = f"{payback_day_idx[0] + 1} 天" if len(payback_day_idx) > 0 else "超过 180 天"

# --- 3. 结果展示 ---

# 指标看板
c1, c2, c3, c4 = st.columns(4)
c1.metric("修正后付费率", f"{adj_pay_rate*100:.2f}%")
c2.metric("修正后 ARPPU", f"${adj_arppu:.2f}")
c3.metric("预计回本周期", payback_result)
c4.metric("180日 ROI", f"{(cum_ltv[-1]/cpi)*100:.1f}%")

# LTV 图表
fig = go.Figure()
fig.add_trace(go.Scatter(x=days, y=cum_ltv, name="累计 LTV", line=dict(color='#00CC96', width=3)))
fig.add_hline(y=cpi, line_dash="dash", line_color="#EF553B", annotation_text=f"CPI 成本 ${cpi}")
fig.update_layout(title="LTV 回收趋势预估 (180天)", xaxis_title="天数", yaxis_title="金额 ($)", hovermode="x unified")
st.plotly_chart(fig, use_container_width=True)

# --- 4. 压力测试 (Sensitivity Analysis) ---
st.divider()
st.subheader("☢️ 压力测试：不同 CPI 与付费率下的回本天数")
st.write("如果市场环境变差（CPI上升或转化下降），你的回本周期会如何变化？")

# 构建矩阵
cpi_range = [cpi * 0.8, cpi * 0.9, cpi, cpi * 1.1, cpi * 1.2]
discount_range = [pay_discount * 0.8, pay_discount * 0.9, pay_discount, pay_discount * 1.1]

matrix_data = []
for d in discount_range:
    row = []
    temp_pay_rate = base_pay_rate * d
    temp_daily_net_arpu = temp_pay_rate * adj_arppu * (1 - platform_fee)
    temp_cum_ltv = np.cumsum(retention_curve * temp_daily_net_arpu)
    
    for c in cpi_range:
        idx = np.where(temp_cum_ltv >= c)[0]
        day = f"{idx[0] + 1}d" if len(idx) > 0 else ">180d"
        row.append(day)
    matrix_data.append(row)

# 转为 DataFrame 展示
sensitivity_df = pd.DataFrame(
    matrix_data, 
    index=[f"付费折损 {int(d*100)}%" for d in discount_range],
    columns=[f"CPI ${c:.2f}" for c in cpi_range]
)

st.table(sensitivity_df)

st.caption("注：压力测试中，ARPPU 和留存曲线保持不变，仅波动 CPI 和付费率折损系数。")
