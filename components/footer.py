
import streamlit as st

def footer_component():
    """
    Renders a professional institutional footer with personal branding,
    social links, and copyright info.
    """
    st.markdown("---")
    st.markdown('''
        <style>
            .footer-container {
                text-align: center; 
                padding: 30px 20px;
                margin-top: 2rem;
            }
            .footer-brand {
                color: #002147; 
                font-weight: bold;
                letter-spacing: 1.5px;
                margin-bottom: 5px;
                text-transform: uppercase;
                font-size: 1.1rem;
            }
            .footer-tagline {
                color: #6c757d; 
                font-style: italic;
                font-size: 0.9rem;
                margin-bottom: 20px;
            }
            .social-links {
                margin-bottom: 20px;
            }
            .social-links a {
                text-decoration: none;
                color: #004b8d;
                font-weight: bold;
                margin: 0 15px;
                transition: 0.3s;
                font-size: 0.9rem;
            }
            .social-links a:hover {
                color: #FFD700;
            }
            .footer-copyright {
                color: #adb5bd;
                font-size: 0.8rem;
                margin-top: 10px;
                line-height: 1.5;
            }
        </style>
        
        <div class="footer-container">
            <div class="footer-brand">🏔️ The Mountain Path - World of Finance</div>
            <div class="footer-tagline">Institutional LBO Modeling & Asset Valuation Suite</div>
            
            <div class="social-links">
                <a href="https://www.linkedin.com/in/trichyravis" target="_blank">🔗 LinkedIn Profile</a>
                <a href="https://github.com/trichyravis" target="_blank">💻 GitHub Repository</a>
            </div>
            
            <div class="footer-copyright">
                © 2026 <b>Prof. V. Ravichandran</b>. All rights reserved.<br>
                Empowering the next generation of Finance Professionals.
            </div>
        </div>
    ''', unsafe_allow_html=True)
