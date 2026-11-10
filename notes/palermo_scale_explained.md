# The Palermo scale and the Sentry plot, in plain terms

Notes for project 07 (`plots/sentry_risk.png`). Written for a non-astronomer.

## What a Palermo value means

Earth gets hit by space rocks all the time, mostly small ones, and big ones are rarer. The Palermo scale asks one question about a known asteroid:

> Is this asteroid more or less likely to hit us than a random, not-yet-discovered rock of the same size would be, over the same stretch of time?

- **0** means "about as likely as the normal background chance." Worth paying attention to.
- **-1** means 10 times less likely than background.
- **-2** means 100 times less likely than background.
- **-6** means a million times less likely than background.
- Above 0 would mean "more likely than background." No object on the list is above 0 right now.

Each step of 1 is a factor of 10, like the Richter scale for earthquakes.

Three things push the score up or down:

1. **Chance of impact.** Higher chance gives a higher score.
2. **Size.** Big impacts are naturally rare, so a big asteroid with even a small chance stands out more. Bigger gives a higher score.
3. **How far away the date is.** The further in the future, the more time there is for a random background rock to hit first, so the specific asteroid matters less. Further away gives a lower score.

## How to read the plot

- Each dot is one asteroid on NASA/JPL's Sentry list.
- Left to right: chance of impact. Each tick mark is 100 times more likely than the one before.
- Bottom to top: the Palermo score. Higher means more worth worrying about.
- Dot size: how big the asteroid is.

## Why the dots form a diagonal band

The chance of impact is the biggest ingredient in the Palermo score, so more likely objects (further right) generally score higher (further up). That gives the lower-left to upper-right trend.

It is a band and not a thin line because size and timing also move each dot:

- **Big asteroids sit above the band.** The large dots on the upper left have tiny odds but score high because they are big.
- **Small asteroids sit below where their odds alone would put them.** 2010 RF12, the dot at the far right, has about a 1 in 10 chance of hitting, the highest on the list, but it is very small, so its score is only about -2.9.
- **The top object, 1950 DA,** has only about a 1 in 3,000 chance, and its possible date is the year 2880, which lowers its score. It still ranks first (-0.98) because it is 1.3 km across.

## One-sentence takeaway

Even the "most worrying" asteroids are below the everyday background risk, and the Palermo scale exists so that a small rock with high odds and a big rock with low odds can be compared on one ruler.

Data: NASA/JPL CNEOS Sentry API, https://ssd-api.jpl.nasa.gov/doc/sentry.html
