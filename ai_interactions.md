# AI Interactions Log

> **Stretch features only.** Only fill in the sections that apply to stretch features you attempted. If you did not attempt a stretch feature, leave its section blank or delete it. This file is not required for the core project.

---

## Agentic Workflow (SF8)

> Document your experience using an AI agent (e.g., Cursor Agent, Claude, Copilot) to make multi-step changes autonomously.

**What task did you give the agent?**

Build out the music recommender end to end: design the scoring recipe,
implement `load_songs`, `score_song`, and `recommend_songs`, format the CLI
output, and commit/push the work. Later I asked it to tune the ranking so
"Gratitude" by Asake would land at #2 for my afrobeats/happy profile.

**Prompts used:**

- "how much should a Mood match count compared to a Genre match?"
- "fix the mood genre thing" (mood_score was scoring genre, not mood)
- "Sketch the recommendation logic / finalize my point-weighting recipe"
- "implement load_songs using the csv module, convert numeric values to floats"
- "implement score_song: return a numeric score AND a list of reasons"
- "most Pythonic way to score all songs and return the top k sorted; explain
  .sort() vs sorted()"
- "I don't like the recommendations — Gratitude should be #2"

**What did the agent generate or change?**

- `src/recommender.py` — split mood vs. genre into separate scoring signals,
  added tolerant genre matching (afrobeats ~ afrobeats amapiano) and fuzzy
  mood matching (happy ~ uplifting), point-aware reason strings, and a
  Pythonic `recommend_songs` using `sorted(..., reverse=True)`.
- `src/main.py` — numbered CLI layout (title, artist, score, reasons); runs
  as both `python src/main.py` and `python -m src.main`.
- `README.md` — Sample Recommendation Output section with real terminal output.
- `data/songs.csv` — expanded the catalog to 17 songs.
- Ran the app and `pytest` to verify; committed and pushed to `main`.

**What did you verify or fix manually?**

- Ran `python -m src.main` and checked the ranking against my own taste — the
  agent's first result buried "Gratitude" at #4, which I rejected. It
  diagnosed why (uplifting mood + amapiano genre both scored as mismatches)
  and I had it add fuzzy mood matching, which moved it to #2.
- Confirmed `tests/test_recommender.py` still passes after the changes.

---

## Design Pattern (SF10)

> Document how AI helped you choose or implement a design pattern.

**Which design pattern did you use?**

A Strategy-style scoring design: each feature (mood, genre, energy, valence,
preference) is its own small scoring function returning 0..1, and a single
weighted combiner blends them. Weights are named constants that sum to 1.0.

**How did AI help you brainstorm or implement it?**

I asked how to balance a mood match against a genre match. The AI recommended
keeping each signal as an independent, swappable scoring function with its own
weight, so I could re-tune one factor (or add fuzzy matching) without touching
the others. That's exactly what happened later: adding fuzzy mood matching
only changed `mood_score`, not the combiner or the other signals.

**How does the pattern appear in your final code?**

In `src/recommender.py`: `mood_score`, `genre_score`, `energy_score`,
`valence_score`, and `preference_score` are the strategies; `_weighted_score`
is the combiner that applies `W_MOOD`, `W_GENRE`, etc. Both the functional
(`score_song`) and OOP (`Recommender`) paths route through the same combiner.
