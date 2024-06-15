from surmount.base_class import Strategy, TargetAllocation
from surmount.logging import log

class TradingStrategy(Strategy):
    def __init__(self):
        # Initialize variables to keep track of purchase state and holding period
        self.bought = False
        self.holding_days = 0
        self.purchase_price = 0

    @property
    def assets(self):
        # This strategy only involves AAPL
        return ["AAPL"]

    @property
    def interval(self):
        # Use daily data for this strategy
        return "1day"

    def run(self, data):
        # Set the initial target allocation to 0, assuming no investment to begin with
        target_allocation = {"AAPL": 0}
        
        # Access the daily OHLCV data for AAPL
        aapl_data = data["ohlcv"]["AAPL"]
        
        # Check if we haven't bought AAPL yet
        if not self.bought:
            # Calculate the percentage change from the previous close to today's open
            if len(aapl_data) > 1:
                previous_close = aapl_data[-2]["close"]
                today_open = aapl_data[-1]["open"]
                percent_change = (today_open - previous_close) / previous_close
                
                # If the stock opens 0.5% or higher, set the allocation to buy
                if percent_change >= 0.005:
                    self.bought = True
                    self.purchase_price = today_open
                    # Assuming $10,000 investment, this part of the strategy isn't directly implementable
                    # due to the TargetAllocation's design, it needs a proportion of portfolio value,
                    # thus, handling exact investment amounts would be done outside of this code block.
                    target_allocation["AAPL"] = 1  # Placeholder to indicate buy decision
                    
        elif self.bought:
            # Increment the holding days each day after purchase
            self.holding_days += 1
            
            # If we've held AAPL for 10 days, sell it
            if self.holding_days >= 10:
                self.bought = False
                self.holding_days = 0  # Reset the holding period
                self.purchase_price = 0  # Reset purchase price
                target_allocation["AAPL"] = 0  # Set allocation to 0 to indicate a sell
            else:
                # Continue holding AAPL by keeping the target allocation the same
                target_allocation["AAPL"] = 1  # Keep the position
                
        # Log for diagnosis or detailed monitoring
        log(f"AAPL Bought: {self.bought}, Holding Days: {self.holding_days}, Purchase Price: {self.purchase_price}")

        return TargetAllocation(target_allocation)