
import streamlit as st

def sidebar_component():
    # Force sidebar header text colors to white using high-specificity selectors
    st.markdown('''
        <style>
        /* 1. Sidebar background color */
        [data-testid="stSidebar"] {
            background-color: #002147 !important;
        }
        
        /* 2. Target the headers (Target Financials, Transaction Setup, etc.) */
        /* This covers the h2 tags specifically created by st.header */
        [data-testid="stSidebar"] h1, 
        [data-testid="stSidebar"] h2, 
        [data-testid="stSidebar"] h3 {
            color: white !important;
        }

        /* 3. Target the specialized Streamlit header containers */
        [data-testid="stSidebar"] [data-testid="stHeader"] h2 {
            color: white !important;
        }

        /* 4. Target the text inside labels and standard markdown */
        [data-testid="stSidebar"] .stMarkdown p, 
        [data-testid="stSidebar"] label {
            color: white !important;
            font-weight: bold;
        }
        
        /* 5. Gold Button Styling */
        div.stButton > button:first-child {
            background-color: #FFD700 !important; 
            color: #002147 !important; 
            font-weight: bold !important; 
            width: 100%; 
            border-radius: 8px; 
            border: none;
        }
        </style>
    ''', unsafe_allow_html=True)
    
    with st.sidebar:
        st.header("🏢 Target Financials")
        # ... rest of your code
