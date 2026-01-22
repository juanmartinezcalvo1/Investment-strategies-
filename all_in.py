# all_in.py
from strategy import Strategy

class AllInStrategy(Strategy):
    """
    Estrategia All-in:
    Quiere invertir el 100% del portfolio en acciones.
    """
    def __init__(self):
        super().__init__(name="All In")


    def percentage_in_actions(self, past_prices, cash, shares):
        #Queremos 100% invertido.
        return 1.0
