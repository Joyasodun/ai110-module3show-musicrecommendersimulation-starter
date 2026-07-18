import csv
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass, field

# ---------------------------------------------------------------------------
# Vibe definition (my personal weights)
#
#   mood        30%  -> real mood-column match (strongest intent signal)
#   valence     20%  -> emotional positivity, use the valence column as-is
#   energy      15%  -> use the energy column as-is
#   genre       15%  -> genre match (tolerant of messy labels)
#   preference  20%  -> "how the user rated songs before"
#
# Mood is weighted above genre: mood is what the listener actually feels and
# is a clean categorical, while genre labels in songs.csv are noisy
# (afrobeats vs afrobeats amapiano), so genre earns fewer, softer points.
#
# Option B: preference gets a real 20% slot in the formula, but there is no
# rating history in songs.csv yet, so preference_score() returns 0 for now.
# When rating history exists, only preference_score() needs to change --
# the weights and the rest of the formula stay untouched.
# ---------------------------------------------------------------------------
W_MOOD = 0.30
W_VALENCE = 0.20
W_ENERGY = 0.15
W_GENRE = 0.15
W_PREFERENCE = 0.20


@dataclass
class Song:
    """
    Represents a song and its attributes.
    Required by tests/test_recommender.py
    """
    id: int
    title: str
    artist: str
    genre: str
    mood: str
    energy: float
    tempo_bpm: float
    valence: float
    danceability: float
    acousticness: float


@dataclass
class UserProfile:
    """
    Represents a user's taste preferences.
    Required by tests/test_recommender.py
    """
    favorite_genre: str
    favorite_mood: str
    target_energy: float
    likes_acoustic: bool
    # Preference slot: song ids the user liked before. Empty for now ->
    # preference contributes 0 until rating history is available.
    liked_song_ids: List[int] = field(default_factory=list)


# ---------------------------------------------------------------------------
# Per-feature scoring pieces (each returns 0..1)
# ---------------------------------------------------------------------------
def valence_score(song_valence: float) -> float:
    """Valence used as-is: the song's own emotional-positivity value (0..1)."""
    return float(song_valence)


# Moods that read as "close enough" to each other -> partial mood credit.
# Symmetric: if A lists B, B is treated as related to A too.
MOOD_NEIGHBORS = {
    "happy": {"uplifting", "hopeful", "playful", "joyful", "upbeat"},
    "chill": {"relaxed", "focused", "calm"},
    "sad": {"moody", "melancholy"},
    "intense": {"energetic", "hype"},
    "romantic": {"hopeful", "moody"},
}


def _mood_related(a: str, b: str) -> bool:
    """True if a and b are listed as neighboring moods (either direction)."""
    return b in MOOD_NEIGHBORS.get(a, set()) or a in MOOD_NEIGHBORS.get(b, set())


def mood_score(favorite_mood: str, song_mood: str) -> float:
    """Mood match: 1.0 exact, 0.6 for a related mood (happy ~ uplifting), else 0.0."""
    fav, sm = favorite_mood.lower(), song_mood.lower()
    if fav == sm:
        return 1.0
    if fav and _mood_related(fav, sm):
        return 0.8
    return 0.0


def genre_score(favorite_genre: str, song_genre: str) -> float:
    """
    Genre match, tolerant of the messy labels in songs.csv.
    1.0 = exact, 0.6 = one label contains the other (afrobeats ~
    afrobeats amapiano), else 0.0.
    """
    fav, sg = favorite_genre.lower(), song_genre.lower()
    if fav == sg:
        return 1.0
    if fav and (fav in sg or sg in fav):
        return 0.6
    return 0.0


def energy_score(target_energy: float, song_energy: float) -> float:
    """
    Energy used as-is: closeness between the user's target energy and the
    song's energy. 1.0 = identical, decreasing toward 0 as they diverge.
    """
    return 1.0 - abs(float(target_energy) - float(song_energy))


def build_taste_profile(liked_songs: List[Dict]) -> Optional[Dict[str, float]]:
    """
    Turn a user's previously-liked songs into a "taste profile": the average
    vibe of the songs they called good before. Returns None if there's no
    history (so preference contributes nothing).

    This is the "it depends on what they called a vibe before" idea: instead
    of matching exact songs, we learn the center of their taste.
    """
    if not liked_songs:
        return None
    n = len(liked_songs)
    return {
        "valence": sum(float(s["valence"]) for s in liked_songs) / n,
        "energy": sum(float(s["energy"]) for s in liked_songs) / n,
    }


def preference_score(taste: Optional[Dict[str, float]],
                     song_valence: float,
                     song_energy: float) -> float:
    """
    Preference slot (Option B), taste-profile version.

    Returns 0.0 when there's no history (taste is None). Otherwise scores how
    close this song's vibe sits to the average vibe of what the user liked
    before -- 1.0 = right on their taste, decreasing as it drifts away.
    """
    if taste is None:
        return 0.0
    dv = abs(taste["valence"] - float(song_valence))
    de = abs(taste["energy"] - float(song_energy))
    # Average distance on two 0..1 axes -> flip to a 0..1 closeness score.
    return 1.0 - (dv + de) / 2.0


