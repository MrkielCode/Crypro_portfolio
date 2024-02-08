#!/usr/bin/python3
from flask import Flask, render_template


app = Flask(__name__)

@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html', title='Home')

@app.route('/portfolio')
def portfolio():
    return render_template('portfolio.html', title='Portfolio')

if __name__ == "__main__":
    app.run(debug=True)