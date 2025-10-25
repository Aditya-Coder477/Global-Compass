# pages/6_💰_Financial_Tools.py
import streamlit as st
import sys
import os
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
# Add these imports to each dashboard file
import pandas as pd
from datetime import datetime, timedelta
import random
from modules.api_services import api_services


# Add modules to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from modules.financial_tools import financial_tools
from modules.api_services import api_services
from modules.auth import Authentication

# Page configuration
st.set_page_config(
    page_title="Financial Tools - Global Compass",
    page_icon="💰",
    layout="wide"
)

# Initialize components
auth = Authentication()

def main():
    # Check authentication
    if not auth.is_authenticated():
        st.warning("Please log in to access the Financial Tools")
        st.stop()
    
    st.title("💰 Financial Planning Tools")
    st.markdown("Comprehensive financial calculators for your international journey")
    
    # Sidebar navigation
    st.sidebar.header("Financial Tools")
    tool_selection = st.sidebar.selectbox(
        "Choose a Tool",
        [
            #"💱 Currency & Cost of Living",
            "🧾 Tax Calculator", 
            "📈 Investment Planning",
            "🏖️ Retirement Planning",
            "🛡️ Insurance Analysis",
            "🎯 Savings Goals"
        ]
    )
    
    #if tool_selection == "💱 Currency & Cost of Living":
      #  show_currency_col_tools()
    if tool_selection == "🧾 Tax Calculator":
        show_tax_calculator()
    elif tool_selection == "📈 Investment Planning":
        show_investment_planning()
    elif tool_selection == "🏖️ Retirement Planning":
        show_retirement_planning()
    elif tool_selection == "🛡️ Insurance Analysis":
        show_insurance_analysis()
    elif tool_selection == "🎯 Savings Goals":
        show_savings_goals()

def show_currency_col_tools():
    """Currency converter and cost of living comparison"""
    st.header("💱 Currency & Cost of Living Tools")
    
    # Real-time currency dashboard
    st.subheader("💱 Live Currency Exchange Rates")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Real-time Currency Converter")
        
        amount = st.number_input("Amount", min_value=1.0, value=1000.0, step=100.0)
        from_currency = st.selectbox("From Currency", ['USD', 'EUR', 'GBP', 'CAD', 'AUD', 'JPY', 'CHF'])
        to_currency = st.selectbox("To Currency", ['EUR', 'USD', 'GBP', 'CAD', 'AUD', 'JPY', 'CHF'])
        
        if st.button("Convert Currency", type="primary"):
            converted_amount = api_services.convert_currency(amount, from_currency, to_currency)
            # Get rate for display (you might need to add a helper method for this)
            #rates_data = api_services.get_currency_rates(from_currency)
            #rate = rates_data['rates'].get(to_currency, {}).get('rate', 0)
            #source = rates_data.get('source', 'Unknown')
            st.success(f"**{amount:,.2f} {from_currency} = {converted_amount:,.2f} {to_currency}**")
            #st.caption(f"Exchange rate: 1 {from_currency} = {rate:.4f} {to_currency}")
            #st.caption(f"Source: {source}")
        
        # Show current rates
        st.subheader("📊 Current Exchange Rates")
        rates_data = api_services.get_currency_rates('USD')
        
        if rates_data['success']:
            rates = rates_data['rates']
            rates_df = pd.DataFrame(list(rates.items()), columns=['Currency', 'Rate'])
            
            fig = px.bar(rates_df, x='Currency', y='Rate', 
                        title='USD Exchange Rates', color='Rate')
            st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("🏙️ Cost of Living Comparison")
        
        col1, col2 = st.columns(2)
        with col1:
            current_city = st.selectbox("Current City", list(financial_tools.cost_of_living_data.keys()))
            current_salary = st.number_input("Current Annual Salary ($)", min_value=10000, value=60000, step=5000)
        
        with col2:
            target_city = st.selectbox("Target City", list(financial_tools.cost_of_living_data.keys()))
        
        if st.button("Compare Cost of Living", type="primary"):
            comparison = financial_tools.compare_cost_of_living(current_city, target_city, current_salary)
            
            if comparison:
                st.info(f"**Equivalent Salary in {target_city}: ${comparison['equivalent_salary']:,.2f}**")
                
                # Display comparison metrics
                metric_col1, metric_col2, metric_col3 = st.columns(3)
                
                with metric_col1:
                    st.metric("Cost of Living Ratio", f"{comparison['col_ratio']:.2f}x")
                    st.metric("Monthly COL Current", f"${comparison['current_monthly_col']:,.0f}")
                
                with metric_col2:
                    st.metric("Monthly COL Target", f"${comparison['target_monthly_col']:,.0f}")
                    st.metric("Annual Savings Current", f"${comparison['current_annual_savings']:,.0f}")
                
                with metric_col3:
                    st.metric("Annual Savings Target", f"${comparison['target_annual_savings']:,.0f}")
                    savings_diff = comparison['savings_difference']
                    st.metric("Savings Difference", 
                             f"${abs(savings_diff):,.0f}",
                             delta=f"{'More' if savings_diff > 0 else 'Less'} savings")
                
                # Detailed breakdown
                st.subheader("Detailed Cost Breakdown")
                current_details = comparison['detailed_comparison']['current']
                target_details = comparison['detailed_comparison']['target']
                
                breakdown_df = pd.DataFrame({
                    'Expense': ['Rent (1bed)', 'Utilities', 'Groceries', 'Transport', 'Total'],
                    current_city: [current_details['rent_1bed'], current_details['utilities'], 
                                 current_details['groceries'], current_details['transport'], current_details['total']],
                    target_city: [target_details['rent_1bed'], target_details['utilities'], 
                                target_details['groceries'], target_details['transport'], target_details['total']]
                })
                
                st.dataframe(breakdown_df, use_container_width=True)

