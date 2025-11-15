"""
ETF Knowledge Base - Beginner-Friendly Explanations
This module contains detailed, easy-to-understand information about various ETFs.
"""

# Comprehensive ETF knowledge base with beginner-friendly explanations
ETF_KNOWLEDGE_BASE = {
    # US Market - Large Cap
    "SPY": {
        "name": "SPDR S&P 500 ETF",
        "simple_name": "America's Top 500 Companies",
        "category": "US Stocks - Large Companies",
        "risk_level": "Medium",
        "expense_ratio": "0.09%",
        "beginner_explanation": (
            "Think of SPY as owning a tiny piece of 500 of America's biggest and most successful companies "
            "like Apple, Microsoft, Amazon, and Google. When you buy SPY, you're spreading your money across "
            "all these companies instead of betting on just one. It's one of the safest ways to invest in stocks "
            "because even if a few companies do badly, the others usually balance it out."
        ),
        "good_for": "Long-term growth, retirement savings, first-time investors",
        "why_beginners_love_it": "It's simple, proven, and you own a piece of America's economy",
        "real_world_example": "If you invested $10,000 in SPY 10 years ago, you'd have about $30,000 today",
    },

    "VOO": {
        "name": "Vanguard S&P 500 ETF",
        "simple_name": "Same as SPY but Cheaper",
        "category": "US Stocks - Large Companies",
        "risk_level": "Medium",
        "expense_ratio": "0.03%",
        "beginner_explanation": (
            "VOO is almost identical to SPY - it owns the same 500 big American companies. "
            "The difference? VOO charges lower fees, which means more money stays in your pocket over time. "
            "Think of it like buying the same product at two stores - VOO is the discount store version."
        ),
        "good_for": "Long-term investors who want to minimize costs",
        "why_beginners_love_it": "Lower fees mean your money grows faster over time",
        "real_world_example": "Over 30 years, the lower fees could save you thousands of dollars",
    },

    "VTI": {
        "name": "Vanguard Total Stock Market ETF",
        "simple_name": "Every US Company, Big and Small",
        "category": "US Stocks - All Sizes",
        "risk_level": "Medium",
        "expense_ratio": "0.03%",
        "beginner_explanation": (
            "VTI is like owning a piece of almost every publicly traded company in America - "
            "not just the big 500, but also thousands of smaller companies. It's the most diversified "
            "way to invest in the US stock market. You get big companies like Apple, plus smaller "
            "companies that might become the next Apple."
        ),
        "good_for": "Maximum diversification in US stocks, long-term growth",
        "why_beginners_love_it": "You own the entire US market with one purchase",
        "real_world_example": "Includes about 4,000 companies - from giants to future stars",
    },

    "QQQ": {
        "name": "Invesco QQQ Trust",
        "simple_name": "Top 100 Tech Companies",
        "category": "Technology Stocks",
        "risk_level": "Higher",
        "expense_ratio": "0.20%",
        "beginner_explanation": (
            "QQQ focuses on the 100 biggest tech and innovation companies traded on the Nasdaq stock exchange. "
            "Think Apple, Microsoft, Tesla, Netflix, and Amazon. If you believe technology will keep growing, "
            "QQQ is your bet. But remember: higher potential rewards come with bigger ups and downs."
        ),
        "good_for": "Tech enthusiasts, long-term growth, higher risk tolerance",
        "why_beginners_love_it": "You own the companies shaping the future",
        "real_world_example": "During tech booms it soars, but during tech downturns it falls harder than SPY",
    },

    # Bonds - Safe & Stable
    "BND": {
        "name": "Vanguard Total Bond Market ETF",
        "simple_name": "The Safety Net",
        "category": "Bonds - Safe Investments",
        "risk_level": "Low",
        "expense_ratio": "0.03%",
        "beginner_explanation": (
            "BND is like a savings account that pays better interest, but is still very safe. "
            "When you buy bonds, you're lending money to the government and big companies, "
            "and they pay you back with interest. Bonds don't grow as fast as stocks, but they "
            "protect your money when the stock market gets scary. Perfect for money you'll need soon."
        ),
        "good_for": "Stability, protecting your money, reducing risk",
        "why_beginners_love_it": "It's boring, and that's a good thing - your money stays safe",
        "real_world_example": "Returns about 3-4% per year - slow and steady wins the race",
    },

    "AGG": {
        "name": "iShares Core U.S. Aggregate Bond ETF",
        "simple_name": "Another Safe Choice",
        "category": "Bonds - Safe Investments",
        "risk_level": "Low",
        "expense_ratio": "0.03%",
        "beginner_explanation": (
            "AGG is very similar to BND - it's another way to own safe bonds. "
            "Think of it as a different brand of the same product. Both are excellent choices "
            "for keeping part of your money safe while earning modest returns."
        ),
        "good_for": "Safety, income, balancing risky investments",
        "why_beginners_love_it": "Reliable and predictable - no surprises",
        "real_world_example": "When stocks crashed in 2020, bonds like AGG stayed stable",
    },

    # International
    "VEA": {
        "name": "Vanguard FTSE Developed Markets ETF",
        "simple_name": "Stable Foreign Companies",
        "category": "International Stocks - Developed Countries",
        "risk_level": "Medium",
        "expense_ratio": "0.05%",
        "beginner_explanation": (
            "VEA lets you own pieces of big companies in wealthy countries like Japan, UK, Canada, "
            "Germany, and France. It's like SPY, but for international companies instead of American ones. "
            "This helps you spread risk - if America's economy slows down, other countries might do well."
        ),
        "good_for": "Global diversification, don't want to bet only on America",
        "why_beginners_love_it": "You own companies from all over the developed world",
        "real_world_example": "Includes companies like Toyota, Samsung, and Nestle",
    },

    "VWO": {
        "name": "Vanguard FTSE Emerging Markets ETF",
        "simple_name": "Fast-Growing Countries",
        "category": "International Stocks - Emerging Markets",
        "risk_level": "Higher",
        "expense_ratio": "0.08%",
        "beginner_explanation": (
            "VWO invests in companies from countries that are growing fast, like China, India, Brazil, "
            "and Taiwan. These countries are developing rapidly, which can mean bigger profits - but also "
            "bigger risks. Think of it as investing in countries that might become the next America."
        ),
        "good_for": "Long-term growth, higher risk tolerance, diversification",
        "why_beginners_love_it": "Potential for high growth as these countries develop",
        "real_world_example": "China and India's middle class is growing - millions of new consumers",
    },

    # Dividend ETFs
    "VYM": {
        "name": "Vanguard High Dividend Yield ETF",
        "simple_name": "Companies That Pay You Regularly",
        "category": "Dividend Stocks",
        "risk_level": "Medium",
        "expense_ratio": "0.06%",
        "beginner_explanation": (
            "VYM owns companies that regularly share their profits with investors (called dividends). "
            "It's like getting a paycheck from your investments every few months. These companies are "
            "usually stable and established, like utilities and banks. Good for people who want regular income."
        ),
        "good_for": "Regular income, semi-retirement, stable growth",
        "why_beginners_love_it": "You get paid while your investment grows",
        "real_world_example": "Might pay you $300-400 per year for every $10,000 invested",
    },

    "SCHD": {
        "name": "Schwab U.S. Dividend Equity ETF",
        "simple_name": "Quality Companies That Pay",
        "category": "Dividend Stocks",
        "risk_level": "Medium",
        "expense_ratio": "0.06%",
        "beginner_explanation": (
            "SCHD is pickier than VYM - it only owns high-quality companies with strong finances "
            "that have consistently paid and grown their dividends. It's like VYM but with stricter standards. "
            "Popular with investors who want both income and quality."
        ),
        "good_for": "Income + quality, long-term dividend growth",
        "why_beginners_love_it": "You own the best of the best dividend payers",
        "real_world_example": "Companies that have increased their dividend payments for 10+ years",
    },

    # Sector ETFs
    "XLK": {
        "name": "Technology Select Sector SPDR Fund",
        "simple_name": "Pure Technology",
        "category": "Technology Sector",
        "risk_level": "Higher",
        "expense_ratio": "0.10%",
        "beginner_explanation": (
            "XLK is all-in on technology. It owns the tech companies from the S&P 500, like Apple, Microsoft, "
            "and Nvidia. If you believe tech is the future but want something more focused than QQQ, this is it. "
            "But remember: when tech crashes, this crashes hard."
        ),
        "good_for": "Tech believers, long-term growth, higher risk tolerance",
        "why_beginners_love_it": "Direct bet on technology's growth",
        "real_world_example": "Up over 400% in the past 10 years during the tech boom",
    },

    "XLV": {
        "name": "Health Care Select Sector SPDR Fund",
        "simple_name": "Healthcare Companies",
        "category": "Healthcare Sector",
        "risk_level": "Medium",
        "expense_ratio": "0.10%",
        "beginner_explanation": (
            "XLV owns pharmaceutical companies, hospitals, and medical device makers. "
            "As people age and healthcare advances, these companies tend to grow steadily. "
            "Healthcare is one of the most stable sectors - people always need medicine and doctors."
        ),
        "good_for": "Stability, aging population trend, defensive investing",
        "why_beginners_love_it": "Healthcare demand never stops",
        "real_world_example": "Includes companies like Johnson & Johnson and Pfizer",
    },

    "XLF": {
        "name": "Financial Select Sector SPDR Fund",
        "simple_name": "Banks and Financial Companies",
        "category": "Financial Sector",
        "risk_level": "Medium",
        "expense_ratio": "0.10%",
        "beginner_explanation": (
            "XLF owns banks, insurance companies, and other financial institutions. "
            "These companies make money from interest rates and managing money. When the economy is strong, "
            "they tend to do well. When the economy struggles, they can suffer."
        ),
        "good_for": "Economic growth believers, diversification",
        "why_beginners_love_it": "Banks are the backbone of the economy",
        "real_world_example": "Includes JPMorgan, Bank of America, Wells Fargo",
    },

    "XLE": {
        "name": "Energy Select Sector SPDR Fund",
        "simple_name": "Oil and Energy Companies",
        "category": "Energy Sector",
        "risk_level": "Higher",
        "expense_ratio": "0.10%",
        "beginner_explanation": (
            "XLE owns oil, gas, and energy companies like ExxonMobil and Chevron. "
            "Energy prices go up and down a lot, which makes this investment more volatile. "
            "Good for hedging against inflation - when everything gets expensive, energy often does too."
        ),
        "good_for": "Inflation protection, oil price believers, diversification",
        "why_beginners_love_it": "Performs well when oil prices rise",
        "real_world_example": "Up 50%+ when oil prices surged in 2022",
    },

    # Growth vs Value
    "VUG": {
        "name": "Vanguard Growth ETF",
        "simple_name": "Fast-Growing Companies",
        "category": "Growth Stocks",
        "risk_level": "Higher",
        "expense_ratio": "0.04%",
        "beginner_explanation": (
            "VUG owns companies that are growing fast - think tech companies and innovative businesses. "
            "These companies reinvest their profits to grow bigger rather than paying dividends. "
            "Higher risk, higher potential reward. Like planting a tree that might grow tall."
        ),
        "good_for": "Long-term growth, younger investors, higher risk tolerance",
        "why_beginners_love_it": "Focuses on tomorrow's winners",
        "real_world_example": "Heavy in companies like Amazon and Tesla",
    },

    "VTV": {
        "name": "Vanguard Value ETF",
        "simple_name": "Bargain-Priced Stable Companies",
        "category": "Value Stocks",
        "risk_level": "Medium",
        "expense_ratio": "0.04%",
        "beginner_explanation": (
            "VTV owns established companies that the market thinks are underpriced - basically bargains. "
            "These are often older, stable companies in traditional industries. They may grow slower, "
            "but they're usually safer and pay dividends."
        ),
        "good_for": "Stability, dividend income, defensive investing",
        "why_beginners_love_it": "Buying quality at a discount",
        "real_world_example": "Companies like Berkshire Hathaway and Johnson & Johnson",
    },

    # Small Cap
    "VB": {
        "name": "Vanguard Small-Cap ETF",
        "simple_name": "Small Companies, Big Potential",
        "category": "Small Company Stocks",
        "risk_level": "Higher",
        "expense_ratio": "0.05%",
        "beginner_explanation": (
            "VB owns smaller companies that have room to grow into big companies. "
            "Small companies can grow faster than giants, but they're also riskier - many fail. "
            "Think of it as investing in the next potential Amazon when it was still small."
        ),
        "good_for": "Long-term growth, higher risk tolerance, diversification",
        "why_beginners_love_it": "Hunting for the next big success story",
        "real_world_example": "More volatile but historically outperforms large caps over long periods",
    },

    # Real Estate
    "VNQ": {
        "name": "Vanguard Real Estate ETF",
        "simple_name": "Owning Buildings Without the Hassle",
        "category": "Real Estate",
        "risk_level": "Medium",
        "expense_ratio": "0.12%",
        "beginner_explanation": (
            "VNQ lets you invest in real estate without buying actual property. You own pieces of companies "
            "that own malls, apartment buildings, offices, and warehouses. They collect rent and share the "
            "profits with you. It's like being a landlord without fixing toilets."
        ),
        "good_for": "Diversification, passive real estate exposure, income",
        "why_beginners_love_it": "Real estate exposure without buying a house",
        "real_world_example": "Paid good dividends from rental income",
    },

    # ESG/Sustainable
    "ESGU": {
        "name": "iShares ESG Aware MSCI USA ETF",
        "simple_name": "Responsible Investing",
        "category": "Sustainable/ESG Investing",
        "risk_level": "Medium",
        "expense_ratio": "0.15%",
        "beginner_explanation": (
            "ESGU invests in companies that score well on environmental, social, and governance (ESG) factors. "
            "It avoids companies with bad environmental records or poor labor practices. "
            "You can grow your money while supporting companies that do good."
        ),
        "good_for": "Values-based investing, socially conscious investors",
        "why_beginners_love_it": "Invest according to your values",
        "real_world_example": "Excludes tobacco, weapons, and major polluters",
    },

    # Gold/Commodities
    "GLD": {
        "name": "SPDR Gold Trust",
        "simple_name": "Digital Gold",
        "category": "Commodities - Gold",
        "risk_level": "Medium",
        "expense_ratio": "0.40%",
        "beginner_explanation": (
            "GLD tracks the price of gold. When people get scared about the economy or inflation, "
            "they buy gold, and GLD goes up. It's a hedge - insurance against your other investments falling. "
            "Gold doesn't pay dividends or grow like companies, but it holds value when things get uncertain."
        ),
        "good_for": "Portfolio insurance, inflation hedge, diversification",
        "why_beginners_love_it": "Gold has been valuable for thousands of years",
        "real_world_example": "Surged during 2008 financial crisis and 2020 pandemic",
    },

    # Target Date Funds
    "VTTVX": {
        "name": "Vanguard Target Retirement 2030",
        "simple_name": "Auto-Pilot Retirement Fund",
        "category": "Target Date Fund",
        "risk_level": "Medium (Auto-Adjusting)",
        "expense_ratio": "0.08%",
        "beginner_explanation": (
            "This fund does all the work for you. If you plan to retire around 2030, it automatically "
            "adjusts your mix of stocks and bonds as you get closer to retirement. More stocks when you're "
            "young (risky = higher growth), more bonds as you age (safe = preserve wealth). Set it and forget it."
        ),
        "good_for": "Hands-off investors, retirement planning, beginners",
        "why_beginners_love_it": "You don't have to think about it - it rebalances automatically",
        "real_world_example": "Perfect for someone who wants to retire in 2030",
    },

    # Total Market Alternatives
    "ITOT": {
        "name": "iShares Core S&P Total U.S. Stock Market ETF",
        "simple_name": "Another Total Market Option",
        "category": "US Total Market",
        "risk_level": "Medium",
        "expense_ratio": "0.03%",
        "beginner_explanation": (
            "ITOT is similar to VTI - it owns the entire US stock market. Same concept, different company. "
            "Both are excellent choices. Pick based on which broker you use or which has lower fees for you."
        ),
        "good_for": "Total market exposure, diversification",
        "why_beginners_love_it": "Simple, cheap, and effective",
        "real_world_example": "Owns about 3,500 US companies",
    },

    # Innovation/ARK
    "ARKK": {
        "name": "ARK Innovation ETF",
        "simple_name": "Betting on Future Tech",
        "category": "Innovation/Disruptive Tech",
        "risk_level": "Very High",
        "expense_ratio": "0.75%",
        "beginner_explanation": (
            "ARKK invests in companies working on cutting-edge technology like AI, robotics, genomics, "
            "and electric vehicles. It's very aggressive - big wins or big losses. Not for the faint of heart. "
            "Managed by Cathie Wood, a famous (and controversial) investor."
        ),
        "good_for": "Risk-takers, believers in disruptive innovation, small portion of portfolio",
        "why_beginners_love_it": "Focuses on world-changing companies",
        "real_world_example": "Up 150% in 2020, down 70% in 2022 - very volatile!",
    },
}

