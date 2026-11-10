# Project 07: the Sentry risk plot, redrawn for a general audience.
# Same data as starters/07_sentry_risk.py, with plain-language labels added.
# pip install requests pandas matplotlib
import json, os
import requests
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import FixedLocator

API = 'https://ssd-api.jpl.nasa.gov/sentry.api'
CACHE = 'data/sentry_list.json'
os.makedirs('data', exist_ok=True)
os.makedirs('plots', exist_ok=True)

# Download the Sentry list once and keep a copy in data/
if not os.path.exists(CACHE):
    r = requests.get(API, timeout=60)
    r.raise_for_status()
    with open(CACHE, 'w') as f:
        json.dump(r.json(), f)
with open(CACHE) as f:
    raw = json.load(f)

df = pd.DataFrame(raw['data'])
for col in ['ip', 'ps_cum', 'diameter']:
    df[col] = pd.to_numeric(df[col], errors='coerce')   # the API sends numbers as text


def dot_size(diameter_km):
    """Bigger asteroid = bigger dot (same rule as the starter script)."""
    return 5 + 300 * diameter_km


BLUE, INK, MUTED, GRID = '#2a78d6', '#0b0b0b', '#52514e', '#e5e4df'
fig = plt.figure(figsize=(13, 7))
ax = fig.add_axes([0.07, 0.13, 0.62, 0.79])   # plot on the left, explanation panel on the right

# The asteroids
ax.scatter(df['ip'], df['ps_cum'], s=dot_size(df['diameter'].fillna(0)),
           color=BLUE, alpha=0.45, edgecolors='white', linewidths=0.4)

# Reference lines for the "worry score"
ax.axhline(0, color=INK, linewidth=1.2)
ax.text(1.2e-10, 0.12, 'Score 0: as likely to hit as a random, undiscovered rock of the same size',
        fontsize=9, color=INK, va='bottom')
ax.axhspan(0, 1.5, color='#f3f2ee', zorder=0)
ax.text(1.2e-10, 0.75, 'Above this line = more worrying than normal.  Currently empty.',
        fontsize=9, color=MUTED, va='center', style='italic')
ax.axhline(-2, color=MUTED, linewidth=0.8, linestyle='--')
ax.text(1.2e-10, -1.9, 'Score -2: 100 times less likely than that background risk',
        fontsize=8.5, color=MUTED, va='bottom')

# Label a few objects worth talking about (text placed in empty parts of the plot)
callouts = {
    '29075 (1950 DA)':          ('1950 DA: the top score.\n1.3 km wide, possible hit in 2880', (1.5e-5, -0.75), 'right'),
    '101955 Bennu (1999 RQ36)': ('Bennu: 0.49 km wide.\nNASA sampled it in 2023', (2.5e-3, -0.75), 'left'),
    '(2010 RF12)':              ('2010 RF12: best odds (about 1 in 10), but tiny', (0.9, -2.4), 'right'),
}
for name, (text, xy_text, align) in callouts.items():
    row = df[df['fullname'].str.strip() == name].iloc[0]
    ax.annotate(text, (row['ip'], row['ps_cum']), xytext=xy_text, ha=align, va='center',
                fontsize=8.5, color=INK,
                arrowprops=dict(arrowstyle='-', color=MUTED, linewidth=0.8, shrinkA=2, shrinkB=4))

# x axis: write probabilities as "1 in N"
ticks = [1e-10, 1e-8, 1e-6, 1e-4, 1e-2, 1]
ax.set_xscale('log')
ax.xaxis.set_major_locator(FixedLocator(ticks))
ax.set_xticklabels(['1 in 10\nbillion', '1 in 100\nmillion', '1 in 1\nmillion',
                    '1 in\n10,000', '1 in\n100', 'certain'])
ax.set_xlim(5e-11, 1)
ax.set_ylim(-12.6, 1.5)
ax.set_xlabel('Chance of hitting Earth  →  more likely', fontsize=11)
ax.set_ylabel('Worry score (Palermo scale)  →  more worrying', fontsize=11)
ax.grid(color=GRID, linewidth=0.8)
ax.set_axisbelow(True)
ax.spines[['top', 'right']].set_visible(False)

# Size legend: what dot size means (in the right-hand panel)
handles = [ax.scatter([], [], s=dot_size(d), color=BLUE, alpha=0.45, label=lab)
           for d, lab in [(0.01, '10 m (a house)'), (0.1, '100 m (a stadium)'), (1.0, '1 km (a small town)')]]
fig.legend(handles=handles, title='Dot size = asteroid width', loc='upper left',
           bbox_to_anchor=(0.72, 0.92), frameon=False, labelspacing=1.4, fontsize=9.5,
           title_fontsize=10.5, alignment='left')

# How to read it (also in the right-hand panel)
fig.text(0.72, 0.62,
         'How to read this chart\n\n'
         '\u2022 Each dot is one asteroid that can\'t yet be\n'
         '   ruled out as a future impact.\n\n'
         '\u2022 Further right = higher odds of hitting.\n\n'
         '\u2022 Higher up = more worrying overall. The\n'
         '   worry score combines odds, size (bigger\n'
         '   is worse) and timing (far-future dates\n'
         '   count for less). Each step of 1 is 10x.\n\n'
         '\u2022 Dots climb from lower left to upper right\n'
         '   because higher odds mostly mean a higher\n'
         '   score. Big dots sit above the crowd: big\n'
         '   impacts are rare, so even low odds matter.\n\n'
         '\u2022 Nothing reaches score 0, the black line.',
         fontsize=9.5, color=INK, va='top', linespacing=1.25)

fig.suptitle(f'Every known asteroid that might hit Earth: {len(df):,} objects, and none above normal risk',
             x=0.07, ha='left', y=0.975, fontsize=13)
fig.text(0.01, 0.01, 'Data: NASA/JPL CNEOS Sentry API (ssd-api.jpl.nasa.gov/sentry.api). '
         'Odds are cumulative over all possible impact dates.', fontsize=7.5, color=MUTED)
plt.savefig('plots/sentry_risk_explained.png', dpi=150)
print('saved plots/sentry_risk_explained.png')
