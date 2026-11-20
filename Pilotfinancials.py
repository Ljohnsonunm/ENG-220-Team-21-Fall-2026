import pandas as pd
import plotly.graph_objects as go
import streamlit as st

st.set_page_config(
    page_title="Cuba High-Desert Aquaponics Pilot",
    layout="wide",
)

st.title("Cuba, NM High-Desert Aquaponics Pilot — Cost & Labor Model")
st.caption(
    "Extrapolated from Desert Verde Farm (Santa Fe, NM), Engle (SRAC-5006), "
    "and Love et al. (2015) for a 2,000 sq. ft. coupled high-school greenhouse pilot."
)

# --- Base Data (Year 2 Steady-State & Startup CapEx) ---
capex_df = pd.DataFrame({
    "Category": [
        "Greenhouse Retrofit & Thermal Glazing",
        "Tanks, Clarifier, Mineralization & DWC Beds",
        "Winter Heating, Tank Insulation & Backup",
        "NMDGF Permits, Utility Tie-Ins & Contingency",
        "Pumps, Air Blowers, Plumbing & Sensors",
        "Initial Stock (Fingerlings, Seeds) & Tools",
    ],
    "Cost": [22000.0, 14500.0, 7500.0, 7500.0, 6500.0, 4000.0],
})
capex_df["Share (%)"] = (capex_df["Cost"] / capex_df["Cost"].sum() * 100).round(1)

labor_df = pd.DataFrame({
    "Role": [
        "Lead Farm Operator (Local Cuba Hire)",
        "CISD Student Intern #1",
        "CISD Student Intern #2",
    ],
    "Weekly Hours": [18, 6, 6],
    "Hourly Rate ($)": [22.00, 13.50, 13.50],
})
labor_df["Annual Hours"] = labor_df["Weekly Hours"] * 52
labor_df["Annual Wages ($)"] = labor_df["Annual Hours"] * labor_df["Hourly Rate ($)"]

payroll_taxes = labor_df["Annual Wages ($)"].sum() * 0.10
total_labor_opex = labor_df["Annual Wages ($)"].sum() + payroll_taxes

opex_df = pd.DataFrame({
    "Category": [
        "Local Labor & Payroll Taxes (30 hrs/wk)",
        "Winter Heating, Pumps & Aeration Utilities",
        "Feed, Fingerlings, Seeds & Water Buffers",
        "Packaging, Wash/Sanitation & Local Delivery",
        "Routine Maintenance & Water Test Reagents",
    ],
    "Annual Cost": [total_labor_opex, 6800.0, 6200.0, 2800.0, 2200.0],
})
opex_df["Share (%)"] = (opex_df["Annual Cost"] / opex_df["Annual Cost"].sum() * 100).round(1)

# --- Sidebar Controls for Interactive What-Ifs ---
st.sidebar.header("Scenario Controls")
sell_through_pct = st.sidebar.slider(
    "Marketable Greens Sell-Through (% of 72,800 heads/yr)",
    min_value=45,
    max_value=90,
    value=65,
    step=5,
)
head_price = st.sidebar.slider(
    "Avg. Institutional / Market Price per Head ($)",
    min_value=0.80,
    max_value=1.60,
    value=1.10,
    step=0.05,
)
fish_lbs_equiv = st.sidebar.slider(
    "Annual Live-Weight Tilapia Equivalent (lbs/yr)",
    min_value=1000,
    max_value=3500,
    value=1800,
    step=100,
)
fish_price_per_lb = 4.50

marketable_heads = 72800 * (sell_through_pct / 100.0)
greens_rev = marketable_heads * head_price
fish_rev = fish_lbs_equiv * fish_price_per_lb
total_rev = greens_rev + fish_rev
total_opex = opex_df["Annual Cost"].sum()
net_cashflow = total_rev - total_opex

# --- Top KPI Row ---
k1, k2, k3, k4 = st.columns(4)
k1.metric("Startup CapEx", f"${capex_df['Cost'].sum():,.0f}")
k2.metric("Annual OpEx", f"${total_opex:,.0f}")
k3.metric("Projected Annual Value / Sales", f"${total_rev:,.0f}")
k4.metric("Net Annual Operating Balance", f"${net_cashflow:+,.0f}")

# --- Interactive Tabs ---
tab1, tab2, tab3 = st.tabs([
    "Annual OpEx Breakdown",
    "Startup CapEx Breakdown",
    "Revenue vs. OpEx Scenario",
])

with tab1:
    fig_opex = go.Figure(
        go.Bar(
            x=opex_df["Annual Cost"],
            y=opex_df["Category"],
            orientation="h",
            text=[f"${v:,.0f} ({p:.1f}%)" for v, p in zip(opex_df["Annual Cost"], opex_df["Share (%)"])],
            textposition="outside",
            hovertemplate="%{y}<br>Annual Cost: $%{x:,.2f}<extra></extra>",
        )
    )
    fig_opex.update_layout(
        title="Annual Steady-State Operating Expenses (OpEx)",
        xaxis_title="USD / Year",
        yaxis=dict(autorange="reversed"),
        height=420,
        margin=dict(r=120),
    )
    st.plotly_chart(fig_opex, use_container_width=True)
    st.dataframe(labor_df, use_container_width=True, hide_index=True)

with tab2:
    fig_capex = go.Figure(
        go.Bar(
            x=capex_df["Cost"],
            y=capex_df["Category"],
            orientation="h",
            text=[f"${v:,.0f} ({p:.1f}%)" for v, p in zip(capex_df["Cost"], capex_df["Share (%)"])],
            textposition="outside",
            hovertemplate="%{y}<br>Startup Cost: $%{x:,.2f}<extra></extra>",
        )
    )
    fig_capex.update_layout(
        title="Estimated Startup Capital Expenditure (CapEx) — 2,000 sq. ft. Pilot",
        xaxis_title="USD",
        yaxis=dict(autorange="reversed"),
        height=420,
        margin=dict(r=120),
    )
    st.plotly_chart(fig_capex, use_container_width=True)

with tab3:
    fig_scen = go.Figure()
    fig_scen.add_trace(
        go.Bar(
            name="Greens Revenue / Value",
            x=["Projected Scenario", "Steady-State OpEx"],
            y=[greens_rev, 0.0],
            hovertemplate="%{x}<br>Greens: $%{y:,.2f}<extra></extra>",
        )
    )
    fig_scen.add_trace(
        go.Bar(
            name="Tilapia Revenue / Value",
            x=["Projected Scenario", "Steady-State OpEx"],
            y=[fish_rev, 0.0],
            hovertemplate="%{x}<br>Tilapia: $%{y:,.2f}<extra></extra>",
        )
    )
    fig_scen.add_trace(
        go.Bar(
            name="Annual OpEx",
            x=["Projected Scenario", "Steady-State OpEx"],
            y=[0.0, total_opex],
            hovertemplate="%{x}<br>OpEx: $%{y:,.2f}<extra></extra>",
        )
    )
    fig_scen.update_layout(
        barmode="stack",
        title=f"Revenue vs. OpEx ({sell_through_pct}% Sell-Through @ ${head_price:.2f}/head)",
        yaxis_title="USD / Year",
        height=420,
    )
    st.plotly_chart(fig_scen, use_container_width=True)
