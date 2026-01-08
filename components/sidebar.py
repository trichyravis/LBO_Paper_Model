
import streamlit as st

def sidebar_component():
    st.markdown('''
        <style>
        [data-testid="stSidebar"] {background-color: #002147 !important;}
        [data-testid="stSidebar"] * {color: white !important;}
        </style>
    ''', unsafe_allow_html=True)
    
    with st.sidebar:
        st.image("https://via.placeholder.com/150x50?text=THE+MOUNTAIN+PATH", use_container_width=True) # Replace with your logo URL
        st.markdown("### 🏔️ Navigation")
        st.info("Use the tabs on the right to navigate between Data Input and Financial Analysis.")
        st.write("---")
        st.write("**Instructor:** Prof. V. Ravichandran")
