from surmount.base_class import Strategy, TargetAllocation
from surmount.logging import log

class TradingStrategy(Strategy):
    def __init__(self):
        self.ticker = "AAPL"
        self.buy_threshold = 0.005  # 0.5% increase
        self.sell_threshold = -0.005  # 0.5% decrease
        self.buy_amount = 10000  # $10000 worth to buy

    @property
    def assets(self):
        return [self.ticker]

    @property
    def interval(self):
        return "1hour"

    def run(self, data):
        # Collect the last two hourly closing prices to calculate the price change
        closing_prices = [data["ohlcv"][-2][self.ticker]["close"], data["ohlcv"][-1][self.ticker]["close"]] if len(data["ohlcv"]) >= 2 else [None, None]

        if None not in closing_prices:
            # Calculate the percentage change between the last two prices
            change_percentage = (closing_prices[1] - closing_prices[0]) / closing_prices[0]

            # Determine if the change meets the buy/sell threshold
            if change_percentage >= self.buy_threshold:
                # Calculate the number of shares to buy, assuming we buy $10000 worth of AAPL. 
                # This step requires knowing the current price to calculate the number of shares.
                current_price = closing_prices[1]
                num_shares_to_buy = self.buy_amount / current_price
                allocation = {self.ticker: num_shares_to_buy}
                log(f"Buying {num_shares_to_buy} shares of {self.ticker} at {current_price} per share.")
            
            elif change_percentage <= self.sell_threshold:
                # Sell all shares of AAPL by setting its target allocation to 0
                allocation = {self.ticker: 0}
                log(f"Selling all shares of {self.ticker}.")
            else:
                # No action if the price change is within the threshold
                allocation = {}
        else:
            # If there's insufficient data, no trading action is performed
            allocation = {}
            log("Insufficient data for trading decision.")

        return TargetAllocation(allocation)