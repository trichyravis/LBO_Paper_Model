
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from components.header import header_component
from components.footer import footer_component
from components.sidebar import sidebar_component

# Setup
st.set_page_config(page_title="LBO Model | Institutional Suite", layout="wide")
sidebar_component()
header_component("LBO Valuation Framework", "FCFF, Debt Amortization & Returns Analysis")

# 1. TABS DEFINITION
tab_home, tab_fcff, tab_graphs, tab_analysis = st.tabs([
    "🏠 HOME (Inputs)", "📊 FCFF & DEBT", "📈 GRAPHICAL OUTPUT", "🚀 RETURNS & SENSITIVITY"
])

# --- TAB 1: HOME (All user inputs) ---
with tab_home:
    col1, col2 = st.columns(2)
    with col1:
        st.markdown('<div style="background-color:#FFD700; color:#002147; padding:10px; border-radius:5px; text-align:center; font-weight:bold;">🏢 TARGET FINANCIALS</div>', unsafe_allow_html=True)
        ltm_rev = st.number_input("LTM Revenue ($)", value=3000000)
        ltm_ebitda = st.number_input("LTM EBITDA ($)", value=1500000)
        growth = st.slider("Annual Revenue Growth (%)", 0, 30, 10) / 100
        margin = st.slider("EBITDA Margin (%)", 10, 60, 40) / 100
        tax_rate = st.slider("Tax Rate (%)", 0, 40, 30) / 100

    with col2:
        st.markdown('<div style="background-color:#FFD700; color:#002147; padding:10px; border-radius:5px; text-align:center; font-weight:bold;">⚙️ TRANSACTION & DEBT</div>', unsafe_allow_html=True)
        entry_mult = st.slider("Entry EV/EBITDA", 4.0, 15.0, 7.5)
        debt_pct = st.slider("Debt Financing (%)", 10, 90, 65) / 100
        int_rate = st.slider("Interest Rate (%)", 1.0, 15.0, 6.0) / 100
        repay_pct = st.slider("Mandatory Repayment (%)", 0, 20, 10) / 100
        exit_mult = st.slider("Exit EV/EBITDA Multiple", 4.0, 15.0, 8.0)

# --- ENGINE: CALCULATIONS ---
ev = ltm_ebitda * entry_mult
total_cost = ev * 1.05 # 5% fees
debt_raised = total_cost * debt_pct
equity_invested = total_cost - debt_raised

years = [2025, 2026, 2027, 2028, 2029]
proj_list = []
curr_debt = debt_raised
curr_rev = ltm_rev

for y in years:
    curr_rev *= (1 + growth)
    ebitda = curr_rev * margin
    ebit = ebitda - 300000 # Depreciation
    interest = curr_debt * int_rate
    net_income = (ebit - interest) * (1 - tax_rate)
    fcf = net_income + 300000 - 500000 - (-50000) # FCFF formula
    repayment = curr_debt * repay_pct
    
    proj_list.append({
        "Year": y, "Revenue": curr_rev, "EBITDA": ebitda, "Interest": interest,
        "Net Income": net_income, "FCF": fcf, "Repayment": repayment, "Ending Debt": curr_debt - repayment
    })
    curr_debt -= repayment

df = pd.DataFrame(proj_list).set_index("Year")

# --- TAB 2: FCFF & DEBT SCHEDULE ---
with tab_fcff:
    st.subheader("Free Cash Flow & Debt Waterfall")
    st.write("### 💵 Free Cash Flow to Firm (FCFF)")
    st.dataframe(df[["Revenue", "EBITDA", "Net Income", "FCF"]].T.style.format("${:,.0f}"))
    
    st.write("### 💳 Debt Amortization Schedule")
    st.table(df[["Interest", "Repayment", "Ending Debt"]].T.style.format("${:,.0f}"))

# --- TAB 3: GRAPHICAL OUTPUT ---
with tab_graphs:
    st.subheader("Financial Visualization")
    c1, c2 = st.columns(2)
    with c1:
        st.plotly_chart(px.line(df, y=["Revenue", "EBITDA"], title="Top Line & Profitability Growth"), use_container_width=True)
    with c2:
        st.plotly_chart(px.bar(df, y="Ending Debt", title="Deleveraging Profile (Debt Paydown)"), use_container_width=True)
    
    st.plotly_chart(px.area(df, y="FCF", title="Cash Flow Available for Debt Service"), use_container_width=True)

# --- TAB 4: RETURNS & SENSITIVITY ---
with tab_analysis:
    final_ebitda = df.iloc[-1]["EBITDA"]
    exit_val = final_ebitda * exit_mult
    debt_final = df.iloc[-1]["Ending Debt"]
    term_equity = exit_val - debt_final
    moic = term_equity / equity_invested
    irr = (moic**(1/5)) - 1

    st.subheader("Investment Returns")
    m1, m2, m3 = st.columns(3)
    m1.metric("Equity Invested", f"${equity_invested:,.0f}")
    m2.metric("MOIC", f"{moic:.2f}x")
    m3.metric("IRR", f"{irr*100:.2f}%")

    st.write("---")
    st.subheader("Sensitivity Analysis: Exit Multiple vs. IRR")
    multiples = [exit_mult - 1, exit_mult - 0.5, exit_mult, exit_mult + 0.5, exit_mult + 1]
    sens_data = []
    for m in multiples:
        s_ev = final_ebitda * m
        s_term_eq = s_ev - debt_final
        s_moic = s_term_eq / equity_invested
        s_irr = (s_moic**(1/5)) - 1
        # Correct: The 'x' is outside the curly braces or after the format specifier
    sens_data.append({"Exit Multiple": f"{m}x", "IRR": f"{s_irr*100:.2f}%", "MOIC": f"{s_moic:.2f}x"})
    
    st.table(pd.DataFrame(sens_data))

footer_component()
