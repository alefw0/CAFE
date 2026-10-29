import numpy as np
import pandas as pd
from arch.bootstrap import IIDBootstrap, StationaryBootstrap

def r2(usd, trm):
    """
    Calcula el R^2 entre los retornos del café en USD y los retornos del café en COP.
    """
    cop = usd + trm
    return np.corrcoef(cop, usd)[0, 1] ** 2

filas = []
for horizonte in ['diario', 'semanal', 'mensual']:
    r = pd.read_csv(f'data/processed/retornos_{horizonte}.csv', index_col=0)
    usd = r['Cafe'].to_numpy()
    trm = r['TRM'].to_numpy()
    cop = usd + trm

    var_cop = np.var(cop, ddof=1)
    cov_usd_tmr = np.cov(usd, trm)[0, 1]

    # interesante, usar bootstrap para calcular el intervalo de confianza del R^2, pues es una medida de correlación y no tiene distribución normal. Estacionario para diario y IID para semanal y mensual, pues los retornos diarios son autocorrelacionados y los semanales y mensuales no (¿supuesto?).
    # intteresante hablar de esto en la presentacion. Estudiar esto!
    if horizonte == 'diario':
        bootstrap =StationaryBootstrap(20, usd, trm, seed=57)
    else:
        bootstrap = IIDBootstrap(usd, trm, seed=57)
    inferior, superior = bootstrap.conf_int(r2, 1000, method='percentile').ravel()

    filas.append({
        'frecuencia': horizonte,
        'n': len(r),
        'var_cafe': np.var(usd, ddof=1),
        'var_trm': np.var(trm, ddof=1),
        'cov2': 2 * cov_usd_tmr / var_cop,
        'corr_cafe_tmr': np.corrcoef(usd, trm)[0, 1],
        'r2': r2(usd, trm),
        'r2_inf': inferior,
        'r2_sup': superior,
        'horizonte_optimo': np.cov(cop, usd)[0, 1] / np.var(usd, ddof=1),
    })

tabla = pd.DataFrame(filas).round(4)
tabla.to_csv('data/processed/descomposicion.csv', index=False)
print(tabla.to_string(index=False))