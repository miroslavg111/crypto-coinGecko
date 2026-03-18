# Crypto Dashboard

A minimal Flask web app that fetches live cryptocurrency market data from the CoinGecko API and displays it in a clean, server-rendered dashboard.

## Features

- Fetches top cryptocurrencies by market cap
- Displays:
  - price
  - 24h change
  - volume
  - market cap
  - rank
- Search by coin name or symbol
- Sort by:
  - rank
  - market cap
  - price
  - 24h change
  - volume
- Toggle currency:
  - USD
  - EUR
  - BGN
- Minimal UI with plain HTML/CSS
- Ready for deployment on Render

## Tech Stack

- Python
- Flask
- Requests
- Jinja2
- HTML/CSS
- Render

## Project Structure

```text
crypto-coinGecko/
├── app.py
├── services.py
├── requirements.txt
├── render.yaml
├── .env.example
├── .gitignore
├── README.md
├── ARCHITECTURE.md
├── templates/
│   ├── base.html
│   └── index.html
└── static/
    └── style.css