def show_tax_calculator():
    """Income tax calculator for different countries"""
    st.header("🧾 International Tax Calculator")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("Tax Calculation")
        
        selected_countries = st.multiselect(
            "Select Countries to Compare",
            list(financial_tools.tax_brackets.keys()),
            default=['USA', 'UK', 'Germany', 'Canada']
        )
        
        annual_income = st.slider("Annual Income ($)", 10000, 500000, 75000, 5000)
        filing_status = st.selectbox("Filing Status", ['Single', 'Married', 'Head of Household'])
        
        if st.button("Calculate Taxes", type="primary"):
            if selected_countries:
                results = {}
                for country in selected_countries:
                    results[country] = financial_tools.calculate_income_tax(country, annual_income)
                
                # Display results
                st.subheader("Tax Comparison Results")
                
                # Create comparison table
                comparison_data = []
                for country, tax_data in results.items():
                    comparison_data.append({
                        'Country': country,
                        'Gross Income': f"${tax_data['gross_income']:,.0f}",
                        'Total Tax': f"${tax_data['total_tax']:,.0f}",
                        'Net Income': f"${tax_data['net_income']:,.0f}",
                        'Effective Tax Rate': f"{tax_data['effective_tax_rate']:.1%}",
                        'Monthly Net': f"${tax_data['monthly_net']:,.0f}"
                    })
                
                comparison_df = pd.DataFrame(comparison_data)
                st.dataframe(comparison_df, use_container_width=True)
                
                # Visualization
                st.subheader("Tax Burden Comparison")
                
                countries = list(results.keys())
                tax_rates = [results[country]['effective_tax_rate'] for country in countries]
                net_incomes = [results[country]['net_income'] for country in countries]
                
                fig = go.Figure()
                fig.add_trace(go.Bar(name='Effective Tax Rate', x=countries, y=tax_rates, 
                                    text=[f'{rate:.1%}' for rate in tax_rates], textposition='auto'))
                fig.update_layout(title='Effective Tax Rates by Country', yaxis_tickformat='.0%')
                st.plotly_chart(fig, use_container_width=True)
                
                fig2 = go.Figure()
                fig2.add_trace(go.Bar(name='Net Income', x=countries, y=net_incomes,
                                     text=[f'${income:,.0f}' for income in net_incomes], textposition='auto'))
                fig2.update_layout(title='Net Income After Tax by Country')
                st.plotly_chart(fig2, use_container_width=True)
    
    with col2:
        st.subheader("💡 Tax Tips")
        st.info("""
        **Tax Optimization Tips:**
        - Consider countries with territorial tax systems
        - Look for tax treaties between countries
        - Explore tax credits for foreign income
        - Consult with international tax professionals
        """)
        
        st.warning("""
        **Disclaimer:**
        This calculator provides estimates only. 
        Actual tax liability may vary based on specific circumstances.
        Always consult with a qualified tax professional.
        """)

