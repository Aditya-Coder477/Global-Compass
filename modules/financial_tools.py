# modules/financial_tools.py
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
from modules.api_services import api_services

class FinancialTools:
    """Comprehensive financial planning and analysis tools"""
    
    def __init__(self):
        self.cost_of_living_data = self._load_cost_of_living_data()
        self.tax_brackets = self._load_tax_brackets()
        self.insurance_data = self._load_insurance_data()
    
    def _load_cost_of_living_data(self):
        """Load cost of living data for major cities"""
        return {
            'New York': {'rent_1bed': 3200, 'utilities': 150, 'groceries': 400, 'transport': 127, 'total': 4500},
            'London': {'rent_1bed': 1800, 'utilities': 160, 'groceries': 300, 'transport': 150, 'total': 2800},
            'Tokyo': {'rent_1bed': 1100, 'utilities': 150, 'groceries': 350, 'transport': 70, 'total': 2000},
            'Berlin': {'rent_1bed': 900, 'utilities': 120, 'groceries': 250, 'transport': 80, 'total': 1600},
            'Sydney': {'rent_1bed': 1600, 'utilities': 140, 'groceries': 350, 'transport': 110, 'total': 2500},
            'Toronto': {'rent_1bed': 1500, 'utilities': 120, 'groceries': 300, 'transport': 100, 'total': 2200},
            'Singapore': {'rent_1bed': 1800, 'utilities': 100, 'groceries': 350, 'transport': 80, 'total': 2600},
            'Dubai': {'rent_1bed': 1400, 'utilities': 120, 'groceries': 300, 'transport': 90, 'total': 2100}
        }
    
    def _load_tax_brackets(self):
        """Load tax brackets for different countries"""
        return {
            'USA': [
                {'min': 0, 'max': 11000, 'rate': 0.10},
                {'min': 11001, 'max': 44725, 'rate': 0.12},
                {'min': 44726, 'max': 95375, 'rate': 0.22},
                {'min': 95376, 'max': 182100, 'rate': 0.24},
                {'min': 182101, 'max': 231250, 'rate': 0.32},
                {'min': 231251, 'max': 578125, 'rate': 0.35},
                {'min': 578126, 'max': float('inf'), 'rate': 0.37}
            ],
            'UK': [
                {'min': 0, 'max': 12570, 'rate': 0.0},
                {'min': 12571, 'max': 50270, 'rate': 0.20},
                {'min': 50271, 'max': 125140, 'rate': 0.40},
                {'min': 125141, 'max': float('inf'), 'rate': 0.45}
            ],
            'Germany': [
                {'min': 0, 'max': 10908, 'rate': 0.0},
                {'min': 10909, 'max': 62809, 'rate': 0.14},
                {'min': 62810, 'max': 277825, 'rate': 0.42},
                {'min': 277826, 'max': float('inf'), 'rate': 0.45}
            ],
            'Canada': [
                {'min': 0, 'max': 53359, 'rate': 0.15},
                {'min': 53360, 'max': 106717, 'rate': 0.205},
                {'min': 106718, 'max': 165430, 'rate': 0.26},
                {'min': 165431, 'max': 235675, 'rate': 0.29},
                {'min': 235676, 'max': float('inf'), 'rate': 0.33}
            ],
            'Australia': [
                {'min': 0, 'max': 18200, 'rate': 0.0},
                {'min': 18201, 'max': 45000, 'rate': 0.19},
                {'min': 45001, 'max': 120000, 'rate': 0.325},
                {'min': 120001, 'max': 180000, 'rate': 0.37},
                {'min': 180001, 'max': float('inf'), 'rate': 0.45}
            ]
        }
    
    def _load_insurance_data(self):
        """Load average insurance costs by country"""
        return {
            'USA': {'health': 450, 'car': 150, 'renters': 20, 'life': 30},
            'UK': {'health': 200, 'car': 80, 'renters': 15, 'life': 25},
            'Germany': {'health': 400, 'car': 70, 'renters': 12, 'life': 20},
            'Canada': {'health': 150, 'car': 100, 'renters': 18, 'life': 28},
            'Australia': {'health': 180, 'car': 90, 'renters': 16, 'life': 22},
            'Japan': {'health': 250, 'car': 60, 'renters': 10, 'life': 18}
        }
    
    # ===== TAX CALCULATORS =====
    def calculate_income_tax(self, country, annual_income, filing_status='single'):
        """Calculate income tax for a specific country"""
        if country not in self.tax_brackets:
            return self._estimate_tax(annual_income)
        
        brackets = self.tax_brackets[country]
        tax = 0
        remaining_income = annual_income
        
        for bracket in brackets:
            if remaining_income <= 0:
                break
            
            bracket_range = bracket['max'] - bracket['min'] + 1
            taxable_in_bracket = min(remaining_income, bracket_range)
            
            if taxable_in_bracket > 0:
                tax += taxable_in_bracket * bracket['rate']
                remaining_income -= taxable_in_bracket
        
        # Calculate effective tax rate
        effective_rate = tax / annual_income if annual_income > 0 else 0
        
        return {
            'gross_income': annual_income,
            'total_tax': round(tax, 2),
            'net_income': round(annual_income - tax, 2),
            'effective_tax_rate': round(effective_rate, 4),
            'monthly_net': round((annual_income - tax) / 12, 2)
        }
    
    def _estimate_tax(self, annual_income):
        """Estimate tax for countries without specific brackets"""
        # Simple progressive estimation
        if annual_income <= 30000:
            tax_rate = 0.15
        elif annual_income <= 70000:
            tax_rate = 0.25
        elif annual_income <= 120000:
            tax_rate = 0.35
        else:
            tax_rate = 0.45
        
        tax = annual_income * tax_rate
        
        return {
            'gross_income': annual_income,
            'total_tax': round(tax, 2),
            'net_income': round(annual_income - tax, 2),
            'effective_tax_rate': tax_rate,
            'monthly_net': round((annual_income - tax) / 12, 2)
        }
    
    def compare_taxes_across_countries(self, annual_income):
        """Compare tax burden across different countries"""
        comparison = {}
        
        for country in self.tax_brackets.keys():
            tax_data = self.calculate_income_tax(country, annual_income)
            comparison[country] = tax_data
        
        return comparison
    
    # ===== INVESTMENT PLANNING =====
    def calculate_investment_growth(self, initial_investment, monthly_contribution, years, expected_return=0.07):
        """Calculate compound investment growth"""
        monthly_rate = expected_return / 12
        months = years * 12
        
        # Future value of initial investment
        future_value_initial = initial_investment * (1 + expected_return) ** years
        
        # Future value of monthly contributions
        future_value_contributions = monthly_contribution * (((1 + monthly_rate) ** months - 1) / monthly_rate)
        
        total_value = future_value_initial + future_value_contributions
        total_contributions = initial_investment + (monthly_contribution * months)
        total_earnings = total_value - total_contributions
        
        # Year-by-year breakdown
        yearly_breakdown = []
        current_value = initial_investment
        
        for year in range(1, years + 1):
            # Add monthly contributions for the year
            for month in range(12):
                current_value = current_value * (1 + monthly_rate) + monthly_contribution
            
            yearly_breakdown.append({
                'year': year,
                'value': round(current_value, 2),
                'contributions': initial_investment + (monthly_contribution * year * 12),
                'earnings': round(current_value - (initial_investment + (monthly_contribution * year * 12)), 2)
            })
        
        return {
            'total_value': round(total_value, 2),
            'total_contributions': round(total_contributions, 2),
            'total_earnings': round(total_earnings, 2),
            'yearly_breakdown': yearly_breakdown,
            'expected_return': expected_return
        }
    
    def compare_investment_strategies(self, initial_investment, monthly_contribution, years):
        """Compare different investment return scenarios"""
        strategies = {
            'Conservative (4%)': 0.04,
            'Moderate (7%)': 0.07,
            'Aggressive (10%)': 0.10
        }
        
        results = {}
        for strategy_name, return_rate in strategies.items():
            results[strategy_name] = self.calculate_investment_growth(
                initial_investment, monthly_contribution, years, return_rate
            )
        
        return results
    
    # ===== RETIREMENT PLANNING =====
    def calculate_retirement_needs(self, current_age, retirement_age, current_savings, 
                                 desired_retirement_income, life_expectancy=85):
        """Calculate retirement savings needs"""
        retirement_years = life_expectancy - retirement_age
        working_years = retirement_age - current_age
        
        # Adjust for inflation (3% average)
        inflation_adjusted_income = desired_retirement_income * (1.03 ** working_years)
        
        # Calculate total retirement fund needed (4% withdrawal rule)
        total_needed = (inflation_adjusted_income * retirement_years) / 0.04
        
        # Calculate required monthly savings
        expected_return = 0.07  # 7% average market return
        monthly_return = expected_return / 12
        months_to_save = working_years * 12
        
        # Future value of current savings
        future_current_savings = current_savings * (1 + expected_return) ** working_years
        
        # Additional savings needed
        additional_needed = total_needed - future_current_savings
        
        if additional_needed <= 0:
            monthly_savings_needed = 0
        else:
            monthly_savings_needed = additional_needed * (monthly_return / ((1 + monthly_return) ** months_to_save - 1))
        
        return {
            'current_age': current_age,
            'retirement_age': retirement_age,
            'working_years': working_years,
            'retirement_years': retirement_years,
            'total_retirement_needed': round(total_needed, 2),
            'future_current_savings': round(future_current_savings, 2),
            'monthly_savings_needed': round(monthly_savings_needed, 2),
            'inflation_adjusted_income': round(inflation_adjusted_income, 2)
        }
    
    def retirement_readiness_score(self, current_savings, target_savings, years_to_retirement):
        """Calculate retirement readiness score"""
        if years_to_retirement <= 0:
            return 100 if current_savings >= target_savings else 0
        
        annual_savings_needed = (target_savings - current_savings) / years_to_retirement
        current_annual_savings = current_savings / years_to_retirement  # Simplified
        
        if current_annual_savings >= annual_savings_needed:
            score = 100
        else:
            score = max(0, min(100, (current_annual_savings / annual_savings_needed) * 100))
        
        return round(score, 1)
    
    # ===== INSURANCE COST ANALYSIS =====
    def calculate_insurance_costs(self, country, age, coverage_level='standard'):
        """Calculate estimated insurance costs"""
        if country not in self.insurance_data:
            return self._estimate_insurance_costs(age)
        
        base_costs = self.insurance_data[country]
        
        # Adjust for age
        age_multiplier = 1.0
        if age < 25:
            age_multiplier = 1.5
        elif age > 60:
            age_multiplier = 1.8
        
        # Adjust for coverage level
        coverage_multiplier = {
            'basic': 0.7,
            'standard': 1.0,
            'premium': 1.5
        }.get(coverage_level, 1.0)
        
        adjusted_costs = {}
        for insurance_type, base_cost in base_costs.items():
            adjusted_costs[insurance_type] = round(base_cost * age_multiplier * coverage_multiplier, 2)
        
        total_monthly = sum(adjusted_costs.values())
        
        return {
            'country': country,
            'age': age,
            'coverage_level': coverage_level,
            'monthly_costs': adjusted_costs,
            'total_monthly': total_monthly,
            'total_annual': round(total_monthly * 12, 2)
        }
    
    def _estimate_insurance_costs(self, age):
        """Estimate insurance costs for countries without specific data"""
        base_health = 300
        base_car = 100
        base_renters = 15
        base_life = 25
        
        # Age adjustments
        if age < 25:
            multiplier = 1.5
        elif age > 60:
            multiplier = 1.8
        else:
            multiplier = 1.0
        
        costs = {
            'health': round(base_health * multiplier, 2),
            'car': round(base_car * multiplier, 2),
            'renters': round(base_renters * multiplier, 2),
            'life': round(base_life * multiplier, 2)
        }
        
        total_monthly = sum(costs.values())
        
        return {
            'country': 'International Average',
            'age': age,
            'coverage_level': 'standard',
            'monthly_costs': costs,
            'total_monthly': total_monthly,
            'total_annual': round(total_monthly * 12, 2)
        }
    
    # ===== COST OF LIVING COMPARISONS =====
    def compare_cost_of_living(self, current_city, target_city, current_salary):
        """Compare cost of living between cities"""
        if current_city not in self.cost_of_living_data or target_city not in self.cost_of_living_data:
            return None
        
        current_col = self.cost_of_living_data[current_city]
        target_col = self.cost_of_living_data[target_city]
        
        # Calculate equivalent salary
        col_ratio = target_col['total'] / current_col['total']
        equivalent_salary = current_salary * col_ratio
        
        # Calculate savings potential
        current_savings = current_salary - current_col['total'] * 12
        target_savings = equivalent_salary - target_col['total'] * 12
        
        return {
            'current_city': current_city,
            'target_city': target_city,
            'current_salary': current_salary,
            'equivalent_salary': round(equivalent_salary, 2),
            'col_ratio': round(col_ratio, 2),
            'current_monthly_col': current_col['total'],
            'target_monthly_col': target_col['total'],
            'current_annual_savings': round(current_savings, 2),
            'target_annual_savings': round(target_savings, 2),
            'savings_difference': round(target_savings - current_savings, 2),
            'detailed_comparison': {
                'current': current_col,
                'target': target_col
            }
        }
    
    def get_cost_of_living_breakdown(self, city):
        """Get detailed cost of living breakdown for a city"""
        if city in self.cost_of_living_data:
            return self.cost_of_living_data[city]
        return None
    
    # ===== SAVINGS GOAL TRACKING =====
    def calculate_savings_goal(self, goal_amount, current_savings, timeframe_months, monthly_contribution):
        """Calculate if savings goal is achievable"""
        # Simple calculation without interest for simplicity
        total_future_savings = current_savings + (monthly_contribution * timeframe_months)
        
        monthly_needed = (goal_amount - current_savings) / timeframe_months if timeframe_months > 0 else 0
        
        return {
            'goal_amount': goal_amount,
            'current_savings': current_savings,
            'timeframe_months': timeframe_months,
            'monthly_contribution': monthly_contribution,
            'projected_savings': total_future_savings,
            'goal_achievable': total_future_savings >= goal_amount,
            'shortfall': max(0, goal_amount - total_future_savings),
            'monthly_needed': monthly_needed if monthly_needed > 0 else 0
        }
    
    def create_savings_plan(self, goals):
        """Create a comprehensive savings plan for multiple goals"""
        total_monthly_needed = 0
        goal_plans = {}
        
        for goal_name, goal_details in goals.items():
            goal_amount = goal_details['amount']
            timeframe = goal_details['timeframe_months']
            priority = goal_details.get('priority', 'medium')
            
            monthly_needed = goal_amount / timeframe if timeframe > 0 else 0
            total_monthly_needed += monthly_needed
            
            goal_plans[goal_name] = {
                'monthly_needed': monthly_needed,
                'priority': priority,
                'timeframe': timeframe
            }
        
        return {
            'goal_plans': goal_plans,
            'total_monthly_needed': total_monthly_needed,
            'feasibility': 'Achievable' if total_monthly_needed <= goals.get('available_monthly', float('inf')) else 'Adjust Goals'
        }

# Global instance
financial_tools = FinancialTools()