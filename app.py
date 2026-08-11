import io

import numpy as np
import pandas as pd
import plotly.graph_objects as go
import streamlit as st

from core import (
    cumulative_ltv,
    effective_cpi,
    find_payback_day,
    fit_power_law_retention,
    roas_checkpoints,
)

st.set_page_config(page_title="Game Growth Toolkit", page_icon="🎯", layout="wide")

SAMPLE_CSV = """Day,Rate%
1,35.0
3,22.0
7,12.0
14,7.5
30,4.5
"""

st.markdown(
    """
    <style>
    .main { background-color: #f5f7f9; }
    .stMetric {
        background-color: #ffffff;
        padding: 15px;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.title("🎯 Game Growth Toolkit")
st.caption(
    "Fit early retention cohorts, stress-test monetization assumptions, "
    "and estimate payback and ROAS through Day 180."
)

with st.expander("Model assumptions and limitations"):
    st.markdown(
        """
        The current model fits a power-law retention curve and applies a simplified
        daily monetization assumption. It is intended for scenario planning, not
        attribution or financial reporting. Real cohorts can differ because of payer
        conversion timing, repeat purchases, ad revenue, refunds, taxes, whales,
        reactivation, regional mix, and campaign-quality shifts.
        """
    )

tab_ret, tab_mon, tab_roi = st.tabs(
    ["👥 1. Retention", "💰 2. Monetization", "📊 3. Payback & ROAS"]
)

fit = None

with tab_ret:
    st.header("Retention model")
    col_input, col_chart = st.columns([1, 2])

    with col_input:
        st.write("Enter retention points or import a CSV with `Day` and `Rate%` columns.")
        uploaded_file = st.file_uploader(
            "Import cohort CSV",
            type=["csv"],
            help="Example format: Day,Rate% with retention values expressed as percentages.",
        )
        st.download_button(
            "Download sample cohort CSV",
            data=SAMPLE_CSV,
            file_name="sample_cohort.csv",
            mime="text/csv",
        )

        initial_df = pd.read_csv(io.StringIO(SAMPLE_CSV))
        if uploaded_file is not None:
            try:
                uploaded_df = pd.read_csv(uploaded_file)
                missing = {"Day", "Rate%"} - set(uploaded_df.columns)
                if missing:
                    raise ValueError("CSV must include the columns `Day` and `Rate%`.")
                initial_df = uploaded_df[["Day", "Rate%"]].copy()
            except Exception as exc:
                st.error(f"Could not read CSV: {exc}")

        retention_data = st.data_editor(
            initial_df,
            num_rows="dynamic",
            hide_index=True,
            key="retention_editor",
        )

        try:
            clean_df = retention_data[["Day", "Rate%"]].dropna().copy()
            fit = fit_power_law_retention(
                clean_df["Day"].to_numpy(),
                clean_df["Rate%"].to_numpy() / 100.0,
                horizon=180,
            )
        except (KeyError, TypeError, ValueError, RuntimeError) as exc:
            st.error(f"Retention input error: {exc}")

        if fit is not None:
            metric_a, metric_b, metric_r2 = st.columns(3)
            metric_a.metric("a", f"{fit.a:.4f}")
            metric_b.metric("b", f"{fit.b:.4f}")
            metric_r2.metric("R²", f"{fit.r_squared:.4f}")
            if fit.r_squared < 0.90:
                st.warning(
                    "Fit quality is below R² 0.90. Treat downstream forecasts as a rough scenario."
                )

    with col_chart:
        if fit is not None:
            fig_ret = go.Figure()
            fig_ret.add_trace(
                go.Scatter(
                    x=fit.forecast_days,
                    y=fit.forecast * 100,
                    name="Power-law forecast",
                    line={"width": 2},
                )
            )
            fig_ret.add_trace(
                go.Scatter(
                    x=fit.days,
                    y=fit.observed * 100,
                    mode="markers",
                    name="Observed cohort",
                    marker={"size": 10},
                )
            )
            fig_ret.update_layout(
                title="Retention forecast through Day 180",
                xaxis_title="Day",
                yaxis_title="Retention (%)",
                height=430,
                yaxis={"rangemode": "tozero"},
            )
            st.plotly_chart(fig_ret, use_container_width=True)
        else:
            st.info("Add at least two valid retention points to generate a forecast.")

with tab_mon:
    st.header("New-user monetization assumptions")
    c1, c2 = st.columns(2)

    with c1:
        st.subheader("Mature active-user baseline")
        active_payer_rate = (
            st.number_input(
                "Active-user payer rate (%)",
                min_value=0.0,
                max_value=100.0,
                value=5.0,
                step=0.1,
            )
            / 100.0
        )
        active_arppu = st.number_input(
            "Active-user ARPPU ($)",
            min_value=0.0,
            value=50.0,
            step=1.0,
        )

    with c2:
        st.subheader("New-user discount")
        payer_discount = st.slider(
            "Payer-rate multiplier",
            min_value=0.05,
            max_value=1.0,
            value=0.50,
            step=0.01,
        )
        arppu_discount = st.slider(
            "ARPPU multiplier",
            min_value=0.05,
            max_value=1.0,
            value=0.80,
            step=0.01,
        )

    new_user_payer_rate = active_payer_rate * payer_discount
    new_user_arppu = active_arppu * arppu_discount

    st.info(
        "Adjusted new-user assumptions: "
        f"{new_user_payer_rate * 100:.2f}% payer rate and "
        f"${new_user_arppu:.2f} ARPPU."
    )

with tab_roi:
    st.header("Payback and ROAS forecast")

    if fit is None:
        st.warning("A valid retention fit is required before payback and ROAS can be calculated.")
    else:
        c_cost, c_organic, c_margin = st.columns(3)
        with c_cost:
            cpi = st.number_input(
                "Paid acquisition CPI ($)",
                min_value=0.01,
                value=3.0,
                step=0.10,
            )
        with c_organic:
            organic_lift_pct = st.slider(
                "Organic lift (%)",
                min_value=0,
                max_value=200,
                value=20,
                help="Extra organic users attributed to paid acquisition, expressed as a percentage.",
            )
        with c_margin:
            platform_cut_pct = st.slider(
                "Platform / distribution cut (%)",
                min_value=0,
                max_value=95,
                value=30,
            )

        ecpi = effective_cpi(cpi, organic_lift_pct / 100.0)
        cum_ltv = cumulative_ltv(
            fit.forecast,
            new_user_payer_rate,
            new_user_arppu,
            platform_cut_pct / 100.0,
        )
        payback = find_payback_day(cum_ltv, ecpi)
        roas = roas_checkpoints(cum_ltv, ecpi)

        m1, m2, m3, m4 = st.columns(4)
        m1.metric("Effective CPI", f"${ecpi:.2f}")
        m2.metric("Payback", f"Day {payback}" if payback else "180+ days")
        m3.metric("D180 ROAS", f"{roas.get(180, np.nan) * 100:.1f}%")
        m4.metric("D180 cumulative LTV", f"${cum_ltv[-1]:.2f}")

        roas_rows = [
            {
                "Checkpoint": f"D{day}",
                "ROAS": f"{ratio * 100:.1f}%",
                "Cumulative LTV": f"${cum_ltv[day - 1]:.2f}",
            }
            for day, ratio in roas.items()
        ]
        st.subheader("ROAS checkpoints")
        st.dataframe(pd.DataFrame(roas_rows), hide_index=True, use_container_width=True)

        fig_roi = go.Figure()
        fig_roi.add_trace(
            go.Scatter(
                x=fit.forecast_days,
                y=cum_ltv,
                name="Cumulative LTV",
                fill="tozeroy",
            )
        )
        fig_roi.add_hline(
            y=ecpi,
            line_dash="dash",
            annotation_text="Break-even eCPI",
        )
        fig_roi.update_layout(
            title="Cumulative LTV vs. effective CPI",
            xaxis_title="Day",
            yaxis_title="Value ($)",
            height=500,
        )
        st.plotly_chart(fig_roi, use_container_width=True)

        report_df = pd.DataFrame(
            {
                "Day": fit.forecast_days,
                "ForecastRetention%": fit.forecast * 100,
                "CumulativeLTV": cum_ltv,
                "ROAS%": (cum_ltv / ecpi) * 100,
            }
        )
        st.download_button(
            "Download forecast CSV",
            data=report_df.to_csv(index=False),
            file_name="growth_forecast.csv",
            mime="text/csv",
        )

st.divider()
st.caption(
    "Game Growth Toolkit is an open-source scenario-planning tool. "
    "Forecasts depend on the assumptions and cohort data you provide."
)
