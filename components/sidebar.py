
import streamlit as st

def sidebar_component():
    # Force sidebar header text colors to white
    st.markdown('''
        <style>
        /* 1. Sidebar background color */
        [data-testid="stSidebar"] {
            background-color: #002147 !important;
        }
        
        /* 2. Target specific Streamlit Header/Subheader tags in Sidebar */
        [data-testid="stSidebar"] h1, 
        [data-testid="stSidebar"] h2, 
        [data-testid="stSidebar"] h3,
        [data-testid="stSidebar"] .st-emotion-cache-10trblm, /* Common header class */
        [data-testid="stWidgetLabel"] p {
            color: white !important; 
        }

        /* 3. This is the specific fix for "Target Financials" (h2) */
        [data-testid="stSidebar"] [data-testid="stHeader"] {
            color: white !important;
        }
        
        /* 4. Ensure markdown text and labels are also white */
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
        # ... the rest of your inputs ...
