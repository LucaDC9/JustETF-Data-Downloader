# JustETF Data Downloader

A simple Python script to download historical **market price data** (excluding dividends) for a list of ETFs from [justETF.com](https://www.justetf.com).
Each ETF is identified by its ISIN and saved as a separate CSV file for easy analysis.

---

## 🔍 Features

* Downloads daily historical price data (market value only).
* Saves each ETF’s data to a dedicated `.csv` file.
* Skips download if the file already exists.
* Automatically retries on failure (e.g. network errors or rate limiting).

---

## 🧾 Requirements

Python 3.7+ and the following packages:

```bash
pip install requests pandas tqdm
```

---

## ⚙️ Usage

1. Clone this repository.
2. Edit the `ETF_LIST` in `script.py` to include the ISINs and ticker symbols you're interested in:

```python
ETF_LIST = [
    {"ISIN": "IE00BHZRQZ17", "Ticker": "FLXI"},
    {"ISIN": "IE00B6YX5C33", "Ticker": "SPY5"},
    {"ISIN": "IE000YU9K6K2", "Ticker": "JEDI"}
]
```

3. Run the script:

```bash
python script.py
```

Each CSV file will be created in the current directory (e.g., `FLXI.csv`, `SPY5.csv`, etc.).

---

## 📁 Output Format

Each `.csv` file contains:

| Date       | Price  |
| ---------- | ------ |
| 2010-01-04 | 123.45 |
| ...        | ...    |

The `Date` column is used as the index.

---

## 📌 Disclaimer

This project is for educational and personal use only.
Data is retrieved from public endpoints available on [justETF.com](https://www.justetf.com).
The script does **not** access any private or paid APIs, and does **not** bypass authentication.

> This is an unofficial tool, with no affiliation to JustETF.

If you're affiliated with JustETF and would like this repository removed or modified, feel free to [open an issue](https://github.com/LucaDC9/JustETF-Data-Downloader/issues) or contact me directly.

---

## 🪪 License

This project is licensed under the MIT License — see the [`LICENSE`](LICENSE) file for details.
It is an unofficial tool, with no affiliation to JustETF.
