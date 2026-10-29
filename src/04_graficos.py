# en esta parte se generan los dos gráficos del poster. Para no complicarme la vide usé ayuda, por lo que si tienen sugerencias para mejores gráficos, se los agradecería.

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import font_manager as fm

FIN = '2026-10-23'
AZUL, ROSA, GRIS = '#26285B', '#C74994', '#666666'
HORIZONTES = {'diario': 'Diario', 'semanal': 'Semanal', 'mensual': 'Mensual'}

# para usar la fuente del poster
for f in ('Regular', 'Bold'):
    fm.fontManager.addfont(f'poster/fonts/AncizarSans-{f}.ttf')
plt.rcParams.update({
    'font.family': 'Ancizar Sans', 'font.size': 15,
    'axes.spines.top': False, 'axes.spines.right': False,
    'axes.linewidth': 1.2, 'axes.edgecolor': GRIS,
    'xtick.color': GRIS, 'ytick.color': GRIS,
    'legend.frameon': False, 'pdf.fonttype': 42,
})

# figura 1, precios de 2016 a 2026
precios = pd.read_csv('data/raw/datos_raw.csv', index_col=0, parse_dates=True).loc[:FIN]
precios['COP'] = precios['Cafe'] * precios['TRM']
base = 100 * precios / precios.iloc[0]

fig, ax = plt.subplots(figsize=(7.5, 3.9))
for col, color, lw, lab, dy in [('COP', GRIS, 1.6, 'Café en pesos', 9),
                                ('Cafe', AZUL, 2.2, 'Café en dólares (KC=F)', -9),
                                ('TRM', ROSA, 2.2, 'TRM (pesos por dólar)', 0)]:
    ax.plot(base.index, base[col], color=color, lw=lw, label=lab)
    ax.annotate(f'{base[col].iloc[-1]:.0f}', (base.index[-1], base[col].iloc[-1]),
                xytext=(6, dy), textcoords='offset points', va='center',
                color=color, fontsize=14, fontweight='bold')
ax.axhline(100, color=GRIS, lw=0.8, ls=':')
ax.set_ylabel('Índice (enero 2016 = 100)')
ax.legend(loc='upper left', fontsize=13)
ax.grid(axis='y', color='#DDDDDD', lw=0.7)
fig.tight_layout()
fig.savefig('poster/img/fig_niveles.pdf')



# figura 2, R^2 por horizonte (diario, semanal, mensual)

res = pd.read_csv('data/processed/descomposicion.csv').set_index('frecuencia').loc[list(HORIZONTES)]
xs = np.arange(len(res))

fig, ax = plt.subplots(figsize=(7.5, 3.9))
ax.bar(xs, 100 * res['r2'], 0.6, color=AZUL, label='Explicada por el precio del café ($R^2$)')
ax.bar(xs, 100 * (1 - res['r2']), 0.6, bottom=100 * res['r2'], color=ROSA,
       label='Resto: TRM no ligada al café ($1-R^2$)')
for x, (_, row) in zip(xs, res.iterrows()):
    ax.text(x, 100 * row['r2'] / 2, f"{100 * row['r2']:.0f} %", ha='center', va='center',
            color='white', fontsize=20, fontweight='bold')
    ax.text(x, 100 * row['r2'] / 2 - 11, f"IC95 {100 * row['r2_inf']:.0f}–{100 * row['r2_sup']:.0f} %",
            ha='center', va='center', color='white', fontsize=12)
    ax.text(x, 100 * (1 + row['r2']) / 2, f"{100 * (1 - row['r2']):.0f} %", ha='center',
            va='center', color='white', fontsize=14, fontweight='bold')
ax.set_xticks(xs)
ax.set_xticklabels([f'{HORIZONTES[f]}\n(n = {n})' for f, n in res['n'].items()])
ax.set_ylabel('% de la varianza del café en pesos')
ax.set_ylim(0, 100)
ax.legend(loc='lower center', bbox_to_anchor=(0.5, 1.0), ncol=1, fontsize=13)
fig.tight_layout()
fig.savefig('poster/img/fig_r2.pdf', bbox_inches='tight')
print('Guardadas poster/img/fig_niveles.pdf y poster/img/fig_r2.pdf')