def show_investment_planning():
    """Investment growth calculator"""
    st.header("📈 Investment Planning")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Investment Calculator")
        
        initial_investment = st.number_input("Initial Investment ($)", min_value=0, value=10000, step=1000)
        monthly_contribution = st.number_input("Monthly Contribution ($)", min_value=0, value=500, step=50)
        investment_years = st.slider("Investment Period (Years)", 1, 40, 20)
        expected_return = st.slider("Expected Annual Return (%)", 1.0, 15.0, 7.0, 0.5) / 100
        
        if st.button("Calculate Investment Growth", type="primary"):
            # Single strategy calculation
            result = financial_tools.calculate_investment_growth(
                initial_investment, monthly_contribution, investment_years, expected_return
            )
            
            st.success(f"**Projected Value: ${result['total_value']:,.2f}**")
            
            # Display key metrics
            metric_col1, metric_col2, metric_col3 = st.columns(3)
            with metric_col1:
                st.metric("Total Contributions", f"${result['total_contributions']:,.0f}")
            with metric_col2:
                st.metric("Total Earnings", f"${result['total_earnings']:,.0f}")
            with metric_col3:
                st.metric("Return on Investment", f"{(result['total_earnings']/result['total_contributions'])*100:.1f}%")
            
            # Yearly breakdown chart
            yearly_data = result['yearly_breakdown']
            years = [data['year'] for data in yearly_data]
            values = [data['value'] for data in yearly_data]
            contributions = [data['contributions'] for data in yearly_data]
            
            fig = go.Figure()
            fig.add_trace(go.Scatter(name='Portfolio Value', x=years, y=values, fill='tozeroy'))
            fig.add_trace(go.Scatter(name='Total Contributions', x=years, y=contributions, line=dict(dash='dash')))
            fig.update_layout(title='Investment Growth Over Time', xaxis_title='Years', yaxis_title='Value ($)')
            st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("Strategy Comparison")
        
        if st.button("Compare Strategies", type="secondary"):
            strategies = financial_tools.compare_investment_strategies(
                initial_investment, monthly_contribution, investment_years
            )
            
            strategy_data = []
            for strategy_name, strategy_result in strategies.items():
                strategy_data.append({
                    'Strategy': strategy_name,
                    'Final Value': f"${strategy_result['total_value']:,.0f}",
                    'Total Contributions': f"${strategy_result['total_contributions']:,.0f}",
                    'Total Earnings': f"${strategy_result['total_earnings']:,.0f}"
                })
            
            strategy_df = pd.DataFrame(strategy_data)
            st.dataframe(strategy_df, use_container_width=True)
            
            # Strategy comparison chart
            strategy_names = list(strategies.keys())
            final_values = [strategies[name]['total_value'] for name in strategy_names]
            
            fig = px.bar(x=strategy_names, y=final_values, 
                        title='Final Portfolio Value by Strategy',
                        labels={'x': 'Investment Strategy', 'y': 'Final Value ($)'})
            st.plotly_chart(fig, use_container_width=True)
        
        st.subheader("💡 Investment Tips")
        st.info("""
        **Smart Investing:**
        - Start early to benefit from compound growth
        - Diversify across asset classes
        - Consider low-cost index funds
        - Rebalance portfolio annually
        - Stay invested during market fluctuations
        """)

# ... (Similar implementations for other financial tools would follow)

def show_retirement_planning():
    """Retirement planning calculator"""
    st.header("🏖️ Retirement Planning")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Retirement Needs Calculator")
        
        current_age = st.slider("Current Age", 20, 65, 30)
        retirement_age = st.slider("Planned Retirement Age", current_age + 1, 75, 65)
        current_savings = st.number_input("Current Retirement Savings ($)", min_value=0, value=50000, step=5000)
        desired_income = st.number_input("Desired Retirement Income ($/year)", min_value=10000, value=60000, step=5000)
        
        if st.button("Calculate Retirement Plan", type="primary"):
            plan = financial_tools.calculate_retirement_needs(
                current_age, retirement_age, current_savings, desired_income
            )
            
            st.success(f"**Total Retirement Fund Needed: ${plan['total_retirement_needed']:,.2f}**")
            
            # Display retirement metrics
            metric_col1, metric_col2, metric_col3 = st.columns(3)
            with metric_col1:
                st.metric("Working Years Remaining", plan['working_years'])
                st.metric("Monthly Savings Needed", f"${plan['monthly_savings_needed']:,.0f}")
            with metric_col2:
                st.metric("Retirement Years", plan['retirement_years'])
                st.metric("Future Current Savings", f"${plan['future_current_savings']:,.0f}")
            with metric_col3:
                st.metric("Inflation Adjusted Income", f"${plan['inflation_adjusted_income']:,.0f}")
            
            # Retirement readiness
            readiness_score = financial_tools.retirement_readiness_score(
                current_savings, plan['total_retirement_needed'], plan['working_years']
            )
            
            st.subheader(f"Retirement Readiness Score: {readiness_score}/100")
            
            if readiness_score >= 80:
                st.success("🎉 Excellent! You're on track for retirement.")
            elif readiness_score >= 60:
                st.warning("📊 Good progress, but consider increasing savings.")
            else:
                st.error("⚠️ Needs attention. Consider adjusting your retirement plan.")
    
    with col2:
        st.subheader("Retirement Tips")
        st.info("""
        **Retirement Planning Strategies:**
        - Maximize employer retirement contributions
        - Consider Roth options for tax-free growth
        - Plan for healthcare costs in retirement
        - Consider part-time work in early retirement
        - Review and adjust plan annually
        """)

