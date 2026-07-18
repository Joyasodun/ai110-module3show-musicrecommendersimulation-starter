# 🎵 Music Recommender Simulation

## Project Summary

In this project you will build and explain a small music recommender system.

Your goal is to:

- Represent songs and a user "taste profile" as data
- Design a scoring rule that turns that data into recommendations
- Evaluate what your system gets right and wrong
- Reflect on how this mirrors real world AI recommenders

My version scores each song against a user's taste using my own definition of a musical
"vibe": 30% mood, 20% valence (emotional positivity), 15% energy (how close the song's
energy is to what the user wants), 15% genre, and 20% personal preference (how close a
song sits to the average vibe of songs the user liked before). It scores every song,
ranks them, and returns the top matches with a short explanation.

---

## How The System Works

### How real-world recommenders work, and what mine prioritizes

Real-world recommenders (Spotify, YouTube, Netflix) mostly learn from *behavior* — what
huge numbers of people played, skipped, liked, and replayed — and blend that with the
audio/content features of the items themselves. They don't rely on a human writing down
what a "vibe" is; they infer it from patterns in the data. My version is a simplified,
**content-based** recommender: instead of learning from a crowd, I hand-wrote the
definition of a vibe as a weighted formula and prioritize matching the *feel* of a song
(mood, emotional positivity, genre, and energy) to what a user says they want. It also leaves a
place for personal history, so once a user has liked songs before, it can nudge results
toward their established taste — a small step toward how the real systems personalize.

### Features used

**`Song`** uses:
- `mood` — the song's mood label (happy, chill, intense, etc.)
- `genre` — the song's genre label
- `valence` — emotional positivity (0–1)
- `energy` — intensity/pace of the track (0–1)
- (`id`, `title`, `artist`, `tempo_bpm`, `danceability`, `acousticness` are stored but not
  weighted in the current vibe formula)

**`UserProfile`** stores:
- `favorite_mood` — the mood the user is after (the strongest signal)
- `favorite_genre` — the user's preferred genre
- `target_energy` — the energy level the user wants
- `likes_acoustic` — captured for future use
- `liked_song_ids` — the user's history; empty by default, powers the preference term

### How a score is computed

```
vibe score = 0.30 × mood        (1 if mood matches, 0.8 if a related mood, else 0)
           + 0.20 × valence     (the song's own positivity value)
           + 0.15 × energy      (closeness of song energy to target)
           + 0.15 × genre       (1 if genre matches, 0.6 if a partial match, else 0)
           + 0.20 × preference  (closeness to the vibe of past-liked songs; 0 if no history)
```

### How songs are chosen

Every song is scored, the full list is sorted best-first, and the top *k* are returned
along with a short reason for each.

### The decisions behind the math

- **Mood is its own signal, and it counts the most.** The mood you are in is what you most
  want to hear, so it gets the biggest weight (30%). It is also a clean label, unlike the
  messy genre labels.
- **Close matches earn partial credit.** A match does not have to be exact. A related mood
  (happy ~ uplifting) earns 0.8, and a partial genre match (afrobeats ~ afrobeats amapiano)
  earns 0.6. This stops a good "same vibe" song from being buried just because its label is
  worded differently.
- **Closeness, not magnitude, for energy.** For energy I do not reward "more" — I reward
  *matching*. A user who wants calm music (target 0.3) should not get a high-energy track
  just because its energy number is large. So I measure the distance between the user's
  target and the song, then flip it: `energy_score = 1 - abs(target - song)`. Identical
  energy scores 1.0; opposite ends score near 0.
- **Valence used as-is.** The dataset already provides valence as a 0–1 positivity value,
  so I use it directly rather than deriving it — there are no lyrics in the data to compute
  it from.
- **Genre counts, but less.** The genre labels in the data are noisy (afrobeats vs.
  afrobeats amapiano), so genre earns fewer, softer points than mood.
