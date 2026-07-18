# 🎧 Model Card: Music Recommender Simulation

## 1. Model Name

**CheckDaVibezz**

---

## 2. Goal / Task

CheckDaVibezz suggests songs you might like. You tell it three things: a favorite
genre, a favorite mood, and how much energy you want. It then looks at every
song in the catalog and picks the top few for you. Each pick comes with a short
reason, so you can see why it was chosen. It is not trying to predict the
future. It is just ranking the songs it has and putting the best matches first.

---

## 3. Data Used

- **Size:** 17 songs. Small on purpose, so it is easy to read and test.
- **Features per song:** title, artist, genre, mood, energy, tempo, valence
  (how positive it feels), danceability, and acousticness.
- **Genres:** pop, lofi, rock, ambient, jazz, synthwave, indie pop, rap, pop
  rock, afrobeats, afrobeats amapiano, funk pop, reggaeton.
- **Moods:** happy, chill, intense, relaxed, moody, focused, sad, uplifting,
  hopeful, playful, romantic.
- **Limits:** The catalog is tiny. It leans toward upbeat pop and afrobeats.
  Many kinds of music (classical, country, metal, and most non-Western genres)
  are not in it. If a song is not in the data, it can never be suggested.

---

## 4. Algorithm Summary

Think of scoring like giving out points. Each song starts at zero. Then it
earns points for each way it matches your taste:

- **Mood** is worth the most (30%). The mood you want is what you really want
  to hear.
- **Positivity (valence)** and **preference** are next (20% each). Preference is
  a slot for past likes, but there is no like history yet, so it is 0 for now.
- **Energy** and **genre** are worth less (15% each). Genre counts less because
  the genre labels are messy.

Matches do not have to be exact. A close match earns partial points. So
*afrobeats amapiano* counts as close to *afrobeats*, and *uplifting* counts as
close to *happy*. Once every song has a score, the songs are sorted from highest
to lowest, and the top few are shown.

Two things I changed from the starter code:

1. Mood and genre are now two separate signals. The starter said "mood" but was
   really comparing genres.
2. Close matches now earn partial credit, instead of only exact matches.

---

## 5. Observed Behavior / Biases

The main pattern I found is a **high-energy filter bubble**. The system gives
every upbeat, positive song bonus points, no matter what mood you asked for.
Energy only earns points for being close to your target, but positivity is a
free bonus. So loud, happy songs like *Cake by the Ocean* and *Gym Hero* keep
showing up on lists where they do not belong. They appeared for the *sad*
profile and even for the *intense rock* profile. In plain words: cheerful pop
keeps crashing lists it was not invited to. The small, pop-heavy catalog makes
this worse, so quieter or darker tastes get thinner, less accurate results.

Other limits:

- It ignores data it already has: tempo, danceability, and acousticness are
  loaded but never scored.
- It has no real like history, so it cannot learn from what you played.
- The "close match" lists are hand-written by me, so they reflect my judgment
  and can be wrong.
- One genre + mood + energy can dominate the list, which crowds out variety.

---

## 6. Evaluation Process

### Profiles tested

I stress-tested the recommender with five profiles: three ordinary tastes and
two adversarial edge cases designed to try to "trick" the scoring logic. All
five are defined in [src/main.py](src/main.py) and run with
`python3 -m src.main`.

| Profile | genre | mood | energy | Why I picked it |
|---|---|---|---|---|
| High-Energy Pop | pop | happy | 0.90 | clean, upbeat mainstream taste |
| Chill Lofi | lofi | chill | 0.35 | low-energy study/relax taste |
| Deep Intense Rock | rock | intense | 0.90 | loud, high-energy taste |
| Adversarial: High-Energy Sad | pop | sad | 0.95 | mood + energy **contradict** each other |
| Adversarial: Unknown Taste | polka | grief | 0.50 | genre + mood match **nothing** in catalog |

### Terminal output

