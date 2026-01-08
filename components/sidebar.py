import streamlit as st

def sidebar_component():
    # Injecting your custom branding CSS
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
        ltm_rev = st.number_input("LTM Revenue ($)", value=3000000, step=100000)
        ltm_ebitda = st.number_input("LTM EBITDA ($)", value=1500000, step=50000)
        
        st.header("⚙️ Transaction")
        entry_mult = st.slider("Entry EV/EBITDA", 4.0, 15.0, 7.5)
        debt_pct = st.slider("Debt Financing (%)", 10, 90, 65) / 100
        
        st.header("📈 Projections")
        growth = st.slider("Annual Revenue Growth (%)", 0, 30, 10) / 100
        ebitda_margin = st.slider("EBITDA Margin (%)", 10, 60, 40) / 100
        exit_mult = st.slider("Exit EV/EBITDA", 4.0, 15.0, 8.0)
        
        run_btn = st.button("🚀 RUN LBO ANALYSIS")
        
    return ltm_rev, ltm_ebitda, entry_mult, debt_pct, growth, ebitda_margin, exit_mult, run_btn
