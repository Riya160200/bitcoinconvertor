import requests
import matplotlib.pyplot as plt
from datetime import datetime, timedelta

# Replace 'your_api_key' with your actual API key
api_key = 'd09e9b9f586178c0494eddbd179f070b'
currency1 = 'USD'
currency2 = 'EUR'

# Function to fetch exchange rate data from API
def fetch_exchange_rate(api_key, currency1, currency2, start_date, end_date):
    url = f'https://api.exchangerate.host/timeseries?start_date={start_date}&end_date={end_date}&base={currency1}&symbols={currency2}'
    response = requests.get(url)
    data = response.json()
    return data['rates']

# Define the date range for the data
end_date = datetime.today().strftime('%Y-%m-%d')
start_date = (datetime.today() - timedelta(days=30)).strftime('%Y-%m-%d')

# Fetch the exchange rate data
exchange_rates = fetch_exchange_rate(api_key, currency1, currency2, start_date, end_date)

# Extract dates and rates for plotting
dates = list(exchange_rates.keys())
rates = [exchange_rates[date][currency2] for date in dates]

# Plotting the data
plt.figure(figsize=(10, 5))
plt.plot(dates, rates, marker='o', linestyle='-', color='b')
plt.title(f'Exchange Rate: {currency1} to {currency2}')
plt.xlabel('Date')
plt.ylabel('Exchange Rate')
plt.grid(True)
plt.xticks(rotation=45)
plt.tight_layout()

# Show the plot
plt.show()
