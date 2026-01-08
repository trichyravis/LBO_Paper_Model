
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import io

# 1. Import institutional components
from components.header import header_component
from components.footer import footer_component
from components.sidebar import sidebar_component

# Page Configuration
st.set_page_config(
    page_title="LBO Model | The Mountain Path",
    page_icon="🏔️",
    layout="wide"
)

# Render Sidebar Branding
sidebar_component()

# Render Header with stretch-width logic
header_component(
    title="LBO Investment Dashboard", 
    subtitle="Institutional Leveraged Buyout & Debt Waterfall Analysis"
)

# 2. Tab Navigation
tab_home, tab_fcff, tab_graphs, tab_analysis = st.tabs([
    "🏠 HOME (Inputs)", 
    "📊 FCFF & DEBT SCHEDULE", 
    "📈 GRAPHICAL OUTPUT", 
    "🚀 RETURNS & SENSITIVITY"
])

# --- TAB 1: HOME (Inputs) ---
with tab_home:
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('<div style="background-color:#FFD700; color:#002147; padding:10px; border-radius:5px; text-align:center; font-weight:bold; margin-bottom:10px;">🏢 TARGET FINANCIALS</div>', unsafe_allow_html=True)
        ltm_rev = st.number_input("LTM Revenue ($)", value=3000000, step=100000)
        ltm_ebitda = st.number_input("LTM EBITDA ($)", value=1500000, step=50000)
        growth = st.slider("Annual Revenue Growth (%)", 0, 30, 10) / 100
        margin = st.slider("EBITDA Margin (%)", 10, 60, 40) / 100
        tax_rate = st.slider("Tax Rate (%)", 0, 40, 30) / 100

    with col2:
        st.markdown('<div style="background-color:#FFD700; color:#002147; padding:10px; border-radius:5px; text-align:center; font-weight:bold; margin-bottom:10px;">⚙️ TRANSACTION & DEBT</div>', unsafe_allow_html=True)
        entry_mult = st.slider("Entry EV/EBITDA Multiple", 4.0, 15.0, 7.5)
        debt_pct = st.slider("Debt Financing (% of Total Cost)", 10, 90, 65) / 100
        int_rate = st.slider("Interest Rate on Debt (%)", 1.0, 15.0, 6.0) / 100
        repay_pct = st.slider("Mandatory Annual Repayment (%)", 0, 20, 10) / 100
        exit_mult = st.slider("Exit EV/EBITDA Multiple", 4.0, 15.0, 8.0)

# --- ENGINE: CALCULATION LOGIC ---
ev = ltm_ebitda * entry_mult
fees = ev * 0.05
total_acquisition_cost = ev + fees
debt_raised = total_acquisition_cost * debt_pct
equity_invested = total_acquisition_cost - debt_raised

years = [2025, 2026, 2027, 2028, 2029]
proj_results = []
current_debt = debt_raised
curr_rev = ltm_rev

for y in years:
    curr_rev *= (1 + growth)
    ebitda = curr_rev * margin
    depr = 300000
    ebit = ebitda - depr
    interest = current_debt * int_rate
    tax = max(0, (ebit - interest) * tax_rate)
    net_income = ebit - interest - tax
    
    # FCF = Net Income + Depr - CapEx (500k) - WC Change (-50k)
    fcf = net_income + depr - 500000 - (-50000)
    repayment = current_debt * repay_pct
    
    proj_results.append({
        "Year": y, "Revenue": curr_rev, "EBITDA": ebitda, "Interest": interest,
        "Net Income": net_income, "FCF": fcf, "Repayment": repayment, "Ending Debt": current_debt - repayment
    })
    current_debt -= repayment

df = pd.DataFrame(proj_results).set_index("Year")

# --- TAB 2: FCFF & DEBT SCHEDULE ---
with tab_fcff:
    st.subheader("Financial Waterfall Analysis")
    st.dataframe(df[["Revenue", "EBITDA", "Net Income", "FCF"]].T.style.format("${:,.0f}"))
    
    st.subheader("Debt Amortization (Mandatory Repayment)")
    st.table(df[["Interest", "Repayment", "Ending Debt"]].T.style.format("${:,.0f}"))

# --- TAB 3: GRAPHICAL OUTPUT ---
with tab_graphs:
    st.subheader("Visual Performance Trends")
    c1, c2 = st.columns(2)
    
    with c1:
        # Fixed for 2026: width="stretch"
        fig_rev = px.line(df, y=["Revenue", "EBITDA"], title="Revenue & EBITDA Trajectory", markers=True)
        st.plotly_chart(fig_rev, width="stretch")
    
    with c2:
        fig_debt = px.bar(df, y="Ending Debt", title="Annual Deleveraging Profile", color_discrete_sequence=['#FFD700'])
        st.plotly_chart(fig_debt, width="stretch")
    
    st.write("#### Free Cash Flow Cushion")
    st.area_chart(df["FCF"])

# --- TAB 4: RETURNS & SENSITIVITY ---
with tab_analysis:
    final_ebitda = df.iloc[-1]["EBITDA"]
    exit_value = final_ebitda * exit_mult
    debt_rem = df.iloc[-1]["Ending Debt"]
    term_equity = exit_value - debt_rem
    moic = term_equity / equity_invested
    irr = (moic**(1/5)) - 1

    st.subheader("Key Return Metrics")
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Equity Invested", f"${equity_invested:,.0f}")
    m2.metric("Terminal Equity", f"${term_equity:,.0f}")
    m3.metric("MOIC", f"{moic:.2f}x")
    m4.metric("IRR", f"{irr*100:.2f}%")

    st.write("---")
    st.subheader("Sensitivity Analysis: Exit Multiple vs. IRR")
    multiples = [exit_mult - 1.0, exit_mult - 0.5, exit_mult, exit_mult + 0.5, exit_mult + 1.0]
    sens_list = []
    for m in multiples:
        s_val = (final_ebitda * m) - debt_rem
        s_moic = s_val / equity_invested
        s_irr = (s_moic**(1/5)) - 1
        sens_list.append({"Exit Multiple": f"{m:.1f}x", "IRR": f"{s_irr*100:.2f}%", "MOIC": f"{s_moic:.2f}x"})
    
    st.table(pd.DataFrame(sens_list))

    st.download_button(
        label="Download Full Projection (CSV)",
        data=df.to_csv().encode('utf-8'),
        file_name='lbo_model_data.csv',
        mime='text/csv',
    )

# Render Footer
footer_component()
