import streamlit as st

def footer_component():
    """
    Renders a professional institutional footer with 
    The Mountain Path branding.
    """
    st.markdown("---")
    st.markdown('''
        <style>
            .footer-container {
                text-align: center; 
                padding: 40px 20px;
                margin-top: 2rem;
            }
            .footer-brand {
                color: #002147; 
                font-weight: bold;
                letter-spacing: 1px;
                margin-bottom: 5px;
            }
            .footer-tagline {
                color: #6c757d; 
                font-style: italic;
                font-size: 0.9rem;
                margin-bottom: 15px;
            }
            .footer-copyright {
                color: #adb5bd;
                font-size: 0.8rem;
            }
        </style>
        
        <div class="footer-container">
            <h4 class="footer-brand">🏔️ THE MOUNTAIN PATH - WORLD OF FINANCE</h4>
            <p class="footer-tagline">Bridging Academic Theory with Institutional Practice</p>
            <p class="footer-copyright">© 2025 Prof. V. Ravichandran. All rights reserved.</p>
        </div>
    ''', unsafe_allow_html=True)
