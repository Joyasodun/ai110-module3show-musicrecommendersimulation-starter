"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

You will implement the functions in recommender.py:
- load_songs
- score_song
- recommend_songs
"""

import os

# Works whether run as `python src/main.py` or `python -m src.main`.
try:
    from recommender import load_songs, recommend_songs
except ImportError:
    from src.recommender import load_songs, recommend_songs

# Resolve the CSV relative to this file, so cwd doesn't matter.
DATA_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "songs.csv")


# ---------------------------------------------------------------------------
# Evaluation profiles.
#
# The first three are "normal" diverse tastes. The last two are adversarial /
# edge-case profiles used to stress-test the scoring logic (see model_card.md,
# Evaluation section): a self-contradicting profile (high energy + sad mood)
# and an "empty" profile that matches nothing in the catalog.
# ---------------------------------------------------------------------------
PROFILES = {
    "High-Energy Pop": {
        "genre": "pop",
        "mood": "happy",
        "energy": 0.90,
    },
    "Chill Lofi": {
        "genre": "lofi",
        "mood": "chill",
        "energy": 0.35,
    },
    "Deep Intense Rock": {
        "genre": "rock",
        "mood": "intense",
        "energy": 0.90,
    },
    # Adversarial: mood and energy pull in opposite directions. "sad" songs in
    # the catalog are low-energy, but the user demands energy 0.95.
    "Adversarial: High-Energy Sad": {
        "genre": "pop",
        "mood": "sad",
        "energy": 0.95,
    },
    # Adversarial: nothing in the catalog matches genre or mood, so ranking
    # falls back entirely to energy + valence.
    "Adversarial: Unknown Taste": {
        "genre": "polka",
        "mood": "grief",
        "energy": 0.50,
    },
}


def run_profile(name: str, user_prefs: dict, songs: list) -> None:
    recommendations = recommend_songs(user_prefs, songs, k=5)
    print("=" * 70)
    print(f"PROFILE: {name}")
    print(f"  genre={user_prefs['genre']!r} mood={user_prefs['mood']!r} "
          f"energy={user_prefs['energy']}")
    print("=" * 70)
    for rank, (song, score, explanation) in enumerate(recommendations, start=1):
        print(f"{rank}. {song['title']} - {song['artist']}")
        print(f"   Score: {score:.2f}")
        print(f"   Why:   {explanation}")
    print()


def main() -> None:
    songs = load_songs(DATA_PATH)
    print(f"Loaded songs: {len(songs)}\n")
    for name, prefs in PROFILES.items():
        run_profile(name, prefs, songs)


if __name__ == "__main__":
    main()
