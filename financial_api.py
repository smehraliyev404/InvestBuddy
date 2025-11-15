import os
import requests
import yfinance as yf
from typing import Optional, Dict
from datetime import datetime, timedelta
from dotenv import load_dotenv

load_dotenv()

# API Configuration
ALPHA_VANTAGE_API_KEY = os.getenv("ALPHA_VANTAGE_API_KEY", "demo")
ALPHA_VANTAGE_BASE_URL = "https://www.alphavantage.co/query"

# Price cache to reduce API calls
price_cache = {}
CACHE_DURATION_MINUTES = 15

# Popular ETFs for investment recommendations
POPULAR_ETFS = {
    "SPY": "S&P 500 ETF (Large US stocks)",
    "VOO": "Vanguard S&P 500 ETF (Low-cost US stocks)",
    "VTI": "Total Stock Market ETF (All US stocks)",
    "BND": "Bond ETF (Safe, stable bonds)",
    "AGG": "Aggregate Bond ETF (Diverse bonds)",
    "VWO": "Emerging Markets ETF (International growth)",
    "VEA": "Developed Markets ETF (International stability)",
    "QQQ": "Nasdaq 100 ETF (Tech-focused)",
}

# Get stock/ETF price using Alpha Vantage
def get_price_alpha_vantage(symbol: str) -> Optional[Dict]:
    try:
        params = {
            "function": "GLOBAL_QUOTE",
            "symbol": symbol,
            "apikey": ALPHA_VANTAGE_API_KEY
        }

        response = requests.get(ALPHA_VANTAGE_BASE_URL, params=params, timeout=10)
        data = response.json()

        if "Global Quote" in data and data["Global Quote"]:
            quote = data["Global Quote"]
            return {
                "symbol": symbol,
                "price": float(quote.get("05. price", 0)),
                "change": float(quote.get("09. change", 0)),
                "change_percent": quote.get("10. change percent", "0%"),
                "volume": int(quote.get("06. volume", 0)),
                "timestamp": datetime.now().isoformat(),
                "source": "Alpha Vantage"
            }

        # Check if we hit rate limit
        if "Note" in data or "Information" in data:
            print(f"Alpha Vantage rate limit hit or error: {data}")
            return None

    except Exception as e:
        print(f"Alpha Vantage error for {symbol}: {str(e)}")
        return None

# Get stock/ETF price using yfinance (fallback)
def get_price_yfinance(symbol: str) -> Optional[Dict]:
    try:
        ticker = yf.Ticker(symbol)
        info = ticker.info
        history = ticker.history(period="1d")

        if not history.empty:
            current_price = history['Close'].iloc[-1]
            previous_close = info.get('previousClose', current_price)
            change = current_price - previous_close
            change_percent = (change / previous_close) * 100 if previous_close else 0

            return {
                "symbol": symbol,
                "price": round(float(current_price), 2),
                "change": round(float(change), 2),
                "change_percent": f"{change_percent:.2f}%",
                "volume": int(history['Volume'].iloc[-1]) if 'Volume' in history else 0,
                "timestamp": datetime.now().isoformat(),
                "source": "Yahoo Finance"
            }

    except Exception as e:
        print(f"yfinance error for {symbol}: {str(e)}")
        return None

# Main function to get stock price with caching and fallback
def get_stock_price(symbol: str, use_cache: bool = True) -> Optional[Dict]:
    # Check cache first
    if use_cache and symbol in price_cache:
        cached_data = price_cache[symbol]
        cache_time = datetime.fromisoformat(cached_data["timestamp"])
        if datetime.now() - cache_time < timedelta(minutes=CACHE_DURATION_MINUTES):
            print(f"Using cached price for {symbol}")
            return cached_data

    # Try Alpha Vantage first
    print(f"Fetching {symbol} from Alpha Vantage...")
    price_data = get_price_alpha_vantage(symbol)

    # Fallback to yfinance if Alpha Vantage fails
    if not price_data:
        print(f"Falling back to yfinance for {symbol}...")
        price_data = get_price_yfinance(symbol)

    # Cache the result
    if price_data:
        price_cache[symbol] = price_data
        return price_data

    print(f"Failed to fetch price for {symbol} from all sources")
    return None

# Get multiple stock prices
def get_multiple_prices(symbols: list) -> Dict[str, Optional[Dict]]:
    results = {}
    for symbol in symbols:
        results[symbol] = get_stock_price(symbol)
    return results

# Get recommended ETFs with current prices
def get_recommended_etfs() -> Dict[str, Dict]:
    etf_data = {}

    # Fetch prices for key ETFs
    key_etfs = ["SPY", "VOO", "BND", "AGG"]

    for symbol in key_etfs:
        price_info = get_stock_price(symbol)
        if price_info:
            etf_data[symbol] = {
                "name": POPULAR_ETFS.get(symbol, symbol),
                "price": price_info["price"],
                "change_percent": price_info["change_percent"],
                "source": price_info["source"]
            }

    return etf_data

# Format price for display
def format_price(price: float, currency: str = "USD") -> str:
    if currency == "USD":
        return f"${price:,.2f}"
    elif currency == "AZN":
        return f"{price:,.2f} AZN"
    else:
        return f"{price:,.2f}"

# Clear price cache
def clear_cache():
    global price_cache
    price_cache = {}
    print("Price cache cleared")

# Test function
if __name__ == "__main__":
    print("Testing Financial API...")
    print("\n1. Testing SPY (S&P 500 ETF):")
    spy_data = get_stock_price("SPY")
    if spy_data:
        print(f"   Price: {format_price(spy_data['price'])}")
        print(f"   Change: {spy_data['change_percent']}")
        print(f"   Source: {spy_data['source']}")

    print("\n2. Testing recommended ETFs:")
    etfs = get_recommended_etfs()
    for symbol, data in etfs.items():
        print(f"   {symbol}: {format_price(data['price'])} ({data['change_percent']})")

    print("\n3. Testing cache:")
    spy_data_cached = get_stock_price("SPY", use_cache=True)
    print(f"   Cached: {spy_data_cached['source']}")
