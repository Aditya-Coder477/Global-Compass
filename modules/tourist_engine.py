# modules/tourist_engine.py
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
import joblib
import os
import random
from datetime import datetime, timedelta

class TouristEngine:
    def __init__(self):
        self.model = None
        self.label_encoders = {}
        self.load_or_train_model()
    
    def load_or_train_model(self):
        """Load existing model or train a new one"""
        model_path = "models/tourist_model.pkl"
        
        if os.path.exists(model_path):
            self.model, self.label_encoders = joblib.load(model_path)
        else:
            self.train_model()
    
    def train_model(self):
        """Train the tourist recommendation model"""
        # Load or generate sample data
        from modules.data_loader import DataLoader
        data_loader = DataLoader()
        tourist_data = data_loader.load_tourist_data()
        
        # Preprocess data
        X, y, label_encoders = self.preprocess_data(tourist_data)
        
        # Train model
        from sklearn.model_selection import train_test_split
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        
        self.model = RandomForestClassifier(n_estimators=100, random_state=42)
        self.model.fit(X_train, y_train)
        
        self.label_encoders = label_encoders
        
        # Save model
        os.makedirs("models", exist_ok=True)
        joblib.dump((self.model, self.label_encoders), "models/tourist_model.pkl")
    
    def preprocess_data(self, data):
        """Preprocess tourist data for model training"""
        label_encoders = {}
        
        # Encode categorical variables
        categorical_columns = ['travel_style', 'climate_preference', 'travel_companions', 'season']
        
        for col in categorical_columns:
            le = LabelEncoder()
            data[col] = le.fit_transform(data[col])
            label_encoders[col] = le
        
        # Encode target variable
        le_destination = LabelEncoder()
        data['destination'] = le_destination.fit_transform(data['destination'])
        label_encoders['destination'] = le_destination
        
        # Prepare features and target
        feature_columns = ['budget', 'duration'] + categorical_columns
        X = data[feature_columns]
        y = data['destination']
        
        return X, y, label_encoders
    
    def get_recommendations(self, user_input):
        """Get destination recommendations based on user input"""
        # Prepare input features
        features = self.prepare_features(user_input)
        
        # Get predictions
        probabilities = self.model.predict_proba([features])[0]
        
        # Get destination names
        destination_encoder = self.label_encoders['destination']
        destinations = destination_encoder.classes_
        
        # Create results
        destination_probs = list(zip(destinations, probabilities))
        destination_probs.sort(key=lambda x: x[1], reverse=True)
        
        top_destination, top_prob = destination_probs[0]
        
        return {
            'top_recommendation': top_destination,
            'top_probability': top_prob,
            'destination_probabilities': destination_probs,
            'confidence': top_prob
        }
    
    def prepare_features(self, user_input):
        """Prepare user input for model prediction"""
        features = []
        
        # Numerical features
        features.append(user_input['budget'])
        features.append(user_input['duration'])
        
        # Categorical features
        categorical_features = ['travel_style', 'climate_preference', 'travel_companions', 'season']
        
        for feature in categorical_features:
            if feature in user_input:
                le = self.label_encoders[feature]
                # Handle unseen labels
                if user_input[feature] in le.classes_:
                    encoded = le.transform([user_input[feature]])[0]
                else:
                    encoded = 0  # Default value
                features.append(encoded)
        
        return features
    
    def get_destination_details(self, destination):
        """Get detailed information about a destination"""
        destination_details = {
            'Italy': {
                'best_time': 'April-June, September-October',
                'daily_cost': '$150-250',
                'visa_requirements': 'Visa-free for 90 days',
                'safety_rating': '8.5/10',
                'language': 'Italian',
                'currency': 'Euro (€)',
                'attractions': ['Colosseum in Rome', 'Venetian Canals', 'Florence Art Museums', 'Amalfi Coast', 'Tuscany Countryside']
            },
            'Japan': {
                'best_time': 'March-May, September-November',
                'daily_cost': '$100-200',
                'visa_requirements': 'Visa-free for 90 days',
                'safety_rating': '9.5/10',
                'language': 'Japanese',
                'currency': 'Yen (¥)',
                'attractions': ['Tokyo Skytree', 'Kyoto Temples', 'Mount Fuji', 'Osaka Castle', 'Hiroshima Peace Park']
            },
            'Thailand': {
                'best_time': 'November-February',
                'daily_cost': '$50-100',
                'visa_requirements': 'Visa-free for 30 days',
                'safety_rating': '7.5/10',
                'language': 'Thai',
                'currency': 'Baht (฿)',
                'attractions': ['Grand Palace Bangkok', 'Phi Phi Islands', 'Chiang Mai Temples', 'Floating Markets', 'Elephant Sanctuaries']
            },
            'USA': {
                'best_time': 'Varies by region',
                'daily_cost': '$150-300',
                'visa_requirements': 'ESTA required',
                'safety_rating': '8.0/10',
                'language': 'English',
                'currency': 'US Dollar ($)',
                'attractions': ['New York City', 'Grand Canyon', 'Yellowstone National Park', 'Golden Gate Bridge', 'Las Vegas Strip']
            }
        }
        
        return destination_details.get(destination, {})
    
    def generate_itinerary(self, destination, duration, travel_style):
        """Generate a sample itinerary for the destination"""
        base_itineraries = {
            'Cultural': [
                {'title': 'Historical Exploration', 'activities': ['Museum visits', 'Historical sites', 'Guided tours'], 'cost': 120},
                {'title': 'Local Culture', 'activities': ['Traditional workshops', 'Local markets', 'Cultural shows'], 'cost': 80},
                {'title': 'Architecture Tour', 'activities': ['Famous buildings', 'Local neighborhoods', 'Photo spots'], 'cost': 60}
            ],
            'Adventure': [
                {'title': 'Outdoor Activities', 'activities': ['Hiking', 'Water sports', 'Nature exploration'], 'cost': 150},
                {'title': 'Extreme Sports', 'activities': ['Zip lining', 'Rock climbing', 'Adventure parks'], 'cost': 200},
                {'title': 'Wildlife Safari', 'activities': ['Animal watching', 'Nature reserves', 'Guided tours'], 'cost': 180}
            ],
            'Relaxation': [
                {'title': 'Beach Day', 'activities': ['Swimming', 'Sunbathing', 'Beach sports'], 'cost': 50},
                {'title': 'Spa & Wellness', 'activities': ['Massages', 'Yoga', 'Meditation'], 'cost': 120},
                {'title': 'Scenic Views', 'activities': ['Sunset watching', 'Scenic drives', 'Picnics'], 'cost': 40}
            ]
        }
        
        # Get base itinerary for the travel style
        base_days = base_itineraries.get(travel_style, base_itineraries['Cultural'])
        
        # Generate full itinerary based on duration
        itinerary = []
        for i in range(duration):
            day_template = base_days[i % len(base_days)]
            itinerary.append({
                'title': f"Day {i+1}: {day_template['title']}",
                'activities': day_template['activities'],
                'cost': day_template['cost'] + random.randint(-20, 20)
            })
        
        return itinerary