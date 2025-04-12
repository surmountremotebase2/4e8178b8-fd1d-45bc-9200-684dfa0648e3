from surmount.base_class import Strategy, TargetAllocation
from surmount.logging import log
from datetime import datetime as dt

class TradingStrategy(Strategy):
    def __init__(self):
        # Define the asset you are trading. This example uses SPY for simplicity.
        self.tickers = ["SPY", "SH"]  # SH is an ETF that inversely tracks SPY, used for shorting SPY in this example.
        # No additional data_list required as we are using ohlcv data.
    
    @property
    def interval(self):
        return "5min"  # Using 5min interval for the strategy to evaluate the first 5min candle.
    
    @property
    def assets(self):
        return self.tickers
    
    def run(self, data):
        # Initialize the allocation with no position.
        allocation_dict = {"SPY": 0.0, "SH": 0.0}
        
        # Access the ohlcv data for the asset.
        d = data["ohlcv"]
        
        # Verify if there is enough data (at least one 5min candle for the day).
        if not d or "SPY" not in d[-1] or len(d) < 1:
            log("Not enough data.")
            return TargetAllocation(allocation_dict)  # Maintain previous allocations if data is insufficient.
        
        # Extract the first 5min candle of the day for SPY.
        first_candle = d[0]["SPY"]
        
        # Current time in EST to determine if it's time to close positions.
        current_time_est = dt.now().astimezone(tz.gettz('America/New_York')).strftime('%H:%M')
        
        # If the close of the first 5min candle is above the open, go long SPY.
        if first_candle["close"] > first_candle["open"]:
            allocation_dict["SPY"] = 1.0
        
        # If the close of the first 5min candle is below the open, go short SPY by allocating to SH.
        elif first_candle["close"] < first_candle["open"]:
            allocation_dict["SH"] = 1.0
        
        # Check if it's 3:55 PM EST to close all positions.
        if current_time_est == "15:55":
            allocation_dict = {"SPY": 0.0, "SH": 0.0}  # Close all positions by reallocating to 0.
        
        return TargetAllocation(allocation_dict)