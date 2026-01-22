# sma_cross.py
from strategy import Strategy

class SmaCrossStrategy(Strategy):
    """
    Estrategia SMA Cross (cruce de medias móviles).
      - Si SMA_short > SMA_long  → 100% invertido (1.0)
      - Si SMA_short <= SMA_long → 0% invertido (0.0)
    """

    def __init__(self, size_short, size_long):
        #Parametros de la estrategia
        #size_short: tamaño de la media movil corta
        #size_long: tamaño de la media movil larga
        super().__init__(f"SMA Cross {size_short} vs {size_long}")

        self.size_short = size_short
        self.size_long = size_long

    def percentage_in_actions(self, past_prices, cash, shares):
        
        # Obtenemos las SMA del datasource
        sma_short = self.sma(past_prices, self.size_short)
        sma_long  = self.sma(past_prices, self.size_long)
        
        # Si todavía no hay suficientes datos para alguna de las SMA.
        if sma_short is None or sma_long is None:

            return 0.0

        if sma_short > sma_long:
            return 1.0   # 100% en acciones
        else:
            return 0.0   # todo en cash
