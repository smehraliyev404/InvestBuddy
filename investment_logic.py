# Investment Logic Module for InvestBuddy
from typing import Dict, Tuple
from financial_api import get_stock_price

# Exchange rate (approximate)
AZN_TO_USD = 1.7  # 1 USD ≈ 1.7 AZN
USD_TO_AZN = 0.59  # 1 AZN ≈ 0.59 USD

# Safety thresholds
EMERGENCY_FUND_MONTHS = 3  # Minimum emergency fund in months of expenses
HIGH_DEBT_THRESHOLD = 0.3  # Debt > 30% of monthly income is concerning

# Risk profiles based on time horizon
RISK_PROFILES = {
    "conservative": {
        "stocks": 20,
        "bonds": 80,
        "description": "Very safe, minimal risk, lower returns"
    },
    "moderate": {
        "stocks": 60,
        "bonds": 40,
        "description": "Balanced risk and returns"
    },
    "aggressive": {
        "stocks": 80,
        "bonds": 20,
        "description": "Higher risk, higher potential returns"
    }
}

# Perform safety check before investing
def safety_check(
    salary: float,
    savings: float,
    monthly_expenses: float,
    debt: float
) -> Tuple[bool, str, Dict]:
    """
    Check if user is financially ready to invest
    Returns: (is_safe, message, recommendations)
    """

    # Calculate emergency fund requirement
    emergency_fund_needed = monthly_expenses * EMERGENCY_FUND_MONTHS

    # Calculate debt ratio
    debt_ratio = debt / salary if salary > 0 else 0

    recommendations = {
        "can_invest": True,
        "emergency_fund_needed": emergency_fund_needed,
        "current_savings": savings,
        "debt_ratio": debt_ratio,
        "priority_actions": []
    }

    # Check 1: High debt
    if debt_ratio > HIGH_DEBT_THRESHOLD:
        recommendations["can_invest"] = False
        recommendations["priority_actions"].append(
            f"⚠️ Pay down debt first. Your debt is {debt_ratio*100:.1f}% of monthly income."
        )
        recommendations["priority_actions"].append(
            f"💡 Focus on paying at least {debt * 0.1:.2f} AZN/month towards debt."
        )

    # Check 2: Insufficient emergency fund
    if savings < emergency_fund_needed:
        recommendations["can_invest"] = False
        gap = emergency_fund_needed - savings
        recommendations["priority_actions"].append(
            f"⚠️ Build emergency fund first. You need {gap:.2f} AZN more."
        )
        recommendations["priority_actions"].append(
            f"💡 Save {gap/6:.2f} AZN/month for 6 months to reach 3-month safety net."
        )

    # Check 3: Very low savings relative to expenses
    if savings < monthly_expenses and debt_ratio <= HIGH_DEBT_THRESHOLD:
        recommendations["priority_actions"].append(
            f"💡 Consider saving 1 more month of expenses before investing."
        )

    # Generate message
    if recommendations["can_invest"]:
        message = "✅ Great! You're financially ready to start investing."
    else:
        message = "⚠️ Hold on! Let's secure your finances first before investing."

    return recommendations["can_invest"], message, recommendations

# Determine risk profile based on time horizon
def determine_risk_profile(time_horizon_years: int) -> str:
    """
    Determine appropriate risk profile based on investment timeline
    """
    if time_horizon_years < 3:
        return "conservative"
    elif time_horizon_years < 7:
        return "moderate"
    else:
        return "aggressive"

