
import streamlit as st
import pandas as pd
import numpy as np
from components.header import header_component
from components.footer import footer_component
from components.sidebar import sidebar_component

# 1. Setup
st.set_page_config(page_title="LBO Model | FCFF & Debt", layout="wide")
sidebar_component()
header_component("LBO Valuation Framework", "FCFF & Debt Amortization Schedule")

# 2. Tabs
tab_home, tab_fcff, tab_analysis = st.tabs(["🏠 HOME (Inputs)", "📊 FCFF & DEBT SCHEDULE", "📈 RETURNS ANALYSIS"])

with tab_home:
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("### 🏢 Target Financials")
        ltm_rev = st.number_input("LTM Revenue ($)", value=3000000)
        ltm_ebitda = st.number_input("LTM EBITDA ($)", value=1500000)
        tax_rate = st.slider("Tax Rate (%)", 0, 40, 30) / 100
    with col2:
        st.markdown("### ⚙️ Debt & Operations")
        entry_mult = st.slider("Entry EV/EBITDA", 4.0, 15.0, 7.5)
        debt_pct = st.slider("Debt Financing (%)", 10, 90, 65) / 100
        int_rate = st.slider("Interest Rate (%)", 1.0, 15.0, 6.0) / 100
        repay_pct = st.slider("Mandatory Repayment (%)", 0, 20, 10) / 100

    st.markdown("### 📈 Operational Assumptions")
    growth = st.slider("Revenue Growth (%)", 0, 25, 10) / 100
    margin = st.slider("EBITDA Margin (%)", 10, 60, 40) / 100
    capex = st.number_input("Annual CapEx ($)", value=500000)
    depr = st.number_input("Annual Depreciation ($)", value=300000)
    wc_change = st.number_input("Change in WC ($)", value=-50000) # As per your Excel snippet

# 3. Calculation Engine (Shared across tabs)
ev = ltm_ebitda * entry_mult
debt_raised = ev * debt_pct
equity_invested = ev - debt_raised

years = [2025, 2026, 2027, 2028, 2029]
fcff_data = []
current_debt = debt_raised
curr_rev = ltm_rev

for y in years:
    curr_rev *= (1 + growth)
    ebitda = curr_rev * margin
    ebit = ebitda - depr
    interest = current_debt * int_rate
    ebt = ebit - interest
    net_income = ebt * (1 - tax_rate)
    
    # FCFF Calculation
    fcf = net_income + depr - capex - wc_change
    mandatory_repayment = current_debt * repay_pct
    ending_debt = current_debt - mandatory_repayment
    
    fcff_data.append({
        "Year": y,
        "Revenue": curr_rev,
        "EBITDA": ebitda,
        "Interest": interest,
        "Net Income": net_income,
        "FCF": fcf,
        "Debt Repayment": mandatory_repayment,
        "Ending Debt": ending_debt
    })
    current_debt = ending_debt

df_model = pd.DataFrame(fcff_data).set_index("Year")

with tab_fcff:
    st.subheader("Free Cash Flow to Firm (FCFF) Model")
    # Display FCFF metrics
    st.dataframe(df_model[["Revenue", "EBITDA", "Net Income", "FCF"]].T.style.format("${:,.0f}"))
    
    st.subheader("Debt Amortization Schedule")
    # Display Debt metrics
    st.table(df_model[["Interest", "Debt Repayment", "Ending Debt"]].T.style.format("${:,.0f}"))
    
    st.info("Ending Debt decreases annually based on the mandatory repayment percentage set in the Home tab.")

with tab_analysis:
    exit_mult = 8.0 # Default
    final_ebitda = df_model.iloc[-1]["EBITDA"]
    exit_val = final_ebitda * exit_mult
    debt_final = df_model.iloc[-1]["Ending Debt"]
    terminal_equity = exit_val - debt_final
    
    moic = terminal_equity / equity_invested
    irr = (moic**(1/5)) - 1
    
    st.subheader("Final Returns Analysis")
    c1, c2, c3 = st.columns(3)
    c1.metric("Exit Enterprise Value", f"${exit_val:,.0f}")
    c2.metric("MOIC", f"{moic:.2f}x")
    c3.metric("IRR", f"{irr*100:.2f}%")

footer_component()
