"""
VitaNova Gold Price API Server with Authentication
===================================================
Main Flask application combining gold price APIs and user authentication
"""

import http.client
import json
import csv
import os
import requests
from flask import Flask, jsonify, request
from flask_cors import CORS
from datetime import datetime, timedelta

# Initialize Flask app
app = Flask(__name__)
CORS(app, supports_credentials=True)  # Enable credentials for auth cookies

# ============== CONFIGURATION ==============
BASE_DIR = os.path.dirname(__file__)

# Import config
try:
    from config import SECRET_KEY, SQLALCHEMY_DATABASE_URI
    app.config['SECRET_KEY'] = SECRET_KEY
    app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
except ImportError:
    # Fallback if config not yet created
    import secrets
    app.config['SECRET_KEY'] = secrets.token_hex(32)

# CSV file paths for gold prices
DAILY_CSV_PATH = os.path.join(BASE_DIR, 'DailyGold.csv')
HISTORICAL_CSV_PATH = os.path.join(BASE_DIR, 'HistoricalMVPGold.csv')
LAST_HISTORICAL_MONTH_FILE = os.path.join(BASE_DIR, 'last_historical_month.txt')

# Fixed USD to AED exchange rate (pegged currency)
USD_TO_AED_RATE = 3.6728
# Grams per troy ounce
GRAMS_PER_OUNCE = 31.1035

# APISED Gold API Configuration
# Host: gold.g.apised.com
# Endpoint: /v1/latest
APISED_API_HOST = "gold.g.apised.com"
APISED_API_ENDPOINT = "/v1/latest"
APISED_API_KEY = "sk_FfA3E90701ED46464540dAE68655797368A43C7Ec9bA7352"

# Standard number of data points for charts
CHART_DATA_POINTS = 8
CHART_DATA_POINTS_1D = 9


# ============== AUTHENTICATION INITIALIZATION ==============
try:
    from auth_routes import init_auth
    init_auth(app)
    AUTH_ENABLED = True
    print("🔐 Authentication system enabled")
except ImportError as e:
    AUTH_ENABLED = False
    print(f"⚠️ Authentication system not available: {e}")


# ============== ORDERS INITIALIZATION ==============
try:
    from orders_handler import init_orders
    init_orders(app)
    ORDERS_ENABLED = True
    print("📦 Orders system enabled")
except ImportError as e:
    ORDERS_ENABLED = False
    print(f"⚠️ Orders system not available: {e}")


# ============== GOLD PRICE HELPER FUNCTIONS ==============

def get_last_logged_historical_month():
    """Get the last month that was logged to HistoricalMVPGold.csv"""
    try:
        if os.path.exists(LAST_HISTORICAL_MONTH_FILE):
            with open(LAST_HISTORICAL_MONTH_FILE, 'r') as f:
                content = f.read().strip()
                if content:
                    return content  # Format: MM/YYYY
    except Exception as e:
        print(f"⚠️ Error reading last historical month: {e}")
    return None


def set_last_logged_historical_month(month_str):
    """Set the last month that was logged to HistoricalMVPGold.csv"""
    try:
        with open(LAST_HISTORICAL_MONTH_FILE, 'w') as f:
            f.write(month_str)
        print(f"📝 Updated last historical month to: {month_str}")
    except Exception as e:
        print(f"❌ Error writing last historical month: {e}")


