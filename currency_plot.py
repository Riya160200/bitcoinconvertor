import requests
import pandas as pd
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np

# Function to fetch exchange rates from ExchangeRate-API
def get_exchange_rates(api_key, base_currency, target_currencies):
    url = f"https://v6.exchangerate-api.com/v6/{api_key}/latest/{base_currency}"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        if data['result'] == 'success':
            rates = data['conversion_rates']
            # Filter only the target currencies
            filtered_rates = {currency: rates.get(currency) for currency in target_currencies}
            return filtered_rates
        else:
            print("Error: Invalid response from the API.")
            return {}
    else:
        print(f"Error: Failed to fetch data (Status Code: {response.status_code})")
        return {}

# Define your API key and other parameters
api_key = 'adccf6fba77803b80b484db2'  # Replace with your actual API key
base_currency = 'USD'  # Change to any base currency you prefer
target_currencies = ['EUR', 'GBP', 'INR', 'AUD', 'CAD', 'JPY']  # List of target currencies

# Fetch the exchange rates
exchange_rates = get_exchange_rates(api_key, base_currency, target_currencies)

# Check if we received any valid exchange rates
if exchange_rates:
    # Convert the exchange rates to a pandas DataFrame
    rates_df = pd.DataFrame.from_dict(exchange_rates, orient='index', columns=['Exchange Rate'])
    rates_df.index.name = 'Currency'

    # Reverse the exchange rates: stronger currencies have lower values for 1 USD
    rates_df['Strength'] = 1 / rates_df['Exchange Rate']  # Inverse to show strength

    # Sort the DataFrame by strength (highest strength at the top)
    rates_df = rates_df.sort_values('Strength', ascending=False)

    # 3D Bar Plot with animation
    fig = plt.figure(figsize=(10, 6))
    ax = fig.add_subplot(111, projection='3d')

    # Prepare data for 3D plot
    x = np.arange(len(rates_df))
    y = np.zeros_like(x)  # Base level for bars
    z = np.zeros_like(x)  # Z-axis (height)

    # Set the bar heights based on strength (higher for stronger currencies)
    dx = np.ones_like(x)  # Bar width in the x direction
    dy = np.ones_like(x)  # Bar depth in the y direction
    dz = rates_df['Strength'].values  # Bar heights based on strength

    # Bar colors (optional, customize as needed)
    colors = plt.cm.viridis(np.linspace(0, 1, len(rates_df)))

    # Create 3D bars
    ax.bar3d(x, y, z, dx, dy, dz, color=colors)

    # Set axis labels and title
    ax.set_xlabel('Currencies')
    ax.set_ylabel('Y')
    ax.set_zlabel('Strength')
    ax.set_title(f'3D Currency Strength Comparison for 1 {base_currency}')

    # Set the x-ticks to currency names
    ax.set_xticks(x)
    ax.set_xticklabels(rates_df.index, rotation=45)

    # Add simple animation to rotate the 3D plot
    def update_rotation(i):
        ax.view_init(elev=20, azim=i)

    # Animation loop
    for i in range(360):
        update_rotation(i)
        plt.pause(0.01)

    plt.show()

else:
    print("No valid exchange rates were fetched.")


