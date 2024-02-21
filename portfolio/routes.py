#!/usr/bin/python3
import json
import os
from datetime import datetime, timedelta
from flask import render_template, jsonify, flash, redirect, url_for
from portfolio import app, db, bcrypt
from portfolio.forms import RegistrationForm, LoginForm, TransactionForm
from portfolio.models import User, Transaction
from flask_login import login_user, current_user, logout_user, login_required
import requests


def get_current_price_from_file(asset_name):
    """Get the current price from the saved JSON file."""
    data = load_from_json()
    if data and asset_name in data and 'usd' in data[asset_name]:
        return float(data[asset_name]['usd'])
    else:
        return None

def save_to_json(data):
    """Save data to a JSON file."""
    filename = 'price.json'

    existing_data = load_from_json() or {}  # Load existing data or create an empty dictionary

    # Update existing data only for keys that are not present
    for key, value in data.items():
        if key not in existing_data:
            existing_data[key] = value

    with open(filename, 'w') as file:
        json.dump(existing_data, file)

    print(f"Data saved to {filename}")

def load_from_json():
    """Load data from a JSON file."""
    filename = 'price.json'
    if os.path.exists(filename):
        with open(filename, 'r') as file:
            return json.load(file)
    else:
        return None

def update_json_data_hourly():
    """Update JSON file every hour."""
    last_updated = load_last_updated_time()
    
    if not last_updated or datetime.now() - last_updated >= timedelta(hours=1):
        # If the file is older than 1 hour or doesn't exist, update it
        data = get_current_price()
        if data:
            save_to_json(data)
            save_last_updated_time(datetime.now())
            print("JSON file updated successfully")

def save_last_updated_time(last_updated):
    """Save the last update time to a JSON file."""
    filename = 'last_updated.json'
    with open(filename, 'w') as file:
        json.dump(last_updated.isoformat(), file)

def load_last_updated_time():
    """Load the last update time from a JSON file."""
    filename = 'last_updated.json'
    if os.path.exists(filename):
        with open(filename, 'r') as file:
            return datetime.fromisoformat(json.load(file))
    else:
        return None
    
def get_total_current_balance(user_id):
    user = User.query.get(user_id)

    if not user:
        return jsonify(error="User not found")

    transactions = user.transactions
    total_balance = 0

    for t in transactions:
        current_price = get_current_price_from_file(t.asset_name)

        if current_price and isinstance(current_price, float):
            total_balance += current_price * t.quantity

    return round(total_balance, 2)

def get_total_profit_loss(user_id):
    user = User.query.get(user_id)

    if not user:
        return jsonify(error="User not found")

    transactions = user.transactions
    total_profit_loss = 0
    total_cost = 0

    for t in transactions:
        if t.transaction_type == 1:
            total_cost += t.cost
        elif t.transaction_type == 2:
            total_profit_loss += (get_current_price_from_file(t.asset_name) * t.quantity) - t.cost

    total_value = get_total_current_balance(user_id)
    total_profit_loss += total_value - total_cost

    if total_cost == 0:
        return {'total_profit_loss': 0, 'profit_loss_percentage': 0}

    profit_loss_percentage = (total_profit_loss / total_cost) * 100

    return {
        'total_profit_loss': round(total_profit_loss, 2),
        'profit_loss_percentage': round(profit_loss_percentage, 2)
    }


