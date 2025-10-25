# pages/8_🤖_AI_Assistant.py - Simplified version
import streamlit as st
import sys
import os
import json
from datetime import datetime
from streamlit_extras.switch_page_button import switch_page

# Add modules to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from modules.advanced_chatbot import advanced_chatbot
from modules.auth import Authentication

# Page configuration
st.set_page_config(
    page_title="AI Assistant - Global Compass",
    page_icon="🤖",
    layout="centered"  # Changed to centered for better chat experience
)

# Initialize components
auth = Authentication()

def main():
    # Check authentication
    if not auth.is_authenticated():
        st.warning("Please log in to access the AI Assistant")
        st.stop()
    
    st.title("🤖 Global Compass AI Assistant")
    st.markdown("Your intelligent guide for studying, traveling, and working abroad")
    
    # Initialize chat history
    if "chat_messages" not in st.session_state:
        st.session_state.chat_messages = [
            {
                "role": "assistant",
                "content": "Hello! I'm your Global Compass assistant. I can help you with studying abroad, travel planning, career opportunities, and financial planning. What would you like to know today?",
                "timestamp": datetime.now().isoformat()
            }
        ]
    
    # Display chat messages
    for message in st.session_state.chat_messages:
        with st.chat_message(message["role"]):
            st.write(message["content"])
            
            # Show quick actions for assistant messages
            if message["role"] == "assistant" and "quick_actions" in message:
                st.markdown("**Quick actions:**")
                for action in message["quick_actions"]:
                    if st.button(action["label"], key=f"{action['action']}_{message['timestamp']}"):
                        handle_main_chat_action(action["action"])
    
    # Chat input - This must be at the bottom, outside any containers
    user_input = st.chat_input("Ask me about studying, traveling, or working abroad...")
    
    if user_input:
        # Add user message to chat history
        st.session_state.chat_messages.append({
            "role": "user",
            "content": user_input,
            "timestamp": datetime.now().isoformat()
        })
        
        # Get bot response
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                user_data = auth.get_user_data()
                response = advanced_chatbot.process_enhanced_message(user_input, user_data)
                
                # Get quick actions
                quick_actions = advanced_chatbot.suggest_quick_actions(user_input)
                
                st.write(response)
                
                # Show quick actions
                if quick_actions:
                    st.markdown("**Quick actions:**")
                    for action in quick_actions:
                        if st.button(action["label"], key=f"{action['action']}_{datetime.now().timestamp()}"):
                            handle_main_chat_action(action["action"])
        
        # Add assistant response to chat history
        st.session_state.chat_messages.append({
            "role": "assistant",
            "content": response,
            "quick_actions": quick_actions,
            "timestamp": datetime.now().isoformat()
        })
        
        # Rerun to update the display
        st.rerun()
    
    # Simple controls at the bottom
    st.markdown("---")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🔄 Clear Conversation", use_container_width=True):
            st.session_state.chat_messages = [
                {
                    "role": "assistant", 
                    "content": "Conversation cleared! How can I help you today?",
                    "timestamp": datetime.now().isoformat()
                }
            ]
            st.rerun()
    
    with col2:
        if st.button("💾 Export Conversation", use_container_width=True):
            export_conversation()

def handle_main_chat_action(action):
    """Handle actions from the main chat interface"""
    if action == "navigate_student":
        switch_page("Student Dashboard")
    elif action == "navigate_tourist":
        switch_page("Tourist Dashboard")
    elif action == "navigate_professional":
        switch_page("Professional Dashboard")
    elif action == "navigate_financial":
        switch_page("Financial Tools")
    elif action == "navigate_maps":
        switch_page("world map visualization")
        
def export_conversation():
    """Export conversation history"""
    if "chat_messages" in st.session_state:
        conversation_data = {
            "exported_at": datetime.now().isoformat(),
            "conversation": st.session_state.chat_messages
        }
        
        st.download_button(
            label="📥 Download Conversation JSON",
            data=json.dumps(conversation_data, indent=2),
            file_name=f"global_compass_conversation_{datetime.now().strftime('%Y%m%d_%H%M')}.json",
            mime="application/json"
        )

if __name__ == "__main__":
    main()