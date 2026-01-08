
import streamlit as st

def header_component(title, subtitle):
    header_html = f"""
    <style>
        .main-header {{
            background: linear-gradient(135deg, #002147 0%, #004b8d 100%); 
            padding: 2rem; 
            border-radius: 15px; 
            color: white; 
            text-align: center; 
            margin-bottom: 2rem; 
            border-bottom: 5px solid #FFD700;
        }}
    </style>
    <div class="main-header">
        <h1 style="color:white; margin:0;">{title}</h1>
        <h2 style="font-size: 1.3rem; opacity: 0.9; color: white; margin:0;">{subtitle}</h2>
        <p style="font-weight: bold; color: #FFD700; margin-top:10px;">
            Prof. V. Ravichandran | The Mountain Path
        </p>
    </div>
    """
    st.markdown(header_html, unsafe_allow_html=True)
