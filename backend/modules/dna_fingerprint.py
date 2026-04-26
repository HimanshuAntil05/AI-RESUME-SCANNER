import re
import textstat

# Action verbs by category
LEADERSHIP_VERBS = {"led","managed","directed","oversaw","supervised","spearheaded","coordinated","mentored"}
ACHIEVEMENT_VERBS = {"achieved","delivered","increased","reduced","improved","optimized","launched","built","created","developed"}
COLLABORATION_VERBS = {"collaborated","partnered","worked","supported","assisted","contributed","engaged","facilitated"}
ANALYTICAL_VERBS = {"analyzed","evaluated","assessed","researched","investigated","identified","designed","architected"}

BUZZWORDS = {"synergy","leverage","passionate","hardworking","team player","go-getter","results-driven",
             "detail-oriented","self-starter","dynamic","proactive","innovative","guru","ninja","rockstar"}


def generate_dna(text: str) -> dict:
    words = re.findall(r"\b\w+\b", text.lower())
    sentences = re.split(r"[.!?]+", text)
    sentences = [s.strip() for s in sentences if len(s.strip()) > 5]
    word_count = len(words)

    if word_count == 0:
        return {}

    unique_ratio = len(set(words)) / word_count

    def verb_score(verb_set):
        hits = sum(1 for w in words if w in verb_set)
        return round(min(hits / max(len(sentences), 1) * 100, 100), 1)

    leadership    = verb_score(LEADERSHIP_VERBS)
    achievement   = verb_score(ACHIEVEMENT_VERBS)
    collaboration = verb_score(COLLABORATION_VERBS)
    analytical    = verb_score(ANALYTICAL_VERBS)

    buzzword_hits = sum(1 for w in words if w in BUZZWORDS)
    buzzword_density = round(buzzword_hits / word_count * 100, 2)

    try:
        readability = round(textstat.flesch_reading_ease(text), 1)
    except Exception:
        readability = 50.0

    avg_sentence_len = round(word_count / max(len(sentences), 1), 1)

    # Vocabulary complexity: words > 8 chars
    complexity = round(sum(1 for w in words if len(w) > 8) / word_count * 100, 1)

    # Quantification: presence of numbers/metrics
    metrics_count = len(re.findall(r"\b\d+[%x]?\b", text))
    quantification = round(min(metrics_count / max(len(sentences), 1) * 100, 100), 1)

    # Tone: formal vs casual (ratio of formal indicators)
    formal_words = {"therefore","consequently","furthermore","however","nevertheless","accordingly","thus"}
    casual_words = {"awesome","cool","stuff","things","lots","really","very","just","basically"}
    formal_hits = sum(1 for w in words if w in formal_words)
    casual_hits = sum(1 for w in words if w in casual_words)
    total_tone = formal_hits + casual_hits + 1
    formality = round(formal_hits / total_tone * 100, 1)

    radar = {
        "Leadership":      leadership,
        "Achievement":     achievement,
        "Collaboration":   collaboration,
        "Analytical":      analytical,
        "Quantification":  quantification,
        "Vocabulary":      complexity,
        "Formality":       formality,
        "Readability":     round(max(0, min(readability, 100)), 1),
    }

    personality_type = _infer_personality(radar)

    return {
        "radar": radar,
        "personality_type": personality_type,
        "buzzword_density": buzzword_density,
        "avg_sentence_length": avg_sentence_len,
        "unique_word_ratio": round(unique_ratio * 100, 1),
        "total_words": word_count,
    }


def _infer_personality(radar: dict) -> str:
    scores = radar
    top = max(scores, key=scores.get)
    mapping = {
        "Leadership":    "The Commander — natural leader, takes ownership",
        "Achievement":   "The Achiever — results-focused, metric-driven",
        "Collaboration": "The Team Builder — people-first, cooperative",
        "Analytical":    "The Strategist — data-driven, systematic thinker",
        "Quantification":"The Executor — impact-oriented, numbers-first",
        "Vocabulary":    "The Expert — deep domain knowledge, precise communicator",
        "Formality":     "The Professional — structured, formal, corporate-ready",
        "Readability":   "The Communicator — clear, concise, accessible writer",
    }
    return mapping.get(top, "The Generalist")