# Calculate portfolio allocation
def calculate_portfolio(
    monthly_investment: float,
    time_horizon_years: int,
    goal: str = "general"
) -> Dict:
    """
    Calculate recommended portfolio allocation with real ETF prices
    """

    # Determine risk profile
    risk_profile = determine_risk_profile(time_horizon_years)
    allocation = RISK_PROFILES[risk_profile]

    # Calculate amounts
    monthly_investment_usd = monthly_investment * USD_TO_AZN
    stocks_amount_usd = monthly_investment_usd * (allocation["stocks"] / 100)
    bonds_amount_usd = monthly_investment_usd * (allocation["bonds"] / 100)

    # Get current ETF prices
    stock_etf = "SPY"  # S&P 500
    bond_etf = "BND"   # Bond ETF

    stock_price_data = get_stock_price(stock_etf)
    bond_price_data = get_stock_price(bond_etf)

    portfolio = {
        "risk_profile": risk_profile,
        "time_horizon_years": time_horizon_years,
        "monthly_investment_azn": monthly_investment,
        "monthly_investment_usd": round(monthly_investment_usd, 2),
        "allocations": []
    }

    # Stocks allocation
    if stocks_amount_usd > 0 and stock_price_data:
        shares = stocks_amount_usd / stock_price_data["price"]
        portfolio["allocations"].append({
            "asset_type": "Stocks",
            "etf": stock_etf,
            "etf_name": "S&P 500 ETF",
            "percentage": allocation["stocks"],
            "monthly_amount_usd": round(stocks_amount_usd, 2),
            "monthly_amount_azn": round(monthly_investment * (allocation["stocks"] / 100), 2),
            "current_price": stock_price_data["price"],
            "shares_per_month": round(shares, 4),
            "description": "Large US companies - Apple, Microsoft, Amazon, etc."
        })

    # Bonds allocation
    if bonds_amount_usd > 0 and bond_price_data:
        shares = bonds_amount_usd / bond_price_data["price"]
        portfolio["allocations"].append({
            "asset_type": "Bonds",
            "etf": bond_etf,
            "etf_name": "Total Bond Market ETF",
            "percentage": allocation["bonds"],
            "monthly_amount_usd": round(bonds_amount_usd, 2),
            "monthly_amount_azn": round(monthly_investment * (allocation["bonds"] / 100), 2),
            "current_price": bond_price_data["price"],
            "shares_per_month": round(shares, 4),
            "description": "Government and corporate bonds - stable and safe"
        })

    return portfolio

# Generate investment recommendation text
def generate_recommendation_text(
    portfolio: Dict,
    goal: str,
    salary: float,
    savings: float
) -> str:
    """
    Generate human-readable investment recommendation
    """

    risk_profile = portfolio["risk_profile"]
    time_horizon = portfolio["time_horizon_years"]
    monthly_inv_azn = portfolio["monthly_investment_azn"]
    monthly_inv_usd = portfolio["monthly_investment_usd"]

    # Calculate projections (conservative estimates)
    if risk_profile == "conservative":
        expected_return = 0.04  # 4% annual
    elif risk_profile == "moderate":
        expected_return = 0.07  # 7% annual
    else:
        expected_return = 0.09  # 9% annual

    total_invested = monthly_inv_azn * time_horizon * 12
    future_value = monthly_inv_azn * (((1 + expected_return/12)**(time_horizon*12) - 1) / (expected_return/12)) * (1 + expected_return/12)
    gains = future_value - total_invested

    text = f"""
📊 **Your Personalized Investment Plan**

🎯 **Goal**: {goal.title()}
⏰ **Time Horizon**: {time_horizon} years
💰 **Monthly Investment**: {monthly_inv_azn:.2f} AZN (~${monthly_inv_usd:.2f} USD)

---

📈 **Recommended Portfolio ({risk_profile.upper()} risk)**

"""

    for alloc in portfolio["allocations"]:
        text += f"""
**{alloc['asset_type']} - {alloc['percentage']}% allocation**
• ETF: {alloc['etf']} ({alloc['etf_name']})
• Current Price: ${alloc['current_price']:.2f}
• Monthly Investment: {alloc['monthly_amount_azn']:.2f} AZN (~${alloc['monthly_amount_usd']:.2f})
• Shares/month: ~{alloc['shares_per_month']:.3f}
• What it is: {alloc['description']}

"""

    text += f"""
---

💡 **Why This Plan?**

• **Time Horizon**: {time_horizon} years gives you {"enough time to recover from market dips" if time_horizon >= 7 else "a moderate timeframe, so we balance risk" if time_horizon >= 3 else "limited time, so we prioritize safety"}
• **Risk Level**: {RISK_PROFILES[risk_profile]['description']}
• **Diversification**: Mix of stocks and bonds reduces risk

📊 **Projected Results** (Conservative estimate)
• Total Invested: {total_invested:,.2f} AZN
• Expected Growth: {gains:,.2f} AZN ({expected_return*100:.0f}% avg annual return)
• Final Value: ~{future_value:,.2f} AZN

---

🚀 **How to Start**

1. Open a brokerage account (Interactive Brokers, Trading212, etc.)
2. Set up automatic monthly investments of {monthly_inv_azn:.2f} AZN
3. Buy {portfolio['allocations'][0]['etf']} and {portfolio['allocations'][1]['etf'] if len(portfolio['allocations']) > 1 else 'bonds'} according to percentages above
4. Don't panic during market drops - stay the course!
5. Review your portfolio every 6 months

⚠️ **Important Reminders**
• Past performance doesn't guarantee future returns
• Keep your emergency fund separate (don't invest it!)
• Only invest money you won't need for {time_horizon} years
• Consider talking to a licensed financial advisor for personalized advice

---

💬 **Questions?** Feel free to ask me anything about your plan!
"""

    return text

