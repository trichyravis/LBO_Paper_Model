
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
                letter-spacing: 1.5px;
                margin-bottom: 5px;
                text-transform: uppercase;
            }
            .footer-tagline {
                color: #6c757d; 
                font-style: italic;
                font-size: 0.95rem;
                margin-bottom: 15px;
            }
            .footer-copyright {
                color: #adb5bd;
                font-size: 0.85rem;
                margin-top: 10px;
            }
            .mountain-emoji {
                font-size: 1.5rem;
                display: block;
                margin-bottom: 10px;
            }
        </style>
        
        <div class="footer-container">
            <span class="mountain-emoji">🏔️</span>
            <div class="footer-brand">The Mountain Path - World of Finance</div>
            <div class="footer-tagline">Advanced Financial Modeling & Institutional Asset Valuation</div>
            <div class="footer-copyright">
                © 2026 Prof. V. Ravichandran. All rights reserved.<br>
                For Educational and Institutional Use Only.
            </div>
        </div>
    ''', unsafe_allow_html=True)
