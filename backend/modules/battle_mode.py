from .skill_extractor import extract_skills, compute_job_fit
from .dna_fingerprint import generate_dna
from .lie_detector import score_credibility


def battle(text_a: str, sections_a: dict, text_b: str, sections_b: dict) -> dict:
    # Analyze both resumes
    skills_a = extract_skills(text_a)
    skills_b = extract_skills(text_b)

    dna_a = generate_dna(text_a)
    dna_b = generate_dna(text_b)

    cred_a = score_credibility(text_a, sections_a)
    cred_b = score_credibility(text_b, sections_b)

    fit_a = compute_job_fit(skills_a["skills"])
    fit_b = compute_job_fit(skills_b["skills"])

    top_fit_a = fit_a[0] if fit_a else {"score": 0, "role": "N/A"}
    top_fit_b = fit_b[0] if fit_b else {"score": 0, "role": "N/A"}

    # Head-to-head scoring across 5 dimensions
    rounds = {
        "Skill Breadth":    (_cap(skills_a["total"] * 5),    _cap(skills_b["total"] * 5)),
        "Credibility":      (cred_a["credibility_score"],     cred_b["credibility_score"]),
        "Job Market Fit":   (top_fit_a["score"],              top_fit_b["score"]),
        "Leadership DNA":   (dna_a.get("radar", {}).get("Leadership", 0),
                             dna_b.get("radar", {}).get("Leadership", 0)),
        "Achievement DNA":  (dna_a.get("radar", {}).get("Achievement", 0),
                             dna_b.get("radar", {}).get("Achievement", 0)),
    }

    wins_a = sum(1 for a, b in rounds.values() if a > b)
    wins_b = sum(1 for a, b in rounds.values() if b > a)

    overall_a = round(sum(a for a, _ in rounds.values()) / len(rounds), 1)
    overall_b = round(sum(b for _, b in rounds.values()) / len(rounds), 1)

    if overall_a > overall_b:
        winner = "Resume A"
        margin = round(overall_a - overall_b, 1)
    elif overall_b > overall_a:
        winner = "Resume B"
        margin = round(overall_b - overall_a, 1)
    else:
        winner = "Tie"
        margin = 0

    return {
        "winner": winner,
        "margin": margin,
        "rounds": {k: {"a": v[0], "b": v[1], "winner": "A" if v[0] > v[1] else ("B" if v[1] > v[0] else "Tie")}
                   for k, v in rounds.items()},
        "overall": {"a": overall_a, "b": overall_b},
        "wins": {"a": wins_a, "b": wins_b},
        "resume_a": {
            "skills": skills_a["by_category"],
            "total_skills": skills_a["total"],
            "personality": dna_a.get("personality_type", ""),
            "credibility": cred_a["credibility_score"],
            "top_role": top_fit_a["role"],
            "top_fit_score": top_fit_a["score"],
        },
        "resume_b": {
            "skills": skills_b["by_category"],
            "total_skills": skills_b["total"],
            "personality": dna_b.get("personality_type", ""),
            "credibility": cred_b["credibility_score"],
            "top_role": top_fit_b["role"],
            "top_fit_score": top_fit_b["score"],
        },
    }


def _cap(val: float) -> float:
    return round(min(val, 100), 1)
