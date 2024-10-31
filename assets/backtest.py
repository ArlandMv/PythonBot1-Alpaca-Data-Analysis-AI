from datetime import datetime
from lumibot.backtesting import YahooDataBacktesting
from strategy import SentimentTradingStrategy


def run_backtest():
    # Define backtest parameters
    start_date = datetime(2023, 1, 1)
    end_date = datetime(2023, 12, 31)

    # Initialize backtesting
    backtester = YahooDataBacktesting(
        start_date,
        end_date,
    )

    # Create and run strategy
    strategy = SentimentTradingStrategy(
        symbol="AAPL",
        sentiment_threshold=0.75,
        position_size=100
    )

    # Run backtest
    backtester.run(strategy)