- **A preference slot that stays at 0 until there is history.** Personal preference is worth
  20%, but it only activates once a user has liked songs before. With no history it
  contributes 0. When history exists, I average the valence and energy of past-liked songs
  into a "taste profile" and score new songs by closeness to that center — reusing the same
  distance-then-invert idea as energy.

---

## Getting Started

### Setup

1. Create a virtual environment (optional but recommended):

   ```bash
   python -m venv .venv
   source .venv/bin/activate      # Mac or Linux
   .venv\Scripts\activate         # Windows
   ```

2. Install dependencies

```bash
pip install -r requirements.txt
```

3. Run the app:

```bash
python -m src.main
```

### Running Tests

Run the starter tests with:

```bash
pytest
```

You can add more tests in `tests/test_recommender.py`.

---

## Sample Recommendation Output

Running `python -m src.main` with the demo **afrobeats / happy** profile
(`genre=afrobeats, mood=happy, energy=0.75`) produces:

```
Loaded songs: 17

Top 5 recommendations for happy / afrobeats:

1. Ogaranya - Adekunle Gold
   Score: 0.76
   Why:   mood match: happy (+0.30), genre match: afrobeats (+0.15), upbeat, positive feel (+0.16), energy close to target (+0.15)

2. Gratitude - Asake
   Score: 0.63
   Why:   related mood: uplifting (+0.24), partial genre match: afrobeats amapiano (+0.09), upbeat, positive feel (+0.15), energy close to target (+0.15)

3. Rooftop Lights - Indigo Parade
   Score: 0.61
   Why:   mood match: happy (+0.30), upbeat, positive feel (+0.16), energy close to target (+0.15)

4. Sunrise City - Neon Echo
   Score: 0.61
   Why:   mood match: happy (+0.30), upbeat, positive feel (+0.17), energy close to target (+0.14)

5. Cake by the Ocean - DNCE
   Score: 0.55
   Why:   related mood: playful (+0.24), upbeat, positive feel (+0.18), energy close to target (+0.13)
```

---

## Experiments You Tried

I stress-tested the recommender with five taste profiles: three normal ones
(High-Energy Pop, Chill Lofi, Deep Intense Rock) and two adversarial ones built
to trick the scoring. The first adversarial profile asked for a *sad* mood but
*high* energy, which contradict each other. The second asked for a genre and
mood that are not in the catalog at all (polka / grief).

I also ran a weight experiment: I doubled the energy weight (0.15 → 0.30) and
halved the genre weight (0.15 → 0.075), keeping all weights summing to exactly
1.0 so the math stayed valid. The result was more *different* than more
*accurate* — the top picks barely moved, but loud, upbeat songs climbed higher.

The full profiles, terminal output, side-by-side comparisons, and experiment
numbers are documented in the model card.

---

## Limitations and Risks

- It only works on a tiny catalog (17 songs), so it can never suggest anything
  outside that list.
- It does not understand lyrics or language — it only reads a few labels and
  numbers per song.
- It over-favors upbeat, high-energy songs. They earn a positivity bonus no
  matter what mood you ask for, so they crash lists they do not belong on.
- The catalog leans toward pop and afrobeats, so those tastes get good results
  while other tastes get thin ones.

I go deeper on these in the [model card](model_card.md).

---

## Reflection

Building this made "recommendation" feel a lot less like magic. Under the hood
it is just scoring every song against your taste and sorting the list. All the
"smarts" live in how you weight each feature. A recommender does not really
*know* you — it turns a few numbers into a ranking, and that ranking is only as
good as the data and the weights behind it.

The project also showed me how easily bias creeps in. My scoring gave every
upbeat song a free positivity bonus, so cheerful pop kept showing up even for a
*sad* request. On top of that, my catalog leaned toward pop and afrobeats, so
those tastes always won. In a real system, the same two things — a scoring
choice and a skewed dataset — are exactly where unfairness would show up:
whatever the data includes and whatever the formula rewards quietly decides what
anyone is ever shown.

For the full write-up, see the [model card](model_card.md).



