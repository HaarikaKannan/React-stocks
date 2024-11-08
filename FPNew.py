import os
import mysql.connector
import pandas as pd

from datetime import datetime, timedelta
from decimal import Decimal
from fyers_apiv3.FyersWebsocket import data_ws
from flask import Flask, jsonify
from flask_cors import CORS



# Flask app setup
app = Flask(__name__)
CORS(app)

stock_data_dict = {}

stock_data_list = []

# Database configuration
db_config = {
    'user': 'root',
    'password': 'root',
    'host': 'localhost',
    'database': 'stock_data'
}

# Path to Excel file with symbols
excel_file_path = "C:\\Users\\Haarika\\Downloads\\nsedata\\Stock_symbol.xlsx"

# Load symbols from Excel
def load_symbols_from_excel(file_path):
    try:
        df = pd.read_excel(file_path)
        symbols = df['Symbol'].apply(lambda x: f"NSE:{x}-EQ").tolist()  # Format as needed
        return symbols
    except Exception as e:
        print("Error loading symbols from Excel:", e)
        return []

# Validate symbols by sending a test API request (replace with actual Fyers validation API call if available)
def validate_symbols(symbols):
    valid_symbols = []
    for symbol in symbols:
        response = {'s': 'ok'}  # Replace with actual API call to validate symbol
        if response['s'] == 'ok':
            valid_symbols.append(symbol)
        else:
            print(f"Invalid symbol removed: {symbol}")
    return valid_symbols

