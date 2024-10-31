
# run_bot.py
from lumibot.brokers import Alpaca
from lumibot.traders import Trader
from strategy import SentimentTradingStrategy
from config import API_KEY, API_SECRET, PAPER_TRADING


def run_live_bot():
    # Initialize broker
    broker = Alpaca(
        API_KEY,
        API_SECRET,
        paper=PAPER_TRADING
    )

    # Create strategy instance
    strategy = SentimentTradingStrategy(
        symbol="AAPL",
        sentiment_threshold=0.75,
        position_size=100
    )

    # Create and run trader
    trader = Trader(strategy, broker)
    trader.run()


if __name__ == "__main__":
    run_live_bot()