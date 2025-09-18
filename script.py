import requests
import os
import csv
from dotenv import load_dotenv

load_dotenv()

POLYGON_API_KEY = os.getenv("POLYGON_API_KEY")
LIMIT = 1000
url = f'https://api.polygon.io/v3/reference/tickers?market=stocks&active=true&order=asc&limit={LIMIT}&sort=ticker&apiKey={POLYGON_API_KEY}'

response = requests.get(url)
tickers = []
data = response.json()

# Check if the response is successful and has results
if response.status_code == 200 and 'results' in data:
    for ticker in data['results']:
        tickers.append(ticker)
else:
    print(f"Error in initial request: {response.status_code}")
    print(f"Response: {data}")
    exit(1)

while 'next_url' in data:
    print('requesting next page', data['next_url'])
    response = requests.get(data['next_url'] + f'&apiKey={POLYGON_API_KEY}')
    data = response.json()

    # Check if the response is successful and has results
    if response.status_code == 200 and 'results' in data:
        for ticker in data['results']:
            tickers.append(ticker)
    else:
        print(f"Error in pagination request: {response.status_code}")
        print(f"Response: {data}")
        break


example_ticker = {'ticker': 'HTUS', 'name': 'Hull Tactical US ETF', 'market': 'stocks', 'locale': 'us', 'primary_exchange': 'BATS', 'type': 'ETF', 'active': True, 'currency_name': 'usd', 'cik': '0001452937', 'composite_figi': 'BBG01GVX6Q02', 'share_class_figi': 'BBG01GVX6QV8', 'last_updated_utc': '2025-09-18T06:05:34.657275514Z'}

print(len(tickers))

# Write tickers to CSV file
csv_filename = 'tickers.csv'
fieldnames = list(example_ticker.keys())

with open(csv_filename, 'w', newline='', encoding='utf-8') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(tickers)

print(f"Successfully wrote {len(tickers)} tickers to {csv_filename}")









