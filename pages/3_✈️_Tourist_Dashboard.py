# pages/3_✈️_Tourist_Dashboard.py
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

from modules.tourist_engine import TouristEngine
from modules.visualization import Visualization
from modules.auth import Authentication
from modules.world_map import world_map  # ADD THIS IMPORT

# Page configuration
st.set_page_config(
    page_title="Tourist Dashboard - Global Compass",
    page_icon="✈️",
    layout="wide"
)

# Initialize components
auth = Authentication()
tourist_engine = TouristEngine()
viz = Visualization()

def main():
    # Check authentication
    if not auth.is_authenticated():
        st.warning("Please log in to access the Tourist Dashboard")
        st.stop()
    
    st.title("✈️ Tourist Dashboard")
    st.markdown("Discover perfect travel destinations based on your preferences and interests")
    
    # Sidebar for user inputs
    with st.sidebar:
        st.header("Your Travel Preferences")
        
        budget = st.slider("Travel Budget ($)", 1000, 10000, 3000)
        travel_style = st.selectbox(
            "Travel Style",
            ['Adventure', 'Cultural', 'Relaxation', 'Food', 'Historical', 'Beach', 'City Break']
        )
        climate_preference = st.selectbox(
            "Climate Preference",
            ['Tropical', 'Temperate', 'Cold', 'Mediterranean', 'Desert', 'Mountain']
        )
        duration = st.slider("Trip Duration (days)", 3, 30, 10)
        travel_companions = st.selectbox(
            "Travel Companions",
            ['Solo', 'Couple', 'Family', 'Friends', 'Business']
        )
        season = st.selectbox(
            "Preferred Season",
            ['Spring', 'Summer', 'Fall', 'Winter', 'Any']
        )
        
        if st.button("Find Destinations", type="primary"):
            user_input = {
                'budget': budget,
                'travel_style': travel_style,
                'climate_preference': climate_preference,
                'duration': duration,
                'travel_companions': travel_companions,
                'season': season
            }
            
            # Get recommendations
            recommendations = tourist_engine.get_recommendations(user_input)
            
            # Save to search history
            auth.add_to_search_history({
                'type': 'tourist',
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
            top_destination = recommendations['top_recommendation']
            st.success(f"🎯 Top Destination: **{top_destination}**")
            
            # Show probability chart
            fig = viz.create_country_probability_chart(recommendations['destination_probabilities'])
            st.plotly_chart(fig, use_container_width=True)
            
            # Destination details
            st.subheader("🏝️ Destination Highlights")
            destination_info = tourist_engine.get_destination_details(top_destination)
            
            if destination_info:
                # This set of columns is the intended level 1 nesting and should be fine
                dest_col1, dest_col2, dest_col3 = st.columns(3)
                
                with dest_col1:
                    st.metric("Best Time to Visit", destination_info['best_time'])
                    st.metric("Average Daily Cost", destination_info['daily_cost'])
                
                with dest_col2:
                    st.metric("Visa Requirements", destination_info['visa_requirements'])
                    st.metric("Safety Rating", destination_info['safety_rating'])
                
                with dest_col3:
                    st.metric("Language", destination_info['language'])
                    st.metric("Currency", destination_info['currency'])
                
                # Highlights
                st.subheader("✨ Must-See Attractions")
                for attraction in destination_info['attractions']:
                    st.write(f"• {attraction}")
            
            # Itinerary suggestions
            st.subheader("🗓️ Sample Itinerary")
            itinerary = tourist_engine.generate_itinerary(top_destination, duration, travel_style)
            for i, day in enumerate(itinerary, 1):
                with st.expander(f"Day {i}: {day['title']}"):
                    st.write(f"**Activities:** {', '.join(day['activities'])}")
                    st.write(f"**Estimated Cost:** ${day['cost']}")
        
        else:
            st.info("👆 Configure your travel preferences in the sidebar and click 'Find Destinations' to get started!")
    
    with col2:
        st.subheader("📊 Travel Insights")
        
        if 'recommendations' in st.session_state:
            recommendations = st.session_state.recommendations
            
            # ----------------------------------------------------------------------
            # FIX: The nested st.columns(2) is removed to eliminate the API exception.
            # The metrics will now stack vertically within the existing col2 space.
            # ----------------------------------------------------------------------
            st.metric("Destinations Analyzed", len(recommendations['destination_probabilities']))
            st.metric("Budget Compatibility", "Excellent" if budget >= 2000 else "Good")
            st.metric("Confidence Score", f"{recommendations['confidence']:.1%}")
            st.metric("Season Match", "Perfect" if season != 'Any' else "Good")
        
        st.subheader("🛂 Visa Information")
        st.write("Based on your nationality:")
        st.write("- Visa-free access to 120+ countries")
        st.write("- E-visa available for 50+ countries")
        st.write("- Visa on arrival for 30+ countries")
        
        st.subheader("💰 Budget Tips")
        st.write("To maximize your budget:")
        st.write("- Travel during shoulder season")
        st.write("- Book flights 6-8 weeks in advance")
        st.write("- Consider alternative accommodations")
        
    # FIXED: World Map Visualization Section
    st.markdown("---")
    st.subheader("🗺️ Travel Destination Map")

    if 'recommendations' in st.session_state:
        # Create tourism map - NOW THIS WILL WORK
        try:
            fig_tourism = world_map.create_tourism_map()
            st.plotly_chart(fig_tourism, use_container_width=True)
        except Exception as e:
            st.warning(f"Map visualization temporarily unavailable: {str(e)}")
        
        # Add personalized map
        try:
            user_data = {
                'travel_style': travel_style,
                'budget': budget
            }
            fig_personal = world_map.create_comparison_map(user_data, 'tourist')
            st.plotly_chart(fig_personal, use_container_width=True)
        except Exception as e:
            st.warning(f"Personalized map temporarily unavailable: {str(e)}")
            
    # pages/3_✈️_Tourist_Dashboard.py (Add these sections)

    # Add this after the main recommendation section
    st.markdown("---")
    st.subheader("✈️ Live Travel Tools")

    col1, col2 = st.columns(2)

    with col1:  
        st.markdown("#### 🗺️ Destination Information")
    if 'recommendations' in st.session_state:
        top_destination = st.session_state.recommendations['top_recommendation']
        
        country_info = api_services.get_country_info(top_destination)
        if country_info['success']:
            st.write(f"**Quick facts about {top_destination}:**")
            st.write(f"• **Capital:** {country_info.get('capital', 'N/A')}")
            st.write(f"• **Language:** {', '.join(country_info.get('languages', ['N/A']))}")
            st.write(f"• **Currency:** {', '.join(country_info.get('currencies', ['N/A']))}")
            st.write(f"• **Region:** {country_info.get('region', 'N/A')}")
            
            # Weather information
            if country_info.get('capital') and country_info['capital'] != 'N/A':
                weather = api_services.get_weather_data(country_info['capital'], top_destination)
                if weather['success']:
                    st.write(f"• **Current Weather:** {weather['temperature']}°C, {weather['description']}")
        
        st.caption(f"Source: {country_info.get('source', 'Unknown')}")


# Flight price estimator
st.markdown("---")
st.subheader("✈️ Flight Price Estimator")

flight_col1, flight_col2, flight_col3 = st.columns(3)

with flight_col1:
    origin_city = st.selectbox("Departure City", 
                              ['New York', 'Los Angeles', 'Chicago', 'Toronto', 'London', 'Sydney'],
                              key="flight_origin")

with flight_col2:
    if 'recommendations' in st.session_state:
        default_dest = st.session_state.recommendations['top_recommendation']
        # Map country to major city
        city_map = {
            'United States': 'New York', 'United Kingdom': 'London', 'Canada': 'Toronto',
            'Australia': 'Sydney', 'Japan': 'Tokyo', 'France': 'Paris', 'Germany': 'Berlin',
            'Italy': 'Rome', 'Spain': 'Madrid'
        }
        destination_city = st.selectbox("Destination City", 
                                       list(city_map.values()),
                                       index=list(city_map.values()).index(city_map.get(default_dest, 'London')),
                                       key="flight_dest")

with flight_col3:
    # Default to 1 month from now
    default_date = (datetime.now() + timedelta(days=30)).strftime('%Y-%m-%d')
    travel_date = st.date_input("Travel Date", 
                              value=datetime.now() + timedelta(days=30),
                              min_value=datetime.now() + timedelta(days=1))

if st.button("Check Flight Prices", key="check_flights"):
    with st.spinner("Searching for flight options..."):
        flight_result = api_services.get_flight_prices(origin_city, destination_city, travel_date.strftime('%Y-%m-%d'))
        
        if flight_result['success']:
            st.success(f"**Estimated Flight Price: ${flight_result['price']}**")
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Airline", flight_result['airline'])
            with col2:
                st.metric("Duration", flight_result['duration'])
            with col3:
                st.metric("Stops", flight_result['stops'])
            

if __name__ == "__main__":
    main()
    