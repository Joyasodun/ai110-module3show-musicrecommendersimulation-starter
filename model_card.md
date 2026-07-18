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

- **Profiles tested:** mainly pop/happy (the default) and afrobeats/happy
  (my own taste).
- **What I looked for:** whether the top results matched what I'd actually
  want to hear, and whether the reasons made sense.
- **What surprised me:** with exact-only matching, *Gratitude* (afrobeats
  amapiano / uplifting) landed at #4 even though it's clearly one of the best
  afrobeats picks — because both its genre and mood were "misses." That pushed
  me to add fuzzy matching, which moved it to #2.
- **Simple tests run:** `tests/test_recommender.py` (ranking + explanations)
  passes, and I re-ran `python -m src.main` after each change to eyeball the
  ranking.

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
