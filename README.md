# 🌍 Global Compass

**Your Intelligent Guide for Studying, Traveling, and Working Abroad**

## 📖 Overview

Global Compass is an AI-powered platform that helps users make informed decisions about international education, travel, and career opportunities. Using machine learning and real-time data, we provide personalized recommendations for universities, travel destinations, and job markets worldwide.

## 🚀 Live Demo

**Experience Global Compass:**
https://global-path-finder.streamlit.app/

## ✨ Features

### 🎓 Student Dashboard
- **University Matching**: Find ideal universities based on your academic profile
- **Scholarship Information**: Discover funding opportunities
- **Visa Guidance**: Understand student visa requirements
- **Cost Analysis**: Compare education expenses across countries

### ✈️ Tourist Dashboard  
- **Destination Recommendations**: Personalized travel suggestions
- **Itinerary Planning**: Create optimized travel plans
- **Budget Tracking**: Manage travel expenses
- **Local Experiences**: Discover authentic cultural activities

### 💼 Professional Dashboard
- **Job Market Analysis**: Explore career opportunities worldwide
- **Salary Insights**: Compare compensation across countries
- **Visa Requirements**: Understand work permit processes
- **Relocation Planning**: Comprehensive moving guidance

### 🤖 AI Assistant
- **Intelligent Chatbot**: Get instant answers to your questions
- **Personalized Advice**: Tailored recommendations based on your profile
- **Quick Actions**: One-click navigation to relevant tools

### 💰 Financial Tools
- **Currency Converter**: Real-time exchange rates
- **Tax Calculators**: Income tax estimates for different countries
- **Investment Planning**: Retirement and savings calculators
- **Cost of Living**: Compare expenses across cities

### 🗺️ World Map Visualization
- **Interactive Maps**: Explore recommendations geographically
- **Heat Map Overlays**: Visualize data across countries
- **Country Comparisons**: Side-by-side analysis

Project Structure:
global-compass/
├── app.py                 # Main application entry point
├── requirements.txt       # Python dependencies
├── .streamlit/           # Streamlit configuration
│   └── config.toml
├── pages/                # Multi-page dashboard
│   ├── 2_🎓_Student_Dashboard.py
│   ├── 3_✈️_Tourist_Dashboard.py
│   ├── 4_💼_Professional_Dashboard.py
│   ├── 6_💰_Financial_Tools.py
│   ├── 7_🗺️_World_Map_Visualization.py
│   └── 8_🤖_AI_Assistant.py
├── modules/              # Core functionality
│   ├── auth.py           # Authentication system
│   ├── student_engine.py # Student recommendation engine
│   ├── tourist_engine.py # Travel recommendation engine
│   ├── professional_engine.py # Career recommendation engine
│   ├── api_services.py   # External API integrations
│   ├── financial_tools.py # Financial calculators
│   ├── world_map.py      # Map visualizations
│   ├── chatbot_engine.py # AI assistant
│   └── data_loader.py    # Data management
├── components/           # Reusable UI components
│   └── chatbot_interface.py
├── utils/                # Utility functions
│   └── config.py         # Configuration management
├── data/                 # Data storage
│   └── user_data/        # User profiles and history
└── models/               # ML models (auto-generated)
    ├── student_model.pkl
    ├── tourist_model.pkl
    └── professional_model.pkl

    
## 🛠️ Technology Stack

### Backend & ML
- **Python 3.8+** - Core programming language
- **Streamlit** - Web application framework
- **Scikit-learn** - Machine learning models
- **Pandas & NumPy** - Data processing and analysis

### Frontend & Visualization
- **Plotly** - Interactive charts and maps
- **Streamlit Components** - UI elements and layout

### APIs & Data Integration
- **REST Countries API** - Country information
- **ExchangeRate-API** - Real-time currency data
- **Universities API** - Global university data
- **OpenWeather API** - Weather information

### Data & Storage
- **JSON** - User data and preferences
- **Joblib** - Machine learning model persistence

## 📦 Installation

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)

### Local Development

1. Clone the repository
   git clone https://github.com/yourusername/global-compass.git
   cd global-compass
2.Create virtual environment
   python -m venv .venv
# Windows
.venv\Scripts\activate
# Mac/Linux
source .venv/bin/activate
3.Install dependencies
pip install -r requirements.txt
4.Set up environment variables
# Create .env file
echo "OPENWEATHER_API_KEY=your_api_key_here" > .env
5.Run the application
streamlit run app.py
