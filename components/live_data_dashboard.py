# components/live_data_dashboard.py
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from datetime import datetime, timedelta
from modules.api_services import api_services
import random

def show_live_currency_dashboard():
    """Show live currency exchange dashboard"""
    st.subheader("💱 Live Currency Exchange Dashboard")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # Currency converter
        st.markdown("#### Currency Converter")
        conv_col1, conv_col2, conv_col3 = st.columns(3)
        
        with conv_col1:
            amount = st.number_input("Amount", min_value=1.0, value=100.0, step=10.0, key="conv_amount")
            from_currency = st.selectbox("From", ['USD', 'EUR', 'GBP', 'JPY', 'CAD', 'AUD'], key="conv_from")
        
        with conv_col2:
            to_currency = st.selectbox("To", ['EUR', 'USD', 'GBP', 'JPY', 'CAD', 'AUD'], key="conv_to")
        
        with conv_col3:
            st.markdown("")  # Spacer
            st.markdown("")  # Spacer
            if st.button("Convert", use_container_width=True):
                result = api_services.convert_currency(amount, from_currency, to_currency)
                
                st.success(
                    f"**{result['original_amount']} {result['original_currency']} = "
                    f"{result['converted_amount']} {result['target_currency']}**"
                )
                st.caption(f"Exchange rate: 1 {from_currency} = {result['exchange_rate']:.4f} {to_currency}")
                st.caption(f"Source: {result['source']}")
    
    with col2:
        # Live rates summary
        st.markdown("#### Live Rates (vs USD)")
        rates_data = api_services.get_currency_rates('USD')
        
        if rates_data['success']:
            rates = rates_data['rates']
            for currency, data in list(rates.items())[:4]:  # Show top 4
                st.metric(
                    label=currency,
                    value=f"{data['rate']:.4f}",
                    delta=f"{data['name']}"
                )
            st.caption(f"Last updated: {rates_data['last_updated']}")
        else:
            st.warning("Using simulated exchange rates")
    
    # Currency trends chart
    st.markdown("#### Currency Trends")
    show_currency_trends()

def show_currency_trends():
    """Show historical currency trends (simulated)"""
    # Generate realistic trend data
    currencies = ['EUR', 'GBP', 'JPY', 'CAD', 'AUD']
    dates = pd.date_range(start='2024-01-01', end=datetime.now(), freq='D')
    
    trend_data = []
    for currency in currencies:
        # Start with realistic base rates
        base_rates = {'EUR': 0.85, 'GBP': 0.73, 'JPY': 110.0, 'CAD': 1.25, 'AUD': 1.35}
        base_rate = base_rates[currency]
        
        # Add some realistic fluctuation
        for date in dates:
            # Weekend effect
            day_effect = 0.98 if date.weekday() >= 5 else 1.0
            
            # Random walk with slight appreciation/depreciation trend
            trend = 1.0 + (date - dates[0]).days * 0.0001  # Very slight trend
            fluctuation = random.uniform(0.95, 1.05)
            
            rate = base_rate * day_effect * trend * fluctuation
            
            trend_data.append({
                'Date': date,
                'Currency': currency,
                'Exchange Rate': round(rate, 4)
            })
    
    df = pd.DataFrame(trend_data)
    
    fig = px.line(df, x='Date', y='Exchange Rate', color='Currency',
                  title='Currency Exchange Rate Trends (2024)',
                  labels={'Exchange Rate': 'Rate vs USD'})
    
    fig.update_layout(
        xaxis_title='Date',
        yaxis_title='Exchange Rate (vs USD)',
        hovermode='x unified'
    )
    
    st.plotly_chart(fig, use_container_width=True)

