# pages/4_💼_Professional_Dashboard.py
import streamlit as st
import sys
import os
# Add these imports to each dashboard file
import pandas as pd
from datetime import datetime, timedelta
import random
from modules.api_services import api_services

# Add modules to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from modules.professional_engine import ProfessionalEngine
from modules.visualization import Visualization
from modules.auth import Authentication
from modules.world_map import world_map  # ADD THIS LINE

# Page configuration
st.set_page_config(
    page_title="Professional Dashboard - Global Compass",
    page_icon="💼",
    layout="wide"
)

# Initialize components
auth = Authentication()
professional_engine = ProfessionalEngine()
viz = Visualization()

def main():
    # Check authentication
    if not auth.is_authenticated():
        st.warning("Please log in to access the Professional Dashboard")
        st.stop()
    
    st.title("💼 Professional Dashboard")
    st.markdown("Find ideal countries for career opportunities and international relocation")
    
    # Sidebar for user inputs
    with st.sidebar:
        st.header("Your Professional Profile")
        
        experience_years = st.slider("Years of Experience", 0, 30, 5)
        education_level = st.selectbox(
            "Education Level",
            ['High School', 'Bachelor', 'Master', 'PhD', 'Diploma/Certificate']
        )
        industry = st.selectbox(
            "Industry",
            ['Technology', 'Finance', 'Healthcare', 'Education', 'Engineering', 
             'Marketing', 'Sales', 'Design', 'Consulting', 'Manufacturing']
        )
        salary_expectation = st.slider("Expected Annual Salary ($)", 30000, 200000, 70000)
        job_type = st.selectbox(
            "Preferred Job Type",
            ['Full-time', 'Contract', 'Remote', 'Freelance', 'Startup']
        )
        relocation_timeline = st.selectbox(
            "Relocation Timeline",
            ['Immediately', '3-6 months', '6-12 months', '1-2 years', 'Exploring options']
        )
        
        if st.button("Find Opportunities", type="primary"):
            user_input = {
                'experience_years': experience_years,
                'education_level': education_level,
                'industry': industry,
                'salary_expectation': salary_expectation,
                'job_type': job_type,
                'relocation_timeline': relocation_timeline
            }
            
            # Get recommendations
            recommendations = professional_engine.get_recommendations(user_input)
            
            # Save to search history
            auth.add_to_search_history({
                'type': 'professional',
                'input': user_input,
                'recommendations': recommendations
            })
            
            st.session_state.recommendations = recommendations
    
    # Main content area
    col1, col2 = st.columns([2, 1])
    
    with col1:
        if 'recommendations' in st.session_state:
            recommendations = st.session_state.recommendations
            
            # Display top recommendation
            top_country = recommendations['top_recommendation']
            st.success(f"🎯 Top Opportunity: **{top_country}**")
            
            # Show probability chart
            fig = viz.create_country_probability_chart(recommendations['country_probabilities'])
            st.plotly_chart(fig, use_container_width=True)
            
            # Job market analysis
            st.subheader("📈 Job Market Analysis")
            market_analysis = professional_engine.get_job_market_analysis(top_country, industry)
            
            if market_analysis:
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.metric("Market Demand", market_analysis['demand'])
                    st.metric("Average Salary", market_analysis['avg_salary'])
                
                with col2:
                    st.metric("Growth Rate", market_analysis['growth_rate'])
                    st.metric("Competition Level", market_analysis['competition'])
                
                with col3:
                    st.metric("Remote Work", market_analysis['remote_work'])
                    st.metric("Visa Sponsorship", market_analysis['visa_sponsorship'])
                
                # Top companies
                st.subheader("🏢 Top Companies Hiring")
                for company in market_analysis['top_companies']:
                    st.write(f"• **{company['name']}** - {company['hiring_status']}")
            
            # Salary comparison
            st.subheader("💰 Salary Comparison")
            salary_data = professional_engine.get_salary_comparison(industry, experience_years)
            if salary_data:
                fig = viz.create_salary_comparison_chart(salary_data)
                st.plotly_chart(fig, use_container_width=True)
        
        else:
            st.info("👆 Configure your professional profile in the sidebar and click 'Find Opportunities' to get started!")
    
    with col2:
        st.subheader("📊 Career Insights")
        
        if 'recommendations' in st.session_state:
            recommendations = st.session_state.recommendations
            
            col1, col2 = st.columns(2)
            with col1:
                st.metric("Markets Analyzed", len(recommendations['country_probabilities']))
                st.metric("Salary Match", "Excellent" if salary_expectation <= 100000 else "Good")
            
            with col2:
                st.metric("Confidence Score", f"{recommendations['confidence']:.1%}")
                st.metric("Experience Level", "Senior" if experience_years >= 5 else "Mid-Level")
        
        st.subheader("🛂 Visa & Relocation")
        st.write("Based on your profile:")
        st.write("- Eligible for skilled worker visas")
        st.write("- Potential for express entry programs")
        st.write("- Family sponsorship options available")
        
        st.subheader("📝 Application Tips")
        st.write("To improve your chances:")
        st.write("- Tailor resume for international roles")
        st.write("- Highlight cross-cultural experience")
        st.write("- Network with global professionals")
    # Then in the main function, update the map section:
st.markdown("---")
st.subheader("🗺️ Global Job Market Overview")

# Create job market map
try:
    fig_jobs = world_map.create_job_market_map()
    st.plotly_chart(fig_jobs, use_container_width=True)
except Exception as e:
    st.warning(f"Job market map temporarily unavailable: {str(e)}")
    
# pages/4_💼_Professional_Dashboard.py (Add these sections)

# Add this after the main recommendation section
st.markdown("---")
st.subheader("💼 Live Market Data & Tools")

col1, col2 = st.columns(2)

with col1:
    st.markdown("#### 🌍 Country Economic Overview")
    if 'recommendations' in st.session_state:
        top_country = st.session_state.recommendations['top_recommendation']
        
        country_info = api_services.get_country_info(top_country)
        if country_info['success']:
            st.write(f"**{top_country} - Key Information:**")
            st.write(f"• **Population:** {country_info.get('population', 0):,}")
            st.write(f"• **Area:** {country_info.get('area', 0):,} km²")
            st.write(f"• **Capital:** {country_info.get('capital', 'N/A')}")
            st.write(f"• **Languages:** {', '.join(country_info.get('languages', ['N/A']))}")
            st.write(f"• **Currency:** {', '.join(country_info.get('currencies', ['N/A']))}")
            
            # Economic indicators (simulated but realistic)
            gdp_per_capita = country_info.get('population', 1) / country_info.get('area', 1) * 1000
            st.write(f"• **Economic Development:** {'Developed' if gdp_per_capita > 10000 else 'Developing'}")


# Enhanced job market analysis with real-time data
st.markdown("---")
st.subheader("📊 Live Job Market Analysis")

if 'recommendations' in st.session_state:
    top_country = st.session_state.recommendations['top_recommendation']
    
    # Get current industry from session state or use default
    current_industry = st.session_state.get('user_industry', 'Technology')
    
    market_data = api_services.get_job_market_data(top_country, current_industry)
    
    if market_data['success']:
        data = market_data['data']
        
        st.markdown(f"#### {current_industry} Market in {top_country}")
        
        # Key metrics
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Market Demand", data['demand'])
        with col2:
            st.metric("Average Salary", f"${data['avg_salary']:,}")
        with col3:
            st.metric("Growth Rate", data['growth'])
        with col4:
            st.metric("Remote Work", data['remote_work'])
        
        # Industry comparison
        st.markdown("#### 📈 Industry Comparison")
        industries = ['Technology', 'Finance', 'Healthcare', 'Engineering']
        
        comparison_data = []
        for industry in industries:
            industry_data = api_services.get_job_market_data(top_country, industry)
            if industry_data['success']:
                comp_data = industry_data['data']
                comparison_data.append({
                    'Industry': industry,
                    'Average Salary': comp_data['avg_salary'],
                    'Demand': comp_data['demand'],
                    'Growth': comp_data['growth']
                })
        
        if comparison_data:
            comp_df = pd.DataFrame(comparison_data)
            st.dataframe(comp_df, use_container_width=True)

# Cost of living comparison
st.markdown("---")
st.subheader("🏠 Cost of Living Comparison")

col1, col2 = st.columns(2)

with col1:
    current_city = st.selectbox("Your Current City", 
                               ['New York', 'London', 'Tokyo', 'Sydney', 'Berlin'],
                               key="current_city")

with col2:
    if 'recommendations' in st.session_state:
        target_city_map = {
            'United States': 'New York', 'United Kingdom': 'London', 'Canada': 'Toronto',
            'Australia': 'Sydney', 'Japan': 'Tokyo', 'Germany': 'Berlin', 'France': 'Paris'
        }
        target_city = st.selectbox("Target City", 
                                  list(target_city_map.values()),
                                  index=list(target_city_map.values()).index(target_city_map.get(
                                      st.session_state.recommendations['top_recommendation'], 'London')),
                                  key="target_city")


if __name__ == "__main__":
    main()
    