```
======================================================================
PROFILE: High-Energy Pop
  genre='pop' mood='happy' energy=0.9
======================================================================
1. Sunrise City - Neon Echo
   Score: 0.76
   Why:   mood match: happy (+0.30), genre match: pop (+0.15), upbeat, positive feel (+0.17), energy close to target (+0.14)
2. Rooftop Lights - Indigo Parade
   Score: 0.68
   Why:   mood match: happy (+0.30), partial genre match: indie pop (+0.09), upbeat, positive feel (+0.16), energy close to target (+0.13)
3. Cake by the Ocean - DNCE
   Score: 0.65
   Why:   related mood: playful (+0.24), partial genre match: funk pop (+0.09), upbeat, positive feel (+0.18), energy close to target (+0.15)
4. Never Say Never - Justin Bieber
   Score: 0.65
   Why:   related mood: hopeful (+0.24), genre match: pop (+0.15), energy close to target (+0.14)
5. Ogaranya - Adekunle Gold
   Score: 0.59
   Why:   mood match: happy (+0.30), upbeat, positive feel (+0.16), energy close to target (+0.12)
```

```
======================================================================
PROFILE: Chill Lofi
  genre='lofi' mood='chill' energy=0.35
======================================================================
1. Library Rain - Paper Lanterns
   Score: 0.72
   Why:   mood match: chill (+0.30), genre match: lofi (+0.15), energy close to target (+0.15)
2. Midnight Coding - LoRoom
   Score: 0.70
   Why:   mood match: chill (+0.30), genre match: lofi (+0.15), energy close to target (+0.14)
3. Focus Flow - LoRoom
   Score: 0.65
   Why:   related mood: focused (+0.24), genre match: lofi (+0.15), energy close to target (+0.14)
4. Spacewalk Thoughts - Orbit Bloom
   Score: 0.57
   Why:   mood match: chill (+0.30), energy close to target (+0.14)
5. Coffee Shop Stories - Slow Stereo
   Score: 0.53
   Why:   related mood: relaxed (+0.24), upbeat, positive feel (+0.14), energy close to target (+0.15)
```

```
======================================================================
PROFILE: Deep Intense Rock
  genre='rock' mood='intense' energy=0.9
======================================================================
1. Storm Runner - Voltline
   Score: 0.69
   Why:   mood match: intense (+0.30), genre match: rock (+0.15), energy close to target (+0.15)
2. Gym Hero - Max Pulse
   Score: 0.60
   Why:   mood match: intense (+0.30), upbeat, positive feel (+0.15), energy close to target (+0.15)
3. Fighting My Demons - Ken Carson
   Score: 0.51
   Why:   mood match: intense (+0.30), darker, moodier feel (+0.07), energy close to target (+0.14)
4. Cake by the Ocean - DNCE
   Score: 0.32
   Why:   upbeat, positive feel (+0.18), energy close to target (+0.15)
5. Despacito - Luis Fonsi
   Score: 0.31
   Why:   upbeat, positive feel (+0.17), energy close to target (+0.14)
```

```
======================================================================
PROFILE: Adversarial: High-Energy Sad
  genre='pop' mood='sad' energy=0.95
======================================================================
1. The Man Who Cant Be Moved - The Script
   Score: 0.56
   Why:   mood match: sad (+0.30), partial genre match: pop rock (+0.09), darker, moodier feel (+0.08)
2. Night Drive Loop - Neon Echo
   Score: 0.46
   Why:   related mood: moody (+0.24), energy close to target (+0.12)
3. Gym Hero - Max Pulse
   Score: 0.45
   Why:   genre match: pop (+0.15), upbeat, positive feel (+0.15), energy close to target (+0.15)
4. Sunrise City - Neon Echo
   Score: 0.45
   Why:   genre match: pop (+0.15), upbeat, positive feel (+0.17), energy close to target (+0.13)
5. Cake by the Ocean - DNCE
   Score: 0.41
   Why:   partial genre match: funk pop (+0.09), upbeat, positive feel (+0.18), energy close to target (+0.14)
```

```
======================================================================
PROFILE: Adversarial: Unknown Taste
  genre='polka' mood='grief' energy=0.5
======================================================================
1. Ogaranya - Adekunle Gold
   Score: 0.28
   Why:   upbeat, positive feel (+0.16)
2. Rooftop Lights - Indigo Parade
   Score: 0.27
   Why:   upbeat, positive feel (+0.16)
3. Cake by the Ocean - DNCE
   Score: 0.27
   Why:   upbeat, positive feel (+0.18)
4. Coffee Shop Stories - Slow Stereo
   Score: 0.27
   Why:   upbeat, positive feel (+0.14), energy close to target (+0.13)
5. Despacito - Luis Fonsi
   Score: 0.27
   Why:   upbeat, positive feel (+0.17)
```

