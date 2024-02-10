from binance.client import Client # pip install python-binance
from binance.enums import *
import pandas as pd # pip install pandas
import numpy as np # pip install numpy
import os

API_KEY = os.getenv('API_KEY')
API_SECRET = os.getenv('API_SECRET')

# Configs for DEMO Account
client = Client(api_key=API_KEY, api_secret=API_SECRET, testnet=True)

# Function to fetch candlestick data:
def fetch_data(symbol, interval, lookback):
    bars = client.futures_historical_klines(symbol, interval, lookback)
    df = pd.DataFrame(bars, columns=['timestamp', 'open', 'high', 'low', 'close'])
    df['close'] = pd.to_numeric(df['close'])
    df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
    return df[['timestamp', 'close']] # We return only what we'll need from the data

# Main strategy logic & execution 👇
def sma_strategy(symbol='BTCUSDT', interval='1h', short_window=50, long_window=200, lookback='30 days ago UTC'):
    data = fetch_data(symbol, interval, lookback)
    
    data['short_sma'] = data['close'].rolling(window=short_window).mean()
    data['long_sma'] = data['close'].rolling(window=long_window).mean()
    
    # Assuming you're starting without an open position
    in_position = False

    # Check for SMA crossover
    # If SMA crosses LMA Going short on the crypto)👇
    if data['short_sma'].iloc[-2] < data['long_sma'].iloc[-2] and data['short_sma'].iloc[-1] > data['long_sma'].iloc[-1]:

        if not in_position:
            print("Signal to BUY!")
            order = client.futures_create_order(symbol=symbol, side='BUY', type='MARKET', quantity=0.01)
            in_position = True
            print(order)

    # If LMA crosses SMA (Going short on the crypto) 👇  
    elif data['short_sma'].iloc[-2] > data['long_sma'].iloc[-2] and data['short_sma'].iloc[-1] < data['long_sma'].iloc[-1]:

        if in_position:
            print("Signal to SELL!")
            order = client.futures_create_order(symbol=symbol, side='SELL', type='MARKET', quantity=0.01)
            in_position = False
            

if __name__ == '__main__':
    sma_strategy()