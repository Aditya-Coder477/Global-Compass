# app.py - Main entry point
import streamlit as st
from modules.auth import Authentication
import base64
from components.chatbot_interface import render_chatbot_interface, render_floating_chatbot

# Page configuration
st.set_page_config(
    page_title="Global Compass",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
def load_css():
    with open("assets/css/custom.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

def main():
    load_css()
    
    # Initialize authentication
    auth = Authentication()
    
    # Check if user is logged in
    if not auth.is_authenticated():
        # Show landing page with login option
        show_landing_page(auth)
    else:
        # Show main dashboard
        show_main_dashboard(auth)
        
    # Render chatbot interface (appears on all pages when logged in)
        render_chatbot_interface()

def show_landing_page(auth):
    """Show the main landing page when user is not logged in"""
    st.markdown('<h1 class="main-header">Global Compass</h1>', unsafe_allow_html=True)
    st.markdown('<p style="text-align: center; font-size: 1.2rem; color: #555;">Your intelligent guide for studying, traveling, and working abroad</p>', unsafe_allow_html=True)
    
    
    # Login/Signup section
    st.markdown("---")
    auth.show_login_form()

def show_main_dashboard(auth):
    """Show the main dashboard after login"""
    st.sidebar.success(f"Welcome, {auth.get_current_user()}!")
    
    if st.sidebar.button("Logout"):
        auth.logout()
        st.rerun()
    
    st.markdown(f'<h1 class="main-header">Welcome to Global Compass, {auth.get_current_user()}!</h1>', unsafe_allow_html=True)
    
    # Quick access cards - ADD CHATBOT CARD
    col1, col2, col3, col4, col5, col6 = st.columns(6)
    
    with col1:
        if st.button("🎓 Student Dashboard", use_container_width=True):
            st.switch_page("Student Dashboard")
    
    with col2:
        if st.button("✈️ Tourist Dashboard", use_container_width=True):
            st.switch_page("Tourist Dashboard")
    
    with col3:
        if st.button("💼 Professional Dashboard", use_container_width=True):
            st.switch_page("Professional Dashboard")
            
    with col4:
        if st.button("💰 Financial Tools", use_container_width=True):
            st.switch_page("Financial Tools")
    with col5:
        if st.button("🗺️ World Maps", use_container_width=True):
            st.switch_page("world map visualization")
    with col6:
        if st.button("🤖 AI Assistant", use_container_width=True):
            st.switch_page("AI Assistant")        
            
            
if __name__ == "__main__":
    main()
