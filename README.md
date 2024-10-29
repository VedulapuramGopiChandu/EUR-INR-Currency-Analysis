# EUR-INR-Currency-Analysis

## Overview
The EUR-INR Analysis App is a web application built using Streamlit that allows users to analyze stock data, calculate technical indicators, and generate trading signals. The application fetches currency data from Yahoo Finance and visualizes it using various technical analysis tools.

## Features
- Fetch currency data for specified stock symbols.
- Calculate technical indicators: 
  - 20-day Moving Average (MA)
  - Bollinger Bands
  - Commodity Channel Index (CCI)
- Generate trading signals based on the calculated indicators.
- Interactive visualizations of the stock data and indicators.

## Technologies Used
- **Python**: Programming language.
- **Streamlit**: Web application framework for data visualization.
- **yfinance**: Library to fetch stock data from Yahoo Finance.
- **pandas**: Data manipulation and analysis library.
- **numpy**: Library for numerical operations.
- **ta**: Technical analysis library for financial data.
- **matplotlib**: Plotting library for visualizing data.

## Installation

### Prerequisites
- Python 3.x installed on your machine.

### Setup
### 1. Clone this repository:
   
   git clone https://github.com/VedulapuramGopiChandu/EUR-INR-Currency-Analysis.git
   
   cd EUR-INR-Currency-Analysis

   
### 2.Install the required packages

pip install -r requirements.txt


### 3.Run the application:

streamlit run app.py


### 4.Open your web browser and go to http://localhost:8501 to access the app.

Usage
Enter a stock symbol (e.g., EURINR=X) in the input box.
Click the "Analyze" button to fetch data and generate analysis.
View the technical indicators and trading signals displayed on the screen.


## Acknowledgments
Thanks to Yahoo Finance for providing financial data.
Thanks to Streamlit for making it easy to create interactive web applications.