# Store stock data in MySQL
def store_stock_data(symbol, ltp, timestamp):
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT INTO stock_prices (symbol, ltp, timestamp)
            VALUES (%s, %s, %s)
        """, (symbol, ltp, timestamp))
        
        conn.commit()
        cursor.close()
        conn.close()
    except mysql.connector.Error as err:
        print("Error storing data in MySQL:", err)

# Retrieve 5-minute and 10-minute values from MySQL
def fetch_past_values_5(symbol, lower_bound_str,upper_bound_str):
    five_min_ago, ten_min_ago = None, None
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor(dictionary=True)
        

       
        # 5-minute ago data
        cursor.execute("""
            SELECT ltp
            FROM stock_prices
            WHERE symbol = %s
            AND timestamp BETWEEN %s AND %s
            ORDER BY timestamp DESC
            LIMIT 1;
            
        """, (symbol, lower_bound_str,upper_bound_str))
        result = cursor.fetchone()
        if result and isinstance(result['ltp'], Decimal):
            five_min_ago = float(result['ltp'])
        else:
            five_min_ago = result['ltp'] if result else None


        
        cursor.close()
        conn.close()
    except mysql.connector.Error as err:
        print("Error fetching past values from MySQL:", err)

    return five_min_ago

def fetch_past_values_10(symbol, timestamp):
    five_min_ago, ten_min_ago = None, None
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor(dictionary=True)
        
        # 10-minute ago data
        cursor.execute("""
            SELECT ltp FROM stock_prices
            WHERE symbol = %s AND timestamp >= %s - INTERVAL 10 MINUTE
            ORDER BY timestamp ASC LIMIT 1
        """, (symbol, timestamp))
        result = cursor.fetchone()
        if result and isinstance(result['ltp'], Decimal):
            ten_min_ago = float(result['ltp'])
        else:
            ten_min_ago = result['ltp'] if result else None

        
        cursor.close()
        conn.close()
    except mysql.connector.Error as err:
        print("Error fetching past values from MySQL:", err)

    return ten_min_ago

# Handle WebSocket message
def onmessage(message):
    if 'symbol' in message and 'ltp' in message:
        symbol = message['symbol']
        ltp = float(message['ltp'])
        timestamp = datetime.now()

        # Store data in MySQL
        store_stock_data(symbol, ltp, timestamp)
        
         # Calculate the lower and upper bounds for 5 minutes ago ± 30 seconds
        lower_bound = timestamp - timedelta(minutes=5, seconds=30)
        upper_bound = timestamp - timedelta(minutes=5, seconds=-30)

        # Convert datetime to string to use in SQL query
        lower_bound_str = lower_bound.strftime('%Y-%m-%d %H:%M:%S')
        upper_bound_str = upper_bound.strftime('%Y-%m-%d %H:%M:%S')

        # Fetch past values from MySQL
        five_min_ago = fetch_past_values_5(symbol,lower_bound_str,upper_bound_str)
        ten_min_ago = fetch_past_values_10(symbol, timestamp)

        # Calculate percentage change
        five_min_change = round(((ltp - five_min_ago) / five_min_ago) * 100, 2) if five_min_ago else 'NA'
        ten_min_change = round(((ltp - ten_min_ago) / ten_min_ago) * 100, 2) if ten_min_ago else 'NA'

        # Append to list for API response
        stock_data_dict[symbol] = {
            "timestamp": timestamp.strftime('%Y-%m-%d %H:%M:%S'),
            "symbol": symbol,
            "current_ltp": ltp,
            "five_min_ago_ltp": five_min_ago or 'NA',
            "ten_min_ago_ltp": ten_min_ago or 'NA',
            "five_min_change": five_min_change,
            "ten_min_change": ten_min_change
        }

# WebSocket error handling
def onerror(message):
    print("Error:", message)

def onclose(message):
    print("Connection closed:", message)

def onopen(valid_symbols):
    fyers.subscribe(symbols=valid_symbols, data_type="SymbolUpdate")
    fyers.keep_running()

# Load and validate symbols
symbols = load_symbols_from_excel(excel_file_path)
validated_symbols = validate_symbols(symbols)

# WebSocket setup if there are valid symbols
if validated_symbols:
    access_token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJhcGkuZnllcnMuaW4iLCJpYXQiOjE3MzA5NTE2NzgsImV4cCI6MTczMTAyNTgzOCwibmJmIjoxNzMwOTUxNjc4LCJhdWQiOlsieDowIiwieDoxIiwieDoyIiwiZDoxIiwiZDoyIiwieDoxIiwieDowIl0sInN1YiI6ImFjY2Vzc190b2tlbiIsImF0X2hhc2giOiJnQUFBQUFCbkxEbi1zanN0b2ZJZDdLWk96NU5uQmxIT2luNENRdnVVN01NMkktZzFodXgteDZPR1BNVG4taE5heGg2MWJRV05rRDhmbF85RkRNTzBnRndCM1Rkb3NaWG81VFdET0NEY3FWUjAxWjBGRHdHQk1qRT0iLCJkaXNwbGF5X25hbWUiOiJOIE0gTklUSElOIEtSSVNITkEiLCJvbXMiOiJLMSIsImhzbV9rZXkiOiIwYjE1Y2U3MzRlOTEwNTYyNmU0MjFhNTdlODMxMWY0ZDY5ZGJhYmE3NTE3ZjcwMmNkYzI0Nzk5OCIsImZ5X2lkIjoiRk4wOTQzIiwiYXBwVHlwZSI6MTAwLCJwb2FfZmxhZyI6Ik4ifQ.Qx1YnNxJyaUZTlSZeU-t6NifArdRAXtQmkyygNk64og"
    fyers = data_ws.FyersDataSocket(
        access_token=access_token,
        log_path=os.path.join(os.getcwd(), "fyers_logs"),
        litemode=False,
        write_to_file=False,
        reconnect=True,
        on_connect=lambda: onopen(validated_symbols),
        on_close=onclose,
        on_error=onerror,
        on_message=onmessage
    )
    fyers.connect()

# Flask route to get stock data
@app.route('/api/stocks', methods=['GET'])
def get_stock_data():
    return jsonify(list(stock_data_dict.values()))

if __name__ == "__main__":
    gunicorn -w 4 -b 0.0.0.0:5000 app:app

   # app.run(debug=True)

