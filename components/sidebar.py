
import streamlit as st

def sidebar_component():
    # Injecting CSS for background and button
    st.markdown('''
        <style>
        /* Sidebar background */
        [data-testid="stSidebar"] {
            background-color: #002147 !important;
        }
        
        /* Make all standard text and labels white */
        [data-testid="stSidebar"] .stMarkdown p, 
        [data-testid="stSidebar"] label {
            color: white !important; 
            font-weight: bold !important;
        }

        /* Gold Header Style (similar to button) */
        .sidebar-header {
            background-color: #FFD700;
            color: #002147;
            padding: 10px;
            border-radius: 5px;
            font-weight: bold;
            text-align: center;
            margin-top: 20px;
            margin-bottom: 15px;
            font-family: sans-serif;
            text-transform: uppercase;
            font-size: 1rem;
        }
        
        /* The Execute Button Styling */
        div.stButton > button:first-child {
            background-color: #FFD700 !important; 
            color: #002147 !important; 
            font-weight: bold !important; 
            width: 100%; 
            border-radius: 8px; 
            border: none;
            padding: 10px;
        }
        </style>
    ''', unsafe_allow_html=True)
    
    with st.sidebar:
        # We use st.markdown with our custom class instead of st.header
        st.markdown('<div class="sidebar-header">🏢 Target Financials</div>', unsafe_allow_html=True)
        ltm_rev = st.number_input("LTM Revenue ($)", value=3000000, step=100000)
        ltm_ebitda = st.number_input("LTM EBITDA ($)", value=1500000, step=50000)
        
        st.markdown('<div class="sidebar-header">⚙️ Transaction Setup</div>', unsafe_allow_html=True)
        entry_mult = st.slider("Entry EV/EBITDA", 4.0, 15.0, 7.5)
        debt_pct = st.slider("Debt Financing (%)", 10, 90, 65) / 100
        
        st.markdown('<div class="sidebar-header">📈 Growth & Exit</div>', unsafe_allow_html=True)
        growth = st.slider("Annual Revenue Growth (%)", 0, 30, 10) / 100
        margin = st.slider("EBITDA Margin (%)", 10, 60, 40) / 100
        exit_mult = st.slider("Exit EV/EBITDA", 4.0, 15.0, 8.0)
        
        st.write("") # Spacer
        run_btn = st.button("🚀 EXECUTE LBO ANALYSIS")
        
    return ltm_rev, ltm_ebitda, entry_mult, debt_pct, growth, margin, exit_mult, run_btn
