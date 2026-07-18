# 🎧 Model Card: Music Recommender Simulation

## 1. Model Name

**VibeFinder 1.0**

---

## 2. Intended Use

VibeFinder recommends songs from a small catalog based on a listener's stated
taste: a favorite genre, a favorite mood, and a target energy level. Given
those preferences, it ranks every song and returns the top few, each with a
short explanation of *why* it was picked.

- **What it generates:** a ranked shortlist of songs with human-readable reasons.
- **Assumptions about the user:** that they can describe their taste as a
  genre + mood + energy target, and that a single profile captures what they
  want right now (it has no long-term listening history yet).
- **Who it's for:** classroom exploration, not real users. It's a simulation
  for learning how recommenders turn data into ranked predictions.

---

## 3. How the Model Works

Think of each song as having a few labels and dials: a genre (afrobeats, pop),
a mood (happy, chill), and numbers for how energetic and how positive it feels.
You tell VibeFinder your favorite genre, favorite mood, and how energetic you
want the music. For every song, it awards points for each thing that lines up
with your taste, adds the points into one score, and then sorts all the songs
so the best matches come first.

The points aren't all equal. Mood counts the most, because the mood you're in
is really what you want to hear. Genre counts, but a little less, because the
genre labels are messy. Energy and positivity add smaller amounts based on how
close the song is to what you asked for.

The two biggest changes I made from the starter logic:

1. **Mood and genre became separate signals.** The starter code said "mood"
   but was secretly comparing genres, and the real mood label was never used.
2. **Matches can be "close," not just exact.** Instead of a song being either a
   perfect match or a total miss, near-matches earn partial credit — so
   *afrobeats amapiano* counts as close to *afrobeats*, and an *uplifting*
   song counts as close to *happy*.

---

## 4. Data

- **Catalog size:** 17 songs (I expanded the starter set from 10).
- **Genres represented:** pop, lofi, rock, ambient, jazz, synthwave, indie pop,
  rap, pop rock, afrobeats, afrobeats amapiano, funk pop, reggaeton.
- **Moods represented:** happy, chill, intense, relaxed, moody, focused, sad,
  uplifting, hopeful, playful, romantic.
- **Changes I made:** added 7 songs, including several afrobeats/afrobeats
  amapiano tracks that reflect my own taste.
- **What's missing:** the catalog is tiny and skewed toward upbeat pop and
  afrobeats. Whole traditions (classical, country, metal, most non-Western
  genres) aren't represented at all, so it can't recommend what isn't there.

---

## 5. Strengths

- Works well for a clear, upbeat profile — e.g. afrobeats/happy surfaces
  *Ogaranya* and *Gratitude* at the top, which matched my intuition.
- The partial-credit matching captures "these are basically the same vibe"
  cases that exact matching would miss (amapiano ~ afrobeats, uplifting ~ happy).
- Every recommendation comes with a breakdown of the points it earned, so the
  ranking is transparent, not a black box.

---

## 6. Limitations and Bias

**The weakness I confirmed during testing — a "high-energy filter bubble."**
The scoring only rewards energy for being *close* to your target, but valence
(positivity) is added as a flat bonus regardless of what you asked for. That
means loud, upbeat, positive songs like *Cake by the Ocean* and *Gym Hero*
leak into the top 5 of profiles they don't belong to — they showed up for the
sad-mood profile and even the intense-rock profile. In plain terms: happy,
high-energy pop keeps crashing lists where it wasn't invited, because the
system likes positivity for its own sake. Combined with the catalog leaning
toward pop/afrobeats (6 of 17 songs), quieter or darker tastes get a thinner,
less accurate shortlist — a filter bubble that favors the loud and the sunny.

Other limitations:

- **Ignores several features it has data for:** tempo, danceability, and
  acousticness are loaded but not scored.
- **No real preference history:** the preference slot exists but contributes 0
  until there's rating data, so it can't learn from what you actually played.
- **Hand-built "related" lists:** which moods/genres count as close is a fixed
  table I wrote, so it reflects my judgment and can be wrong or incomplete.
- **Catalog bias:** because the data leans pop/afrobeats, those tastes get good
  results while underrepresented genres get thin or no recommendations.
- **Single-profile overfitting:** one genre + mood + energy can dominate the
  ranking, crowding out variety.

---

## 7. Evaluation

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

The two adversarial profiles are where the logic showed its seams:

- **High-Energy Sad** exposes a contradiction the system can't satisfy: the
  catalog has no sad songs that are also high-energy, so it correctly puts the
  one true sad song first, then falls back to *loud, happy pop* (*Gym Hero*,
  *Sunrise City*) — the opposite of a sad mood. The user asked for sad, and by
  #3 the list is cheerful. That's the surprise, and it points straight at the
  bias in Section 6.
- **Unknown Taste** (polka / grief) matches nothing, so every score collapses
  to roughly 0.27 and the ranking is decided almost entirely by valence. The
  system never says "I have nothing for you" — it confidently recommends happy
  afrobeats to someone who asked for polka grief.

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
enough to outrank a real genre match. This confirms the finding in Section 6:
leaning harder on energy amplifies the high-energy filter bubble rather than
fixing it. I reverted to the original weights afterward, so
[src/recommender.py](src/recommender.py) is unchanged.

### Simple tests run

`tests/test_recommender.py` (ranking + explanations) passes, and I re-ran
`python3 -m src.main` after each change to eyeball the ranking.

---

## 8. Future Work

- Score the unused features (tempo, danceability, acousticness).
- Wire up real preference history so the model learns from what you liked.
- Add diversity to the top results so one genre/mood can't dominate.
- Replace the hand-written "related mood/genre" tables with something learned
  or data-driven.
- Handle multi-mood or shifting tastes instead of a single fixed profile.

---

## 9. Personal Reflection

<!-- A few sentences in your own voice. Some things you could touch on: -->
<!-- - Building this made "recommendation" concrete: it's really just scoring   -->
<!--   every item and sorting. The judgment is all in how you weight things.    -->
<!-- - The Gratitude example showed me how easily a scoring choice can bury a   -->
<!--   good result, and how small a tweak can fix it.                           -->
<!-- - It made me think about how the data you include (and leave out) quietly  -->
<!--   decides what any recommender can ever suggest.                           -->
