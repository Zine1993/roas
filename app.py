import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go
from scipy.optimize import curve_fit

st.set_page_config(page_title="高级 LTV 留存拟合工具", layout="wide")

# --- 1. 定义拟合函数 (幂律分布) ---
def retention_func(t, a, b):
    # a: 初始强度, b: 衰减速率 (通常为负)
    return a * np.power(t, b)

st.title("🧪 多点留存动态拟合与回收预估")
st.markdown("请输入实测留存数据点（至少2个，最多10个）。系统将自动拟合 180 天留存曲线。")

# --- 2. 侧边栏：动态点位管理 ---
with st.sidebar:
    st.header("📍 留存配置")
    
    # 使用 Data Editor 让用户动态增删行
    default_data = pd.DataFrame([
        {"天数": 1, "留存率%": 35.0},
        {"天数": 7, "留存率%": 12.0},
        {"天数": 30, "留存率%": 4.5}
    ])
    
    st.subheader("编辑留存点位")
    edited_df = st.data_editor(
        default_data,
        num_rows="dynamic", # 允许增删行
        column_config={
            "天数": st.column_config.NumberColumn("天数 (Day)", min_value=1, max_value=365, step=1),
            "留存率%": st.column_config.NumberColumn("留存率 (%)", min_value=0.0, max_value=100.0, format="%.2f")
        },
        hide_index=True,
    )

    st.divider()
    st.header("💰 经济指标")
    cpi = st.number_input("预计 CPI ($)", value=3.0)
    pay_rate = st.number_input("新用户付费率 (%)", value=1.5) / 100
    arppu = st.number_input("新用户 ARPPU ($)", value=45.0)
    margin = st.slider("渠道分成后比例 (%)", 50, 100, 70) / 100

# --- 3. 核心拟合与计算 ---
# 清理数据：排序并确保至少有两个点
plot_df = edited_df.dropna().sort_values("天数")
x_obs = plot_df["天数"].values
y_obs = plot_df["留存率%"].values / 100

if len(plot_df) < 2:
    st.warning("⚠️ 请至少输入 2 个留存点位进行拟合。")
    st.stop()
elif len(plot_df) > 10:
    st.error("❌ 最多支持 10 个点位，请删除多余行。")
    st.stop()

# 执行拟合
try:
    # p0 是初始猜测值，有助于收敛
    popt, _ = curve_fit(retention_func, x_obs, y_obs, p0=[y_obs[0], -0.5], maxfev=5000)
    a_fit, b_fit = popt
except Exception as e:
    st.error(f"拟合失败: {e}。请确保留存数据随天数增加而下降。")
    st.stop()

# 生成 180 天数据
days_predict = np.arange(1, 181)
y_predict = retention_func(days_predict, a_fit, b_fit)

# 计算 LTV 和 ROI
daily_rev = pay_rate * arppu * margin
cum_ltv = np.cumsum(y_predict * daily_rev)
payback_idx = np.where(cum_ltv >= cpi)[0]
payback_day = f"{payback_idx[0] + 1} 天" if len(payback_idx) > 0 else "180天内未回本"

# --- 4. 结果展示 ---
col1, col2, col3 = st.columns(3)
col1.metric("拟合曲线初始值 (a)", f"{a_fit*100:.1f}%")
col2.metric("衰减斜率 (b)", f"{b_fit:.4f}")
col3.metric("预计回本周期", payback_day)

# 绘图
fig = go.Figure()
# 拟合曲线
fig.add_trace(go.Scatter(x=days_predict, y=y_predict, name="拟合 LTV 留存曲线", line=dict(color='#1f77b4', width=2)))
# 实测点
fig.add_trace(go.Scatter(x=x_obs, y=y_obs, mode='markers', name="实测输入点", marker=dict(size=10, color='red', symbol='x')))
# LTV 曲线 (次坐标轴)
fig.add_trace(go.Scatter(x=days_predict, y=cum_ltv, name="累计 LTV ($)", yaxis="y2", line=dict(color='#2ca02c', dash='dot')))

fig.update_layout(
    title="留存拟合与 LTV 增长趋势",
    xaxis=dict(title="天数"),
    yaxis=dict(title="留存率", tickformat=".1%"),
    yaxis2=dict(title="累计 LTV ($)", overlaying="y", side="right"),
    hovermode="x unified",
    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
)
st.plotly_chart(fig, use_container_width=True)

# 压力测试表格 (简版)
st.subheader("📑 预估明细表 (前30天)")
report_df = pd.DataFrame({
    "天数": days_predict[:30],
    "拟合留存": [f"{v*100:.2f}%" for v in y_predict[:30]],
    "单日贡献": [f"${v * daily_rev:.4f}" for v in y_predict[:30]],
    "累计LTV": [f"${v:.2f}" for v in cum_ltv[:30]]
})
st.dataframe(report_df, use_container_width=True)
