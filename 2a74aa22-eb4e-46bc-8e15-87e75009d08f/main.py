from surmount.base_class import Strategy, TargetAllocation
from surmount.logging import log

class TradingStrategy(Strategy):

    def __init__(self):
        # AAPL is the target stock for this strategy
        self.symbol = "AAPL"
        self.investment_amount = 10000  # This example amount is not fits into TargetAllocation directly but symbolizes the intent

    @property
    def assets(self):
        # The strategy is interested in Apple only
        return [self.symbol]

    @property
    def interval(self):
        # Assuming daily data is sufficient for this strategy
        return "1day"

    def run(self, data):
        # The actual logic based on historical events cannot be directly implemented.
        # Instead, this is a placeholder for how you might structure the decision to buy based on external conditions.
        # This if-statement serves as a placeholder for the "event" of interest, adjusting for the hypothetical nature of the request.
        if self._oj_simpson_verdict():
            allocation_percentage = 1  # This represents a decision to allocate 100% of the strategy's capacity to AAPL
        else:
            allocation_percentage = 0  # No allocation if the condition isn't met

        return TargetAllocation({self.symbol: allocation_percentage})

    def _oj_simpson_verdict(self):
        # Mock function to represent the decision-making logic
        # In practice, this could be a check against a database or an API that provides historical event data
        # O.J. Simpson was found not guilty of murder in 1995, so this returns False to reflect historical accuracy
        return False