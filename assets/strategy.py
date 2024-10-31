from lumibot.strategies.strategy import Strategy
from lumibot.entities import Asset
from datetime import datetime
from finbert_utils import estimate_sentiment
import logging


class SentimentTradingStrategy(Strategy):
    def initialize(self, symbol: str = "SPY",
                   sentiment_threshold: float = 0.75,
                   position_size: int = 100):
        """
        Initialize the trading strategy

        Parameters:
        - symbol: The stock symbol to trade
        - sentiment_threshold: Minimum sentiment score to trigger a trade
        - position_size: Number of shares to trade
        """
        # Setup basic logging
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(self.__class__.__name__)

        # Strategy parameters
        self.symbol = symbol
        self.sentiment_threshold = sentiment_threshold
        self.position_size = position_size

        # Set trading time frames
        self.set_market_hours(
            market_open=datetime.strptime("9:30", "%H:%M").time(),
            market_close=datetime.strptime("16:00", "%H:%M").time(),
        )

    def on_trading_iteration(self):
        """
        Main trading logic - runs on each iteration
        """
        try:
            # Get current position
            current_position = self.get_position(self.symbol)

            # Get sentiment score
            sentiment_score = estimate_sentiment(self.symbol)
            self.logger.info(f"Sentiment score for {self.symbol}: {sentiment_score}")

            # Trading logic
            if sentiment_score > self.sentiment_threshold:
                if current_position is None:
                    self.logger.info(f"Strong positive sentiment detected. Buying {self.symbol}")
                    asset = Asset(self.symbol)
                    self.submit_order(
                        asset=asset,
                        quantity=self.position_size,
                        side="buy",
                    )
            elif sentiment_score < -self.sentiment_threshold:
                if current_position is not None:
                    self.logger.info(f"Strong negative sentiment detected. Selling {self.symbol}")
                    asset = Asset(self.symbol)
                    self.submit_order(
                        asset=asset,
                        quantity=self.position_size,
                        side="sell",
                    )

        except Exception as e:
            self.logger.error(f"Error in trading iteration: {str(e)}")