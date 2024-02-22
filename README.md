# Cryptocurrency Portfolio Management

This Flask-based web application allows users to manage their cryptocurrency portfolios, providing features such as user registration, login, transaction addition, and portfolio visualization. It leverages the CoinGecko API to fetch real-time cryptocurrency market data and updates prices periodically.

## Features

- User registration and authentication.
- Adding cryptocurrency transactions, specifying details like asset name, quantity, cost, and transaction type.
- Real-time portfolio data with details on assets, quantities, current values, profit/loss, and more.
- Periodic updates of cryptocurrency prices from the CoinGecko API.
- Calculation of total portfolio balance and profit/loss percentages.

## Prerequisites

- Python 3.x
- Flask
- Flask Login
- Flask Bcrypt
- Flask SQLAlchemy
- Requests library

## Setup

1. Install the required Python packages:

   pip install Flask Flask-Login Flask-Bcrypt Flask-SQLAlchemy requests

2. Run the Flask application:
   python app.py

3. Access the application at http://localhost:5000 in your web browser.

## Usage

Register a new account or log in if you already have one.
Add cryptocurrency transactions using the provided form.
View your portfolio, including total balance and profit/loss data.
External APIs
The application utilizes the CoinGecko API to fetch real-time cryptocurrency market data. Make sure to check their documentation for any updates or changes.

## File Structure
- app.py: Main application file containing Flask routes and configurations.
- portfolio/: Package containing modules for forms, models, and the main application.
- templates/: HTML templates for rendering web pages.
- price.json: JSON file storing cryptocurrency prices.
- last_updated.json: JSON file storing the timestamp of the last data update.

## Contributing

Feel free to contribute to the project by opening issues or submitting pull requests. Bug reports, feature requests, and feedback are highly appreciated.