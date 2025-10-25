# modules/student_engine.py
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
import joblib
import os

class StudentEngine:
    def __init__(self):
        self.model = None
        self.label_encoders = {}
        self.load_or_train_model()
    
    def load_or_train_model(self):
        """Load existing model or train a new one"""
        model_path = "models/student_model.pkl"
        
        if os.path.exists(model_path):
            self.model, self.label_encoders = joblib.load(model_path)
        else:
            self.train_model()
    
    def train_model(self):
        """Train the student recommendation model"""
        # Load or generate sample data
        from modules.data_loader import DataLoader
        data_loader = DataLoader()
        student_data = data_loader.load_student_data()
        
        # Preprocess data
        X, y, label_encoders = self.preprocess_data(student_data)
        
        # Train model
        from sklearn.model_selection import train_test_split
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        
        self.model = RandomForestClassifier(n_estimators=100, random_state=42)
        self.model.fit(X_train, y_train)
        
        self.label_encoders = label_encoders
        
        # Save model
        os.makedirs("models", exist_ok=True)
        joblib.dump((self.model, self.label_encoders), "models/student_model.pkl")
    
    def preprocess_data(self, data):
        """Preprocess student data for model training"""
        label_encoders = {}
        
        # Encode categorical variables
        categorical_columns = ['preferred_major', 'language_preference', 'degree_level']
        
        for col in categorical_columns:
            le = LabelEncoder()
            data[col] = le.fit_transform(data[col])
            label_encoders[col] = le
        
        # Encode target variable
        le_country = LabelEncoder()
        data['country'] = le_country.fit_transform(data['country'])
        label_encoders['country'] = le_country
        
        # Prepare features and target
        feature_columns = ['academic_score', 'budget'] + categorical_columns
        X = data[feature_columns]
        y = data['country']
        
        return X, y, label_encoders
    
    def get_recommendations(self, user_input):
        """Get country recommendations based on user input"""
        # Prepare input features
        features = self.prepare_features(user_input)
        
        # Get predictions
        probabilities = self.model.predict_proba([features])[0]
        
        # Get country names
        country_encoder = self.label_encoders['country']
        countries = country_encoder.classes_
        
        # Create results
        country_probs = list(zip(countries, probabilities))
        country_probs.sort(key=lambda x: x[1], reverse=True)
        
        top_country, top_prob = country_probs[0]
        
        return {
            'top_recommendation': top_country,
            'top_probability': top_prob,
            'country_probabilities': country_probs,
            'confidence': top_prob
        }
    
    def prepare_features(self, user_input):
        """Prepare user input for model prediction"""
        features = []
        
        # Numerical features
        features.append(user_input['academic_score'])
        features.append(user_input['budget'])
        
        # Categorical features
        categorical_features = ['preferred_major', 'language_preference', 'degree_level']
        
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
    
    def get_universities_by_country(self, country, major):
        """Get university recommendations for a specific country and major"""
        # This would typically query a database
        # For now, return sample data
        sample_universities = {
            'USA': [
                {'name': 'Stanford University', 'location': 'California', 'ranking': '#2', 
                 'programs': ['Computer Science', 'Engineering', 'Business'], 
                 'cost': 55000, 'scholarship': 'High'},
                {'name': 'MIT', 'location': 'Massachusetts', 'ranking': '#1', 
                 'programs': ['Engineering', 'Computer Science', 'Physics'], 
                 'cost': 53000, 'scholarship': 'Medium'},
            ],
            'UK': [
                {'name': 'University of Oxford', 'location': 'Oxford', 'ranking': '#1', 
                 'programs': ['Law', 'Medicine', 'Humanities'], 
                 'cost': 35000, 'scholarship': 'High'},
                {'name': 'Imperial College London', 'location': 'London', 'ranking': '#3', 
                 'programs': ['Engineering', 'Medicine', 'Business'], 
                 'cost': 38000, 'scholarship': 'Medium'},
            ],
            # Add more countries...
        }
        
        return sample_universities.get(country, [])