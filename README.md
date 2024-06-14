# Crypto Price Checker

## Overview

This project is a cryptocurrency price checking application that fetches data from CoinMarketCap for various cryptocurrencies. It extracts and displays key information such as **price**, **24-hour trading volume**, and percentage changes over different time periods.

## User Interface

![User_interface](https://github.com/Oljake/Stocks-app/assets/109909586/42b20b3c-9d83-47b8-9c71-a0b3cb2969aa)

## Settings menu

![Settings_menu](https://github.com/Oljake/Stocks-app/assets/109909586/22daf1c5-ebde-438e-858e-8a2e3f327632)

## Files

- **crypto_names.json**: Contains a list of cryptocurrency names to monitor.
- **current_holdings.json**: Placeholder for storing user's current holdings of cryptocurrencies.
- **settings.json**: Configuration file for customizing the display format of cryptocurrency data.

### Python Scripts

- **user_interface.py**: Runs the main application. It fetches cryptocurrency prices from the web and logs them according to settings specified in `settings.json`. Additional information displayed includes **24-hour trading volume**, **price**, **24 hours**, **7 days**, and **30 days**.

- **new_coin.py**: Allows users to update `crypto_names.json` by adding new cryptocurrency names. It ensures that duplicate names are not added to the file.

- **get_data.py**: Retrieves cryptocurrency data from CoinMarketCap using web scraping techniques. It extracts **price**, **24-hour trading volume**, and percentage changes over **24 hours**, **7 days**, and **30 days**. Ensure the script is configured to match the structure of the actual website providing cryptocurrency data.

## Usage

1. **Setup**: Ensure `crypto_names.json`, `current_holdings.json`, and `settings.json` are correctly populated with initial data.

2. **Run Application**: Execute `user_interface.py` to start the application. It will fetch data from CoinMarketCap and log it based on the settings configured in `settings.json`.

### Adding New Cryptocurrencies

To add new cryptocurrency names to `crypto_names.json`, use **new_coin.py**. This script ensures that each cryptocurrency name is unique to avoid duplication in the list.

### Adding and Removing Cryptocurrencies in the App

In the application (**user_interface.py**), you can dynamically add or remove cryptocurrencies using a user interface. Here's how it works:

1. **Adding Cryptocurrencies**:
   - Type the cryptocurrency name into the first entry field.
   - Enter the amount in the second entry field.
   - Click on the "Add" button to add the cryptocurrency with the specified amount to your holdings.

2. **Removing Cryptocurrencies**:
   - Similarly, type the cryptocurrency name into the first entry field.
   - Enter the amount in the second entry field (typically as a negative value to indicate removal).
   - Click on the "Remove" button to adjust your holdings by removing the specified amount of the cryptocurrency.

These features allow for easy management and updating of your cryptocurrency holdings directly within the application interface.

## Dependencies

- Python 3.x
- Libraries: [requests](https://pypi.org/project/requests/) (for fetching data from URLs), [Beautiful Soup](https://pypi.org/project/beautifulsoup4/) (for HTML parsing)

## Notes

- Ensure internet connectivity for fetching live cryptocurrency data from CoinMarketCap.
- Use **new_coin.py** and **get_data.py** responsibly and in compliance with the terms of service of CoinMarketCap or any other website from which data is fetched.
