#!/usr/bin/python3
from portfolio import app
from portfolio.routes import calculate_user_portfolio
if __name__ == '__main__':
    app.run(debug=True)