### Does it feel right? What surprised me

For **High-Energy Pop**, the top of the list feels right to my own intuition —
*Sunrise City* and *Rooftop Lights* are exactly the bright, danceable pop I'd
expect. The surprise was lower down: *Cake by the Ocean* (a *playful* funk-pop
song) beat *Never Say Never* (an actual *pop* song), because the valence bonus
for being upbeat outweighed the exact genre match. That was my first hint that
positivity was pulling too hard.

I also want to note that to get *Ogaranya* and *Gratitude* to rank close to each
other, I had to teach the system that some labels mean almost the same thing. I
set it up so that *afrobeats* and *afrobeats amapiano* count as basically the
same genre, and *happy* and *uplifting* count as basically the same mood. Before
that, the system treated those labels as totally foreign to each other, which
pushed two very similar songs far apart.

The two adversarial profiles are where the logic showed its seams:

- **High-Energy Sad** exposes a contradiction the system can't satisfy: the
  catalog has no sad songs that are also high-energy, so it correctly puts the
  one true sad song first, then falls back to *loud, happy pop* (*Gym Hero*,
  *Sunrise City*) — the opposite of a sad mood. The user asked for sad, and by
  #3 the list is cheerful. That's the surprise, and it points straight at the
  bias in the "Observed Behavior / Biases" section.
- **Unknown Taste** (polka / grief) matches nothing, so every score collapses
  to roughly 0.27 and the ranking is decided almost entirely by valence. The
  system never says "I have nothing for you" — it confidently recommends happy
  afrobeats to someone who asked for polka grief.

Another weak spot is the definitions behind the algorithm — how each attribute
is scored and which words are treated as related. Those are hand-written by me,
so they are a place we still need to work on to make the results as accurate as
possible.

### Profile-to-profile comparisons

- **High-Energy Pop vs. Chill Lofi:** these are near-opposites and the outputs
  prove the energy signal works. Pop pulls loud, sunny songs (energy ~0.8+);
  lofi pulls quiet study tracks (energy ~0.35). No song appears on both lists.
  This makes sense: same scoring formula, but a low energy target flips which
  songs sit "close," and the two genres don't overlap.
- **Deep Intense Rock vs. High-Energy Pop:** both want energy 0.90, so the gap
  is driven by mood and genre, not energy. Rock surfaces *Storm Runner* /
  *Gym Hero* / *Fighting My Demons* (all *intense*); pop surfaces happy tracks.
  Tellingly, *Cake by the Ocean* sneaks into **both** lists — a sign that a
  loud, positive song is hard to keep out of any high-energy profile.
- **Deep Intense Rock vs. Chill Lofi:** the clearest contrast — high energy +
  intense mood vs. low energy + chill mood. Scores also drop faster for rock
  (#4 is only 0.32) because the catalog has just three genuinely intense songs,
  so after the real matches it scrapes the barrel. Lofi stays higher because
  there are more low-energy songs to fill the list.
- **High-Energy Sad vs. High-Energy Pop:** same genre (pop) and similar energy,
  only the mood differs. Yet three songs (*Gym Hero*, *Sunrise City*,
  *Cake by the Ocean*) appear on **both** lists. That overlap is the bug, not a
  feature: a "sad" request should not share most of its results with a "happy"
  one.

**Explaining it to a non-programmer:** think of the score as points. Every song
gets bonus points just for *sounding upbeat and positive*, no matter what mood
you asked for. So an upbeat song like *Gym Hero* walks in with free points and
lands near the top of almost every list — even a sad one. That's why the same
few "happy" songs keep showing up for people who wanted something completely
different: the system quietly rewards cheerfulness on top of what you actually
requested.

### Data experiment: double energy weight, halve genre weight

I tested the system's sensitivity by **doubling the energy weight (0.15 →
0.30) and halving the genre weight (0.15 → 0.075)**. To keep the math valid I
re-balanced so the five weights still sum to exactly **1.0** (the freed budget
went to the preference slot, which is 0 with no rating history, so it doesn't
distort the live signals). I verified the sum with an assertion before running.

