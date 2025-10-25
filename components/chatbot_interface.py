# components/chatbot_interface.py
import streamlit as st
import json
from datetime import datetime

def initialize_chatbot_session():
    """Initialize chatbot session state"""
    if 'chatbot_initialized' not in st.session_state:
        st.session_state.chatbot_initialized = True
        st.session_state.chatbot_messages = []
        st.session_state.show_chatbot = False
        st.session_state.chatbot_minimized = False

def render_chatbot_interface():
    """Render the chatbot interface"""
    initialize_chatbot_session()
    
    # Chatbot toggle button (always visible)
    col1, col2, col3 = st.columns([3, 1, 1])
    
    with col3:
        if st.session_state.show_chatbot:
            if st.button("🗨️ Close Chat", use_container_width=True):
                st.session_state.show_chatbot = False
                st.rerun()
        else:
            if st.button("💬 Ask Assistant", use_container_width=True, type="secondary"):
                st.session_state.show_chatbot = True
                st.rerun()
    
    # Chatbot interface
    if st.session_state.show_chatbot:
        st.markdown("---")
        
        # Chat header
        header_col1, header_col2 = st.columns([3, 1])
        with header_col1:
            st.subheader("🤖 Global Compass Assistant")
        with header_col2:
            if st.button("Minimize", use_container_width=True):
                st.session_state.chatbot_minimized = not st.session_state.chatbot_minimized
                st.rerun()
        
        if not st.session_state.chatbot_minimized:
            # Chat container
            chat_container = st.container(height=400, border=True)
            
            with chat_container:
                # Display chat messages
                for message in st.session_state.chatbot_messages:
                    if message["role"] == "user":
                        st.chat_message("user").write(message["content"])
                    else:
                        st.chat_message("assistant").write(message["content"])
                        
                        # Show quick actions if available
                        if "quick_actions" in message:
                            cols = st.columns(len(message["quick_actions"]))
                            for idx, action in enumerate(message["quick_actions"]):
                                with cols[idx]:
                                    if st.button(action["label"], use_container_width=True, key=f"action_{idx}_{message['timestamp']}"):
                                        handle_quick_action(action["action"])
            
            # Chat input
            user_input = st.chat_input("Ask me about studying, traveling, or working abroad...")
            
            if user_input:
                # Add user message to chat
                st.session_state.chatbot_messages.append({
                    "role": "user", 
                    "content": user_input,
                    "timestamp": datetime.now().isoformat()
                })
                
                # Get bot response
                from modules.advanced_chatbot import advanced_chatbot
                from modules.auth import Authentication
                
                auth = Authentication()
                user_data = auth.get_user_data() if auth.is_authenticated() else {}
                
                bot_response = advanced_chatbot.process_enhanced_message(user_input, user_data)
                
                # Get quick actions suggestions
                quick_actions = advanced_chatbot.suggest_quick_actions(user_input)
                
                # Add bot response to chat
                st.session_state.chatbot_messages.append({
                    "role": "assistant",
                    "content": bot_response,
                    "quick_actions": quick_actions,
                    "timestamp": datetime.now().isoformat()
                })
                
                st.rerun()

def handle_quick_action(action):
    """Handle quick action button clicks"""
    if action == "navigate_student":
        st.switch_page("pages/2_🎓_Student_Dashboard.py")
    elif action == "navigate_tourist":
        st.switch_page("pages/3_✈️_Tourist_Dashboard.py")
    elif action == "navigate_professional":
        st.switch_page("pages/4_💼_Professional_Dashboard.py")
    elif action == "navigate_financial":
        st.switch_page("pages/6_💰_Financial_Tools.py")
    elif action == "show_scholarships":
        st.info("💡 Check the Student Dashboard for scholarship opportunities and financial aid information!")
    elif action == "show_visa_info":
        st.info("🌍 Visa requirements vary by country. Check the respective dashboards for detailed visa guidance!")
    elif action == "compare_salaries":
        st.info("💰 Use the Professional Dashboard to compare salaries across different countries and industries!")
    elif action == "show_currency":
        st.info("💱 Real-time currency conversion is available in the Financial Tools section!")

def render_floating_chatbot():
    """Render a floating chatbot button (for mobile-friendly view)"""
    initialize_chatbot_session()
    
    # Floating chat button (CSS-based)
    st.markdown("""
    <style>
    .floating-chatbot {
        position: fixed;
        bottom: 20px;
        right: 20px;
        z-index: 1000;
    }
    .chatbot-button {
        background-color: #1f3a60;
        color: white;
        border: none;
        border-radius: 50%;
        width: 60px;
        height: 60px;
        font-size: 24px;
        cursor: pointer;
        box-shadow: 0 4px 8px rgba(0,0,0,0.2);
        transition: all 0.3s ease;
    }
    .chatbot-button:hover {
        background-color: #2c4d80;
        transform: scale(1.1);
    }
    </style>
    
    <div class="floating-chatbot">
        <button class="chatbot-button" onclick="document.getElementById('chatbot-toggle').click()">💬</button>
    </div>
    """, unsafe_allow_html=True)
    
    # Hidden button to trigger chatbot
    if st.button("Toggle Chat", key="chatbot-toggle", type="primary", use_container_width=True):
        st.session_state.show_chatbot = not st.session_state.show_chatbot
        st.rerun()