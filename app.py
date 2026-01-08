
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import io

# Import custom components
from components.header import header_component
from components.footer import footer_component
from components.sidebar import sidebar_component

# 1. Page Configuration
st.set_page_config(
    page_title="LBO Model | The Mountain Path",
    page_icon="🏔️",
    layout="wide"
)

# Apply Sidebar Styling & Branding
sidebar_component()

# Apply Header
header_component(
    title="LBO Valuation Framework", 
    subtitle="Institutional FCFF, Debt Amortization & Returns Analysis"
)

# 2. Create Tabs
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
        debt_pct = st.slider("Debt Financing (% of Purchase)", 10, 90, 65) / 100
        int_rate = st.slider("Interest Rate on Debt (%)", 1.0, 15.0, 6.0) / 100
        repay_pct = st.slider("Mandatory Annual Repayment (%)", 0, 20, 10) / 100
        exit_mult = st.slider("Exit EV/EBITDA Multiple", 4.0, 15.0, 8.0)

    st.info("Adjust the assumptions above. The model updates automatically across all tabs.")

# --- CALCULATION ENGINE (Shared Logic) ---
# Transaction Summary
ev = ltm_ebitda * entry_mult
fees = ev * 0.05
total_acquisition_cost = ev + fees
debt_raised = total_acquisition_cost * debt_pct
equity_invested = total_acquisition_cost - debt_raised

# 5-Year Projection Logic
years = [2025, 2026, 2027, 2028, 2029]
proj_results = []
current_debt = debt_raised
curr_rev = ltm_rev

for y in years:
    curr_rev *= (1 + growth)
    ebitda = curr_rev * margin
    depreciation = 300000  # Based on Excel Workout
    ebit = ebitda - depreciation
    interest = current_debt * int_rate
    taxable_income = ebit - interest
    tax = max(0, taxable_income * tax_rate)
    net_income = taxable_income - tax
    
    # FCFF Formula: NI + Depr - CapEx - Change in WC
    # Assumptions from your Excel snippet: CapEx (500k), WC Change (-50k)
    fcf = net_income + depreciation - 500000 - (-50000) 
    
    repayment = current_debt * repay_pct
    ending_debt = current_debt - repayment
    
    proj_results.append({
        "Year": y,
        "Revenue": curr_rev,
        "EBITDA": ebitda,
        "Interest": interest,
        "Net Income": net_income,
        "FCF": fcf,
        "Debt Repayment": repayment,
        "Ending Debt": ending_debt
    })
    current_debt = ending_debt

df = pd.DataFrame(proj_results).set_index("Year")

# --- TAB 2: FCFF & DEBT SCHEDULE ---
with tab_fcff:
    st.subheader("Free Cash Flow to Firm (FCFF) Waterfall")
    st.dataframe(df[["Revenue", "EBITDA", "Net Income", "FCF"]].T.style.format("${:,.0f}"))
    
    st.subheader("Debt Amortization Schedule")
    st.table(df[["Interest", "Debt Repayment", "Ending Debt"]].T.style.format("${:,.0f}"))

# --- TAB 3: GRAPHICAL OUTPUT ---
with tab_graphs:
    st.subheader("Visual Performance Trends")
    c1, c2 = st.columns(2)
    
    with c1:
        fig_rev = px.line(df, y=["Revenue", "EBITDA"], title="Revenue & EBITDA Growth", markers=True)
        st.plotly_chart(fig_rev, use_container_width=True)
    
    with c2:
        fig_debt = px.bar(df, y="Ending Debt", title="Deleveraging Profile (Debt Paydown)", color_discrete_sequence=['#FFD700'])
        st.plotly_chart(fig_debt, use_container_width=True)
    
    st.write("#### Annual Free Cash Flow Generation")
    st.area_chart(df["FCF"])

# --- TAB 4: RETURNS & SENSITIVITY ---
with tab_analysis:
    # Exit Calculations
    final_ebitda = df.iloc[-1]["EBITDA"]
    exit_value = final_ebitda * exit_mult
    debt_remaining = df.iloc[-1]["Ending Debt"]
    terminal_equity_value = exit_value - debt_remaining
    
    moic = terminal_equity_value / equity_invested
    irr = (moic**(1/5)) - 1

    st.subheader("Investment Returns Summary")
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Equity Invested", f"${equity_invested:,.0f}")
    m2.metric("Terminal Equity", f"${terminal_equity_value:,.0f}")
    m3.metric("MOIC", f"{moic:.2f}x")
    m4.metric("IRR", f"{irr*100:.2f}%")

    st.write("---")
    
    # Sensitivity Table
    st.subheader("Sensitivity Analysis: Exit Multiple vs. IRR")
    multiples = [exit_mult - 1.0, exit_mult - 0.5, exit_mult, exit_mult + 0.5, exit_mult + 1.0]
    sens_list = []
    
    for m in multiples:
        s_exit_val = final_ebitda * m
        s_term_eq = s_exit_val - debt_remaining
        s_moic = s_term_eq / equity_invested
        s_irr = (s_moic**(1/5)) - 1
        
        sens_list.append({
            "Exit Multiple": f"{m:.1f}x",
            "IRR (%)": f"{s_irr*100:.2f}%",
            "MOIC (x)": f"{s_moic:.2f}x"
        })
    
    sens_df = pd.DataFrame(sens_list)
    st.table(sens_df)

    # Download Feature
    st.write("---")
    st.subheader("📥 Export Financial Data")
    csv = df.to_csv().encode('utf-8')
    st.download_button(
        label="Download Full Projection (CSV)",
        data=csv,
        file_name='lbo_projections.csv',
        mime='text/csv',
    )

# Footer
footer_component()
