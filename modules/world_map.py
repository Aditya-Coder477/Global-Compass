# modules/world_map.py
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np
from modules.api_services import api_services

class WorldMapVisualization:
    """Interactive world map visualization with multiple overlay options"""
    
    def __init__(self):
        self.country_codes = self._load_country_codes()
        self.region_data = self._load_region_data()
    
    def _load_country_codes(self):
        """Load ISO country codes for mapping"""
        return {
            'United States': 'USA', 'United Kingdom': 'GBR', 'Canada': 'CAN', 'Australia': 'AUS',
            'Germany': 'DEU', 'France': 'FRA', 'Japan': 'JPN', 'Italy': 'ITA', 'Spain': 'ESP',
            'Netherlands': 'NLD', 'Sweden': 'SWE', 'Switzerland': 'CHE', 'Singapore': 'SGP',
            'United Arab Emirates': 'ARE', 'Brazil': 'BRA', 'Mexico': 'MEX', 'China': 'CHN',
            'India': 'IND', 'South Korea': 'KOR', 'Thailand': 'THA', 'Vietnam': 'VNM',
            'Portugal': 'PRT', 'Greece': 'GRC', 'Turkey': 'TUR', 'South Africa': 'ZAF',
            'New Zealand': 'NZL', 'Ireland': 'IRL', 'Denmark': 'DNK', 'Norway': 'NOR',
            'Finland': 'FIN', 'Austria': 'AUT', 'Belgium': 'BEL', 'Poland': 'POL',
            'Czech Republic': 'CZE', 'Hungary': 'HUN', 'Romania': 'ROU', 'Ukraine': 'UKR',
            'Russia': 'RUS', 'Saudi Arabia': 'SAU', 'Egypt': 'EGY', 'Nigeria': 'NGA',
            'Kenya': 'KEN', 'Argentina': 'ARG', 'Chile': 'CHL', 'Colombia': 'COL',
            'Peru': 'PER', 'Malaysia': 'MYS', 'Indonesia': 'IDN', 'Philippines': 'PHL'
        }
    
    def _load_region_data(self):
        """Load regional grouping data"""
        return {
            'North America': ['United States', 'Canada', 'Mexico'],
            'Europe': ['United Kingdom', 'Germany', 'France', 'Italy', 'Spain', 'Netherlands', 
                      'Sweden', 'Switzerland', 'Portugal', 'Greece', 'Ireland', 'Denmark', 
                      'Norway', 'Finland', 'Austria', 'Belgium', 'Poland', 'Czech Republic', 
                      'Hungary', 'Romania'],
            'Asia': ['Japan', 'China', 'India', 'South Korea', 'Thailand', 'Vietnam', 
                    'Singapore', 'Malaysia', 'Indonesia', 'Philippines'],
            'Oceania': ['Australia', 'New Zealand'],
            'Middle East': ['United Arab Emirates', 'Turkey', 'Saudi Arabia', 'Egypt'],
            'Africa': ['South Africa', 'Nigeria', 'Kenya'],
            'South America': ['Brazil', 'Argentina', 'Chile', 'Colombia', 'Peru']
        }
    
    def create_base_world_map(self, title="Global Compass - World View"):
        """Create a base world map with country boundaries"""
        # Sample data for all countries
        countries = list(self.country_codes.keys())
        codes = list(self.country_codes.values())
        
        # Create sample values for visualization
        values = np.random.uniform(0, 100, len(countries))
        
        fig = px.choropleth(
            locations=codes,
            color=values,
            hover_name=countries,
            title=title,
            color_continuous_scale='Blues',
            projection='natural earth'
        )
        
        fig.update_layout(
            height=600,
            geo=dict(
                showframe=False,
                showcoastlines=True,
                projection_type='equirectangular'
            ),
            margin={"r":0,"t":50,"l":0,"b":0}
        )
        
        return fig
    
    def create_recommendation_map(self, country_probabilities, title="Country Recommendations"):
        """Create a heat map based on recommendation probabilities"""
        countries = []
        codes = []
        probabilities = []
        
        for country, prob in country_probabilities:
            if country in self.country_codes:
                countries.append(country)
                codes.append(self.country_codes[country])
                probabilities.append(prob * 100)  # Convert to percentage
        
        if not countries:
            return self.create_base_world_map(title)
        
        fig = px.choropleth(
            locations=codes,
            color=probabilities,
            hover_name=countries,
            title=title,
            color_continuous_scale='Viridis',
            range_color=[0, 100],
            labels={'color': 'Recommendation Score (%)'},
            projection='natural earth'
        )
        
        fig.update_layout(
            height=600,
            geo=dict(
                showframe=False,
                showcoastlines=True,
                projection_type='equirectangular'
            ),
            margin={"r":0,"t":50,"l":0,"b":0}
        )
        
        return fig
    
    def create_cost_of_living_map(self):
        """Create a heat map showing cost of living by country"""
        # Sample cost of living data (in reality, this would come from an API)
        cost_data = {
            'United States': 85, 'United Kingdom': 78, 'Canada': 72, 'Australia': 75,
            'Germany': 70, 'France': 68, 'Japan': 82, 'Italy': 65, 'Spain': 60,
            'Netherlands': 73, 'Sweden': 74, 'Switzerland': 95, 'Singapore': 88,
            'United Arab Emirates': 80, 'Brazil': 45, 'Mexico': 48, 'China': 55,
            'India': 35, 'South Korea': 70, 'Thailand': 40, 'Vietnam': 38,
            'Portugal': 58, 'Greece': 56, 'Turkey': 42, 'South Africa': 44
        }
        
        countries = []
        codes = []
        costs = []
        
        for country, cost in cost_data.items():
            if country in self.country_codes:
                countries.append(country)
                codes.append(self.country_codes[country])
                costs.append(cost)
        
        fig = px.choropleth(
            locations=codes,
            color=costs,
            hover_name=countries,
            title="Cost of Living Index by Country",
            color_continuous_scale='Reds',
            range_color=[30, 100],
            labels={'color': 'Cost Index'},
            projection='natural earth'
        )
        
        fig.update_layout(
            height=600,
            geo=dict(
                showframe=False,
                showcoastlines=True,
                projection_type='equirectangular'
            ),
            margin={"r":0,"t":50,"l":0,"b":0}
        )
        
        return fig
    
    def create_education_quality_map(self):
        """Create a heat map showing education quality by country"""
        # Sample education quality data
        education_data = {
            'United States': 85, 'United Kingdom': 88, 'Canada': 84, 'Australia': 83,
            'Germany': 87, 'France': 82, 'Japan': 86, 'Italy': 78, 'Spain': 76,
            'Netherlands': 85, 'Sweden': 84, 'Switzerland': 89, 'Singapore': 90,
            'United Arab Emirates': 65, 'Brazil': 55, 'Mexico': 58, 'China': 75,
            'India': 60, 'South Korea': 88, 'Thailand': 52, 'Vietnam': 56,
            'Portugal': 72, 'Greece': 68, 'Turkey': 62, 'South Africa': 58
        }
        
        countries = []
        codes = []
        scores = []
        
        for country, score in education_data.items():
            if country in self.country_codes:
                countries.append(country)
                codes.append(self.country_codes[country])
                scores.append(score)
        
        fig = px.choropleth(
            locations=codes,
            color=scores,
            hover_name=countries,
            title="Higher Education Quality Index",
            color_continuous_scale='Greens',
            range_color=[50, 95],
            labels={'color': 'Quality Score'},
            projection='natural earth'
        )
        
        fig.update_layout(
            height=600,
            geo=dict(
                showframe=False,
                showcoastlines=True,
                projection_type='equirectangular'
            ),
            margin={"r":0,"t":50,"l":0,"b":0}
        )
        
        return fig
    
    def create_job_market_map(self):
        """Create a heat map showing job market strength by country"""
        # Sample job market data
        job_data = {
            'United States': 82, 'United Kingdom': 75, 'Canada': 78, 'Australia': 76,
            'Germany': 80, 'France': 72, 'Japan': 74, 'Italy': 65, 'Spain': 62,
            'Netherlands': 77, 'Sweden': 79, 'Switzerland': 85, 'Singapore': 88,
            'United Arab Emirates': 78, 'Brazil': 58, 'Mexico': 55, 'China': 72,
            'India': 68, 'South Korea': 75, 'Thailand': 52, 'Vietnam': 56,
            'Portugal': 60, 'Greece': 58, 'Turkey': 62, 'South Africa': 54
        }
        
        countries = []
        codes = []
        scores = []
        
        for country, score in job_data.items():
            if country in self.country_codes:
                countries.append(country)
                codes.append(self.country_codes[country])
                scores.append(score)
        
        fig = px.choropleth(
            locations=codes,
            color=scores,
            hover_name=countries,
            title="Job Market Strength Index",
            color_continuous_scale='Purples',
            range_color=[50, 90],
            labels={'color': 'Market Score'},
            projection='natural earth'
        )
        
        fig.update_layout(
            height=600,
            geo=dict(
                showframe=False,
                showcoastlines=True,
                projection_type='equirectangular'
            ),
            margin={"r":0,"t":50,"l":0,"b":0}
        )
        
        return fig
    
    def create_tourism_map(self):
        """Create a heat map showing tourism popularity by country"""
        # Sample tourism data
        tourism_data = {
            'United States': 85, 'United Kingdom': 82, 'Canada': 70, 'Australia': 75,
            'Germany': 78, 'France': 90, 'Japan': 80, 'Italy': 88, 'Spain': 87,
            'Netherlands': 72, 'Sweden': 65, 'Switzerland': 75, 'Singapore': 78,
            'United Arab Emirates': 82, 'Brazil': 68, 'Mexico': 72, 'China': 75,
            'India': 70, 'South Korea': 65, 'Thailand': 85, 'Vietnam': 72,
            'Portugal': 80, 'Greece': 85, 'Turkey': 78, 'South Africa': 68
        }
        
        countries = []
        codes = []
        scores = []
        
        for country, score in tourism_data.items():
            if country in self.country_codes:
                countries.append(country)
                codes.append(self.country_codes[country])
                scores.append(score)
        
        fig = px.choropleth(
            locations=codes,
            color=scores,
            hover_name=countries,
            title="Tourism Popularity Index",
            color_continuous_scale='Oranges',
            range_color=[60, 95],
            labels={'color': 'Tourism Score'},
            projection='natural earth'
        )
        
        fig.update_layout(
            height=600,
            geo=dict(
                showframe=False,
                showcoastlines=True,
                projection_type='equirectangular'
            ),
            margin={"r":0,"t":50,"l":0,"b":0}
        )
        
        return fig
    
    def create_comparison_map(self, user_data, comparison_type='overall'):
        """Create a comprehensive comparison map based on user preferences"""
        scores = {}
        
        for country in self.country_codes.keys():
            score = self._calculate_country_score(country, user_data, comparison_type)
            scores[country] = score
        
        countries = []
        codes = []
        final_scores = []
        
        for country, score in scores.items():
            if country in self.country_codes and score > 0:
                countries.append(country)
                codes.append(self.country_codes[country])
                final_scores.append(score)
        
        if not countries:
            return self.create_base_world_map("Country Comparison")
        
        fig = px.choropleth(
            locations=codes,
            color=final_scores,
            hover_name=countries,
            title=f"Personalized {comparison_type.title()} Score",
            color_continuous_scale='Plasma',
            range_color=[0, 100],
            labels={'color': 'Match Score (%)'},
            projection='natural earth'
        )
        
        fig.update_layout(
            height=600,
            geo=dict(
                showframe=False,
                showcoastlines=True,
                projection_type='equirectangular'
            ),
            margin={"r":0,"t":50,"l":0,"b":0}
        )
        
        return fig
    
    def _calculate_country_score(self, country, user_data, comparison_type):
        """Calculate a personalized score for a country based on user data"""
        base_score = 50
        
        if comparison_type == 'student':
            # Factors: education quality, cost, language
            education_scores = {
                'United States': 85, 'United Kingdom': 88, 'Canada': 84, 'Germany': 87,
                'Australia': 83, 'Japan': 86, 'France': 82, 'Netherlands': 85
            }
            cost_scores = {
                'United States': 40, 'United Kingdom': 60, 'Canada': 70, 'Germany': 75,
                'Australia': 65, 'Japan': 55, 'France': 70, 'Netherlands': 72
            }
            
            education = education_scores.get(country, 50)
            cost = cost_scores.get(country, 50)
            
            # Adjust based on user budget
            user_budget = user_data.get('budget', 25000)
            if user_budget > 30000:
                cost_weight = 0.3
            else:
                cost_weight = 0.6
            
            score = (education * 0.7) + (cost * cost_weight)
            
        elif comparison_type == 'professional':
            # Factors: job market, salary, visa ease
            job_scores = {
                'United States': 85, 'United Kingdom': 78, 'Canada': 80, 'Germany': 82,
                'Australia': 76, 'Japan': 75, 'Singapore': 88, 'Switzerland': 90
            }
            salary_scores = {
                'United States': 90, 'United Kingdom': 70, 'Canada': 75, 'Germany': 75,
                'Australia': 72, 'Japan': 70, 'Singapore': 85, 'Switzerland': 95
            }
            
            job = job_scores.get(country, 50)
            salary = salary_scores.get(country, 50)
            
            score = (job * 0.6) + (salary * 0.4)
            
        elif comparison_type == 'tourist':
            # Factors: attractions, cost, safety
            tourism_scores = {
                'France': 90, 'Italy': 88, 'Spain': 87, 'United States': 85,
                'Thailand': 85, 'Japan': 80, 'United Kingdom': 82, 'Greece': 85
            }
            safety_scores = {
                'Japan': 95, 'Singapore': 95, 'Switzerland': 90, 'Canada': 90,
                'Australia': 88, 'Germany': 85, 'United Kingdom': 85, 'France': 80
            }
            
            tourism = tourism_scores.get(country, 50)
            safety = safety_scores.get(country, 50)
            
            score = (tourism * 0.7) + (safety * 0.3)
            
        else:  # overall
            score = base_score
        
        return min(100, max(0, score))
    
    def create_interactive_marker_map(self, selected_countries=None, user_data=None):
        """Create an interactive map with markers for selected countries"""
        if selected_countries is None:
            selected_countries = ['United States', 'United Kingdom', 'Canada', 'Australia']
        
        # Create base map
        fig = go.Figure()
        
        # Add country boundaries
        fig.add_trace(go.Choropleth(
            locations=list(self.country_codes.values()),
            z=[1] * len(self.country_codes),  # Dummy data
            colorscale=['lightgray', 'lightgray'],
            showscale=False,
            hoverinfo='skip'
        ))
        
        # Add markers for selected countries
        lats = []
        lons = []
        names = []
        sizes = []
        
        # Sample coordinates for major cities
        city_coordinates = {
            'United States': (39.8283, -98.5795),  # Geographic center
            'United Kingdom': (55.3781, -3.4360),
            'Canada': (56.1304, -106.3468),
            'Australia': (-25.2744, 133.7751),
            'Germany': (51.1657, 10.4515),
            'France': (46.2276, 2.2137),
            'Japan': (36.2048, 138.2529),
            'Italy': (41.8719, 12.5674),
            'Spain': (40.4637, -3.7492),
            'Netherlands': (52.1326, 5.2913)
        }
        
        for country in selected_countries:
            if country in city_coordinates:
                lat, lon = city_coordinates[country]
                lats.append(lat)
                lons.append(lon)
                names.append(country)
                sizes.append(20)  # Marker size
        
        # Add scatter markers
        fig.add_trace(go.Scattergeo(
            lon=lons,
            lat=lats,
            text=names,
            mode='markers+text',
            marker=dict(
                size=sizes,
                color='red',
                opacity=0.8,
                line=dict(width=2, color='darkred')
            ),
            textposition="top center",
            name="Recommended Countries"
        ))
        
        fig.update_layout(
            title="Recommended Countries - Interactive View",
            geo=dict(
                showframe=False,
                showcoastlines=True,
                projection_type='equirectangular',
                landcolor='lightgray',
                countrycolor='white'
            ),
            height=600,
            margin={"r":0,"t":50,"l":0,"b":0}
        )
        
        return fig

# Global instance
world_map = WorldMapVisualization()