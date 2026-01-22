# Vol_scaling.py
from strategy import Strategy

class VolScalingStrategy(Strategy):
    """
    Vol Scaling:
    - Si rompe por arriba: comprar 10% del cash → aumentar porcentaje acciones
    - Si rompe por abajo: vender 10% del stock → disminuir porcentaje acciones
    - Si no → mantener
    """

    def __init__(self, size, multiplier):
        # Parámetros de la estrategia:
        # size : tamaño usado para la SMA y la sigma.
        # multiplier : anchura de las bandas en múltiplos de sigma.
        super().__init__(f"Vol Scaling {size} mult={multiplier:.2f}")

        self.size = size
        self.multiplier = multiplier
        self.current_ptg_actions = 0.0  # % invertido actualmente

    def percentage_in_actions(self, past_prices, cash, shares):
        # Cálculo de SMA y sigma a partir del datasource
        sma = self.sma(past_prices, self.size)
        sigma = self.sigma(past_prices, self.size)

        # Sin datos → mantenemos la última
        if sma is None or sigma is None:
            return self.current_ptg_actions

        # Calculamos los límites alrededor de la SMA
        upper = sma + self.multiplier * sigma
        lower = sma - self.multiplier * sigma

        # Valor actual del portfolio y de las acciones
        # El "precio actual" que usamos para comparar con las bandas es el último de past_prices
        price = past_prices[-1]
        portfolio_value = cash + shares * price
        current_stock_value = shares * price

        if price > upper:
            # Comprar 10% del cash
            buy_amount = 0.10 * cash
            new_stock_value = current_stock_value + buy_amount

        elif price < lower:
            # Vender 10% del stock
            sell_amount = 0.10 * current_stock_value
            new_stock_value = current_stock_value - sell_amount

        else:
            # Mantener
            new_stock_value = current_stock_value
            
        self.current_ptg_actions =new_stock_value / portfolio_value
        return self.current_ptg_actions