def _weighted_score(
    favorite_genre: str,
    favorite_mood: str,
    target_energy: float,
    taste: Optional[Dict[str, float]],
    song_genre: str,
    song_mood: str,
    song_valence: float,
    song_energy: float,
) -> Tuple[float, List[str]]:
    """Combine the vibe pieces into one score plus human-readable reasons."""
    v = valence_score(song_valence)
    m = mood_score(favorite_mood, song_mood)
    g = genre_score(favorite_genre, song_genre)
    e = energy_score(target_energy, song_energy)
    p = preference_score(taste, song_valence, song_energy)

    score = (
        W_MOOD * m
        + W_VALENCE * v
        + W_ENERGY * e
        + W_GENRE * g
        + W_PREFERENCE * p
    )

    # Each reason names the points that signal actually contributed to the
    # score (weight x sub-score), so the user can see *why* a song ranked.
    reasons: List[str] = []
    if m >= 1.0:
        reasons.append(f"mood match: {song_mood} (+{W_MOOD * m:.2f})")
    elif m > 0.0:
        reasons.append(f"related mood: {song_mood} (+{W_MOOD * m:.2f})")
    if g >= 1.0:
        reasons.append(f"genre match: {song_genre} (+{W_GENRE * g:.2f})")
    elif g > 0.0:
        reasons.append(
            f"partial genre match: {song_genre} (+{W_GENRE * g:.2f})"
        )
    if v >= 0.7:
        reasons.append(f"upbeat, positive feel (+{W_VALENCE * v:.2f})")
    elif v <= 0.4:
        reasons.append(f"darker, moodier feel (+{W_VALENCE * v:.2f})")
    if e >= 0.8:
        reasons.append(f"energy close to target (+{W_ENERGY * e:.2f})")
    if p >= 0.8:
        reasons.append(f"close to what you liked before (+{W_PREFERENCE * p:.2f})")
    if not reasons:
        reasons.append("a reasonable overall vibe match")

    return score, reasons


# ---------------------------------------------------------------------------
# OOP implementation (required by tests)
# ---------------------------------------------------------------------------
class Recommender:
    """
    OOP implementation of the recommendation logic.
    Required by tests/test_recommender.py
    """
    def __init__(self, songs: List[Song]):
        self.songs = songs
        self._by_id = {s.id: s for s in songs}

    def _taste(self, user: UserProfile) -> Optional[Dict[str, float]]:
        liked = [
            {"valence": self._by_id[sid].valence, "energy": self._by_id[sid].energy}
            for sid in user.liked_song_ids
            if sid in self._by_id
        ]
        return build_taste_profile(liked)

    def _score(self, user: UserProfile, song: Song,
               taste: Optional[Dict[str, float]] = None) -> Tuple[float, List[str]]:
        if taste is None:
            taste = self._taste(user)
        return _weighted_score(
            favorite_genre=user.favorite_genre,
            favorite_mood=user.favorite_mood,
            target_energy=user.target_energy,
            taste=taste,
            song_genre=song.genre,
            song_mood=song.mood,
            song_valence=song.valence,
            song_energy=song.energy,
        )

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        taste = self._taste(user)  # built once from history, reused per song
        ranked = sorted(
            self.songs,
            key=lambda s: self._score(user, s, taste)[0],
            reverse=True,
        )
        return ranked[:k]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        score, reasons = self._score(user, song)
        return f"Score {score:.2f} - " + ", ".join(reasons)


# ---------------------------------------------------------------------------
# Functional implementation (required by src/main.py)
# ---------------------------------------------------------------------------
def load_songs(csv_path: str) -> List[Dict]:
    """
    Loads songs from a CSV file into a list of dicts, with numeric
    columns converted to floats/ints.
    Required by src/main.py
    """
    float_cols = {"energy", "valence", "danceability", "acousticness", "tempo_bpm"}
    songs: List[Dict] = []
    with open(csv_path, newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            song: Dict = dict(row)
            song["id"] = int(song["id"])
            for col in float_cols:
                if col in song:
                    song[col] = float(song[col])
            songs.append(song)
    return songs


def score_song(user_prefs: Dict, song: Dict) -> Tuple[float, List[str]]:
    """
    Scores a single song against user preferences using the vibe weights.
    Expected return format: (score, reasons)
    """
    # "liked_songs" is a list of previously-liked song dicts (empty for now).
    taste = build_taste_profile(user_prefs.get("liked_songs", []))
    return _weighted_score(
        favorite_genre=user_prefs.get("genre", ""),
        favorite_mood=user_prefs.get("mood", ""),
        target_energy=float(user_prefs.get("energy", 0.0)),
        taste=taste,
        song_genre=song.get("genre", ""),
        song_mood=song.get("mood", ""),
        song_valence=float(song.get("valence", 0.0)),
        song_energy=float(song.get("energy", 0.0)),
    )


def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5) -> List[Tuple[Dict, float, str]]:
    """Score every song, then return the top k ranked highest-to-lowest."""
    # Judge every song into (song, score, explanation) tuples...
    scored = [
        (song, score, ", ".join(reasons))
        for song in songs
        for score, reasons in [score_song(user_prefs, song)]
    ]
    # ...then rank. sorted() returns a NEW sorted list, leaving `songs`
    # untouched; reverse=True puts the highest score first.
    scored = sorted(scored, key=lambda item: item[1], reverse=True)
    return scored[:k]
