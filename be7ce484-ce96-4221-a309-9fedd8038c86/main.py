from surmount.base_class import Strategy, TargetAllocation
from surmount.logging import log

class TradingStrategy(Strategy):
    def __init__(self):
        self.purchase_made = False  # Flag to indicate if purchase is made
        self.sell_date = None       # Date to sell the purchased stock
        
    @property
    def assets(self):
        return ["AAPL"]
    
    @property
    def interval(self):
        return "1hour"
    
    def run(self, data):
        # Initial allocation is 0 (not holding the asset)
        allocation = 0
        
        # Data required for processing
        d = data["ohlcv"]
        current_date = d[-1]["AAPL"]["date"]  # To be used for checking sell date
        
        # Check if purchase is already made and if sell date is reached or not
        if self.purchase_made:
            if self.sell_date and current_date >= self.sell_date:
                # Time to sell the stock
                self.purchase_made = False  # Reset purchase flag
                allocation = -1 # Signal to sell all holdings of "AAPL"
                log("Selling $10000 worth of AAPL")
        else:
            # Checking if the condition to buy is met
            if len(d) > 1:  # Ensure there are at least 2 data points to compare
                previous_close = d[-2]["AAPL"]["close"]
                current_close = d[-1]["AAPL"]["close"]
                percent_change = (current_close - previous_close) / previous_close
                
                # If stock has gone up by 0.5%
                if percent_change >= 0.005:
                    # Mark as purchase made and set the sell date (10 days later)
                    self.purchase_made = True
                    allocation = 1  # Allocation set to buy $10000 worth of "AAPL"
                    self.sell_date = str(pd.to_datetime(current_date) + pd.Timedelta(days=10))[:10]
                    log("Buying $10000 worth of AAPL")
        
        return TargetAllocation({"AAPL": allocation})