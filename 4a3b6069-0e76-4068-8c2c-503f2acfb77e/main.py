from surmount.base_class import Strategy, TargetAllocation
from surmount.data import OHLCV
from surmount.logging import log

class TradingStrategy(Strategy):
    def __init__(self):
        self.tickers = ["AAPL"]
        self.last_price = None

    @property
    def interval(self):
        # Assume daily data is sufficient to decide on 0.5% price movements.
        return "1day"

    @property
    def assets(self):
        # We're only trading AAPL in this strategy.
        return self.tickers

    @property
    def data(self):
        # OHLCV data is needed for price movements analysis.
        return [OHLCV(ticker) for ticker in self.tickers]

    def run(self, data):
        # Extract the close price for AAPL
        close_prices = [entry["AAPL"]["close"] for entry in data["ohlcv"]]

        if not close_prices or len(close_prices) < 2:
            log("Not enough data to make a decision.")
            return TargetAllocation({})

        current_price = close_prices[-1]
        previous_price = close_prices[-2]

        allocation = {}

        # Check if the price increased by more than 0.5% from the previous close
        if (current_price / previous_price - 1) > 0.005:
            log("AAPL price increased by more than 0.5%, buying.")
            allocation["AAPL"] = 1  # Here you would implement your logic to buy $10,000 worth of AAPL based on its price.
        
        # Check if the price decreased by more than 0.5% from the last price when bought.
        elif self.last_price and (self.last_price / current_price - 1) > 0.005:
            log("AAPL price decreased by more than 0.5%, selling.")
            allocation["AAPL"] = 0  # Sell all AAPL shares. 

        self.last_price = current_price
        
        # Ensure we always return an allocation, or an empty dict if no action is taken.
        return TargetAllocation(allocation)