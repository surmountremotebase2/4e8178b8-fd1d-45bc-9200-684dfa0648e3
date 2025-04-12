from surmount.base_class import Strategy, TargetAllocation
from surmount.data import Asset
from surmount.logging import log

class TradingStrategy(Strategy):
    def __init__(self):
        # Define a single ticker to trade.
        self.ticker = "SPY"

    @property
    def assets(self):
        return [self.ticker]

    @property
    def interval(self):
        # 5-minute intervals for intraday data
        return "5min"

    def run(self, data):
        allocation = {}
        
        # Ensure there's enough data
        if len(data["ohlcv"]) > 1:
            first_bar = data["ohlcv"][0][self.ticker]
            last_bar = data["ohlcv"][-1][self.ticker]
            date_last_bar = last_bar["date"]
            hour_minute_last_bar = date_last_bar.split(" ")[1][:-3]  # Extract HH:MM format

            # Check if first 5-minute bar closed above its open
            if first_bar["close"] > first_bar["open"]:
                allocation[self.ticker] = 1.0  # Go long
            # Check if first 5-minute bar closed below its open
            elif first_bar["close"] < first_bar["open"]:
                allocation[self.ticker] = -1.0  # Go short

            # Close position at 3:55 PM EST
            if hour_minute_last_bar == "15:55":
                allocation[self.ticker] = 0  # Close position

        return TargetAllocation(allocation)