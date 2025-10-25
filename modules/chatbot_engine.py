# modules/chatbot_engine.py
import streamlit as st
import json
import re
from datetime import datetime
import random

class ChatbotEngine:
    """AI-powered chatbot assistant for Global Compass"""
    
    def __init__(self):
        self.conversation_history = []
        self.user_context = {}
        self.knowledge_base = self._initialize_knowledge_base()
    
    def _initialize_knowledge_base(self):
        """Initialize the chatbot's knowledge base"""
        return {
            'greetings': {
                'patterns': ['hello', 'hi', 'hey', 'greetings', 'good morning', 'good afternoon'],
                'responses': [
                    "Hello! I'm your Global Compass assistant. How can I help you with studying, traveling, or working abroad today?",
                    "Hi there! Ready to explore international opportunities? What can I assist you with?",
                    "Greetings! I'm here to help you navigate studying, traveling, or working abroad. What's on your mind?"
                ]
            },
            'studying_abroad': {
                'patterns': ['study', 'university', 'education', 'student', 'degree', 'course', 'scholarship'],
                'responses': [
                    "I can help you find the perfect study destination! Tell me about your academic interests and budget.",
                    "Studying abroad is an amazing opportunity! What field are you interested in?",
                    "I have information on universities worldwide. What's your preferred country or program?"
                ],
                'follow_up': "Would you like me to show you university recommendations or scholarship opportunities?"
            },
            'traveling': {
                'patterns': ['travel', 'tourist', 'vacation', 'holiday', 'destination', 'itinerary'],
                'responses': [
                    "I'd love to help plan your trip! What type of travel experience are you looking for?",
                    "Travel planning is exciting! Tell me about your travel preferences and budget.",
                    "I can recommend amazing destinations based on your interests. What do you enjoy doing while traveling?"
                ],
                'follow_up': "Should I show you destination recommendations or help with itinerary planning?"
            },
            'working_abroad': {
                'patterns': ['work', 'job', 'career', 'professional', 'employment', 'relocation'],
                'responses': [
                    "I can help you explore international career opportunities! What's your industry and experience level?",
                    "Working abroad can be life-changing! Tell me about your professional background.",
                    "I have insights on job markets worldwide. What type of work are you looking for?"
                ],
                'follow_up': "Would you like to see job market analysis or visa requirements for specific countries?"
            },
            'visa_questions': {
                'patterns': ['visa', 'immigration', 'permit', 'document', 'requirements', 'application'],
                'responses': [
                    "Visa processes can vary by country and purpose. Which country are you interested in?",
                    "I can provide general visa guidance. What type of visa are you looking for?",
                    "Visa requirements depend on your nationality and destination. Tell me more about your situation."
                ]
            },
            'cost_questions': {
                'patterns': ['cost', 'expensive', 'budget', 'affordable', 'price', 'money'],
                'responses': [
                    "Costs vary significantly by country and city. What's your budget range?",
                    "I can help you compare costs across different destinations. What specific expenses are you concerned about?",
                    "Living costs depend on location and lifestyle. Tell me about your financial considerations."
                ]
            },
            'country_specific': {
                'patterns': ['usa', 'united states', 'uk', 'united kingdom', 'canada', 'australia', 'germany', 'france', 'japan'],
                'responses': [
                    "I have detailed information about {country}. What would you like to know specifically?",
                    "{country} is a popular choice! What aspect are you most interested in?",
                    "Great choice! {country} offers many opportunities. What would you like to explore?"
                ]
            },
            'financial_advice': {
                'patterns': ['financial', 'money', 'savings', 'tax', 'insurance', 'investment'],
                'responses': [
                    "Financial planning is crucial for international moves. What specific financial aspect concerns you?",
                    "I can help with financial planning for your international journey. What are your main questions?",
                    "Let's discuss the financial aspects of your plans. What would you like to know about?"
                ]
            },
            'fallback': {
                'responses': [
                    "I'm not sure I understand. Could you rephrase that?",
                    "I'm still learning! Could you provide more details about what you're looking for?",
                    "I want to make sure I help you properly. Could you tell me more about your question?",
                    "I specialize in studying, traveling, and working abroad. How can I assist you with those topics?"
                ]
            }
        }
    
    def process_message(self, user_message, user_data=None):
        """Process user message and generate response"""
        # Store user message in history
        self.conversation_history.append({
            'role': 'user',
            'message': user_message,
            'timestamp': datetime.now().isoformat()
        })
        
        # Update user context if provided
        if user_data:
            self.user_context.update(user_data)
        
        # Generate response
        bot_response = self._generate_response(user_message)
        
        # Store bot response in history
        self.conversation_history.append({
            'role': 'assistant',
            'message': bot_response,
            'timestamp': datetime.now().isoformat()
        })
        
        return bot_response
    
    def _generate_response(self, user_message):
        """Generate appropriate response based on user message"""
        user_message_lower = user_message.lower()
        
        # Check for specific intents
        intent = self._classify_intent(user_message_lower)
        
        if intent:
            response_template = random.choice(self.knowledge_base[intent]['responses'])
            
            # Handle country-specific responses
            if intent == 'country_specific':
                country = self._extract_country(user_message_lower)
                if country:
                    response = response_template.format(country=country)
                else:
                    response = response_template.format(country="that country")
            else:
                response = response_template
            
            # Add follow-up question if available
            if 'follow_up' in self.knowledge_base[intent]:
                response += " " + self.knowledge_base[intent]['follow_up']
            
            return response
        
        # Fallback response
        return random.choice(self.knowledge_base['fallback']['responses'])
    
    def _classify_intent(self, message):
        """Classify user intent based on message patterns"""
        for intent, data in self.knowledge_base.items():
            if intent in ['greetings', 'fallback']:
                continue
            
            for pattern in data['patterns']:
                if re.search(r'\b' + re.escape(pattern) + r'\b', message):
                    return intent
        
        # Check for greetings separately
        for pattern in self.knowledge_base['greetings']['patterns']:
            if re.search(r'\b' + re.escape(pattern) + r'\b', message):
                return 'greetings'
        
        return None
    
    def _extract_country(self, message):
        """Extract country name from message"""
        country_keywords = {
            'usa': 'United States', 'united states': 'United States', 'us': 'United States',
            'uk': 'United Kingdom', 'united kingdom': 'United Kingdom', 'britain': 'United Kingdom',
            'canada': 'Canada', 'australia': 'Australia', 'germany': 'Germany',
            'france': 'France', 'japan': 'Japan', 'italy': 'Italy', 'spain': 'Spain',
            'netherlands': 'Netherlands', 'sweden': 'Sweden', 'switzerland': 'Switzerland',
            'singapore': 'Singapore'
        }
        
        for keyword, country in country_keywords.items():
            if keyword in message:
                return country
        
        return None
    
    def get_conversation_history(self):
        """Get the conversation history"""
        return self.conversation_history
    
    def clear_conversation_history(self):
        """Clear the conversation history"""
        self.conversation_history = []
    
    def suggest_quick_actions(self, user_message):
        """Suggest quick actions based on user message"""
        message_lower = user_message.lower()
        
        suggestions = []
        
        if any(word in message_lower for word in ['study', 'university', 'education']):
            suggestions.extend([
                {"label": "🎓 Find Universities", "action": "navigate_student"},
                {"label": "💰 Scholarship Info", "action": "show_scholarships"},
                {"label": "🌍 Compare Countries", "action": "compare_education"}
            ])
        
        if any(word in message_lower for word in ['travel', 'vacation', 'destination']):
            suggestions.extend([
                {"label": "✈️ Find Destinations", "action": "navigate_tourist"},
                {"label": "🗺️ Travel Itinerary", "action": "show_itinerary"},
                {"label": "💰 Budget Planning", "action": "show_travel_budget"}
            ])
        
        if any(word in message_lower for word in ['work', 'job', 'career']):
            suggestions.extend([
                {"label": "💼 Job Market Analysis", "action": "navigate_professional"},
                {"label": "🧾 Visa Requirements", "action": "show_visa_info"},
                {"label": "💰 Salary Comparison", "action": "compare_salaries"}
            ])
        
        if any(word in message_lower for word in ['cost', 'budget', 'money']):
            suggestions.extend([
                {"label": "💰 Cost Calculator", "action": "navigate_financial"},
                {"label": "💱 Currency Converter", "action": "show_currency"},
                {"label": "🏠 Cost of Living", "action": "show_col"}
            ])
        
        # Add general suggestions if none matched
        if not suggestions:
            suggestions = [
                {"label": "🎓 Study Abroad", "action": "navigate_student"},
                {"label": "✈️ Travel Planning", "action": "navigate_tourist"},
                {"label": "💼 Work Abroad", "action": "navigate_professional"},
                {"label": "💰 Financial Tools", "action": "navigate_financial"}
            ]
        
        return suggestions[:4]  # Return max 4 suggestions

# Global instance
chatbot = ChatbotEngine()