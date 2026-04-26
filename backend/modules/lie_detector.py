import re
from datetime import datetime

VAGUE_PHRASES = [
    "various", "multiple projects", "several", "many", "etc", "and more",
    "responsible for", "worked on", "involved in", "assisted with",
    "helped with", "participated in", "exposure to", "familiar with",
    "knowledge of", "understanding of", "experience with"
]

INFLATED_SKILLS = [
    "expert in", "master of", "guru", "ninja", "rockstar", "wizard",
    "proficient in all", "extensive experience", "deep expertise",
    "10+ years" , "15+ years", "20+ years"
]

BUZZWORD_OVERLOAD = [
    "synergy", "leverage", "paradigm", "disruptive", "innovative solution",
    "cutting-edge", "world-class", "best-in-class", "thought leader",
    "visionary", "game-changer", "revolutionary"
]


def score_credibility(text: str, sections: dict) -> dict:
    flags = []
    deductions = 0

    lower = text.lower()

    # 1. Vague language check
    vague_hits = [p for p in VAGUE_PHRASES if p in lower]
    if len(vague_hits) > 4:
        flags.append({"type": "Vague Language", "severity": "medium",
                      "detail": f"Found {len(vague_hits)} vague phrases: {', '.join(vague_hits[:5])}"})
        deductions += min(len(vague_hits) * 2, 15)

    # 2. Skill inflation
    inflation_hits = [p for p in INFLATED_SKILLS if p in lower]
    if inflation_hits:
        flags.append({"type": "Skill Inflation", "severity": "high",
                      "detail": f"Suspicious claims: {', '.join(inflation_hits)}"})
        deductions += len(inflation_hits) * 5

    # 3. Buzzword overload
    buzz_hits = [p for p in BUZZWORD_OVERLOAD if p in lower]
    if len(buzz_hits) > 2:
        flags.append({"type": "Buzzword Overload", "severity": "low",
                      "detail": f"{len(buzz_hits)} marketing buzzwords detected"})
        deductions += len(buzz_hits) * 2

    # 4. Employment gap detection
    years = sorted(set(map(int, re.findall(r"\b(20[0-2]\d|199\d)\b", text))))
    if years:
        gaps = [years[i+1] - years[i] for i in range(len(years)-1)]
        large_gaps = [g for g in gaps if g > 2]
        if large_gaps:
            flags.append({"type": "Employment Gap", "severity": "medium",
                          "detail": f"Possible gap of {max(large_gaps)} year(s) detected in timeline"})
            deductions += 5

    # 5. No quantifiable achievements
    metrics = re.findall(r"\b\d+[%x]?\b", text)
    if len(metrics) < 3:
        flags.append({"type": "Lack of Metrics", "severity": "medium",
                      "detail": "Very few quantifiable achievements found. Strong resumes use numbers."})
        deductions += 10

    # 6. Suspiciously short experience section
    exp_text = sections.get("experience", "")
    if exp_text and len(exp_text.split()) < 30:
        flags.append({"type": "Thin Experience", "severity": "high",
                      "detail": "Experience section is unusually brief — may be padded elsewhere"})
        deductions += 10

    # 7. No contact info check
    has_email = bool(re.search(r"[\w.+-]+@[\w-]+\.[a-zA-Z]{2,}", text))
    if not has_email:
        flags.append({"type": "Missing Contact", "severity": "low",
                      "detail": "No email address found"})
        deductions += 5

    score = max(0, 100 - deductions)
    verdict = _verdict(score)

    return {
        "credibility_score": score,
        "verdict": verdict,
        "flags": flags,
        "total_flags": len(flags),
    }


def _verdict(score: int) -> str:
    if score >= 85:
        return "✅ Highly Credible — clean, specific, well-supported resume"
    elif score >= 65:
        return "⚠️ Mostly Credible — a few areas need more specificity"
    elif score >= 45:
        return "🔶 Questionable — multiple red flags detected"
    else:
        return "🚨 Low Credibility — significant inflation or vagueness detected"
