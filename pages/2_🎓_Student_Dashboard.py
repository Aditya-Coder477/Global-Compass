#Student_Dashboard.py
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

from modules.student_engine import StudentEngine
from modules.visualization import Visualization
from modules.auth import Authentication
from modules.world_map import world_map  # ADD THIS LINE

# Page configuration
st.set_page_config(
    page_title="Student Dashboard - Global Compass",
    page_icon="🎓",
    layout="wide"
)

# Initialize components
auth = Authentication()
student_engine = StudentEngine()
viz = Visualization()

def main():
    # Check authentication
    if not auth.is_authenticated():
        st.warning("Please log in to access the Student Dashboard")
        st.stop()
    
    st.title("🎓 Student Dashboard")
    st.markdown("Find your ideal study destination and universities based on your academic profile")
    
    # Sidebar for user inputs
    with st.sidebar:
        st.header("Your Academic Profile")
        
        academic_score = st.slider("Academic Score (%)", 60, 100, 80)
        budget = st.slider("Annual Budget ($)", 10000, 50000, 25000)
        preferred_major = st.selectbox(
            "Preferred Major",
            ['Computer Science', 'Business', 'Engineering', 'Arts', 'Medicine', 'Law', 'Social Sciences']
        )
        language_preference = st.selectbox(
            "Language Preference",
            ['English', 'French', 'German', 'Spanish', 'Chinese', 'Japanese', 'Korean']
        )
        degree_level = st.selectbox(
            "Degree Level",
            ['Bachelor', 'Master', 'PhD', 'Diploma']
        )
        
        if st.button("Find Recommendations", type="primary"):
            user_input = {
                'academic_score': academic_score,
                'budget': budget,
                'preferred_major': preferred_major,
                'language_preference': language_preference,
                'degree_level': degree_level
            }
            
            # Get recommendations
            recommendations = student_engine.get_recommendations(user_input)
            
            # Save to search history
            auth.add_to_search_history({
                'type': 'student',
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
            st.success(f"🎯 Top Recommendation: **{top_country}**")
            
            # Show probability chart
            fig = viz.create_country_probability_chart(recommendations['country_probabilities'])
            st.plotly_chart(fig, use_container_width=True)
            
            # University recommendations
            st.subheader("🏫 Recommended Universities")
            universities = student_engine.get_universities_by_country(top_country, preferred_major)
            
            for uni in universities:
                with st.expander(f"**{uni['name']}** - {uni['ranking']}"):
                    st.write(f"**Location:** {uni['location']}")
                    st.write(f"**Popular Programs:** {', '.join(uni['programs'])}")
                    st.write(f"**Estimated Cost:** ${uni['cost']:,}/year")
                    st.write(f"**Scholarship Availability:** {uni['scholarship']}")
        
        else:
            st.info("👆 Configure your academic profile in the sidebar and click 'Find Recommendations' to get started!")
    
    with col2:
        st.subheader("📊 Quick Stats")
        
        if 'recommendations' in st.session_state:
            recommendations = st.session_state.recommendations
            
            # Display key metrics
            col1, col2 = st.columns(2)
            with col1:
                st.metric("Countries Considered", len(recommendations['country_probabilities']))
                st.metric("Confidence Score", f"{recommendations['confidence']:.1%}")
            
            with col2:
                st.metric("Top Match Score", f"{recommendations['top_probability']:.1%}")
                st.metric("Budget Fit", "Good" if budget >= 20000 else "Moderate")
        
        st.subheader("ℹ️ Visa Information")
        st.write("Based on your profile, you may be eligible for:")
        st.write("- Student Visa (F-1 for USA)")
        st.write("- Tier 4 Visa (UK)")
        st.write("- Student Permit (Canada)")
        
        st.subheader("💰 Scholarship Opportunities")
        st.write("Based on your academic score, consider:")
        st.write("- Merit-based scholarships")
        st.write("- Country-specific grants")
        st.write("- University financial aid")
        
    # Then in the main function, update the map section:
st.markdown("---")
st.subheader("🗺️ Geographic Distribution")

if 'recommendations' in st.session_state:
    # Create recommendation map
    try:
        fig = world_map.create_recommendation_map(
            st.session_state.recommendations['country_probabilities'],
            "Recommended Study Destinations"
        )
        st.plotly_chart(fig, use_container_width=True)
    except Exception as e:
        st.warning(f"Map visualization temporarily unavailable: {str(e)}")
    
    # Add education quality map
    st.subheader("🎓 Global Education Quality")
    try:
        fig_edu = world_map.create_education_quality_map()
        st.plotly_chart(fig_edu, use_container_width=True)
    except Exception as e:
        st.warning(f"Education map temporarily unavailable: {str(e)}")

# pages/2_🎓_Student_Dashboard.py (Add these sections)

# Add this after the main recommendation section
st.markdown("---")
st.subheader("🌍 Live Country & University Data")

# Live country information
if 'recommendations' in st.session_state:
    top_country = st.session_state.recommendations['top_recommendation']
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown(f"#### 🇺🇳 About {top_country}")
        country_info = api_services.get_country_info(top_country)
        
        if country_info['success']:
            info_col1, info_col2 = st.columns(2)
            with info_col1:
                st.metric("Capital", country_info.get('capital', 'N/A'))
                st.metric("Population", f"{country_info.get('population', 0):,}")
            with info_col2:
                st.metric("Area", f"{country_info.get('area', 0):,} km²")
                st.metric("Languages", ', '.join(country_info.get('languages', ['N/A']))[:20] + '...')
            
            st.caption(f"Source: {country_info.get('source', 'Unknown')}")
        else:
            st.info(f"Basic information about {top_country}")
            st.write(f"• Region: {country_info.get('region', 'N/A')}")
            st.write(f"• Currency: {', '.join(country_info.get('currencies', ['N/A']))}")


# Real-time university data
st.markdown("---")
st.subheader("🎓 Live University Finder")

uni_country = st.selectbox(
    "Search universities in:",
    ['United States', 'United Kingdom', 'Canada', 'Australia', 'Germany', 'France', 'Japan'],
    key="uni_finder"
)

if st.button("Find Universities", key="find_unis"):
    with st.spinner(f"Searching universities in {uni_country}..."):
        universities = api_services.get_universities_by_country(uni_country)
        
        if universities:
            st.success(f"Found {len(universities)} universities in {uni_country}")
            
            # Display first 3 universities in detail
            for i, uni in enumerate(universities[:3]):
                with st.expander(f"**{uni['name']}** - {uni['ranking']}", expanded=i==0):
                    col1, col2 = st.columns(2)
                    with col1:
                        st.write(f"**Country:** {uni['country']}")
                        st.write(f"**Estimated Cost:** ${uni['estimated_cost']:,}/year")
                        st.write(f"**Students:** {uni.get('students', 'N/A'):,}")
                    with col2:
                        st.write(f"**Popular Programs:** {', '.join(uni['popular_programs'])}")
                        if uni.get('founded'):
                            st.write(f"**Founded:** {uni['founded']}")
                        st.write(f"**Source:** {uni.get('source', 'Unknown')}")
                    
                    if uni['web_pages']:
                        st.write(f"🌐 **Website:** {uni['web_pages'][0]}")
        


if __name__ == "__main__":
    main()
    