# Cryptocurrency Arbitrage Trading Bot

A simple trading bot that simulates arbitrage opportunities between two cryptocurrency exchanges for XRP.

## Overview

This trading bot looks for price differences between two trading venues and executes trades when the difference exceeds a configurable threshold. The bot buys XRP at the lower-priced venue and sells it at the higher-priced venue to make a profit.

## Features

- Simulates cryptocurrency arbitrage trading between two venues
- Tracks and logs all trading activity
- Records detailed trade history in CSV format
- Persists trading capital and profit information between sessions
- Handles transaction fees
- Configurable arbitrage threshold
- Graceful shutdown with Ctrl+C

## Files

- `trading_bot.log`: Log file containing all trading activity
- `profit_tracker.csv`: Tracks capital, profits, and trade counts between sessions
- `trade_history.csv`: Detailed record of each individual buy/sell transaction

## Usage

Run the bot with:

```
python trading_bot.py
```

Stop the bot by pressing Ctrl+C. The bot will save its current state before exiting.

## Configuration Parameters

The following parameters can be adjusted in the code:

- `arbitrage_threshold`: The minimum price difference (as a percentage) required to execute a trade (default: 1%)
- `transaction_fee`: Fee charged per transaction (default: 0.1%)
- Default initial capital: 1000 USD (used if no previous session data exists)

## How It Works

1. The bot loads previous session data (if available) or starts with default capital
2. It continuously monitors prices on two simulated venues
3. When a price difference greater than the threshold is detected:
   - The bot buys XRP on the cheaper venue (up to 100 USD per trade)
   - It then sells the XRP on the more expensive venue
   - All transaction details are recorded
4. When stopped, it saves the current state for the next session

## CSV File Formats

### profit_tracker.csv
Tracks overall performance across sessions:
- timestamp: When the record was saved
- capital: Current USD balance
- xrp_balance: Current XRP balance
- total_profit: Cumulative profit
- trade_count: Total number of trades executed

### trade_history.csv
Records individual transactions:
- timestamp: When the trade occurred
- action: BUY or SELL
- amount: Quantity of XRP
- price: Price per XRP
- venue: Which venue the trade occurred on
- total_value: Total value of the transaction in USD
- fee: Transaction fee paid
- remaining_capital: USD balance after the trade
- xrp_balance: XRP balance after the trade

## Limitations

- Uses simulated random price data rather than real exchange APIs
- Does not account for order book depth or slippage
- Limited risk management features
- Simple arbitrage strategy without advanced techniques

## Future Improvements

- Connect to real exchange APIs
- Add more sophisticated trading strategies
- Implement proper risk management
- Add a web interface for monitoring
- Support for multiple cryptocurrencies