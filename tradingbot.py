import random
import time
import logging
import signal
import sys
import csv
import os
from datetime import datetime

# Initialize logging
logging.basicConfig(filename='trading_bot.log', level=logging.INFO, format='%(asctime)s - %(message)s')

# CSV file settings
profit_tracker_file = 'profit_tracker.csv'
profit_csv_header = ['timestamp', 'capital', 'xrp_balance', 'total_profit', 'trade_count']


# Setup CSV for trade tracking
csv_file = 'trade_history.csv'
csv_header = ['timestamp', 'action', 'amount', 'price', 'venue', 'total_value', 'fee', 'remaining_capital', 'xrp_balance']

# Initialize variables
capital = 0
xrp_balance = 0
total_profit = 0
trade_count = 0

# Trading strategy parameters
arbitrage_threshold = 0.01  # 1% price difference
transaction_fee = 0.001  # 0.1% fee per trade

# Load initial capital and stats from CSV or create new file if it doesn't exist
def initialize_from_csv():
    global capital, xrp_balance, total_profit, trade_count
    
    if os.path.exists(profit_tracker_file):
        with open(profit_tracker_file, 'r', newline='') as file:
            reader = csv.reader(file)
            headers = next(reader)  # Skip header row
            
            try:
                # Try to read the last row to get the most recent values
                last_row = None
                for row in reader:
                    last_row = row
                
                if last_row:
                    # timestamp = last_row[0]  # Not needed for initialization
                    capital = float(last_row[1])
                    xrp_balance = float(last_row[2])
                    total_profit = float(last_row[3])
                    trade_count = int(last_row[4])
                    logging.info(f"Loaded from CSV: Capital={capital}, XRP={xrp_balance}, Profit={total_profit}, Trades={trade_count}")
                else:
                    # No data rows found, use default values
                    capital = 1000  # Default initial capital
                    logging.info(f"No data in CSV, using default capital: {capital}")
            except (IndexError, ValueError) as e:
                # Handle malformed CSV
                capital = 1000  # Default initial capital
                logging.error(f"Error reading CSV: {e}. Using default capital: {capital}")
    else:
        # Create new file with headers
        capital = 1000  # Default initial capital
        with open(profit_tracker_file, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(profit_csv_header)
            logging.info(f"Created new profit tracker file with initial capital: {capital}")
    
    return capital

# Create CSV file with headers if it doesn't exist
if not os.path.exists(csv_file):
    with open(csv_file, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(csv_header)

# Update profit tracker CSV
def update_profit_tracker():
    with open(profit_tracker_file, 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([
            datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            f"{capital:.2f}",
            f"{xrp_balance:.2f}",
            f"{total_profit:.2f}",
            f"{trade_count}"
        ])
    logging.info(f"Updated profit tracker: Capital={capital}, Profit={total_profit}, Trades={trade_count}")


def record_trade(action, amount, price, venue, total_value, fee):
    with open(csv_file, 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([
            datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            action,
            f"{amount:.2f}",
            f"{price:.4f}",
            venue,
            f"{total_value:.2f}",
            f"{fee:.2f}",
            f"{capital:.2f}",
            f"{xrp_balance:.2f}"
        ])




# Simulated market data for two trading venues
def get_market_price_venue1():
    set.seed(123)
    return random.uniform(0.45, 0.55)  # Random price between 0.45 and 0.55 USD/XRP

def get_market_price_venue2():
    set.seed(123)
    return random.uniform(0.45, 0.55)  # Random price between 0.45 and 0.55 USD/XRP

# Trading functions
def buy_xrp(amount_usd, price, venue):
    global capital, xrp_balance
    fee = amount_usd * transaction_fee
    xrp_bought = (amount_usd - fee) / price
    capital -= amount_usd
    xrp_balance += xrp_bought
    logging.info(f"Bought {xrp_bought:.2f} XRP at {price:.4f} USD/XRP for {amount_usd:.2f} USD (Fee: {fee:.2f} USD)")
    record_trade("BUY", xrp_bought, price, venue, amount_usd, fee)

def sell_xrp(amount_xrp, price, venue):
    global capital, xrp_balance
    fee = amount_xrp * price * transaction_fee
    usd_earned = amount_xrp * price - fee
    capital += usd_earned
    xrp_balance -= amount_xrp
    logging.info(f"Sold {amount_xrp:.2f} XRP at {price:.4f} USD/XRP for {usd_earned:.2f} USD (Fee: {fee:.2f} USD)")
    record_trade("SELL", amount_xrp, price, venue, usd_earned, fee)


# Function to handle interruption (Ctrl + C)
def signal_handler(sig, frame):
    print("\nTrading session interrupted.")
    print(f"Total trades executed: {trade_count}")
    print(f"Total profit: {total_profit:.2f} USD")
    print(f"Final capital: {capital:.2f} USD")
    print(f"Final XRP balance: {xrp_balance:.2f} XRP")
    
    # Update the profit tracker before exiting
    update_profit_tracker()
    print(f"Profit tracker updated in {profit_tracker_file}")
    
    sys.exit(0)

# Arbitrage trading bot
def arbitrage_trading_bot():
    global capital, xrp_balance, trade_count, total_profit
    initial_capital_value = capital  # Store initial capital for profit calculation

    while True:  # Run indefinitely
        price_venue1 = get_market_price_venue1()
        price_venue2 = get_market_price_venue2()

        # Check for arbitrage opportunity
        if price_venue1 < price_venue2 * (1 - arbitrage_threshold):
            amount_usd = min(100, capital)  # Trade with a maximum of 100 USD per trade
            if amount_usd > 0:
                buy_xrp(amount_usd, price_venue1, "Venue1")
                sell_xrp(xrp_balance, price_venue2, "Venue2")
                total_profit = capital - initial_capital_value
                trade_count += 1
                logging.info(f"Arbitrage profit: {total_profit:.2f} USD")

        elif price_venue2 < price_venue1 * (1 - arbitrage_threshold):
            amount_usd = min(100, capital)  # Trade with a maximum of 100 USD per trade
            if amount_usd > 0:
                buy_xrp(amount_usd, price_venue2, "Venue2")
                sell_xrp(xrp_balance, price_venue1, "Venue1")
                total_profit = capital - initial_capital_value
                trade_count += 1
                logging.info(f"Arbitrage profit: {total_profit:.2f} USD")

        time.sleep(1)  # Wait for 1 second before next iteration

if __name__ == "__main__":
    # Load initial values from CSV
    initial_capital = initialize_from_csv()
    
    # Set up signal handler for Ctrl + C
    signal.signal(signal.SIGINT, signal_handler)
    
    print(f"Starting trading bot with initial capital: ${capital:.2f}")
    print(f"Previous profit: ${total_profit:.2f}")
    print(f"Previous trades: {trade_count}")
    print("Press Ctrl + C to stop and save progress.")
    
    arbitrage_trading_bot()