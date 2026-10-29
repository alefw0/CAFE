# este script calcula los retornos (logaritmicos) en tres horizontes (diario, semanal y mensual)
import numpy as np
import pandas as pd
from pathlib import Path

Path('data/processed').mkdir(parents=True, exist_ok=True)

precios = pd.read_csv('data/raw/datos_raw.csv', index_col=0, parse_dates=True)

horizontes = {
    'diario': precios,
    'semanal': precios.resample('W-FRI').last(),   
    'mensual': precios.resample('ME').last().iloc[:-1] #quitando el ultimo mes pues está incompleto
}

for horizonte, p in horizontes.items():
    r = 100 * np.log(p).diff().dropna()
    r.to_csv(f'data/processed/retornos_{horizonte}.csv')
    print(f'{horizonte}: {len(r)} retornos')