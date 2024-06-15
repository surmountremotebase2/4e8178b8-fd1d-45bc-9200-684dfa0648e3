from surmount.base_class import Strategy, TargetAllocation
from surmount.logging import log

class TradingStrategy(Strategy):

    def __init__(self):
        # List of assets this strategy will trade
        self.tickers = ["AAPL"]
        # Initial capital to buy AAPL
        self.buy_amount = 10000
        # Track the last action to avoid re-buying or re-selling without a condition change
        self.last_action = None

    @property
    def assets(self):
        # Specifies the asset(s) the strategy trades
        return self.tickers

    @property
    def interval(self):
        # Sets the data interval to 1 hour
        return "1hour"

    def run(self, data):
        # Assuming 'data' contains historical price data for each ticker
        ohlcv = data["ohlcv"]

        # Check if there's enough data to compare current price with the previous price
        if len(ohlcv) < 2:
            log("Not enough data to execute strategy")
            return TargetAllocation({})

        # Get the latest two closes for AAPL
        current_close = ohlcv[-1]["AAPL"]["close"]
        previous_close = ohlcv[-2]["AAPL"]["close"]

        # Calculate the percentage change
        percentage_change = (current_close - previous_close) / previous_close

        # Initialize allocation with no position
        allocation_dict = {"AAPL": 0}

        # Check if the price increased by 0.5% and the last action wasn't a buy
        if percentage_change >= 0.005 and self.last_action != "buy":
            log("Price increased by 0.5% or more, buying $10000 worth of AAPL")
            # Instead of a direct buy amount, we need to specify the fraction of the portfolio to invest in AAPL,
            # but since we're working with a hypothetical API here, let's assume there's a way to convert
            # the buy amount to a target allocation fraction implicitly.
            allocation_dict["AAPL"] = 1  # Assuming buying $10000 worth implicitly as a 'buy' signal
            self.last_action = "buy"

        # Check if the price decreased by 0.5% and the last action wasn't a sell
        elif percentage_change <= -0.005 and self.last_action != "sell":
            log("Price decreased by 0.5% or more, selling all AAPL")
            allocation_dict["AAPL"] = 0
            self.last_action = "sell"

        # Return the target allocation
        return TargetAllocation(allocation_data=allocation_dict)

    # Optionally, include methods to handle tick level data or live updates if the platform supports it