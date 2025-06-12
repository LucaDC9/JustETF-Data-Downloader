import requests
import pandas as pd
import time
import os
from tqdm import tqdm

ETF_LIST = [
    {"ISIN": "IE00BHZRQZ17", "Ticker": "FLXI"},
    {"ISIN": "IE00B6YX5C33", "Ticker": "SPY5"},
    {"ISIN": "IE000YU9K6K2", "Ticker": "JEDI"}
]

DATE_FROM = "2010-01-01"
DATE_TO = "2025-06-12"

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                  'AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/114.0.0.0 Safari/537.36',
    'accept': 'application/json, text/plain, */*'
}

def fetch_etf_data(ISIN, Ticker, max_retries=3):
    url = f"https://www.justetf.com/api/etfs/{ISIN}/performance-chart"
    params = {
        'locale': 'en',
        'currency': 'EUR',
        'valuesType': 'MARKET_VALUE',
        'reduceData': 'false',
        'includeDividends': 'false',
        'features': 'DIVIDENDS',
        'dateFrom': DATE_FROM,
        'dateTo': DATE_TO
    }
    HEADERS['referer'] = f'https://www.justetf.com/en/etf-profile.html?ISIN={ISIN}'

    for attempt in range(1, max_retries + 1):
        try:
            response = requests.get(url, params=params, headers=HEADERS, timeout=15)
            if response.status_code == 429:
                wait_time = 30 * attempt
                print(f"  -> 429 Too Many Requests, waiting {wait_time} seconds before retrying...")
                time.sleep(wait_time)
                continue
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            wait_time = 5 * attempt
            print(f"  -> Attempt {attempt} failed: {e}. Retrying in {wait_time} seconds...")
            time.sleep(wait_time)
    print(f"  -> Failed to fetch data for {Ticker} after {max_retries} attempts.")
    return None

print("--- Launching JustETF Data Downloader ---")

with tqdm(total=len(ETF_LIST), unit="ETF") as pbar:
    for etf in ETF_LIST:
        ISIN = etf["ISIN"]
        Ticker = etf["Ticker"]
        csv_filename = f"{Ticker}.csv"

        if os.path.exists(csv_filename):
            tqdm.write(f"File '{csv_filename}' already exists, skipping {Ticker}.")
            pbar.update(1)
            continue

        pbar.set_description(f"Working on {Ticker}")
        tqdm.write(f"Working on: {Ticker} ({ISIN})...")

        json_data = fetch_etf_data(ISIN, Ticker)
        if not json_data:
            tqdm.write(f"  -> FAILURE: unable to fetch data for {Ticker}.")
            pbar.update(1)
            continue

        raw_data = json_data.get('series', [])
        if not raw_data:
            tqdm.write("  -> ATTENTION: no historical data received.")
            pbar.update(1)
            continue

        data_for_table = [{'Date': p['date'], 'Price': float(p['value']['raw'])} for p in raw_data]
        df = pd.DataFrame(data_for_table)
        df['Date'] = pd.to_datetime(df['Date'])
        df = df.set_index('Date')

        df.to_csv(csv_filename)
        tqdm.write(f"  -> SUCCESS! File '{csv_filename}' created with {len(df)} rows.")

        pbar.update(1)
        time.sleep(15)

print("\n--- Process completed ---")
