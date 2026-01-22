# personal_strategy.py
from strategy import Strategy

class PersonalStrategy(Strategy):
    """
    - Solo invertimos si el precio está por encima de una SMA (tendencia alcista).
    - Dentro de la tendencia, ajustamos el porcentaje invertido según la volatilidad:
        * Volatilidad baja  -> porcentaje alto de acciones (max_ptg)
        * Volatilidad alta  -> porcentaje bajo de acciones (min_ptg)
        * Vol intermedia    -> interpolación lineal entre las dos.
    """

    def __init__(self, sma_size, vol_size,vol_low, vol_high, min_ptg=0.2, max_ptg=1.0):

        #Parámetros:
        #sma_size : tamaño de la media móvil (tendencia)
        #vol_size : tamaño para calcular sigma (volatilidad)
        #vol_low  : umbral inferior de sigma
        #vol_high : umbral superior de sigma
        #min_ptg  : porcentaje mínimo a invertir (si vol es muy alta)
        #max_ptg  : porcentaje máximo a invertir (si vol es muy baja)
        super().__init__(name="Personal Strategy")
        
        self.sma_size = sma_size
        self.vol_size = vol_size
        self.vol_low = vol_low
        self.vol_high = vol_high
        self.min_ptg = min_ptg
        self.max_ptg = max_ptg
        self.ptg_actions = 0.0


    def percentage_in_actions(self, past_prices, cash, shares):
        # Calculamos SMA (tendencia) y sigma (volatilidad)
        sma = self.sma(past_prices, self.sma_size)
        sigma = self.sigma(past_prices, self.vol_size)

        # Precio de cierre del día anterior
        price = past_prices[-1]  

        # Si no tenemos suficientes datos o tenemos una tendencia en el que el SMA esta por encima del precio, no invertimos.
        if sma is None or sigma is None or price<sma:
            self.ptg_actions = 0.0
            return self.ptg_actions

        # En tendencia alcista:
        if sigma <= self.vol_low:
            # Volatilidad baja -> podemos ir con máximo riesgo
            self.ptg_actions = self.max_ptg
        elif sigma >= self.vol_high:
            # Volatilidad muy alta -> reducimos porcentaje invertido
            self.ptg_actions = self.min_ptg
        else:
            # Vol intermedia -> interpolación lineal entre max_ptg y min_ptg,
            #teniendo en cuenta que cuanto más baja es la volatilidad, más alto es el porcentaje invertido.
            factor = (sigma - self.vol_low) / (self.vol_high - self.vol_low)
            self.ptg_actions = self.max_ptg - factor * (self.max_ptg - self.min_ptg)

        return self.ptg_actions
