from surmount.base_class import Strategy, TargetAllocation

class TradingStrategy(Strategy):
    def __init__(self):
        super().__init__()
        # Predefined list of tickers, ideally this would be dynamically generated
        # by querying an external API or database like Financial Modeling Prep
        # for all available tickers, then filtering for those containing 'AA'.
        self.tickers = ["AAPL", "AAL", "AA", "BA", "CAAS"]

    @property
    def interval(self):
        # Specifies the data update interval; adjust as needed.
        return "1day"

    @property
    def assets(self):
        # Filters the predefined tickers to include only those with 'AA' in their symbol.
        return [ticker for ticker in self.tickers if "AA" in ticker]

    def run(self, data):
        aa_tickers = self.assets
        if not aa_tickers:
            return TargetAllocation({})
        # Equally divides the allocation among all selected tickers.
        allocation_dict = {ticker: 1/len(aa_tickers) for ticker in aa_tickers}
        return TargetAllocation(allocation_dict)