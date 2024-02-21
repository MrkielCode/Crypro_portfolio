#!/usr/bin/python3
from portfolio import app
from portfolio.routes import get_current_price_from_file
if __name__ == '__main__':

    app.run(debug=True)