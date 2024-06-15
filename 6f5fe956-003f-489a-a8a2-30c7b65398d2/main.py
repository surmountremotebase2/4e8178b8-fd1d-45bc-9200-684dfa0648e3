from surmount.base_class import Strategy, TargetAllocation
from surmount.logging import log
from surmount.data import Asset

class TradingStrategy(Strategy):

    def __init__(self):
        # Initializing with the AAPL ticker
        self.ticker = "AAPL"

    @property
    def interval(self):
        # Setting data interval to daily for checking daily percent changes
        return "1day"

    @property
    def assets(self):
        # The strategy is focused on the Apple stock
        return [self.ticker]

    @property
    def data(self):
        # No additional data is required for this strategy
        return []

    def run(self, data):
        # Initialization of the allocation_dict
        allocation_dict = {}

        # Check if there is enough data to assess
        if len(data["ohlcv"]) > 2:
            # Calculate percent changes for the last 3 days
            close_prices = [data["ohlcv"][-3][self.ticker]["close"],
                            data["ohlcv"][-2][self.ticker]["close"],
                            data["ohlcv"][-1][self.ticker]["close"]]
            pct_changes = [(close_prices[i] - close_prices[i-1]) / close_prices[i-1] for i in range(1, 3)]

            # Determine strategy action based on percent changes
            if pct_changes[0] > 0.005 and pct_changes[1] > 0.005:
                # If the stock was up more than 0.5% two days in a row, buy/hold $10000 worth of AAPL
                allocation_dict[self.ticker] = 1  # Using 1 as a proxy, should adjust based on actual account management strategy
            elif pct_changes[0] < -0.005 and pct_changes[1] < -0.005:
                # If the stock was down more than 0.5% two days in a row, sell all holdings of AAPL
                allocation_dict[self.ticker] = 0  # This means selling all AAPL
            else:
                # No action if the criteria are not met
                log("No action criteria met for AAPL.")

        else:
            # Log the situation when not enough data is available
            log("Not enough data to make a decision for AAPL.")

        # Return the allocation object
        return TargetAllocation(allocation_dict)