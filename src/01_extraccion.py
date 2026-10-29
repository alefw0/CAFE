import pandas as pd
import yfinance as yf
from pathlib import Path

Path('data/raw').mkdir(parents=True, exist_ok=True)

Inicio = '2016-01-01'
Fin = '2026-10-23'

# café arábica bolsa de NY [centavos/libra] desde yahoo finance
cafe = yf.download('KC=F', start=Inicio, end='2026-10-24', auto_adjust=False, progress=False)['Close'].squeeze() # toca hacer end = Fin + 1 día porque yahoo finance no incluye el último día

# TRM desde la página de datos del gobierno
url = ('https://www.datos.gov.co/resource/32sa-8pi3.csv''?$limit=50000&$order=vigenciadesde')
trm = pd.read_csv(url, parse_dates=['vigenciadesde'])
trm = trm.groupby(trm['vigenciadesde'].dt.normalize())['valor'].last()

# TRM vigente del día que cotiza el café
trm = trm.reindex(cafe.index, method='ffill')

precios = pd.DataFrame({'TRM': trm, 'Cafe': cafe}).dropna().loc[Inicio:Fin]
precios.index.name = 'Fecha'
precios.to_csv('data/raw/datos_raw.csv')
print(f'{len(precios)} días, del {precios.index[0].date()} al {precios.index[-1].date()}')