def append_to_historical_csv(price_aed_per_gram):
    """
    Append a new monthly entry to HistoricalMVPGold.csv
    
    Format: Date,USD_to_UAE,Price_oz_USD,Price_g_USD,Price_g_UAE
    Example: 02/2026,3.6728,2894.73,93.0676612,341.818906
    """
    now = datetime.now()
    month_str = now.strftime("%m/%Y")  # Format: MM/YYYY
    
    # Calculate all the values
    price_g_aed = price_aed_per_gram
    price_g_usd = price_g_aed / USD_TO_AED_RATE
    price_oz_usd = price_g_usd * GRAMS_PER_OUNCE
    
    # Append to CSV
    try:
        with open(HISTORICAL_CSV_PATH, 'a', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow([
                month_str,
                USD_TO_AED_RATE,
                round(price_oz_usd, 2),
                round(price_g_usd, 9),  # More precision for grams
                round(price_g_aed, 9)
            ])
        
        print(f"📊 HISTORICAL PRICE LOGGED for {month_str}:")
        print(f"   - Price/gram (AED): {price_g_aed:.2f}")
        print(f"   - Price/gram (USD): {price_g_usd:.6f}")
        print(f"   - Price/oz (USD): {price_oz_usd:.2f}")
        
        # Update the tracking file
        set_last_logged_historical_month(month_str)
        
        return True
    except Exception as e:
        print(f"❌ Error appending to historical CSV: {e}")
        return False


def check_and_log_monthly_historical(price_aed_per_gram):
    """
    Check if it's the 1st of a new month and log to historical CSV if needed.
    This ensures we capture the first price of each month for historical records.
    """
    now = datetime.now()
    
    # Only proceed if it's the 1st of the month
    if now.day != 1:
        return False
    
    current_month_str = now.strftime("%m/%Y")  # Format: MM/YYYY
    last_logged_month = get_last_logged_historical_month()
    
    # Check if we've already logged this month
    if last_logged_month == current_month_str:
        # Already logged this month, skip
        return False
    
    print(f"\n🗓️ First day of {current_month_str} detected!")
    print(f"   Last logged month: {last_logged_month or 'None'}")
    print(f"   Logging first price of the month to historical CSV...")
    
    # Log to historical CSV
    return append_to_historical_csv(price_aed_per_gram)


def append_price_to_csv(price):
    """Append the fetched price to DailyGold.csv with full timestamp"""
    now = datetime.now()
    timestamp = now.strftime("%S/%M/%H/%d/%m/%Y")
    
    with open(DAILY_CSV_PATH, 'a', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow([timestamp, f"{price:.2f}"])
    
    print(f"✅ Price {price:.2f} AED/gram appended with timestamp {timestamp}")
    
    # Check if we need to log to historical CSV (first price of the month)
    check_and_log_monthly_historical(price)


def parse_daily_timestamp(ts_str):
    """Parse DailyGold.csv timestamp format: SS/MM/HH/DD/MM/YYYY"""
    try:
        parts = ts_str.split('/')
        if len(parts) == 6:
            sec, minute, hour, day, month, year = parts
            return datetime(int(year), int(month), int(day), int(hour), int(minute), int(sec))
    except:
        pass
    return None


def parse_historical_date(date_str):
    """Parse HistoricalMVPGold.csv date format: MM/YYYY"""
    try:
        parts = date_str.split('/')
        if len(parts) == 2:
            month, year = parts
            return datetime(int(year), int(month), 1)
    except:
        pass
    return None


def load_daily_prices():
    """Load all prices from DailyGold.csv"""
    prices = []
    if not os.path.exists(DAILY_CSV_PATH):
        return prices
    
    with open(DAILY_CSV_PATH, 'r', newline='') as csvfile:
        reader = csv.reader(csvfile)
        header = next(reader, None)
        
        for row in reader:
            if len(row) >= 2:
                ts = parse_daily_timestamp(row[0])
                try:
                    price = float(row[1])
                    if ts:
                        prices.append({'timestamp': ts, 'price': price})
                except:
                    pass
    
    return prices


def load_historical_prices():
    """Load all prices from HistoricalMVPGold.csv"""
    prices = []
    if not os.path.exists(HISTORICAL_CSV_PATH):
        return prices
    
    with open(HISTORICAL_CSV_PATH, 'r', newline='') as csvfile:
        reader = csv.reader(csvfile)
        header = next(reader, None)
        
        for row in reader:
            if len(row) >= 5:
                ts = parse_historical_date(row[0])
                try:
                    price = float(row[4])
                    if ts:
                        prices.append({'timestamp': ts, 'price': price})
                except:
                    pass
    
    return prices


def generate_target_timestamps(timeframe, start_date, end_date, now):
    """Generate target timestamps based on timeframe."""
    targets = []
    
    if timeframe == '1D':
        today = now.replace(hour=0, minute=0, second=0, microsecond=0)
        hours = [0, 3, 6, 9, 12, 15, 18, 21, 24]
        
        for hour in hours:
            if hour == 24:
                target = today.replace(hour=23, minute=59, second=59)
            else:
                target = today.replace(hour=hour)
            
            is_future = target > now
            next_hour = hour + 3 if hour < 24 else 24
            next_target = today.replace(hour=min(next_hour, 23), minute=59 if next_hour >= 24 else 0, second=59 if next_hour >= 24 else 0)
            is_current_interval = (target <= now < next_target) if hour < 24 else False
            
            targets.append({
                'timestamp': target,
                'is_future': is_future,
                'is_current_interval': is_current_interval,
                'hour': hour
            })
    
    elif timeframe == '1W':
        for i in range(7, -1, -1):
            target = (now - timedelta(days=i)).replace(hour=12, minute=0, second=0, microsecond=0)
            targets.append({
                'timestamp': target,
                'is_future': False
            })
    
    else:
        total_seconds = (end_date - start_date).total_seconds()
        interval_seconds = total_seconds / 7
        
        for i in range(8):
            target = start_date + timedelta(seconds=interval_seconds * i)
            targets.append({
                'timestamp': target,
                'is_future': target > now
            })
    
    return targets


def find_closest_price(target_ts, all_prices, max_tolerance_days=None):
    """Find the price closest to the target timestamp."""
    if not all_prices:
        return None
    
    closest = None
    min_diff = float('inf')
    
    for p in all_prices:
        diff = abs((p['timestamp'] - target_ts).total_seconds())
        if diff < min_diff:
            min_diff = diff
            closest = p
    
    if max_tolerance_days and closest:
        if min_diff > (max_tolerance_days * 24 * 60 * 60):
            return None
    
    return closest


def interpolate_price(target_ts, all_prices):
    """Interpolate price at target timestamp based on surrounding data points."""
    if not all_prices:
        return None
    
    sorted_prices = sorted(all_prices, key=lambda x: x['timestamp'])
    
    before = None
    after = None
    
    for p in sorted_prices:
        if p['timestamp'] <= target_ts:
            before = p
        elif p['timestamp'] > target_ts and after is None:
            after = p
            break
    
    if before and after:
        total_diff = (after['timestamp'] - before['timestamp']).total_seconds()
        target_diff = (target_ts - before['timestamp']).total_seconds()
        
        if total_diff > 0:
            ratio = target_diff / total_diff
            interpolated_price = before['price'] + (after['price'] - before['price']) * ratio
            return {'timestamp': target_ts, 'price': interpolated_price, 'interpolated': True}
    
    if before:
        return {'timestamp': target_ts, 'price': before['price'], 'interpolated': True}
    
    if after:
        return {'timestamp': target_ts, 'price': after['price'], 'interpolated': True}
    
    return None


# ============== GOLD PRICE API ROUTES ==============

@app.route("/")
def home():
    """API root endpoint"""
    return jsonify({
        'name': 'VitaNova Gold API',
        'version': '2.0',
        'auth_enabled': AUTH_ENABLED,
        'endpoints': {
            'gold_price': {
                '/price': 'Get current gold price',
                '/price/history': 'Get historical price data',
                '/price/stats': 'Get price statistics'
            },
            'auth': {
                '/auth/register': 'Register new user',
                '/auth/login': 'Login user',
                '/auth/logout': 'Logout user',
                '/auth/me': 'Get current user',
                '/auth/check': 'Check authentication status',
                '/auth/verify-email/<token>': 'Verify email',
                '/auth/forgot-password': 'Request password reset',
                '/auth/reset-password/<token>': 'Reset password',
                '/auth/change-password': 'Change password (logged in)'
            } if AUTH_ENABLED else 'Authentication not enabled'
        }
    })


@app.route("/price")
def price():
    """Get current gold price from APISED and append to DailyGold.csv"""
    try:
        # APISED API request using http.client (as per their documentation)
        conn = http.client.HTTPSConnection(APISED_API_HOST, timeout=15)
        
        # Build query string with required parameters
        query_params = "metals=XAU&base_currency=AED&weight_unit=gram"
        full_endpoint = f"{APISED_API_ENDPOINT}?{query_params}"
        
        headers = {
            'x-api-key': APISED_API_KEY
        }
        
        print(f"📡 Fetching from APISED: https://{APISED_API_HOST}{full_endpoint}")
        
        conn.request("GET", full_endpoint, '', headers)
        res = conn.getresponse()
        
        print(f"📡 APISED Response Status: {res.status}")
        
        if res.status != 200:
            error_body = res.read().decode('utf-8')
            print(f"❌ APISED HTTP Error: {res.status} - {error_body}")
            return jsonify({"error": f"API returned status {res.status}: {error_body}"}), 500
        
        raw_data = res.read().decode('utf-8')
        print(f"📡 APISED Raw Response: {raw_data[:500]}...")
        
        data = json.loads(raw_data)
        conn.close()
        
        if data.get("status") == "error" or "error" in data:
            error_msg = data.get('message') or data.get('error') or 'Unknown error'
            print(f"❌ APISED Error: {error_msg}")
            return jsonify({"error": error_msg}), 500
        
        # APISED returns data in various formats, try to extract gold price
        gold_price = None
        
        # Try common APISED response structures
        # Structure 1: {"data": {"metal_prices": {"XAU": {"price": xxx}}}}
        if "data" in data and "metal_prices" in data.get("data", {}):
            xau_data = data["data"]["metal_prices"].get("XAU", {})
            gold_price = xau_data.get("price_gram_24k") or xau_data.get("price_24k") or xau_data.get("price")
        
        # Structure 2: {"metals": {"XAU": {"price": xxx}}}
        if gold_price is None and "metals" in data:
            xau_data = data["metals"].get("XAU", {})
            gold_price = xau_data.get("price_gram_24k") or xau_data.get("price_24k") or xau_data.get("price")
        
        # Structure 3: {"XAU": xxx} or {"gold": xxx}
        if gold_price is None:
            gold_price = data.get("XAU") or data.get("gold") or data.get("price")
        
        # Structure 4: {"data": {"XAU": xxx}}
        if gold_price is None and "data" in data:
            gold_price = data["data"].get("XAU") or data["data"].get("price")
        
        # Structure 5: Nested under different keys
        if gold_price is None:
            # Look for any XAU-related key at any level
            for key in ["XAU", "XAUAED", "gold_price", "gold"]:
                if key in data:
                    val = data[key]
                    if isinstance(val, dict):
                        gold_price = val.get("price") or val.get("price_gram_24k") or val.get("value")
                    else:
                        gold_price = val
                    if gold_price:
                        break
        
        if gold_price is None:
            print(f"❌ Could not extract price from APISED response: {data}")
            return jsonify({"error": "Could not extract price from API response", "raw_response": data}), 500
        
        # Ensure price is a number
        gold_price = float(gold_price)
        
        append_price_to_csv(gold_price)
        
        print(f"📊 APISED Response:")
        print(f"   - Price per gram (24k AED): {gold_price:.2f} AED")
        
        return jsonify({
            "price": round(gold_price, 2),
            "timestamp": datetime.now().isoformat(),
            "currency": "AED",
            "unit": "gram",
            "karat": "24k",
            "source": "gold.g.apised.com"
        })
    except http.client.HTTPException as e:
        print(f"❌ APISED HTTP Exception: {e}")
        return jsonify({"error": f"HTTP error: {str(e)}"}), 500
    except TimeoutError:
        print(f"❌ APISED Timeout")
        return jsonify({"error": "API request timed out"}), 500
    except ConnectionError as e:
        print(f"❌ APISED Connection Error: {e}")
        return jsonify({"error": f"Connection error: {str(e)}"}), 500
    except Exception as e:
        print(f"❌ Error fetching price: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500


@app.route("/price/history")
def price_history():
    """Get historical price data for charts from CSV files."""
    timeframe = request.args.get('timeframe', '1D')
    
    start_date_param = request.args.get('start_date')
    end_date_param = request.args.get('end_date')
    
    now = datetime.now()
    
    if timeframe == 'CUSTOM' and start_date_param and end_date_param:
        try:
            start_date = datetime.fromisoformat(start_date_param.replace('Z', '').replace('+00:00', ''))
            start_date = start_date.replace(hour=0, minute=0, second=0, microsecond=0)
            
            end_date = datetime.fromisoformat(end_date_param.replace('Z', '').replace('+00:00', ''))
            end_date = end_date.replace(hour=23, minute=59, second=59, microsecond=999999)
            
            if end_date > now:
                end_date = now
        except Exception as e:
            print(f"Date parsing error: {e}")
            start_date = datetime(2000, 1, 1)
            end_date = now
    elif timeframe == '1D':
        start_date = now.replace(hour=0, minute=0, second=0, microsecond=0)
        end_date = now
    elif timeframe == '1W':
        start_date = (now - timedelta(days=7)).replace(hour=0, minute=0, second=0, microsecond=0)
        end_date = now
    else:
        ranges = {
            '1M': now - timedelta(days=30),
            '6M': now - timedelta(days=180),
            '1Y': now - timedelta(days=365),
            '5Y': now - timedelta(days=365*5),
            '15Y': now - timedelta(days=365*15)
        }
        start_date = ranges.get(timeframe, ranges['1M'])
        end_date = now
    
    historical = load_historical_prices()
    daily = load_daily_prices()
    all_prices = historical + daily
    all_prices.sort(key=lambda x: x['timestamp'])
    
    targets = generate_target_timestamps(timeframe, start_date, end_date, now)
    
    result_data = []
    
    for target_info in targets:
        target_ts = target_info['timestamp']
        is_future = target_info['is_future']
        
        if timeframe == '1D':
            is_current_interval = target_info.get('is_current_interval', False)
            hour = target_info.get('hour', 0)
            
            if is_future:
                result_data.append({
                    'timestamp': target_ts.isoformat(),
                    'price': None,
                    'is_fixed_point': True
                })
            else:
                closest = find_closest_price(target_ts, all_prices)
                if closest:
                    result_data.append({
                        'timestamp': target_ts.isoformat(),
                        'price': round(closest['price'], 2),
                        'actual_timestamp': closest['timestamp'].isoformat(),
                        'is_fixed_point': True
                    })
                else:
                    interpolated = interpolate_price(target_ts, all_prices)
                    if interpolated:
                        result_data.append({
                            'timestamp': target_ts.isoformat(),
                            'price': round(interpolated['price'], 2),
                            'interpolated': True,
                            'is_fixed_point': True
                        })
                    else:
                        result_data.append({
                            'timestamp': target_ts.isoformat(),
                            'price': None,
                            'is_fixed_point': True
                        })
                
                current_minute = now.minute
                current_second = now.second
                is_exactly_on_interval = (current_minute == 0 and current_second == 0)
                
                if is_current_interval and not is_exactly_on_interval:
                    latest_price = find_closest_price(now, all_prices)
                    if latest_price:
                        result_data.append({
                            'timestamp': now.isoformat(),
                            'price': round(latest_price['price'], 2),
                            'is_current_time': True,
                            'is_fixed_point': False
                        })
        else:
            if is_future:
                continue
            
            closest = find_closest_price(target_ts, all_prices)
            if closest:
                result_data.append({
                    'timestamp': target_ts.isoformat(),
                    'price': round(closest['price'], 2),
                    'actual_timestamp': closest['timestamp'].isoformat()
                })
            else:
                interpolated = interpolate_price(target_ts, all_prices)
                if interpolated:
                    result_data.append({
                        'timestamp': target_ts.isoformat(),
                        'price': round(interpolated['price'], 2),
                        'interpolated': True
                    })
    
    period_change = None
    period_change_percent = None
    
    valid_prices = [p for p in result_data if p.get('price') is not None]
    
    if len(valid_prices) >= 2:
        first_price = valid_prices[0]['price']
        last_price = valid_prices[-1]['price']
        period_change = last_price - first_price
        period_change_percent = (period_change / first_price) * 100 if first_price != 0 else 0
    elif len(valid_prices) == 1:
        period_change = 0
        period_change_percent = 0
    
    expected_points = CHART_DATA_POINTS_1D if timeframe == '1D' else CHART_DATA_POINTS
    
    return jsonify({
        'timeframe': timeframe,
        'count': len(result_data),
        'expected_points': expected_points,
        'start_date': start_date.isoformat(),
        'end_date': end_date.isoformat(),
        'period_change': round(period_change, 2) if period_change is not None else None,
        'period_change_percent': round(period_change_percent, 2) if period_change_percent is not None else None,
        'data': result_data
    })


@app.route("/price/stats")
def price_stats():
    """Get price statistics from CSV data"""
    daily_prices = load_daily_prices()
    
    if not daily_prices:
        return jsonify({
            'current': None,
            'today_high': None,
            'today_low': None,
            'change': None,
            'change_percent': None
        })
    
    today_start = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
    today_prices = [p for p in daily_prices if p['timestamp'] >= today_start]
    
    yesterday_start = today_start - timedelta(days=1)
    yesterday_prices = [p for p in daily_prices if yesterday_start <= p['timestamp'] < today_start]
    
    current = daily_prices[-1]['price'] if daily_prices else None
    
    today_high = max(p['price'] for p in today_prices) if today_prices else current
    today_low = min(p['price'] for p in today_prices) if today_prices else current
    
    yesterday_close = yesterday_prices[-1]['price'] if yesterday_prices else None
    
    change = None
    change_percent = None
    if current and yesterday_close:
        change = current - yesterday_close
        change_percent = (change / yesterday_close) * 100
    
    return jsonify({
        'current': current,
        'today_high': today_high,
        'today_low': today_low,
        'change': round(change, 2) if change else None,
        'change_percent': round(change_percent, 2) if change_percent else None
    })


# ============== MAIN ==============

if __name__ == "__main__":
    print("🚀 Starting VitaNova Gold Price API Server...")
    print(f"📁 Daily prices CSV: {DAILY_CSV_PATH}")
    print(f"📁 Historical prices CSV: {HISTORICAL_CSV_PATH}")
    print(f"🔑 Using APISED Gold API (gold.g.apised.com)")
    print(f"📊 Chart data points: {CHART_DATA_POINTS} (8 for most, 9 for 1D)")
    
    # Show last logged historical month
    last_month = get_last_logged_historical_month()
    print(f"🗓️ Last historical month logged: {last_month or 'None'}")
    print(f"🗓️ Monthly historical logging: ENABLED (logs on 1st of each month)")
    print(f"   USD/AED rate: {USD_TO_AED_RATE}")
    print(f"   Grams per oz: {GRAMS_PER_OUNCE}")
    
    if AUTH_ENABLED:
        print("🔐 Authentication endpoints available at /auth/*")
    
    if ORDERS_ENABLED:
        print("📦 Orders endpoints available at /orders/*")
    
    print("✅ Server ready on http://127.0.0.1:5000")
    print("\n📍 Gold Price Endpoints:")
    print("  GET  /price - Fetch current price from APISED")
    print("  GET  /price/history?timeframe=1D - Get chart data points")
    print("  GET  /price/stats - Get today's statistics")
    
    if ORDERS_ENABLED:
        print("\n📦 Order Management Endpoints:")
        print("  POST /orders/create - Create new order(s) and save to CSV")
        print("  GET  /orders/customer/<customer_id> - Get all orders for a customer")
    
    if AUTH_ENABLED:
        print("\n🔐 Authentication Endpoints:")
        print("  POST /auth/register - Register new user")
        print("  POST /auth/login - Login user")
        print("  POST /auth/logout - Logout user")
        print("  GET  /auth/me - Get current user info")
        print("  GET  /auth/check - Check auth status")
    
    port = int(os.environ.get('PORT', 8080))
    app.run(host="0.0.0.0", port=port)