# Generate full investment recommendation
def generate_investment_recommendation(
    salary: float,
    savings: float,
    monthly_expenses: float,
    debt: float,
    monthly_investment: float,
    goal: str,
    time_horizon_years: int
) -> Dict:
    """
    Main function to generate complete investment recommendation
    """

    # Safety check first
    is_safe, safety_message, safety_details = safety_check(
        salary, savings, monthly_expenses, debt
    )

    result = {
        "is_safe_to_invest": is_safe,
        "safety_message": safety_message,
        "safety_details": safety_details
    }

    # Generate portfolio recommendation only if safe
    if is_safe:
        portfolio = calculate_portfolio(monthly_investment, time_horizon_years, goal)
        recommendation_text = generate_recommendation_text(
            portfolio, goal, salary, savings
        )

        result["portfolio"] = portfolio
        result["recommendation_text"] = recommendation_text
    else:
        # Provide guidance on what to do instead
        actions_text = "\n".join(safety_details["priority_actions"])
        result["recommendation_text"] = f"""
{safety_message}

{actions_text}

**Why this matters:**
Investing without a safety net is risky. If an emergency happens, you might need to sell investments at a loss. Let's build your financial foundation first!

**Next Steps:**
1. Create a budget to track expenses
2. Build your emergency fund to {safety_details['emergency_fund_needed']:.2f} AZN
3. Pay down high-interest debt
4. Then come back and we'll create your investment plan!

💬 Need help creating a savings plan? Just ask!
"""

    return result

# Test function
if __name__ == "__main__":
    print("Testing Investment Logic...")

    # Test case 1: Safe to invest
    print("\n=== Test 1: Good Financial Position ===")
    result1 = generate_investment_recommendation(
        salary=3000,
        savings=10000,
        monthly_expenses=1500,
        debt=0,
        monthly_investment=500,
        goal="house",
        time_horizon_years=7
    )
    print(f"Safe to invest: {result1['is_safe_to_invest']}")
    print(result1['safety_message'])
    if result1['is_safe_to_invest']:
        print("\nPortfolio:")
        for alloc in result1['portfolio']['allocations']:
            print(f"  {alloc['etf']}: {alloc['percentage']}% = {alloc['monthly_amount_azn']:.2f} AZN")

    # Test case 2: High debt
    print("\n=== Test 2: High Debt ===")
    result2 = generate_investment_recommendation(
        salary=2000,
        savings=5000,
        monthly_expenses=1200,
        debt=1500,
        monthly_investment=300,
        goal="retirement",
        time_horizon_years=10
    )
    print(f"Safe to invest: {result2['is_safe_to_invest']}")
    print(result2['safety_message'])
    print("\nActions:")
    for action in result2['safety_details']['priority_actions']:
        print(f"  {action}")
