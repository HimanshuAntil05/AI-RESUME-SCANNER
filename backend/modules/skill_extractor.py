import re
import os
import requests

# Comprehensive skill taxonomy
SKILL_DB = {
    "programming": ["python","java","javascript","typescript","c++","c#","go","rust","kotlin","swift",
                    "php","ruby","scala","r","matlab","bash","shell","perl"],
    "web": ["react","angular","vue","nextjs","nodejs","express","django","flask","fastapi","spring",
            "html","css","tailwind","bootstrap","graphql","rest api","webpack"],
    "data": ["sql","mysql","postgresql","mongodb","redis","elasticsearch","pandas","numpy","matplotlib",
             "seaborn","tableau","power bi","excel","spark","hadoop","kafka","airflow","dbt"],
    "ml_ai": ["machine learning","deep learning","tensorflow","pytorch","keras","scikit-learn","nlp",
              "computer vision","transformers","llm","openai","langchain","huggingface","reinforcement learning"],
    "cloud": ["aws","azure","gcp","docker","kubernetes","terraform","ansible","ci/cd","jenkins",
              "github actions","linux","nginx","microservices","serverless"],
    "soft": ["leadership","communication","problem solving","teamwork","agile","scrum","project management",
             "critical thinking","time management","mentoring"],
}

# Flat skill list for matching
ALL_SKILLS = {skill: category for category, skills in SKILL_DB.items() for skill in skills}

# Job role profiles: required skills
JOB_PROFILES = {
    "Data Scientist":       ["python","machine learning","sql","pandas","numpy","scikit-learn","statistics","tensorflow"],
    "Frontend Developer":   ["javascript","react","html","css","typescript","webpack","rest api"],
    "Backend Developer":    ["python","nodejs","sql","rest api","docker","postgresql","redis"],
    "Full Stack Developer": ["javascript","react","nodejs","sql","html","css","docker","rest api"],
    "DevOps Engineer":      ["docker","kubernetes","aws","terraform","ci/cd","linux","bash","ansible"],
    "ML Engineer":          ["python","tensorflow","pytorch","machine learning","docker","sql","mlops","kubernetes"],
    "Data Analyst":         ["sql","excel","python","tableau","power bi","pandas","data visualization"],
    "Cloud Architect":      ["aws","azure","gcp","terraform","kubernetes","docker","microservices","security"],
}


def extract_skills(text: str) -> dict:
    lower = text.lower()
    found = {}
    for skill, category in ALL_SKILLS.items():
        pattern = r"\b" + re.escape(skill) + r"\b"
        if re.search(pattern, lower):
            found[skill] = category

    by_category = {}
    for skill, cat in found.items():
        by_category.setdefault(cat, []).append(skill)

    return {"skills": found, "by_category": by_category, "total": len(found)}


def compute_job_fit(skills_found: dict) -> list:
    found_set = set(skills_found.keys())
    results = []
    for role, required in JOB_PROFILES.items():
        matched = [s for s in required if s in found_set]
        missing = [s for s in required if s not in found_set]
        score = round(len(matched) / len(required) * 100, 1)
        results.append({
            "role": role,
            "score": score,
            "matched": matched,
            "missing": missing,
            "verdict": _fit_verdict(score),
        })
    return sorted(results, key=lambda x: x["score"], reverse=True)


def _fit_verdict(score: float) -> str:
    if score >= 80: return "Strong Fit"
    if score >= 55: return "Good Fit"
    if score >= 35: return "Partial Fit"
    return "Weak Fit"


def fetch_live_jobs(role: str, skills: list) -> list:
    """Fetch live job postings via JSearch RapidAPI."""
    api_key = os.getenv("JSEARCH_API_KEY", "")
    if not api_key:
        return _mock_jobs(role)

    query = f"{role} {' '.join(skills[:3])}"
    url = "https://jsearch.p.rapidapi.com/search"
    headers = {"X-RapidAPI-Key": api_key, "X-RapidAPI-Host": "jsearch.p.rapidapi.com"}
    params = {"query": query, "page": "1", "num_pages": "1"}

    try:
        resp = requests.get(url, headers=headers, params=params, timeout=8)
        data = resp.json().get("data", [])[:5]
        return [{"title": j.get("job_title"), "company": j.get("employer_name"),
                 "location": j.get("job_city", "Remote"), "url": j.get("job_apply_link")} for j in data]
    except Exception:
        return _mock_jobs(role)


def _mock_jobs(role: str) -> list:
    return [
        {"title": f"Senior {role}", "company": "TechCorp Inc.", "location": "Remote", "url": "#"},
        {"title": role, "company": "StartupXYZ", "location": "New York, NY", "url": "#"},
        {"title": f"Junior {role}", "company": "DataWave", "location": "San Francisco, CA", "url": "#"},
    ]
