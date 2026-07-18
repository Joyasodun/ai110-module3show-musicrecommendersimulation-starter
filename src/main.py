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


def main() -> None:
    songs = load_songs(DATA_PATH)
    print(f"Loaded songs: {len(songs)}")

    # Default demo profile: someone who wants happy, upbeat pop.
    user_prefs = {
        "genre": "pop",    # favorite_genre
        "mood": "happy",   # favorite_mood
        "energy": 0.8,     # target_energy -> songs near this level score higher
    }

    recommendations = recommend_songs(user_prefs, songs, k=5)

    print(f"\nTop {len(recommendations)} recommendations "
          f"for {user_prefs['mood']} / {user_prefs['genre']}:\n")
    for rank, (song, score, explanation) in enumerate(recommendations, start=1):
        print(f"{rank}. {song['title']} - {song['artist']}")
        print(f"   Score: {score:.2f}")
        print(f"   Why:   {explanation}")
        print()


if __name__ == "__main__":
    main()
