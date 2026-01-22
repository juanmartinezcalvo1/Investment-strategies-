# strategy.py
import math 

class Strategy:
    """
    Clase base para estrategias de inversión.
    Todas las estrategias concretas deben implementar percentage_in_actions().
    """

    def __init__(self, name: str):
        self.name = name  # nombre de la estrategia

    def percentage_in_actions(self, past_prices, cash, shares):
        """
        Método obligatorio que decide qué % del portfolio invertir en acciones.
        Las clases hijas deben implementarlo.
        Parámetros:
        - past_prices: con los precios de cierre hasta ayer.
        - cash: efectivo actual
        - shares: nº de acciones actuales

        """
        raise NotImplementedError("La estrategia debe implementar percentage_in_actions().")

    @staticmethod
    def sma(past_prices, n):
        """
        Media móvil simple (SMA) de los últimos n precios ANTERIORES a hoy.
        Equivalente a coger los n valores anteriores a 'date' en tu versión original.
        """
        # necesitamos al menos n días anteriores
        if len(past_prices) < n:
            return None

        precios = past_prices[-(n+1):-1]   # lista con exactamente n precios ANTERIORES,sin tener en cuenta el de hoy, que es el precio de cierre del día anterior.

        # Saco la media manualmente
        return sum(precios) / len(precios)

    @staticmethod
    def sigma(past_prices, n):
        """
        Desviación típica de los últimos n precios ANTERIORES a hoy.
        Conserva la misma lógica paso a paso que tu versión para DataFrame.
        """
        # necesitamos al menos n días anteriores
        if len(past_prices) < n:
            return None

        # Coger los n valores anteriores al dia,sin incluir el de precio del dia que es el de cierre del día anterior.
        precios = past_prices[-(n+1):-1]

        # Realizo los cálculos de media y varianza manualmente
        mean = sum(precios) / len(precios)
        var = sum((p - mean) ** 2 for p in precios) / len(precios)

        return math.sqrt(var)