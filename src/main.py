"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

You will implement the functions in recommender.py:
- load_songs
- score_song
- recommend_songs
"""

from recommender import load_songs, recommend_songs


def main() -> None:
    songs = load_songs("data/songs.csv") 

    # My taste profile: someone who loves upbeat, high-energy afrobeats.
    # Target values for the features my recommender scores on.
    user_prefs = {
        "genre": "afrobeats",   # favorite_genre  -> drives the mood/genre match
        "mood": "happy",        # favorite_mood
        "energy": 0.75,         # target_energy   -> songs near this level score higher
    }

    recommendations = recommend_songs(user_prefs, songs, k=5)

    print("\nTop recommendations:\n")
    for rec in recommendations:
        # You decide the structure of each returned item.
        # A common pattern is: (song, score, explanation)
        song, score, explanation = rec
        print(f"{song['title']} - Score: {score:.2f}")
        print(f"Because: {explanation}")
        print()


if __name__ == "__main__":
    main()
