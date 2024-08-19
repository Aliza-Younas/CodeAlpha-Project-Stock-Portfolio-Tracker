import sqlite3

# Connect to the SQLite database (or create it if it doesn't exist)
conn = sqlite3.connect('portfolio.db')
cursor = conn.cursor()

# Create a table to store the portfolio
cursor.execute('''
CREATE TABLE IF NOT EXISTS portfolio (
    id INTEGER PRIMARY KEY,
    symbol TEXT NOT NULL,
    shares INTEGER NOT NULL,
    purchase_price REAL NOT NULL,
    purchase_date TEXT NOT NULL
)
''')

conn.commit()
import yfinance as yf
from datetime import datetime

def add_stock(symbol, shares, purchase_price):
    cursor.execute('''
    INSERT INTO portfolio (symbol, shares, purchase_price, purchase_date)
    VALUES (?, ?, ?, ?)
    ''', (symbol, shares, purchase_price, datetime.now().strftime("%Y-%m-%d")))
    conn.commit()
    print(f"Added {shares} shares of {symbol} at ${purchase_price} each.")

def remove_stock(symbol):
    cursor.execute('DELETE FROM portfolio WHERE symbol = ?', (symbol,))
    conn.commit()
    print(f"Removed {symbol} from the portfolio.")

# Example usage
add_stock('AAPL', 10, 150.00)
remove_stock('AAPL')
def get_stock_price(symbol):
    stock = yf.Ticker(symbol)
    data = stock.history(period="1d")
    return data['Close'][0]

def track_portfolio():
    cursor.execute('SELECT symbol, shares, purchase_price FROM portfolio')
    portfolio = cursor.fetchall()

    total_investment = 0
    current_value = 0

    for stock in portfolio:
        symbol, shares, purchase_price = stock
        current_price = get_stock_price(symbol)
        investment_value = shares * purchase_price
        current_stock_value = shares * current_price

        total_investment += investment_value
        current_value += current_stock_value

        print(f"{symbol}:")
        print(f"  Shares: {shares}")
        print(f"  Purchase Price: ${purchase_price}")
        print(f"  Current Price: ${current_price:.2f}")
        print(f"  Investment Value: ${investment_value:.2f}")
        print(f"  Current Value: ${current_stock_value:.2f}")
        print(f"  Profit/Loss: ${current_stock_value - investment_value:.2f}\n")

    print(f"Total Investment: ${total_investment:.2f}")
    print(f"Current Portfolio Value: ${current_value:.2f}")
    print(f"Overall Profit/Loss: ${current_value - total_investment:.2f}")

# Example usage
track_portfolio()
add_stock('AAPL', 10, 150.00)
add_stock('GOOGL', 5, 2000.00)

track_portfolio()

remove_stock('AAPL')

track_portfolio()
conn.close()
