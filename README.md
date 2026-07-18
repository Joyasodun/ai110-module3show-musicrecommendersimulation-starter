# 🎵 Music Recommender Simulation

## Project Summary

In this project you will build and explain a small music recommender system.

Your goal is to:

- Represent songs and a user "taste profile" as data
- Design a scoring rule that turns that data into recommendations
- Evaluate what your system gets right and wrong
- Reflect on how this mirrors real world AI recommenders

My version scores each song against a user's taste using my own definition of a musical
"vibe": 30% valence (emotional positivity), 30% mood (approximated by genre match),
20% energy (how close the song's energy is to what the user wants), and 20% personal
preference (how close a song sits to the average vibe of songs the user liked before).
It scores every song, ranks them, and returns the top matches with a short explanation.

---

## How The System Works

### How real-world recommenders work, and what mine prioritizes

Real-world recommenders (Spotify, YouTube, Netflix) mostly learn from *behavior* — what
huge numbers of people played, skipped, liked, and replayed — and blend that with the
audio/content features of the items themselves. They don't rely on a human writing down
what a "vibe" is; they infer it from patterns in the data. My version is a simplified,
**content-based** recommender: instead of learning from a crowd, I hand-wrote the
definition of a vibe as a weighted formula and prioritize matching the *feel* of a song
(emotional positivity, genre, and energy) to what a user says they want. It also leaves a
place for personal history, so once a user has liked songs before, it can nudge results
toward their established taste — a small step toward how the real systems personalize.

### Features used

**`Song`** uses:
- `genre` — stands in for mood matching
- `valence` — emotional positivity (0–1)
- `energy` — intensity/pace of the track (0–1)
- (`id`, `title`, `artist`, `tempo_bpm`, `danceability`, `acousticness` are stored but not
  weighted in the current vibe formula)

**`UserProfile`** stores:
- `favorite_genre` — drives the mood/genre match
- `target_energy` — the energy level the user is after
- `favorite_mood`, `likes_acoustic` — captured for future use
- `liked_song_ids` — the user's history; empty by default, powers the preference term

### How a score is computed

```
vibe score = 0.30 × valence      (song's own positivity value)
           + 0.30 × mood          (1 if genre matches, else 0)
           + 0.20 × energy         (closeness of song energy to target)
           + 0.20 × preference     (closeness to the vibe of past-liked songs; 0 if no history)
```

### How songs are chosen

Every song is scored, the full list is sorted best-first, and the top *k* are returned
along with a short reason for each.

### The decisions behind the math

- **Closeness, not magnitude, for energy.** For energy I don't reward "more" — I reward
  *matching*. A user who wants calm music (target 0.3) should not get a high-energy track
  just because its energy number is large. So I measure the distance between the user's
  target and the song, then flip it: `energy_score = 1 - abs(target - song)`. Identical
  energy scores 1.0; opposite ends score near 0. This "distance-then-invert" trick is what
  makes the score reward closeness.
- **Valence used as-is.** The dataset already provides valence as a 0–1 positivity value,
  so I use it directly rather than deriving it — there are no lyrics in the data to compute
  it from.
- **Mood as a genre match.** With no separate "mood distance" available, I treat a genre
  match as a clean 1/0 signal: right genre = full mood points, wrong genre = none.
- **Weights reflect what matters most to me.** I split the score 30/30/20/20. Valence and
  genre-mood are the biggest drivers of vibe for me, so they get 30% each; energy fit and
  personal history each get 20%. A feature's weight answers "how much does getting this
  wrong ruin the vibe?" — the more it does, the higher the weight.
- **A preference slot that stays at 0 until there's history.** Personal preference is worth
  20%, but it only activates once a user has liked songs before. With no history it
  contributes 0, so today a vibe is effectively 30% valence + 30% mood + 20% energy. When
  history exists, I average the valence and energy of past-liked songs into a "taste
  profile" and score new songs by closeness to that center — reusing the same
  distance-then-invert idea as energy.

---

## Getting Started

### Setup

1. Create a virtual environment (optional but recommended):

   ```bash
   python -m venv .venv
   source .venv/bin/activate      # Mac or Linux
   .venv\Scripts\activate         # Windows

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

2. Rooftop Lights - Indigo Parade
   Score: 0.61
   Why:   mood match: happy (+0.30), upbeat, positive feel (+0.16), energy close to target (+0.15)

3. Sunrise City - Neon Echo
   Score: 0.61
   Why:   mood match: happy (+0.30), upbeat, positive feel (+0.17), energy close to target (+0.14)

4. Gratitude - Asake
   Score: 0.39
   Why:   partial genre match: afrobeats amapiano (+0.09), upbeat, positive feel (+0.15), energy close to target (+0.15)

5. Cake by the Ocean - DNCE
   Score: 0.31
   Why:   upbeat, positive feel (+0.18), energy close to target (+0.13)
```

---

## Experiments You Tried

Use this section to document the experiments you ran. For example:

- What happened when you changed the weight on genre from 2.0 to 0.5
- What happened when you added tempo or valence to the score
- How did your system behave for different types of users

---

## Limitations and Risks

Summarize some limitations of your recommender.

Examples:

- It only works on a tiny catalog
- It does not understand lyrics or language
- It might over favor one genre or mood

You will go deeper on this in your model card.

---

## Reflection

Read and complete `model_card.md`:

[**Model Card**](model_card.md)

Write 1 to 2 paragraphs here about what you learned:

- about how recommenders turn data into predictions
- about where bias or unfairness could show up in systems like this



