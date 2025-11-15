"""
Live ETF Data Fetcher
Fetches real-time ETF data including prices, holdings, performance, etc.
"""

import yfinance as yf
from datetime import datetime, timedelta
import requests
from typing import Dict, Optional
import time

# Cache to avoid hammering APIs
_price_cache = {}
_cache_duration = 900  # 15 minutes

def get_live_etf_data(symbol: str) -> Dict:
    """
    Fetch comprehensive live data for an ETF

    Returns:
        Dict with current price, performance, holdings, and other live data
    """
    cache_key = f"{symbol}_live"
    current_time = time.time()

    # Check cache
    if cache_key in _price_cache:
        cached_data, cached_time = _price_cache[cache_key]
        if current_time - cached_time < _cache_duration:
            return cached_data

    try:
        # Fetch data using yfinance
        ticker = yf.Ticker(symbol)

        # Get current price and info
        info = ticker.info
        hist = ticker.history(period="1mo")

        # Calculate performance metrics
        current_price = info.get('regularMarketPrice', 0) or info.get('currentPrice', 0)
        previous_close = info.get('regularMarketPreviousClose', 0) or info.get('previousClose', 0)

        if current_price and previous_close:
            day_change = ((current_price - previous_close) / previous_close) * 100
        else:
            day_change = 0

        # Get 1-month performance
        if not hist.empty and len(hist) > 0:
            month_start_price = hist['Close'].iloc[0]
            month_change = ((current_price - month_start_price) / month_start_price) * 100 if month_start_price else 0
        else:
            month_change = 0

        # Get year-to-date performance
        ytd_hist = ticker.history(period="ytd")
        if not ytd_hist.empty and len(ytd_hist) > 0:
            ytd_start_price = ytd_hist['Close'].iloc[0]
            ytd_change = ((current_price - ytd_start_price) / ytd_start_price) * 100 if ytd_start_price else 0
        else:
            ytd_change = 0

        # Compile live data
        live_data = {
            'symbol': symbol,
            'current_price': current_price,
            'previous_close': previous_close,
            'day_change': day_change,
            'month_change': month_change,
            'ytd_change': ytd_change,
            'volume': info.get('volume', 'N/A'),
            'market_cap': info.get('totalAssets', 'N/A'),
            'expense_ratio': info.get('annualReportExpenseRatio', 'N/A'),
            'dividend_yield': info.get('yield', 0) or info.get('trailingAnnualDividendYield', 0),
            'avg_volume': info.get('averageVolume', 'N/A'),
            'holdings_count': info.get('holdings', {}).get('count', 'N/A') if 'holdings' in info else 'N/A',
            'last_updated': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'fifty_two_week_high': info.get('fiftyTwoWeekHigh', 'N/A'),
            'fifty_two_week_low': info.get('fiftyTwoWeekLow', 'N/A'),
        }

        # Cache the result
        _price_cache[cache_key] = (live_data, current_time)

        return live_data

    except Exception as e:
        print(f"Error fetching live data for {symbol}: {e}")
        # Return minimal data on error
        return {
            'symbol': symbol,
            'current_price': 0,
            'error': str(e),
            'last_updated': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }

def get_multiple_live_data(symbols: list) -> Dict[str, Dict]:
    """
    Fetch live data for multiple ETFs

    Args:
        symbols: List of ETF symbols

    Returns:
        Dict mapping symbol to live data
    """
    results = {}
    for symbol in symbols:
        results[symbol] = get_live_etf_data(symbol)
        time.sleep(0.2)  # Small delay to avoid rate limiting

    return results

def format_live_data_for_ai(symbol: str, live_data: Dict) -> str:
    """
    Format live data into a readable string for AI context

    Args:
        symbol: ETF symbol
        live_data: Live data dict from get_live_etf_data

    Returns:
        Formatted string with current market data
    """
    if 'error' in live_data:
        return f"**{symbol} - Live Data Unavailable**\nError: {live_data['error']}"

    # Format market cap
    market_cap = live_data.get('market_cap', 'N/A')
    if isinstance(market_cap, (int, float)) and market_cap != 'N/A':
        if market_cap >= 1e9:
            market_cap_str = f"${market_cap/1e9:.2f}B"
        elif market_cap >= 1e6:
            market_cap_str = f"${market_cap/1e6:.2f}M"
        else:
            market_cap_str = f"${market_cap:,.0f}"
    else:
        market_cap_str = "N/A"

    # Format expense ratio
    expense_ratio = live_data.get('expense_ratio', 'N/A')
    if isinstance(expense_ratio, (int, float)) and expense_ratio != 'N/A':
        expense_ratio_str = f"{expense_ratio*100:.2f}%"
    else:
        expense_ratio_str = "N/A"

    # Format dividend yield
    dividend_yield = live_data.get('dividend_yield', 0)
    if isinstance(dividend_yield, (int, float)) and dividend_yield > 0:
        dividend_yield_str = f"{dividend_yield*100:.2f}%"
    else:
        dividend_yield_str = "N/A"

    formatted = f"""
**{symbol} - Current Market Data (as of {live_data['last_updated']})**

📊 **Current Price:** ${live_data['current_price']:.2f}
📈 **Today's Change:** {live_data['day_change']:+.2f}%
📅 **1-Month Performance:** {live_data['month_change']:+.2f}%
📆 **Year-to-Date:** {live_data['ytd_change']:+.2f}%
💰 **Total Assets:** {market_cap_str}
💵 **Expense Ratio:** {expense_ratio_str}
💎 **Dividend Yield:** {dividend_yield_str}
📊 **52-Week High:** ${live_data['fifty_two_week_high']} | Low: ${live_data['fifty_two_week_low']}
"""

    return formatted.strip()

# Test if running directly
if __name__ == "__main__":
    print("🔄 Testing Live ETF Data Fetcher...\n")

    test_symbols = ['SPY', 'BND', 'QQQ']

    for symbol in test_symbols:
        print(f"\n{'='*60}")
        print(f"Fetching live data for {symbol}...")
        print(f"{'='*60}")

        live_data = get_live_etf_data(symbol)
        formatted = format_live_data_for_ai(symbol, live_data)
        print(formatted)
        print()

    print("✅ Live data fetch test complete!")
