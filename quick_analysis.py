
import requests
import pandas as pd
import numpy as np


# Replace with your Alpha Vantage API key
api_key = 'G7596RFIB04K5Y5R' #Input - Current demo key will work: Type personal APIKEY if software needed for large-scale calculations
symbol = 'COF' #<--Input: Type ticker symbol
risk_free_rate = 0.04178 / 12 #<--Input: Type country riskfree rate
equity_risk_premium = 0.0407 / 12 #<--Input: Type ticker equity risk premium
beta = 1.43 #<--Input: Type ticker beta
function = 'TIME_SERIES_MONTHLY_ADJUSTED'

# Construct the API URL
url = f'https://www.alphavantage.co/query?function={function}&symbol={symbol}&apikey={api_key}'

# Make the API request
response = requests.get(url)
data = response.json()

# Extract the time series data
time_series = data['Monthly Adjusted Time Series']

# Convert to a pandas DataFrame
df = pd.DataFrame.from_dict(time_series, orient='index', dtype=float)
df.index = pd.to_datetime(df.index)
df.sort_index(inplace=True)

# Extract the 'close' column and filter the last 10 years
df = df[['4. close']]  # Select only the close price
df = df.loc[df.index >= pd.Timestamp.now() - pd.DateOffset(years=10)]  # Filter for the last 10 years

# Rename column for clarity
df.rename(columns={'4. close': 'Close'}, inplace=True)

#Return column
df['Return'] = df['Close'].pct_change()

# Sharpe Ratio
mean_return = df['Return'].mean()  
variance = df['Return'].std()**2
sharpe_ratio = (mean_return - risk_free_rate) / variance
print(f'Sharpe Ratio: {sharpe_ratio}')

# Treynor Ratio
treynor_ratio = (mean_return - risk_free_rate) / beta
print(f'Treynor Ratio: {treynor_ratio}')

#Alpha
alpha = mean_return - (risk_free_rate + beta * (equity_risk_premium))
print(f'Alpha: {alpha}')
