# vol_breakout.py
from strategy import Strategy

class VolBreakoutStrategy(Strategy):
    """
    Estrategia Vol breakout.
      - Si P_last > SMA + multiplier * sigma → 100% invertido
      - Si P_last < SMA                    → 0% invertido
      - Si no → mantener el porcentaje anterior
    """

    def __init__(self, size, multiplier):
        #Parametros
        #size: ventana para SMA y sigma
        #multiplier: factor multiplicador sobre sigma
        super().__init__(name=f"Vol Breakout {size} mult={multiplier}")

        self.size = size
        self.multiplier = multiplier
        self.ptg_actions = 0.0 # porcentaje actual de inversión.

    def percentage_in_actions(self, past_prices, cash, shares):
        #Llamamos a sma y sigma del datasource
        sma = self.sma(past_prices, self.size)
        sigma = self.sigma(past_prices, self.size)

        # Si todavía no hay suficientes datos para calcular SMA o sigma, mantenemos la posición actual.
        if sma is None or sigma is None:
            return self.ptg_actions

        # El precio es el último precio disponible.
        price = past_prices[-1]
        upper = sma + self.multiplier * sigma  # umbral de breakout

        if price > upper:
            self.ptg_actions = 1.0
        elif price < sma:
            self.ptg_actions = 0.0
        else:
            # mantenemos self.ptg_actions
            pass

        return self.ptg_actions
