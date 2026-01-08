
import streamlit as st
import pandas as pd
import numpy as np
import numpy_financial as npf
from components.header import header_component
from components.footer import footer_component
from components.sidebar import sidebar_component

# 1. Page Configuration
st.set_page_config(
    page_title="LBO Model | The Mountain Path",
    page_icon="🏔️",
    layout="wide"
)

# 2. Header Component
header_component(
    title="LBO Investment Model", 
    subtitle="Leveraged Buyout Analysis & Returns Projection"
)

# 3. Sidebar Component (Modified to capture LBO inputs)
# Note: Based on your uploaded sidebar.py styling, we use the same CSS
# but update the inputs to match your Excel "Transaction Assumptions"
st.markdown("""
    <style>
    [data-testid="stSidebar"] {background-color: #002147 !important;}
    [data-testid="stSidebar"] .stMarkdown p, [data-testid="stSidebar"] label {color: white !important; font-weight: bold;}
    div.stButton > button:first-child {
        background-color: #FFD700 !important; 
        color: #002147 !important; 
        font-weight: bold !important; 
        width: 100%; 
        border-radius: 8px; 
        border: none;
    }
    </style>
""", unsafe_allow_html=True)

with st.sidebar:
    st.header("🏢 Target Financials")
    ltm_revenue = st.number_input("LTM Revenue ($)", value=3000000, step=100000)
    ltm_ebitda = st.number_input("LTM EBITDA ($)", value=1500000, step=50000)
    
    st.header("⚙️ Transaction Setup")
    entry_multiple = st.slider("Entry EV/EBITDA Multiple", 4.0, 15.0, 7.46)
    debt_pct = st.slider("Debt Financing (%)", 10, 90, 65) / 100
    fee_pct = st.slider("Transaction Fees (%)", 1.0, 10.0, 5.0) / 100
    
    st.header("📈 Growth & Exit")
    rev_growth = st.slider("Annual Revenue Growth (%)", 0, 25, 10) / 100
    ebitda_margin = st.slider("EBITDA Margin (%)", 10, 60, 40) / 100
    exit_multiple = st.slider("Exit EV/EBITDA Multiple", 4.0, 15.0, 8.0)
    
    run_btn = st.button("🚀 EXECUTE LBO ANALYSIS")

# 4. Main Application Logic
if run_btn:
    # --- Transaction Summary ---
    enterprise_value = ltm_ebitda * entry_multiple
    fees = enterprise_value * fee_pct
    total_purchase_price = enterprise_value + fees
    debt_raised = total_purchase_price * debt_pct
    equity_invested = total_purchase_price - debt_raised

    # --- 5-Year Financial Projection ---
    years = [2025, 2026, 2027, 2028, 2029]
    projection_data = []
    current_rev = ltm_revenue
    
    # Simple Debt Schedule Assumptions (based on your Excel logic)
    interest_rate = 0.06
    mandatory_repay_pct = 0.10
    current_debt = debt_raised

    for year in years:
        current_rev *= (1 + rev_growth)
        ebitda = current_rev * ebitda_margin
        interest = current_debt * interest_rate
        repayment = current_debt * mandatory_repay_pct
        current_debt -= repayment
        
        projection_data.append({
            "Year": year,
            "Revenue": current_rev,
            "EBITDA": ebitda,
            "Interest Expense": interest,
            "Debt Repayment": repayment,
            "Remaining Debt": current_debt
        })

    df_proj = pd.DataFrame(projection_data)

    # --- Returns Analysis ---
    final_ebitda = df_proj.iloc[-1]["EBITDA"]
    exit_value = final_ebitda * exit_multiple
    debt_remaining = df_proj.iloc[-1]["Remaining Debt"]
    terminal_equity_value = exit_value - debt_remaining
    
    moic = terminal_equity_value / equity_invested
    irr = (moic ** (1/5)) - 1

    # --- Display Results ---
    st.subheader("Investment Returns")
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Equity Check", f"${equity_invested:,.0f}")
    c2.metric("Exit Equity", f"${terminal_equity_value:,.0f}")
    c3.metric("MOIC", f"{moic:.2fx}")
    c4.metric("IRR", f"{irr*100:.2f}%")

    st.subheader("Financial Projections")
    st.dataframe(df_proj.set_index("Year").style.format("${:,.0f}"))

    st.subheader("Cash Flow Trajectory")
    st.area_chart(df_proj.set_index("Year")[["Revenue", "EBITDA"]])

else:
    # Welcome screen before calculation
    st.info("👈 Please adjust the transaction and operational assumptions in the sidebar and click 'Execute LBO Analysis'.")
    
    # Optional: Display a breakdown of the Sources and Uses based on default inputs
    st.write("### Preliminary Transaction Structure")
    st.write(f"At an entry multiple of **{entry_multiple}x**, the Enterprise Value is **${ltm_ebitda * entry_multiple:,.0f}**.")

# 5. Footer Component
footer_component()
