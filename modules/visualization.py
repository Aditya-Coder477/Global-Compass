# modules/visualization.py
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from modules.world_map import world_map


class Visualization:
    def __init__(self):
        pass
    
    def create_country_probability_chart(self, country_probabilities):
        """Create a bar chart of country probabilities"""
        countries = [cp[0] for cp in country_probabilities]
        probabilities = [cp[1] for cp in country_probabilities]
        
        df = pd.DataFrame({
            'Country': countries,
            'Probability': probabilities
        })
        
        fig = px.bar(df, x='Country', y='Probability',
                     title='Recommendation Probabilities',
                     color='Probability',
                     color_continuous_scale='Blues')
        
        fig.update_layout(
            xaxis_tickangle=-45,
            yaxis_tickformat='.1%'
        )
        
        return fig
    
    def create_salary_comparison_chart(self, salary_data):
        """Create a bar chart comparing salaries across countries"""
        countries = list(salary_data.keys())
        salaries = list(salary_data.values())
        
        df = pd.DataFrame({
            'Country': countries,
            'Salary': salaries
        })
        
        fig = px.bar(df, x='Country', y='Salary',
                     title='Salary Comparison by Country',
                     color='Salary',
                     color_continuous_scale='Viridis')
        
        fig.update_layout(
            yaxis_tickprefix='$',
            yaxis_tickformat=',.0f'
        )
        
        return fig
    
    def create_recommendation_world_map(self, country_probabilities, title="Country Recommendations"):
        """Create a world map visualization for recommendations"""
        return world_map.create_recommendation_map(country_probabilities, title)
    
    def create_comparison_world_map(self, user_data, comparison_type):
        """Create a personalized comparison world map"""
        return world_map.create_comparison_map(user_data, comparison_type)
    
    def create_world_map(self, country_scores):
        """Create a world map with country scores (placeholder)"""
        # This would require country codes and more data
        # For now, return a simple message
        fig = go.Figure()
        fig.add_annotation(
            text="World Map Visualization - Coming Soon!",
            xref="paper", yref="paper",
            x=0.5, y=0.5,
            showarrow=False,
            font=dict(size=20)
        )
        return fig
    