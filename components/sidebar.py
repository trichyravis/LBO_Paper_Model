
import streamlit as st

def sidebar_component():
    # Force the sidebar and headers to be visible and styled correctly
    st.markdown('''
        <style>
        /* Force Sidebar Background */
        [data-testid="stSidebar"] {
            background-color: #002147 !important;
        }
        
        /* Force all Labels and standard text to White */
        [data-testid="stSidebar"] .stMarkdown p, 
        [data-testid="stSidebar"] label,
        [data-testid="stSidebar"] .stWidgetLabel p {
            color: white !important; 
            font-weight: bold !important;
            font-size: 1rem !important;
        }

        /* GOLD HEADER STYLE: This simulates the button look for section titles */
        .gold-header {
            background-color: #FFD700 !important;
            color: #002147 !important;
            padding: 8px 15px !important;
            border-radius: 8px !important;
            font-weight: bold !important;
            text-align: center !important;
            margin: 20px 0px 10px 0px !important;
            font-size: 1.1rem !important;
            display: block !important;
            width: 100% !important;
        }
        
        /* The Execute Button Styling */
        div.stButton > button:first-child {
            background-color: #FFD700 !important; 
            color: #002147 !important; 
            font-weight: bold !important; 
            width: 100% !important; 
            border-radius: 8px !important; 
            border: 2px solid #FFD700 !important;
            height: 3em !important;
        }
        </style>
    ''', unsafe_allow_html=True)
    
    with st.sidebar:
        # We use manual HTML tags instead of st.header to guarantee visibility
        st.markdown('<div class="gold-header">🏢 TARGET FINANCIALS</div>', unsafe_allow_html=True)
        ltm_rev = st.number_input("LTM Revenue ($)", value=3000000, step=100000)
        ltm_ebitda = st.number_input("LTM EBITDA ($)", value=1500000, step=50000)
        
        st.markdown('<div class="gold-header">⚙️ TRANSACTION SETUP</div>', unsafe_allow_html=True)
        entry_mult = st.slider("Entry EV/EBITDA", 4.0, 15.0, 7.5)
        debt_pct = st.slider("Debt Financing (%)", 10, 90, 65) / 100
        
        st.markdown('<div class="gold-header">📈 GROWTH & EXIT</div>', unsafe_allow_html=True)
        growth = st.slider("Annual Revenue Growth (%)", 0, 30, 10) / 100
        margin = st.slider("EBITDA Margin (%)", 10, 60, 40) / 100
        exit_mult = st.slider("Exit EV/EBITDA", 4.0, 15.0, 8.0)
        
        st.write("") # Spacer
        run_btn = st.button("🚀 EXECUTE LBO ANALYSIS")
        
    return ltm_rev, ltm_ebitda, entry_mult, debt_pct, growth, margin, exit_mult, run_btn
