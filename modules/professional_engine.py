# modules/professional_engine.py
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
import joblib
import os

class ProfessionalEngine:
    def __init__(self):
        self.model = None
        self.label_encoders = {}
        self.load_or_train_model()
    
    def load_or_train_model(self):
        """Load existing model or train a new one"""
        model_path = "models/professional_model.pkl"
        
        if os.path.exists(model_path):
            self.model, self.label_encoders = joblib.load(model_path)
        else:
            self.train_model()
    
    def train_model(self):
        """Train the professional recommendation model"""
        # Load or generate sample data
        from modules.data_loader import DataLoader
        data_loader = DataLoader()
        professional_data = data_loader.load_professional_data()
        
        # Preprocess data
        X, y, label_encoders = self.preprocess_data(professional_data)
        
        # Train model
        from sklearn.model_selection import train_test_split
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        
        self.model = RandomForestClassifier(n_estimators=100, random_state=42)
        self.model.fit(X_train, y_train)
        
        self.label_encoders = label_encoders
        
        # Save model
        os.makedirs("models", exist_ok=True)
        joblib.dump((self.model, self.label_encoders), "models/professional_model.pkl")
    
    def preprocess_data(self, data):
        """Preprocess professional data for model training"""
        label_encoders = {}
        
        # Encode categorical variables
        categorical_columns = ['education_level', 'industry', 'job_type', 'relocation_timeline']
        
        for col in categorical_columns:
            le = LabelEncoder()
            data[col] = le.fit_transform(data[col])
            label_encoders[col] = le
        
        # Encode target variable
        le_country = LabelEncoder()
        data['country'] = le_country.fit_transform(data['country'])
        label_encoders['country'] = le_country
        
        # Prepare features and target
        feature_columns = ['experience_years', 'salary_expectation'] + categorical_columns
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
        features.append(user_input['experience_years'])
        features.append(user_input['salary_expectation'])
        
        # Categorical features
        categorical_features = ['education_level', 'industry', 'job_type', 'relocation_timeline']
        
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
    
    def get_job_market_analysis(self, country, industry):
        """Get job market analysis for a specific country and industry"""
        market_data = {
            'USA': {
                'Technology': {
                    'demand': 'Very High',
                    'avg_salary': '$120,000',
                    'growth_rate': '15%',
                    'competition': 'High',
                    'remote_work': '80%',
                    'visa_sponsorship': 'Medium',
                    'top_companies': [
                        {'name': 'Google', 'hiring_status': 'Active'},
                        {'name': 'Microsoft', 'hiring_status': 'Active'},
                        {'name': 'Amazon', 'hiring_status': 'Selective'}
                    ]
                },
                'Finance': {
                    'demand': 'High',
                    'avg_salary': '$110,000',
                    'growth_rate': '8%',
                    'competition': 'Very High',
                    'remote_work': '40%',
                    'visa_sponsorship': 'Low',
                    'top_companies': [
                        {'name': 'Goldman Sachs', 'hiring_status': 'Active'},
                        {'name': 'JPMorgan', 'hiring_status': 'Selective'},
                        {'name': 'Morgan Stanley', 'hiring_status': 'Active'}
                    ]
                }
            },
            'Germany': {
                'Technology': {
                    'demand': 'High',
                    'avg_salary': '€65,000',
                    'growth_rate': '12%',
                    'competition': 'Medium',
                    'remote_work': '70%',
                    'visa_sponsorship': 'High',
                    'top_companies': [
                        {'name': 'SAP', 'hiring_status': 'Very Active'},
                        {'name': 'Siemens', 'hiring_status': 'Active'},
                        {'name': 'BMW', 'hiring_status': 'Selective'}
                    ]
                },
                'Engineering': {
                    'demand': 'Very High',
                    'avg_salary': '€70,000',
                    'growth_rate': '10%',
                    'competition': 'Medium',
                    'remote_work': '30%',
                    'visa_sponsorship': 'High',
                    'top_companies': [
                        {'name': 'Volkswagen', 'hiring_status': 'Active'},
                        {'name': 'Bosch', 'hiring_status': 'Very Active'},
                        {'name': 'BASF', 'hiring_status': 'Active'}
                    ]
                }
            }
        }
        
        return market_data.get(country, {}).get(industry, {})
    
    def get_salary_comparison(self, industry, experience):
        """Get salary comparison data across countries"""
        salary_data = {
            'Technology': {
                'USA': 120000 + (experience * 8000),
                'Germany': 65000 + (experience * 5000),
                'UK': 70000 + (experience * 6000),
                'Canada': 80000 + (experience * 5500),
                'Australia': 85000 + (experience * 6000),
                'Netherlands': 60000 + (experience * 4500)
            },
            'Finance': {
                'USA': 110000 + (experience * 10000),
                'Germany': 60000 + (experience * 6000),
                'UK': 75000 + (experience * 8000),
                'Canada': 70000 + (experience * 7000),
                'Australia': 80000 + (experience * 7500),
                'Switzerland': 100000 + (experience * 9000)
            },
            'Healthcare': {
                'USA': 130000 + (experience * 7000),
                'Germany': 70000 + (experience * 5000),
                'UK': 60000 + (experience * 4000),
                'Canada': 90000 + (experience * 6000),
                'Australia': 95000 + (experience * 6500),
                'Sweden': 55000 + (experience * 4000)
            }
        }
        
        return salary_data.get(industry, {})