def get_etf_info(symbol):
    """Get detailed information about a specific ETF"""
    return ETF_KNOWLEDGE_BASE.get(symbol.upper())

def get_all_etf_symbols():
    """Get list of all ETF symbols in knowledge base"""
    return list(ETF_KNOWLEDGE_BASE.keys())

def search_etfs_by_category(category):
    """Search ETFs by category"""
    results = []
    for symbol, info in ETF_KNOWLEDGE_BASE.items():
        if category.lower() in info['category'].lower():
            results.append({
                'symbol': symbol,
                **info
            })
    return results

def search_etfs_by_risk(risk_level):
    """Search ETFs by risk level"""
    results = []
    for symbol, info in ETF_KNOWLEDGE_BASE.items():
        if risk_level.lower() in info['risk_level'].lower():
            results.append({
                'symbol': symbol,
                **info
            })
    return results

def get_beginner_friendly_etfs():
    """Get ETFs most suitable for beginners"""
    beginner_friendly = []
    beginner_symbols = ['SPY', 'VOO', 'VTI', 'BND', 'AGG', 'VEA', 'SCHD']

    for symbol in beginner_symbols:
        if symbol in ETF_KNOWLEDGE_BASE:
            beginner_friendly.append({
                'symbol': symbol,
                **ETF_KNOWLEDGE_BASE[symbol]
            })

    return beginner_friendly
