
import streamlit as st

def header_component(title, subtitle):
    """
    Renders a professional institutional header with a gradient background
    and gold accent border.
    """
    st.markdown(f'''
        <style>
            .main-header {{
                background: linear-gradient(135deg, #002147 0%, #004b8d 100%); 
                padding: 2.5rem; 
                border-radius: 15px; 
                color: white; 
                text-align: center; 
                margin-bottom: 2rem; 
                border-bottom: 5px solid #FFD700;
                box-shadow: 0 4px 15px rgba(0,0,0,0.3);
            }}
            .main-header h1 {{
                color: white !important; 
                margin: 0;
                font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
                font-weight: 700;
            }}
            .main-header h2 {{
                font-size: 1.3rem; 
                opacity: 0.9; 
                color: #e0e0e0 !important; 
                margin: 5px 0 0 0;
                font-weight: 400;
            }}
            .branding {{
                font-weight: bold; 
                color: #FFD700; 
                margin-top: 15px;
                letter-spacing: 1px;
                text-transform: uppercase;
                font-size: 0.9rem;
            }}
        </style>
        
        <div class="main-header">
            <h1>{title}</h1>
            <h2>{subtitle}</h2>
            <p class="branding">🏔️ Prof. V. Ravichandran | The Mountain Path</p>
        </div>
    ''', unsafe_allow_html=True)
