
import streamlit as st

def footer_component():
    st.markdown("---")
    
    # Define the HTML in a clean variable
    footer_html = """
    <div style="text-align: center; padding: 30px 20px; margin-top: 2rem;">
        <div style="color: #002147; font-weight: bold; letter-spacing: 1.5px; text-transform: uppercase; font-size: 1.1rem;">
            🏔️ The Mountain Path - World of Finance
        </div>
        
        <div style="margin: 20px 0;">
            <a href="https://www.linkedin.com/in/trichyravis" target="_blank" style="text-decoration: none; color: #004b8d; font-weight: bold; margin: 0 15px;">🔗 LinkedIn Profile</a>
            <a href="https://github.com/trichyravis" target="_blank" style="text-decoration: none; color: #004b8d; font-weight: bold; margin: 0 15px;">💻 GitHub Repository</a>
        </div>
        
        <div style="color: #adb5bd; font-size: 0.8rem;">
            © 2026 <b>Prof. V. Ravichandran</b>. All rights reserved.<br>
            Empowering the next generation of Finance Professionals.
        </div>
    </div>
    """
    
    # This line MUST have unsafe_allow_html=True
    st.markdown(footer_html, unsafe_allow_html=True)
