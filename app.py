
import streamlit as st
import pandas as pd
from components.header import header_component
from components.footer import footer_component
from components.sidebar import sidebar_component

# 1. Setup
st.set_page_config(page_title="LBO Model | Tabs", layout="wide")
sidebar_component()
header_component("LBO Valuation Framework", "Institutional Private Equity Modeling")

# 2. Create Tabs
tab_home, tab_analysis = st.tabs(["🏠 HOME (Inputs)", "📊 INVESTMENT ANALYSIS"])

with tab_home:
    st.subheader("Step 1: Define Transaction & Financial Assumptions")
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("### 🏢 Target Financials")
        ltm_rev = st.number_input("LTM Revenue ($)", value=3000000, step=100000)
        ltm_ebitda = st.number_input("LTM EBITDA ($)", value=1500000, step=50000)
        ebitda_margin = st.slider("Target EBITDA Margin (%)", 10, 60, 40) / 100

    with col2:
        st.markdown("### ⚙️ Transaction Setup")
        entry_mult = st.slider("Entry EV/EBITDA Multiple", 4.0, 15.0, 7.5)
        debt_pct = st.slider("Debt Financing (%)", 10, 90, 65) / 100
        exit_mult = st.slider("Exit EV/EBITDA Multiple", 4.0, 15.0, 8.0)

    st.markdown("---")
    st.markdown("### 📈 Operational Projections")
    growth = st.select_slider("Annual Revenue Growth (%)", options=[0, 5, 10, 15, 20, 25], value=10) / 100
    
    if st.button("🚀 CALCULATE & PROCEED TO ANALYSIS"):
        st.success("Calculations complete! Please click on the 'INVESTMENT ANALYSIS' tab above.")

with tab_analysis:
    # Logic performed only when moving to this tab
    ev = ltm_ebitda * entry_mult
    equity_invested = ev * (1 - debt_pct)
    
    # Simple 5-Year Projection
    years = [2025, 2026, 2027, 2028, 2029]
    rev_proj = [ltm_rev * (1 + growth)**i for i in range(1, 6)]
    ebitda_proj = [r * ebitda_margin for r in rev_proj]
    
    # Exit Calculations
    exit_value = ebitda_proj[-1] * exit_mult
    moic = exit_value / (equity_invested + 1e-9) # Prevent div by zero
    irr = (moic**(1/5)) - 1

    st.subheader("Financial Performance Summary")
    
    m1, m2, m3 = st.columns(3)
    m1.metric("Equity Invested", f"${equity_invested:,.0f}")
    m2.metric("MOIC", f"{moic:.2f}x")
    m3.metric("IRR", f"{irr*100:.2f}%")

    st.markdown("---")
    
    # Visualizations
    st.write("### Revenue & EBITDA Forecast")
    chart_df = pd.DataFrame({
        "Year": years,
        "Revenue": rev_proj,
        "EBITDA": ebitda_proj
    }).set_index("Year")
    st.line_chart(chart_df)

# 3. Footer
footer_component()
