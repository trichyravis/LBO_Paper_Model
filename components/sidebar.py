
import streamlit as st

def sidebar_component():
    # Force the sidebar background and standard label colors
    st.markdown('''
        <style>
        [data-testid="stSidebar"] {
            background-color: #002147 !important;
        }
        [data-testid="stSidebar"] label, [data-testid="stSidebar"] .stMarkdown p {
            color: white !important;
            font-weight: bold !important;
        }
        /* Button Styling */
        div.stButton > button:first-child {
            background-color: #FFD700 !important;
            color: #002147 !important;
            font-weight: bold !important;
            width: 100%;
            border: none;
        }
        </style>
    ''', unsafe_allow_html=True)
    
    with st.sidebar:
        # --- HEADER 1 ---
        st.markdown(
            '<div style="background-color: #FFD700; color: #002147; padding: 10px; border-radius: 5px; text-align: center; font-weight: bold; margin-bottom: 10px;">'
            '🏢 TARGET FINANCIALS'
            '</div>', 
            unsafe_allow_html=True
        )
        ltm_rev = st.number_input("LTM Revenue ($)", value=3000000)
        ltm_ebitda = st.number_input("LTM EBITDA ($)", value=1500000)
        
        # --- HEADER 2 ---
        st.markdown(
            '<div style="background-color: #FFD700; color: #002147; padding: 10px; border-radius: 5px; text-align: center; font-weight: bold; margin-top: 20px; margin-bottom: 10px;">'
            '⚙️ TRANSACTION SETUP'
            '</div>', 
            unsafe_allow_html=True
        )
        entry_mult = st.slider("Entry EV/EBITDA", 4.0, 15.0, 7.5)
        debt_pct = st.slider("Debt Financing (%)", 10, 90, 65) / 100
        
        # --- HEADER 3 ---
        st.markdown(
            '<div style="background-color: #FFD700; color: #002147; padding: 10px; border-radius: 5px; text-align: center; font-weight: bold; margin-top: 20px; margin-bottom: 10px;">'
            '📈 GROWTH & EXIT'
            '</div>', 
            unsafe_allow_html=True
        )
        growth = st.slider("Annual Revenue Growth (%)", 0, 30, 10) / 100
        margin = st.slider("EBITDA Margin (%)", 10, 60, 40) / 100
        exit_mult = st.slider("Exit EV/EBITDA", 4.0, 15.0, 8.0)
        
        st.write("---")
        run_btn = st.button("🚀 EXECUTE LBO ANALYSIS")
        
    return ltm_rev, ltm_ebitda, entry_mult, debt_pct, growth, margin, exit_mult, run_btn
