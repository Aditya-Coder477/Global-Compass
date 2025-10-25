# modules/auth.py
# modules/auth.py
import streamlit as st
import json
import hashlib
import os
from datetime import datetime

class Authentication:
    def __init__(self):
        self.users_file = "data/user_data/users.json"
        self._ensure_users_file()
    
    def _ensure_users_file(self):
        """Create users file if it doesn't exist"""
        os.makedirs(os.path.dirname(self.users_file), exist_ok=True)
        if not os.path.exists(self.users_file):
            with open(self.users_file, 'w') as f:
                json.dump({}, f)
    
    def _hash_password(self, password):
        return hashlib.sha256(password.encode()).hexdigest()
    
    def _load_users(self):
        with open(self.users_file, 'r') as f:
            return json.load(f)
    
    def _save_users(self, users):
        with open(self.users_file, 'w') as f:
            json.dump(users, f, indent=4)
    
    def register(self, username, password, email):
        users = self._load_users()
        
        if username in users:
            return False, "Username already exists"
        
        users[username] = {
            'password': self._hash_password(password),
            'email': email,
            'created_at': datetime.now().isoformat(),
            'preferences': {},
            'search_history': []
        }
        
        self._save_users(users)
        return True, "Registration successful"
    
    def login(self, username, password):
        users = self._load_users()
        
        if username in users and users[username]['password'] == self._hash_password(password):
            st.session_state['authenticated'] = True
            st.session_state['username'] = username
            st.session_state['user_data'] = users[username]
            return True, "Login successful"
        
        return False, "Invalid username or password"
    
    def logout(self):
        for key in ['authenticated', 'username', 'user_data']:
            if key in st.session_state:
                del st.session_state[key]
        st.rerun()
    
    def is_authenticated(self):
        return st.session_state.get('authenticated', False)
    
    def get_current_user(self):
        return st.session_state.get('username', 'Guest')
    
    def get_user_data(self):
        return st.session_state.get('user_data', {})
    
    def update_user_preferences(self, preferences):
        if self.is_authenticated():
            username = self.get_current_user()
            users = self._load_users()
            users[username]['preferences'] = preferences
            self._save_users(users)
            st.session_state['user_data']['preferences'] = preferences
    
    def add_to_search_history(self, search_data):
        if self.is_authenticated():
            username = self.get_current_user()
            users = self._load_users()
            
            search_entry = {
                'timestamp': datetime.now().isoformat(),
                'data': search_data
            }
            
            users[username]['search_history'].insert(0, search_entry)
            # Keep only last 50 searches
            users[username]['search_history'] = users[username]['search_history'][:50]
            
            self._save_users(users)
    
    def show_login_form(self):
        """Display login/signup form"""
        tab1, tab2 = st.tabs(["Login", "Sign Up"])
        
        with tab1:
            with st.form("login_form"):
                username = st.text_input("Username")
                password = st.text_input("Password", type="password")
                submit = st.form_submit_button("Login")
                
                if submit:
                    success, message = self.login(username, password)
                    if success:
                        st.success(message)
                        st.rerun()
                    else:
                        st.error(message)
        
        with tab2:
            with st.form("signup_form"):
                new_username = st.text_input("Choose Username")
                new_email = st.text_input("Email")
                new_password = st.text_input("Choose Password", type="password")
                confirm_password = st.text_input("Confirm Password", type="password")
                submit = st.form_submit_button("Sign Up")
                
                if submit:
                    if new_password != confirm_password:
                        st.error("Passwords do not match")
                    else:
                        success, message = self.register(new_username, new_password, new_email)
                        if success:
                            st.success(message)
                            st.rerun()
                        else:
                            st.error(message)


