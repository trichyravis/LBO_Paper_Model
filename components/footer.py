
import streamlit as st

def footer_component():
    """
    Renders the custom HTML footer. 
    The 'unsafe_allow_html=True' parameter is what prevents the raw code from showing.
    """
    st.markdown("---")
    
    # We wrap the entire HTML block in one st.markdown call
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
                text-transform: uppercase;
                font-size: 1.1rem;
            }
            .social-links {
                margin: 20px 0;
            }
            .social-links a {
                text-decoration: none;
                color: #004b8d;
                font-weight: bold;
                margin: 0 15px;
            }
            .footer-copyright {
                color: #adb5bd;
                font-size: 0.8rem;
            }
        </style>
        
        <div class="footer-container">
            <div class="footer-brand">🏔️ The Mountain Path - World of Finance</div>
            
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
