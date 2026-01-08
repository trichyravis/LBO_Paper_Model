
import streamlit as st

def sidebar_component():
    # CSS to force sidebar text colors to white/gold
    st.markdown('''
        <style>
        /* Sidebar background color */
        [data-testid="stSidebar"] {
            background-color: #002147 !important;
        }
        
        /* Change all sidebar text and headers to white */
        [data-testid="stSidebar"] .stMarkdown p, 
        [data-testid="stSidebar"] label, 
        [data-testid="stSidebar"] h1, 
        [data-testid="stSidebar"] h2, 
        [data-testid="stSidebar"] h3 {
            color: white !important; 
            font-weight: bold;
        }
        
        /* Custom Button Styling */
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
        # ... rest of your inputs ...
