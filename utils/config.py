# utils/config.py
import os
from dotenv import load_dotenv

load_dotenv()

class APIConfig:
    """API Configuration and Keys"""
    
    # Free APIs (No keys required)
    CURRENCY_API_URL = "https://api.exchangerate-api.com/v4/latest/USD"
    REST_COUNTRIES_URL = "https://restcountries.com/v3.1"
    UNIVERSITIES_API = "http://universities.hipolabs.com"
    
    # APIs requiring keys
    OPENWEATHER_KEY = os.getenv('OPENWEATHER_API_KEY', 'd3c0cb54e40d87dcf2f088ea4f72acad')
    
    # APIs that will be simulated (no keys needed)
    SKYSCANNER_SIMULATED = True
    LINKEDIN_SIMULATED = True
    
    # Fallback settings
    USE_SIMULATED_DATA = True  # Set to False if you get real API keys later
    
    