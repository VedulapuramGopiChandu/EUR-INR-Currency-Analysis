import yfinance as yf
import pandas as pd
import numpy as np
from ta.trend import CCIIndicator
from ta.volatility import BollingerBands
import matplotlib.pyplot as plt
import streamlit as st
from datetime import datetime, timedelta
import io

def fetch_currency_data(symbol):
    """
    Fetch currency data from Yahoo Finance
    """
    start_date = "2023-01-01"
    end_date = "2024-09-30"
    df = yf.download(symbol, start=start_date, end=end_date)
    return df

def calculate_indicators(df):
    """
    Calculate technical indicators: Moving Average, Bollinger Bands, and CCI
    """
    df['MA20'] = df['Close'].rolling(window=20).mean()
    
    # Calculate Bollinger Bands
    indicator_bb = BollingerBands(close=df["Close"], window=20, window_dev=2)
    df['BB_upper'] = indicator_bb.bollinger_hband()
    df['BB_middle'] = indicator_bb.bollinger_mavg()
    df['BB_lower'] = indicator_bb.bollinger_lband()
    
    # Calculate CCI
    indicator_cci = CCIIndicator(high=df["High"], low=df["Low"], close=df["Close"], window=20)
    df['CCI'] = indicator_cci.cci()
    
    return df

def generate_signals(df):
    """
    Generate trading signals based on technical indicators
    """
    signals = pd.DataFrame(index=['1 Day', '1 Week'])
    
    last_day = df.iloc[-1]
    last_week = df.iloc[-5:]

    # Moving Average Signals
    signals['MA_Signal'] = 'NEUTRAL'
    signals.loc['1 Day', 'MA_Signal'] = 'BUY' if last_day['Close'] > last_day['MA20'] else 'SELL' if last_day['Close'] < last_day['MA20'] else 'NEUTRAL'
    signals.loc['1 Week', 'MA_Signal'] = 'BUY' if last_week['Close'].mean() > last_week['MA20'].mean() else 'SELL' if last_week['Close'].mean() < last_week['MA20'].mean() else 'NEUTRAL'
    
    # Bollinger Bands Signals
    signals['BB_Signal'] = 'NEUTRAL'
    signals.loc['1 Day', 'BB_Signal'] = 'BUY' if last_day['Close'] < last_day['BB_lower'] else 'SELL' if last_day['Close'] > last_day['BB_upper'] else 'NEUTRAL'
    signals.loc['1 Week', 'BB_Signal'] = 'BUY' if last_week['Close'].mean() < last_week['BB_lower'].mean() else 'SELL' if last_week['Close'].mean() > last_week['BB_upper'].mean() else 'NEUTRAL'
    
    # CCI Signals
    signals['CCI_Signal'] = 'NEUTRAL'
    signals.loc['1 Day', 'CCI_Signal'] = 'BUY' if last_day['CCI'] < -100 else 'SELL' if last_day['CCI'] > 100 else 'NEUTRAL'
    signals.loc['1 Week', 'CCI_Signal'] = 'BUY' if last_week['CCI'].mean() < -100 else 'SELL' if last_week['CCI'].mean() > 100 else 'NEUTRAL'
    
    return signals

def plot_indicators(df):
    """
    Create plots for technical indicators
    """
    plt.figure(figsize=(15, 10))
    
    # Price with Moving Average and Bollinger Bands
    plt.subplot(2, 1, 1)
    plt.plot(df.index, df['Close'], label='Price', alpha=0.7)
    plt.plot(df.index, df['MA20'], label='20-day MA', alpha=0.7)
    plt.plot(df.index, df['BB_upper'], label='BB Upper', alpha=0.7)
    plt.plot(df.index, df['BB_lower'], label='BB Lower', alpha=0.7)
    plt.title('Price with MA and Bollinger Bands')
    plt.legend()
    plt.grid(True)

    # CCI
    plt.subplot(2, 1, 2)
    plt.plot(df.index, df['CCI'], label='CCI', color='purple')
    plt.axhline(y=100, color='r', linestyle='--', alpha=0.5)
    plt.axhline(y=-100, color='g', linestyle='--', alpha=0.5)
    plt.title('Commodity Channel Index (CCI)')
    plt.legend()
    plt.grid(True)

    # Save plot to a BytesIO object
    img_buffer = io.BytesIO()
    plt.tight_layout()
    plt.savefig(img_buffer, format='png')
    img_buffer.seek(0)
    plt.close()
    return img_buffer

def main():
    st.title("Stock Analysis App")
    
    # Input for stock symbol
    stock_symbol = st.text_input("Enter Stock Symbol (e.g., EURINR=X):", "EURINR=X")

    if st.button("Analyze"):
        # Fetch data
        df = fetch_currency_data(stock_symbol)
        
        if df.empty:
            st.error("No data found for the provided symbol.")
            return
        
        # Calculate indicators
        df = calculate_indicators(df)

        # Generate signals
        signals = generate_signals(df)

        # Plot indicators
        plot_img = plot_indicators(df)
        
        # Display plot
        st.image(plot_img, caption='Technical Indicators')

        # Display signals
        st.write("### Trading Signals")
        st.dataframe(signals)

if __name__ == "__main__":
    main()
