
import streamlit as st
import pandas as pd
import numpy as np
from components.header import header_component
from components.footer import footer_component
from components.sidebar import sidebar_component

# 1. Page Config & Components
st.set_page_config(page_title="LBO Model | The Mountain Path", layout="wide")
sidebar_component()
header_component("LBO Valuation Framework", "Institutional FCFF & Debt Amortization")

# 2. Create the 4-Tab Structure
tab_home, tab_fcff, tab_graphs, tab_analysis = st.tabs([
    "🏠 HOME", "📊 FCFF & DEBT", "📈 GRAPHICAL OUTPUT", "🚀 RETURNS"
])

# --- TAB 1: HOME (Inputs) ---
with tab_home:
    col1, col2 = st.columns(2)
    with col1:
        st.markdown('<div style="background-color:#FFD700; color:#002147; padding:5px; border-radius:5px; text-align:center; font-weight:bold;">🏢 TARGET FINANCIALS</div>', unsafe_allow_html=True)
        ltm_rev = st.number_input("LTM Revenue ($)", value=3000000)
        ltm_ebitda = st.number_input("LTM EBITDA ($)", value=1500000)
        tax_rate = st.slider("Tax Rate (%)", 0, 40, 30) / 100
        growth = st.slider("Revenue Growth (%)", 0, 25, 10) / 100
        margin = st.slider("EBITDA Margin (%)", 10, 60, 40) / 100

    with col2:
        st.markdown('<div style="background-color:#FFD700; color:#002147; padding:5px; border-radius:5px; text-align:center; font-weight:bold;">⚙️ TRANSACTION & DEBT</div>', unsafe_allow_html=True)
        entry_mult = st.slider("Entry EV/EBITDA", 4.0, 15.0, 7.5)
        debt_pct = st.slider("Debt Financing (%)", 10, 90, 65) / 100
        int_rate = st.slider("Interest Rate (%)", 1.0, 15.0, 6.0) / 100
        repay_pct = st.slider("Mandatory Repayment (%)", 0, 20, 10) / 100
        exit_mult = st.slider("Exit EV/EBITDA", 4.0, 15.0, 8.0)

# --- CALCULATION ENGINE ---
ev = ltm_ebitda * entry_mult
debt_raised = (ev + (ev * 0.05)) * debt_pct # Including 5% fees
equity_invested = (ev + (ev * 0.05)) - debt_raised

years = [2025, 2026, 2027, 2028, 2029]
projection_data = []
current_debt = debt_raised
curr_rev = ltm_rev

for y in years:
    curr_rev *= (1 + growth)
    ebitda = curr_rev * margin
    ebit = ebitda - 300000 # Depr
    interest = current_debt * int_rate
    net_income = (ebit - interest) * (1 - tax_rate)
    fcf = net_income + 300000 - 500000 - (-50000) # NI + Depr - Capex - WC
    repayment = current_debt * repay_pct
    
    projection_data.append({
        "Year": y, "Revenue": curr_rev, "EBITDA": ebitda, "Interest": interest,
        "FCF": fcf, "Debt Repayment": repayment, "Ending Debt": current_debt - repayment
    })
    current_debt -= repayment

df = pd.DataFrame(projection_data).set_index("Year")

# --- TAB 2: FCFF & DEBT SCHEDULE ---
with tab_fcff:
    st.subheader("Free Cash Flow to Firm (FCFF)")
    st.dataframe(df[["Revenue", "EBITDA", "Interest", "FCF"]].T.style.format("${:,.0f}"))
    
    st.subheader("Debt Amortization Schedule")
    st.table(df[["Interest", "Debt Repayment", "Ending Debt"]].T.style.format("${:,.0f}"))

# --- TAB 3: GRAPHICAL OUTPUT ---
with tab_graphs:
    st.subheader("Visual Financial Trends")
    g1, g2 = st.columns(2)
    
    with g1:
        st.write("#### Revenue vs EBITDA Growth")
        st.line_chart(df[["Revenue", "EBITDA"]])
        
    with g2:
        st.write("#### Debt Deleveraging Profile")
        st.bar_chart(df["Ending Debt"])
    
    st.write("#### Free Cash Flow available for Debt Service")
    st.area_chart(df["FCF"])

# --- TAB 4: RETURNS ANALYSIS ---
with tab_analysis:
    final_ebitda = df.iloc[-1]["EBITDA"]
    exit_val = final_ebitda * exit_mult
    debt_rem = df.iloc[-1]["Ending Debt"]
    term_equity = exit_val - debt_rem
    moic = term_equity / equity_invested
    irr = (moic**(1/5)) - 1

    st.subheader("Return Metrics")
    m1, m2, m3 = st.columns(3)
    m1.metric("Equity Invested", f"${equity_invested:,.0f}")
    m2.metric("MOIC", f"{moic:.2f}x")
    m3.metric("IRR", f"{irr*100:.2f}%")

footer_component()
