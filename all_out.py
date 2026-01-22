# all_out.py
from strategy import Strategy

class AllOutStrategy(Strategy):
    """
    Estrategia All-out:
    Nunca quiere acciones. El 100% del portfolio debe estar en cash.
    """

    def __init__(self):
        super().__init__(name="All Out")


    def percentage_in_actions(self, past_prices, cash, shares):
        # Queremos 0% invertido.
        return 0.0