def show_live_country_comparison():
    """Show live country data comparison"""
    st.subheader("🌍 Live Country Comparison")
    
    countries = st.multiselect(
        "Select countries to compare",
        ['United States', 'United Kingdom', 'Canada', 'Australia', 'Germany', 'Japan'],
        default=['United States', 'United Kingdom', 'Germany']
    )
    
    if countries:
        # Fetch country data
        country_data = []
        for country in countries:
            data = api_services.get_country_info(country)
            if data['success']:
                country_data.append(data)
        
        if country_data:
            # Create comparison table
            comparison_df = pd.DataFrame([
                {
                    'Country': data['name'],
                    'Population': f"{data['population']:,}",
                    'Area (km²)': f"{data['area']:,}",
                    'Capital': data['capital'],
                    'Region': data['region'],
                    'Languages': ', '.join(data['languages'][:2]),
                    'Source': data['source']
                }
                for data in country_data
            ])
            
            st.dataframe(comparison_df, use_container_width=True)
            
            # Population comparison chart
            pop_data = [{'Country': data['name'], 'Population': data['population']} for data in country_data]
            pop_df = pd.DataFrame(pop_data)
            
            fig = px.bar(pop_df, x='Country', y='Population', 
                        title='Population Comparison',
                        color='Country')
            st.plotly_chart(fig, use_container_width=True)

def show_university_finder():
    """Show real-time university finder"""
    st.subheader("🎓 Live University Finder")
    
    col1, col2 = st.columns(2)
    
    with col1:
        country = st.selectbox(
            "Select Country",
            ['United States', 'United Kingdom', 'Canada', 'Australia', 'Germany', 'France', 'Japan'],
            key="uni_country"
        )
    
    with col2:
        if st.button("Find Universities", use_container_width=True):
            with st.spinner(f"Searching universities in {country}..."):
                universities = api_services.get_universities_by_country(country)
                
                if universities:
                    st.success(f"Found {len(universities)} universities in {country}")
                    
                    # Display universities
                    for i, uni in enumerate(universities[:5]):  # Show first 5
                        with st.expander(f"**{uni['name']}** - {uni['ranking']}"):
                            st.write(f"**Country:** {uni['country']}")
                            st.write(f"**Estimated Cost:** ${uni['estimated_cost']:,}/year")
                            st.write(f"**Popular Programs:** {', '.join(uni['popular_programs'])}")
                            if uni['web_pages']:
                                st.write(f"**Website:** {uni['web_pages'][0]}")
                            st.write(f"**Data Source:** {uni.get('source', 'Unknown')}")
                else:
                    st.warning(f"No universities found for {country}")

def show_flight_price_tracker():
    """Show flight price tracking dashboard"""
    st.subheader("✈️ Flight Price Estimates")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        origin = st.selectbox("Origin City", 
                            ['New York', 'London', 'Tokyo', 'Sydney', 'Dubai', 'Paris'],
                            key="flight_origin")
    
    with col2:
        destination = st.selectbox("Destination City",
                                 ['London', 'New York', 'Los Angeles', 'Singapore', 'Paris', 'Dubai'],
                                 key="flight_dest")
    
    with col3:
        # Default to 2 weeks from now
        default_date = (datetime.now() + timedelta(days=14)).strftime('%Y-%m-%d')
        travel_date = st.date_input("Travel Date", 
                                  value=datetime.now() + timedelta(days=14),
                                  min_value=datetime.now() + timedelta(days=1))
    
    if st.button("Check Flight Prices", use_container_width=True):
        with st.spinner("Searching for flights..."):
            result = api_services.get_flight_prices(origin, destination, travel_date.strftime('%Y-%m-%d'))
            
            if result['success']:
                st.success(f"**Best Price: ${result['price']}**")
                
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Airline", result['airline'])
                with col2:
                    st.metric("Duration", result['duration'])
                with col3:
                    st.metric("Stops", result['stops'])
                
                st.caption(f"Source: {result['source']} | {result.get('note', '')}")
            else:
                st.error("Could not fetch flight prices")

# Main dashboard function
def show_live_data_dashboard():
    """Main function to show all live data components"""
    st.title("📊 Real-time Data Dashboard")
    
    tab1, tab2, tab3, tab4 = st.tabs([
        "💱 Currency", "🌍 Countries", "🎓 Universities", "✈️ Flights"
    ])
    
    with tab1:
        show_live_currency_dashboard()
    
    with tab2:
        show_live_country_comparison()
    
    with tab3:
        show_university_finder()
    
    with tab4:
        show_flight_price_tracker()