def get_crypto_data():
    """ To get coingecko market data """
    url = 'https://api.coingecko.com/api/v3/coins/markets'
    params = {
        'vs_currency': 'usd',
        'order': 'market_cap_desc',
        'per_page': 10,  # Number of cryptocurrencies to display
        'page': 1,
        'sparkline': False,
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        # Log the error or handle it as per your requirements
        print(f"Error fetching data. Status Code: {response.status_code}")
        return None

@app.route('/get_crypto_data')
def get_crypto_data_ajax():
    """ New route to provide cryptocurrency data for AJAX requests """

    crypto_data = get_crypto_data()

    if crypto_data:
        cryptocurrencies = []
        for data in crypto_data:
            crypto_info = {
                'name': data['name'],
                'symbol': data['symbol'],
                'price': data['current_price'],
                'market_cap': data['market_cap'],
            }
            cryptocurrencies.append(crypto_info)
    else:
        # Handle the case when API request fails
        cryptocurrencies = []

    return jsonify(cryptocurrencies)

def get_current_price(asset_name):
    """Get the current price of a specific asset and save it to a JSON file."""
    api_url = f'https://api.coingecko.com/api/v3/simple/price?ids={asset_name}&vs_currencies=usd'

    try:
        response = requests.get(api_url)
        data = response.json()

        # Check if asset_name is present in the response data
        if asset_name in data and 'usd' in data[asset_name]:
            # Save data to JSON file
            save_to_json(data)
        else:
            print('Getting price failed: Asset not found or price data unavailable')
            return None
    except requests.RequestException as e:
        print(f'Error fetching data: {str(e)}')
        return None

def get_average_price_per_unit(user_id, asset_name, transaction_type):
    user = User.query.get(user_id)
    transactions = [t for t in user.transactions if t.asset_name == asset_name and t.transaction_type == transaction_type]
    
    total_quantity = sum(t.quantity for t in transactions)
    total_cost = sum(t.cost for t in transactions)

    return total_cost / total_quantity if total_quantity != 0 else 0



def calculate_user_portfolio(user_id):
    user = User.query.get(user_id)

    if not user:
        return jsonify(error="User not found")

    transactions = user.transactions
    assets = []

    for asset_name in set(t.asset_name for t in transactions):
        total_cost = 0
        total_quantity_bought = 0
        total_quantity_sold = 0

        for t in transactions:
            if t.asset_name == asset_name:
                if t.transaction_type == 1:
                    total_cost += t.cost
                    total_quantity_bought += t.quantity
                elif t.transaction_type == 2:
                    total_quantity_sold += t.quantity

        # Adjust total cost and quantity for sell transactions
        selling_value = total_quantity_sold * get_average_price_per_unit(user_id, asset_name, 2)
        total_cost -= selling_value
        total_quantity_bought -= total_quantity_sold

        current_price = get_current_price_from_file(asset_name)
        if current_price and isinstance(current_price, float):
            total_current_value = current_price * total_quantity_bought
            pnl = total_current_value - total_cost
            pnl_percentage = (pnl / (total_cost + selling_value)) * 100 if total_cost != 0 else 0

            # Handle division by zero cases
            average_price_per_unit = total_cost / total_quantity_bought if total_quantity_bought != 0 else 0

            assets.append({
                'asset_name': asset_name,
                'total_cost': round(total_cost + selling_value, 2),
                'average_price_per_unit': round(average_price_per_unit, 2),
                'total_quantity_bought': round(total_quantity_bought, 2),
                'total_quantity_sold': round(total_quantity_sold, 2),
                'current_value': round(total_current_value, 2),
                'pnl': round(pnl, 2),
                'pnl_percentage': round(pnl_percentage, 2)
            })
    return assets


def update_user_assets_prices(user_id):
    """Update prices for all unique assets owned by a user."""
    user = User.query.get(user_id)

    if not user:
        print("User not found")
        return

    transactions = user.transactions
    unique_assets = set(t.asset_name for t in transactions)

    for asset_name in unique_assets:
        get_current_price(asset_name)

@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html', title='Home')

@app.route('/about')
def about():
    return render_template('about.html', title='About')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user=User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            return redirect('home')
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='login', form=form)

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your account hass been created! you can now login', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='register', form=form)


@app.route('/portfolio/add_transaction', methods=['POST', 'GET'])
@login_required
def add_transaction():
    form = TransactionForm()

    if form.validate_on_submit():
        asset_name = form.coin.data
        quantity = form.quantity.data
        cost = form.cost.data
        transaction_type = form.transaction_type.data

        # Insert transaction into the database
        new_transaction = Transaction(
            user=current_user,
            asset_name=asset_name,
            quantity=quantity,
            cost=cost,
            transaction_type=transaction_type
            )
        
        db.session.add(new_transaction)
        db.session.commit()
    return redirect(url_for('portfolio'))


@app.route('/portfolio/', methods=['GET', 'POST'])
@login_required
def portfolio():
    form = TransactionForm()
    user_id = current_user.id
    update_user_assets_prices(user_id)
    
    total_balance = get_total_current_balance(user_id)
    total_profit_loss_data = get_total_profit_loss(user_id)
    
    portfolio_data = calculate_user_portfolio(user_id)

    return render_template('portfolio.html',
                           title='Portfolio',
                           form=form, 
                           portfolio_data=portfolio_data,
                           total_balance=total_balance,
                           total_profit_loss_data=total_profit_loss_data)


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))