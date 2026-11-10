# Project 07: how much energy would an asteroid impact release?
# Compares two asteroids on NASA/JPL's Sentry list with familiar events.
# pip install requests matplotlib
import json, os
import requests
import matplotlib.pyplot as plt

API = 'https://ssd-api.jpl.nasa.gov/sentry.api'
os.makedirs('data', exist_ok=True)
os.makedirs('plots', exist_ok=True)


def sentry_summary(des):
    """Get one object's Sentry summary, cached in data/ so it downloads only once."""
    path = f'data/sentry_{des}.json'
    if not os.path.exists(path):
        r = requests.get(API, params={'des': des}, timeout=60)
        r.raise_for_status()
        with open(path, 'w') as f:
            json.dump(r.json(), f)
    with open(path) as f:
        return json.load(f)['summary']


# Asteroids: energy comes straight from JPL's Sentry data (field "energy", in megatons of TNT)
asteroids = {}
for des, name in [('29075', '1950 DA'), ('101955', 'Bennu')]:
    s = sentry_summary(des)
    asteroids[f"{name} ({float(s['diameter']):.2f} km)"] = float(s['energy'])

# Reference events: published estimates, typed in by hand (sources listed in the notes)
reference = {
    'Hiroshima bomb (1945)': 0.015,          # ~15 kilotons
    'Chelyabinsk meteor (2013)': 0.5,        # ~500 kilotons, Brown et al. 2013, Nature
    'Tsar Bomba, largest nuclear test (1961)': 50,
    'Chicxulub, dinosaur-killer (66 Myr ago)': 1e8,  # order of magnitude only
}

# Combine and sort smallest to largest
rows = [(k, v, 'reference') for k, v in reference.items()] + \
       [(k, v, 'sentry') for k, v in asteroids.items()]
rows.sort(key=lambda r: r[1])

BLUE, GRAY = '#2a78d6', '#a3a29c'
fig, ax = plt.subplots(figsize=(9, 4.8))
labels = [r[0] for r in rows]
values = [r[1] for r in rows]
colors = [BLUE if r[2] == 'sentry' else GRAY for r in rows]
ax.barh(labels, values, color=colors, height=0.6)
ax.set_xscale('log')
ax.set_xlim(1e-3, 1e11)


def nice(mt):
    """Write a megaton value in words people can read."""
    if mt < 1:
        return f'{mt * 1000:,.0f} kilotons'
    if mt >= 1e6:
        return f'{mt / 1e6:,.0f} million megatons'
    return f'{mt:,.0f} megatons'


for i, v in enumerate(values):
    ax.text(v * 1.4, i, nice(v), va='center', fontsize=9, color='#52514e')

ax.set_xlabel('Energy released, megatons of TNT (log scale: each tick is 100x more)')
ax.set_title('How big a bang? Asteroid impacts vs. familiar explosions', loc='left')
ax.spines[['top', 'right']].set_visible(False)
ax.grid(axis='x', color='#e5e4df', linewidth=0.8)
ax.set_axisbelow(True)

from matplotlib.patches import Patch
ax.legend(handles=[Patch(color=BLUE, label='Asteroid on Sentry list, if it hit (JPL data)'),
                   Patch(color=GRAY, label='Reference event (published estimate)')],
          loc='lower right', frameon=False, fontsize=9)
fig.text(0.01, 0.01, 'Data: NASA/JPL CNEOS Sentry API (ssd-api.jpl.nasa.gov/sentry.api). '
         'Chicxulub value is an order-of-magnitude estimate.', fontsize=7.5, color='#52514e')
plt.tight_layout(rect=(0, 0.03, 1, 1))
plt.savefig('plots/sentry_energy_comparison.png', dpi=150)
print('saved plots/sentry_energy_comparison.png')
for k, v, kind in rows:
    print(f'{k:45s} {v:>14,.3f} Mt  ({kind})')
