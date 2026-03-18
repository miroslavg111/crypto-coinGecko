# Setup Guide

This document explains how to run the project locally and how to deploy it on Render.

## Local Setup

### 1. Open the project folder

Make sure you are inside the project directory:

bash
cd crypto-coinGecko

### 2 Create a virtual environment

On macOS or Linux:
python -m venv venv
source venv/bin/activate

On Windows PowerShell:
python -m venv venv
venv\Scripts\Activate.ps1

On Windows Command Prompt:
python -m venv venv
venv\Scripts\activate

### 3. Install dependencies
pip install -r requirements.txt

### 4. Create a local environment file

On macOS or Linux:
cp .env.example .env

On Windows Command Prompt:
copy .env.example .env

### 5. Review the .env file

Example:
FLASK_DEBUG=true
COINGECKO_API_KEY=

Notes:
FLASK_DEBUG=true is useful during local development.
COINGECKO_API_KEY is optional for a basic version of the project.


### 6. Run the Flask app
python app.py


### 7. Open the app in the browser
http://127.0.0.1:5000
Local Testing Examples

Search for Bitcoin:

http://127.0.0.1:5000/?q=bitcoin

Sort by price in descending order:

http://127.0.0.1:5000/?sort=price&direction=desc

Switch currency to EUR:

http://127.0.0.1:5000/?currency=eur

Search and sort together:

http://127.0.0.1:5000/?q=eth&currency=eur&sort=market_cap&direction=desc