def show_insurance_analysis():
    """Insurance cost analysis"""
    st.header("🛡️ Insurance Cost Analysis")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Insurance Cost Calculator")
        
        country = st.selectbox("Country", list(financial_tools.insurance_data.keys()))
        age = st.slider("Age", 18, 80, 35)
        coverage_level = st.selectbox("Coverage Level", ['basic', 'standard', 'premium'])
        
        if st.button("Calculate Insurance Costs", type="primary"):
            insurance_costs = financial_tools.calculate_insurance_costs(country, age, coverage_level)
            
            st.subheader(f"Monthly Insurance Costs for {country}")
            
            # Display insurance costs
            for insurance_type, cost in insurance_costs['monthly_costs'].items():
                st.metric(insurance_type.title(), f"${cost}")
            
            st.metric("Total Monthly", f"${insurance_costs['total_monthly']}")
            st.metric("Total Annual", f"${insurance_costs['total_annual']}")
            
            # Insurance cost breakdown chart
            insurance_types = list(insurance_costs['monthly_costs'].keys())
            costs = list(insurance_costs['monthly_costs'].values())
            
            fig = px.pie(values=costs, names=insurance_types, 
                        title='Monthly Insurance Cost Breakdown')
            st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("Insurance Comparison")
        
        compare_countries = st.multiselect(
            "Compare Countries",
            list(financial_tools.insurance_data.keys()),
            default=['USA', 'UK', 'Germany']
        )
        
        if st.button("Compare Insurance Costs", type="secondary"):
            comparison_data = []
            for country in compare_countries:
                costs = financial_tools.calculate_insurance_costs(country, age, coverage_level)
                comparison_data.append({
                    'Country': country,
                    'Health Insurance': costs['monthly_costs']['health'],
                    'Car Insurance': costs['monthly_costs']['car'],
                    'Renters Insurance': costs['monthly_costs']['renters'],
                    'Life Insurance': costs['monthly_costs']['life'],
                    'Total Monthly': costs['total_monthly']
                })
            
            comparison_df = pd.DataFrame(comparison_data)
            st.dataframe(comparison_df, use_container_width=True)

def show_savings_goals():
    """Savings goal tracking"""
    st.header("🎯 Savings Goals Tracker")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Single Goal Calculator")
        
        goal_name = st.text_input("Goal Name", "New Car")
        goal_amount = st.number_input("Goal Amount ($)", min_value=100, value=25000, step=1000)
        current_savings = st.number_input("Current Savings ($)", min_value=0, value=5000, step=500)
        timeframe = st.slider("Timeframe (Months)", 1, 120, 24)
        monthly_contribution = st.number_input("Monthly Contribution ($)", min_value=0, value=500, step=50)
        
        if st.button("Analyze Goal", type="primary"):
            goal_analysis = financial_tools.calculate_savings_goal(
                goal_amount, current_savings, timeframe, monthly_contribution
            )
            
            if goal_analysis['goal_achievable']:
                st.success(f"✅ You will achieve your {goal_name} goal!")
                st.metric("Projected Savings", f"${goal_analysis['projected_savings']:,.0f}")
            else:
                st.warning(f"⚠️ You'll be ${goal_analysis['shortfall']:,.0f} short of your goal")
                st.metric("Additional Monthly Needed", f"${goal_analysis['monthly_needed']:,.0f}")
    
    with col2:
        st.subheader("Multiple Goals Planner")
        st.info("""
        **Create a comprehensive savings plan:**
        1. List all your financial goals
        2. Set target amounts and timeframes  
        3. Prioritize by importance
        4. Allocate monthly savings
        """)
        
        # Example multiple goals
        example_goals = {
            'Emergency Fund': {'amount': 15000, 'timeframe_months': 12, 'priority': 'high'},
            'Down Payment': {'amount': 50000, 'timeframe_months': 36, 'priority': 'medium'},
            'Vacation': {'amount': 5000, 'timeframe_months': 6, 'priority': 'low'}
        }
        
        available_monthly = st.number_input("Available Monthly Savings ($)", min_value=100, value=1500, step=100)
        
        if st.button("Create Savings Plan", type="secondary"):
            plan = financial_tools.create_savings_plan(example_goals)
            
            st.subheader("Savings Plan Summary")
            for goal, details in plan['goal_plans'].items():
                st.write(f"**{goal}**: ${details['monthly_needed']:,.0f}/month")
            
            st.metric("Total Monthly Needed", f"${plan['total_monthly_needed']:,.0f}")
            st.metric("Feasibility", plan['feasibility'])
            
    

if __name__ == "__main__":
    main()