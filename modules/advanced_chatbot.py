# modules/advanced_chatbot.py
import streamlit as st
import pandas as pd
from modules.chatbot_engine import ChatbotEngine
from modules.api_services import api_services
from modules.financial_tools import financial_tools

class AdvancedChatbot(ChatbotEngine):
    """Enhanced chatbot with data integration and advanced capabilities"""
    
    def __init__(self):
        super().__init__()
        self.enhanced_knowledge = self._enhance_knowledge_base()
    
    def _enhance_knowledge_base(self):
        """Add enhanced knowledge capabilities"""
        return {
            'university_recommendations': {
                'patterns': ['top universities', 'best schools', 'university ranking', 'good colleges'],
                'action': 'provide_university_recommendations'
            },
            'cost_comparison': {
                'patterns': ['compare costs', 'living expenses', 'cost difference', 'affordable cities'],
                'action': 'provide_cost_comparison'
            },
            'visa_guidance': {
                'patterns': ['visa process', 'how to apply', 'document requirements', 'visa timeline'],
                'action': 'provide_visa_guidance'
            },
            'job_insights': {
                'patterns': ['job market', 'employment rate', 'career opportunities', 'industry growth'],  # FIXED: Added missing quote
                'action': 'provide_job_insights'
            },
            'travel_recommendations': {
                'patterns': ['where to travel', 'best destinations', 'places to visit', 'travel spots'],
                'action': 'provide_travel_recommendations'
            }
        }
    
    def process_enhanced_message(self, user_message, user_data=None):
        """Process message with enhanced capabilities"""
        user_message_lower = user_message.lower()
        
        # Check for enhanced actions
        for intent, data in self.enhanced_knowledge.items():
            for pattern in data['patterns']:
                if pattern in user_message_lower:
                    action_method = getattr(self, data['action'], None)
                    if action_method:
                        return action_method(user_message, user_data)
        
        # Fall back to basic processing
        return self.process_message(user_message, user_data)
    
    def provide_university_recommendations(self, user_message, user_data):
        """Provide university recommendations based on query"""
        country = self._extract_country(user_message.lower())
        
        if country:
            universities = api_services.get_universities_by_country(country)
            if universities:
                response = f"Here are some top universities in {country}:\n\n"
                for i, uni in enumerate(universities[:5], 1):
                    response += f"{i}. **{uni['name']}**\n"
                    response += f"   Programs: {', '.join(uni['popular_programs'][:3])}\n"
                    response += f"   Estimated Cost: ${uni['estimated_cost']:,}/year\n"
                    response += f"   Ranking: {uni['ranking']}\n\n"
                
                response += "Would you like more detailed information about any of these universities?"
            else:
                response = f"I don't have specific university data for {country} at the moment. You might want to check the Student Dashboard for comprehensive university matching."
        else:
            response = "I can help you find universities! Which country are you interested in studying in?"
        
        return response
    
    def provide_cost_comparison(self, user_message, user_data):
        """Provide cost of living comparison"""
        cities = list(financial_tools.cost_of_living_data.keys())
        
        if 'vs' in user_message.lower() or 'compare' in user_message.lower():
            # Extract cities from message
            found_cities = []
            for city in cities:
                if city.lower() in user_message.lower():
                    found_cities.append(city)
            
            if len(found_cities) >= 2:
                comparison = financial_tools.compare_cost_of_living(
                    found_cities[0], found_cities[1], 50000
                )
                
                if comparison:
                    response = f"**Cost of Living Comparison: {found_cities[0]} vs {found_cities[1]}**\n\n"
                    response += f"• Monthly cost in {found_cities[0]}: ${comparison['current_monthly_col']:,}\n"
                    response += f"• Monthly cost in {found_cities[1]}: ${comparison['target_monthly_col']:,}\n"
                    response += f"• Cost ratio: {comparison['col_ratio']:.1f}x\n\n"
                    response += f"To maintain the same lifestyle, you'd need ${comparison['equivalent_salary']:,} in {found_cities[1]}"
                    return response
        
        # General cost information
        response = "**Cost of Living Overview:**\n\n"
        for city in cities[:4]:
            cost = financial_tools.cost_of_living_data[city]['total']
            response += f"• {city}: ${cost:,}/month\n"
        
        response += "\nYou can use the Financial Tools for detailed comparisons and personalized calculations."
        return response
    
    def provide_visa_guidance(self, user_message, user_data):
        """Provide visa guidance"""
        country = self._extract_country(user_message.lower())
        
        visa_info = {
            'United States': {
                'student': 'F-1 visa (requires I-20 form, proof of funds, interview)',
                'work': 'H-1B visa (employer sponsorship, lottery system)',
                'tourist': 'ESTA or B-2 visa (90 days visa-free for many countries)'
            },
            'United Kingdom': {
                'student': 'Tier 4 visa (CAS from university, financial requirements)',
                'work': 'Skilled Worker visa (sponsorship, points-based system)',
                'tourist': 'Standard Visitor visa (6 months for tourism)'
            },
            'Canada': {
                'student': 'Study Permit (acceptance letter, proof of funds)',
                'work': 'Work Permit (LMIA often required)',
                'tourist': 'Visitor Visa (eTA for visa-exempt countries)'
            },
            'Australia': {
                'student': 'Student Visa (500 subclass, genuine temporary entrant)',
                'work': 'Temporary Skill Shortage visa (482 subclass)',
                'tourist': 'Visitor Visa (600 subclass, eVisitor for some)'
            }
        }
        
        if country and country in visa_info:
            response = f"**Visa Information for {country}:**\n\n"
            for visa_type, info in visa_info[country].items():
                response += f"• **{visa_type.title()} Visa**: {info}\n"
            
            response += "\n*Note: Always check official government sources for the most current requirements.*"
        else:
            response = "I can provide general visa guidance. Which country are you interested in? Popular options include USA, UK, Canada, and Australia."
        
        return response
    
    def provide_job_insights(self, user_message, user_data):
        """Provide job market insights"""
        country = self._extract_country(user_message.lower())
        
        if country:
            # Get job market data for common industries
            industries = ['Technology', 'Finance', 'Healthcare', 'Engineering']
            response = f"**Job Market Overview for {country}:**\n\n"
            
            for industry in industries[:2]:
                market_data = api_services.get_job_market_data(country, industry)
                if market_data['success']:
                    data = market_data['data']
                    response += f"• **{industry}**: {data['demand']} demand, avg salary ${data['avg_salary']:,}\n"
            
            response += "\nFor detailed salary comparisons and job market analysis, check the Professional Dashboard."
        else:
            response = "I can provide job market insights for different countries. Which country's job market are you interested in?"
        
        return response
    
    def provide_travel_recommendations(self, user_message, user_data):
        """Provide travel recommendations"""
        # Extract travel preferences from message
        message_lower = user_message.lower()
        
        budget_level = 'medium'
        if any(word in message_lower for word in ['cheap', 'budget', 'affordable', 'low cost']):
            budget_level = 'low'
        elif any(word in message_lower for word in ['luxury', 'premium', 'expensive', 'high end']):
            budget_level = 'high'
        
        interests = []
        if any(word in message_lower for word in ['beach', 'coast', 'island', 'ocean']):
            interests.append('beach')
        if any(word in message_lower for word in ['mountain', 'hiking', 'adventure', 'outdoor']):
            interests.append('adventure')
        if any(word in message_lower for word in ['culture', 'historical', 'museum', 'heritage']):
            interests.append('cultural')
        if any(word in message_lower for word in ['city', 'urban', 'metropolitan', 'nightlife']):
            interests.append('city')
        
        # Generate recommendations based on preferences
        recommendations = {
            'low': {
                'beach': ['Thailand', 'Vietnam', 'Portugal'],
                'adventure': ['Nepal', 'Peru', 'Romania'],
                'cultural': ['Mexico', 'Turkey', 'India'],
                'city': ['Budapest', 'Prague', 'Kuala Lumpur']
            },
            'medium': {
                'beach': ['Greece', 'Spain', 'Croatia'],
                'adventure': ['New Zealand', 'Costa Rica', 'Chile'],
                'cultural': ['Italy', 'Japan', 'Morocco'],
                'city': ['Berlin', 'Tokyo', 'Barcelona']
            },
            'high': {
                'beach': ['Maldives', 'Seychelles', 'French Polynesia'],
                'adventure': ['Switzerland', 'Norway', 'Iceland'],
                'cultural': ['France', 'UK', 'USA'],
                'city': ['New York', 'London', 'Singapore']
            }
        }
        
        response = "**Travel Recommendations:**\n\n"
        
        if interests:
            primary_interest = interests[0]
            if primary_interest in recommendations[budget_level]:
                recs = recommendations[budget_level][primary_interest]
                response += f"Based on your interest in {primary_interest} travel with a {budget_level} budget:\n"
                for rec in recs:
                    response += f"• {rec}\n"
        else:
            # General recommendations
            response += f"Popular {budget_level}-budget destinations:\n"
            for rec in list(recommendations[budget_level].values())[0][:3]:
                response += f"• {rec}\n"
        
        response += "\nYou can explore these destinations further in the Tourist Dashboard!"
        
        return response

# Global instance
advanced_chatbot = AdvancedChatbot()