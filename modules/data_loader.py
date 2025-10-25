# modules/data_loader.py
import pandas as pd
import numpy as np
import os

class DataLoader:
    def __init__(self):
        self.data_path = "data/sample_data"
    
    def load_student_data(self):
        """Load or generate student data"""
        file_path = os.path.join(self.data_path, "student_data.csv")
        
        if os.path.exists(file_path):
            return pd.read_csv(file_path)
        else:
            return self.generate_student_data()
    
    def load_tourist_data(self):
        """Load or generate tourist data"""
        file_path = os.path.join(self.data_path, "tourist_data.csv")
        
        if os.path.exists(file_path):
            return pd.read_csv(file_path)
        else:
            return self.generate_tourist_data()
    
    def load_professional_data(self):
        """Load or generate professional data"""
        file_path = os.path.join(self.data_path, "professional_data.csv")
        
        if os.path.exists(file_path):
            return pd.read_csv(file_path)
        else:
            return self.generate_professional_data()
    
    def generate_student_data(self):
        """Generate sample student data"""
        np.random.seed(42)
        n_samples = 1000
        
        data = {
            'academic_score': np.random.randint(60, 100, n_samples),
            'budget': np.random.randint(10000, 50000, n_samples),
            'preferred_major': np.random.choice(
                ['Computer Science', 'Business', 'Engineering', 'Arts', 'Medicine', 'Law', 'Social Sciences'], 
                n_samples
            ),
            'language_preference': np.random.choice(
                ['English', 'French', 'German', 'Spanish', 'Chinese', 'Japanese', 'Korean'], 
                n_samples
            ),
            'degree_level': np.random.choice(['Bachelor', 'Master', 'PhD', 'Diploma'], n_samples),
            'country': np.random.choice(
                ['USA', 'UK', 'Canada', 'Australia', 'Germany', 'France', 'Japan', 'Netherlands', 'Sweden'], 
                n_samples
            )
        }
        
        df = pd.DataFrame(data)
        os.makedirs(self.data_path, exist_ok=True)
        df.to_csv(os.path.join(self.data_path, "student_data.csv"), index=False)
        return df
    
    def generate_tourist_data(self):
        """Generate sample tourist data"""
        np.random.seed(42)
        n_samples = 1000
        
        data = {
            'budget': np.random.randint(1000, 10000, n_samples),
            'travel_style': np.random.choice(
                ['Adventure', 'Cultural', 'Relaxation', 'Food', 'Historical', 'Beach', 'City Break'], 
                n_samples
            ),
            'climate_preference': np.random.choice(
                ['Tropical', 'Temperate', 'Cold', 'Mediterranean', 'Desert', 'Mountain'], 
                n_samples
            ),
            'duration': np.random.randint(3, 30, n_samples),
            'travel_companions': np.random.choice(
                ['Solo', 'Couple', 'Family', 'Friends', 'Business'], 
                n_samples
            ),
            'season': np.random.choice(['Spring', 'Summer', 'Fall', 'Winter', 'Any'], n_samples),
            'destination': np.random.choice(
                ['Italy', 'Japan', 'Thailand', 'USA', 'France', 'Spain', 'Greece', 'Brazil', 'Australia'], 
                n_samples
            )
        }
        
        df = pd.DataFrame(data)
        os.makedirs(self.data_path, exist_ok=True)
        df.to_csv(os.path.join(self.data_path, "tourist_data.csv"), index=False)
        return df
    
    def generate_professional_data(self):
        """Generate sample professional data"""
        np.random.seed(42)
        n_samples = 1000
        
        data = {
            'experience_years': np.random.randint(0, 30, n_samples),
            'education_level': np.random.choice(
                ['High School', 'Bachelor', 'Master', 'PhD', 'Diploma/Certificate'], 
                n_samples
            ),
            'industry': np.random.choice(
                ['Technology', 'Finance', 'Healthcare', 'Education', 'Engineering', 
                 'Marketing', 'Sales', 'Design', 'Consulting', 'Manufacturing'], 
                n_samples
            ),
            'salary_expectation': np.random.randint(30000, 200000, n_samples),
            'job_type': np.random.choice(
                ['Full-time', 'Contract', 'Remote', 'Freelance', 'Startup'], 
                n_samples
            ),
            'relocation_timeline': np.random.choice(
                ['Immediately', '3-6 months', '6-12 months', '1-2 years', 'Exploring options'], 
                n_samples
            ),
            'country': np.random.choice(
                ['USA', 'Germany', 'UK', 'Canada', 'Australia', 'Switzerland', 'Singapore', 'Netherlands', 'UAE'], 
                n_samples
            )
        }
        
        df = pd.DataFrame(data)
        os.makedirs(self.data_path, exist_ok=True)
        df.to_csv(os.path.join(self.data_path, "professional_data.csv"), index=False)
        return df
