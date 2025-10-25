# pages/7_🗺️_World_Map_Visualization.py
import streamlit as st
import sys
import os
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

# Add modules to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from modules.world_map import world_map
from modules.auth import Authentication

# Page configuration
st.set_page_config(
    page_title="World Map Visualization - Global Compass",
    page_icon="🗺️",
    layout="wide"
)

# Initialize components
auth = Authentication()

def main():
    # Check authentication
    if not auth.is_authenticated():
        st.warning("Please log in to access the World Map Visualization")
        st.stop()
    
    st.title("🗺️ Interactive World Map Visualization")
    st.markdown("Explore global data through interactive maps and heat map overlays")
    
    # Sidebar controls
    st.sidebar.header("Map Controls")
    
    map_type = st.sidebar.selectbox(
        "Select Map Type",
        [
            "🌍 Base World Map",
            "🎯 Recommendation Heat Map", 
            "💰 Cost of Living",
            "🎓 Education Quality",
            "💼 Job Market Strength",
            "✈️ Tourism Popularity",
            "🔍 Personalized Comparison",
            "📍 Interactive Markers"
        ]
    )
    
    # Additional controls based on map type
    if map_type == "🔍 Personalized Comparison":
        comparison_category = st.sidebar.selectbox(
            "Comparison Category",
            ["Overall", "Student", "Professional", "Tourist"]
        )
        
        # Sample user data for personalization
        st.sidebar.subheader("Your Preferences")
        if comparison_category == "Student":
            budget = st.sidebar.slider("Budget ($)", 10000, 50000, 25000)
            major = st.sidebar.selectbox("Preferred Major", ["Computer Science", "Business", "Engineering"])
            user_data = {'budget': budget, 'major': major}
        elif comparison_category == "Professional":
            experience = st.sidebar.slider("Years Experience", 0, 20, 5)
            industry = st.sidebar.selectbox("Industry", ["Technology", "Finance", "Healthcare"])
            user_data = {'experience': experience, 'industry': industry}
        elif comparison_category == "Tourist":
            travel_style = st.sidebar.selectbox("Travel Style", ["Cultural", "Adventure", "Relaxation"])
            budget = st.sidebar.slider("Travel Budget ($)", 1000, 10000, 3000)
            user_data = {'travel_style': travel_style, 'budget': budget}
        else:
            user_data = {}
    
    elif map_type == "🎯 Recommendation Heat Map":
        # Sample recommendation data
        sample_recommendations = [
            ('United States', 0.85), ('United Kingdom', 0.78), ('Canada', 0.72),
            ('Australia', 0.68), ('Germany', 0.65), ('Japan', 0.62),
            ('France', 0.58), ('Netherlands', 0.55), ('Singapore', 0.52)
        ]
        country_probabilities = sample_recommendations
    
    elif map_type == "📍 Interactive Markers":
        available_countries = list(world_map.country_codes.keys())
        selected_countries = st.sidebar.multiselect(
            "Select Countries to Highlight",
            available_countries,
            default=['United States', 'United Kingdom', 'Canada', 'Australia', 'Germany']
        )
    
    # Display the selected map
    st.header(map_type)
    
    if map_type == "🌍 Base World Map":
        fig = world_map.create_base_world_map()
        st.plotly_chart(fig, use_container_width=True)
        
    elif map_type == "🎯 Recommendation Heat Map":
        fig = world_map.create_recommendation_map(country_probabilities)
        st.plotly_chart(fig, use_container_width=True)
        
        # Show data table
        st.subheader("Recommendation Scores")
        df = pd.DataFrame(country_probabilities, columns=['Country', 'Score'])
        df['Score'] = (df['Score'] * 100).round(1)
        df = df.sort_values('Score', ascending=False)
        st.dataframe(df, use_container_width=True)
        
    elif map_type == "💰 Cost of Living":
        fig = world_map.create_cost_of_living_map()
        st.plotly_chart(fig, use_container_width=True)
        
        st.info("""
        **Cost of Living Index:**
        - **Red**: Higher cost of living
        - **Light Red**: Lower cost of living
        - Based on average expenses for housing, food, transportation, etc.
        """)
        
    elif map_type == "🎓 Education Quality":
        fig = world_map.create_education_quality_map()
        st.plotly_chart(fig, use_container_width=True)
        
        st.info("""
        **Education Quality Index:**
        - **Green**: Higher education quality
        - **Light Green**: Good education quality
        - Based on university rankings, research output, and academic reputation
        """)
        
    elif map_type == "💼 Job Market Strength":
        fig = world_map.create_job_market_map()
        st.plotly_chart(fig, use_container_width=True)
        
        st.info("""
        **Job Market Strength Index:**
        - **Purple**: Strong job market
        - **Light Purple**: Moderate job market
        - Based on employment rates, salary levels, and industry growth
        """)
        
    elif map_type == "✈️ Tourism Popularity":
        fig = world_map.create_tourism_map()
        st.plotly_chart(fig, use_container_width=True)
        
        st.info("""
        **Tourism Popularity Index:**
        - **Orange**: Highly popular tourist destinations
        - **Light Orange**: Popular destinations
        - Based on visitor numbers, attractions, and tourism infrastructure
        """)
        
    elif map_type == "🔍 Personalized Comparison":
        fig = world_map.create_comparison_map(user_data, comparison_category.lower())
        st.plotly_chart(fig, use_container_width=True)
        
        st.success(f"Personalized {comparison_category} recommendations based on your preferences!")
        
    elif map_type == "📍 Interactive Markers":
        fig = world_map.create_interactive_marker_map(selected_countries)
        st.plotly_chart(fig, use_container_width=True)
        
        st.info("Click and drag to explore the map. Zoom in/out using mouse wheel.")
    
    # Map interaction instructions
    st.sidebar.markdown("---")
    st.sidebar.subheader("🗺️ Map Interaction Guide")
    st.sidebar.info("""
    **Interactive Features:**
    - **Click and Drag**: Rotate the globe
    - **Mouse Wheel**: Zoom in/out
    - **Hover**: See country details
    - **Double Click**: Reset view
    """)
    
    # Additional analytics
    if map_type != "🌍 Base World Map":
        show_map_analytics(map_type)

def show_map_analytics(map_type):
    """Show additional analytics for the current map view"""
    st.markdown("---")
    st.subheader("📊 Map Analytics")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if map_type == "💰 Cost of Living":
            st.metric("Most Expensive", "Switzerland", "95")
            st.metric("Most Affordable", "India", "35")
        elif map_type == "🎓 Education Quality":
            st.metric("Highest Quality", "Singapore", "90")
            st.metric("Good Value", "Germany", "87")
        elif map_type == "💼 Job Market Strength":
            st.metric("Strongest Market", "Singapore", "88")
            st.metric("Fastest Growing", "Vietnam", "56")
    
    with col2:
        if map_type == "💰 Cost of Living":
            st.metric("Average Cost Index", "68")
            st.metric("Recommended Budget", "$2,500/month")
        elif map_type == "🎓 Education Quality":
            st.metric("Average Quality Score", "76")
            st.metric("Top 10 Countries", "8 in Europe")
    
    with col3:
        st.metric("Countries Displayed", "40+")
        st.metric("Data Currency", "2024")

if __name__ == "__main__":
    main()