| Weight | Original | Experiment |
|---|---|---|
| mood | 0.30 | 0.30 |
| valence | 0.20 | 0.20 |
| energy | 0.15 | **0.30** |
| genre | 0.15 | **0.075** |
| preference | 0.20 | 0.125 |
| **sum** | **1.00** | **1.00** ✓ |

```
weights: mood=0.3 valence=0.2 energy=0.3 genre=0.075 pref=0.125
Sum = 1.000  (must equal 1.000)
OK: weights sum to exactly 1.0

============================================================
EXPERIMENT (2x energy, 0.5x genre, sum=1.0) — High-Energy Pop
============================================================
1. Sunrise City - Neon Echo  (Score: 0.82)
2. Rooftop Lights - Indigo Parade  (Score: 0.77)
3. Cake by the Ocean - DNCE  (Score: 0.75)
4. Ogaranya - Adekunle Gold  (Score: 0.71)
5. Never Say Never - Justin Bieber  (Score: 0.71)

============================================================
EXPERIMENT (2x energy, 0.5x genre, sum=1.0) — Deep Intense Rock
============================================================
1. Storm Runner - Voltline  (Score: 0.77)
2. Gym Hero - Max Pulse  (Score: 0.74)
3. Fighting My Demons - Ken Carson  (Score: 0.66)
4. Cake by the Ocean - DNCE  (Score: 0.47)
5. Despacito - Luis Fonsi  (Score: 0.45)
```

**Result: more *different* than more *accurate*.** The top of each list barely
moved (the strong mood/genre matches still win), but energy-heavy songs climbed
— *Cake by the Ocean* rose from #3 to a near-tie for #2 in the pop list, and
*Ogaranya* jumped from #5 to #4. Weakening genre made "close energy + upbeat"
enough to outrank a real genre match. This confirms the "Observed Behavior /
Biases" finding:
leaning harder on energy amplifies the high-energy filter bubble rather than
fixing it. I reverted to the original weights afterward, so
[src/recommender.py](src/recommender.py) is unchanged.

### Simple tests run

`tests/test_recommender.py` (ranking + explanations) passes, and I re-ran
`python3 -m src.main` after each change to eyeball the ranking.

---

## 7. Intended Use and Non-Intended Use

**What it is for:**

- Learning how a recommender works. It shows how scoring and sorting turn data
  into a ranked list.
- Trying out different tastes and seeing why each song was picked.
- A small, safe sandbox for class experiments.

**What it should not be used for:**

- Real music apps or real users. The catalog is tiny and biased.
- Any real decision that matters. It cannot judge songs it does not have.
- Claiming to know someone's true taste. It only reads three inputs, not a
  person.

---

## 8. Ideas for Improvement

- Use the data it already ignores: tempo, danceability, and acousticness.
- Add real like history so it can learn from what you actually play.
- Add variety to the top 5 so one genre or mood cannot take over the list.
- Make sure defnitions are related closer to one another to improve accuracy, maybe get more specific and into detail but that would require more time and coding and better training.

---

## 9. Personal Reflection

**Biggest learning moment.** The big one was realizing a recommender is not
magic. It is just scoring every song and sorting them. All the "smarts" live in
how you weight things. Once I saw that, the whole system stopped feeling
mysterious.

**How AI tools helped, and when I checked them.** AI tools were great for
speeding up boring parts, like drafting the extra profiles and spotting the
filter-bubble bias. But I had to double-check the math. When I ran my
weight-shift experiment, the AI's first version left the weights adding up to
more than 1.0, which is not valid. I caught it, and we fixed it so the weights
sum to exactly 1.0. That reminded me the AI can be confidently wrong, so I
verify numbers myself.

**What surprised me.** I was surprised how much a simple points-and-sort system
can "feel" like a real recommendation. There is no learning and no neural net,
yet the top picks often felt right. It made me see that a lot of "AI feel" is
really just good scoring choices.

**What I would try next.** I would add real like history so it learns from me,
score the unused features like tempo and danceability, and add variety so the
same happy pop songs stop crashing every list.
