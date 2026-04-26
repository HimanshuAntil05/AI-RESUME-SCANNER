# Historical skill demand scores (0-100) by year
# Based on real industry trends
SKILL_TIMELINE = {
    "python":           {2018: 65, 2019: 72, 2020: 80, 2021: 88, 2022: 92, 2023: 95, 2024: 97},
    "machine learning": {2018: 55, 2019: 65, 2020: 72, 2021: 80, 2022: 85, 2023: 90, 2024: 93},
    "react":            {2018: 60, 2019: 70, 2020: 78, 2021: 83, 2022: 85, 2023: 84, 2024: 83},
    "docker":           {2018: 45, 2019: 58, 2020: 68, 2021: 76, 2022: 82, 2023: 87, 2024: 90},
    "kubernetes":       {2018: 30, 2019: 42, 2020: 55, 2021: 65, 2022: 74, 2023: 82, 2024: 87},
    "aws":              {2018: 60, 2019: 68, 2020: 75, 2021: 80, 2022: 85, 2023: 88, 2024: 90},
    "sql":              {2018: 85, 2019: 84, 2020: 83, 2021: 82, 2022: 80, 2023: 78, 2024: 76},
    "java":             {2018: 88, 2019: 85, 2020: 82, 2021: 78, 2022: 74, 2023: 70, 2024: 67},
    "tensorflow":       {2018: 50, 2019: 60, 2020: 68, 2021: 72, 2022: 74, 2023: 73, 2024: 70},
    "pytorch":          {2018: 30, 2019: 42, 2020: 55, 2021: 65, 2022: 74, 2023: 82, 2024: 88},
    "javascript":       {2018: 82, 2019: 84, 2020: 85, 2021: 86, 2022: 86, 2023: 85, 2024: 84},
    "typescript":       {2018: 35, 2019: 48, 2020: 60, 2021: 70, 2022: 78, 2023: 84, 2024: 88},
    "llm":              {2018: 5,  2019: 8,  2020: 12, 2021: 20, 2022: 40, 2023: 82, 2024: 95},
    "langchain":        {2018: 0,  2019: 0,  2020: 0,  2021: 5,  2022: 25, 2023: 70, 2024: 85},
    "rust":             {2018: 15, 2019: 20, 2020: 28, 2021: 35, 2022: 44, 2023: 55, 2024: 63},
    "go":               {2018: 30, 2019: 38, 2020: 46, 2021: 54, 2022: 62, 2023: 68, 2024: 72},
    "excel":            {2018: 80, 2019: 78, 2020: 75, 2021: 70, 2022: 65, 2023: 60, 2024: 55},
    "tableau":          {2018: 55, 2019: 62, 2020: 68, 2021: 72, 2022: 73, 2023: 72, 2024: 70},
    "power bi":         {2018: 40, 2019: 50, 2020: 60, 2021: 68, 2022: 74, 2023: 78, 2024: 80},
    "spark":            {2018: 55, 2019: 60, 2020: 64, 2021: 67, 2022: 68, 2023: 67, 2024: 65},
    "kafka":            {2018: 40, 2019: 48, 2020: 56, 2021: 63, 2022: 70, 2023: 74, 2024: 76},
    "terraform":        {2018: 30, 2019: 40, 2020: 52, 2021: 63, 2022: 72, 2023: 80, 2024: 85},
    "nextjs":           {2018: 10, 2019: 22, 2020: 38, 2021: 55, 2022: 68, 2023: 78, 2024: 83},
    "fastapi":          {2018: 0,  2019: 5,  2020: 20, 2021: 40, 2022: 58, 2023: 72, 2024: 80},
}

YEARS = [2018, 2019, 2020, 2021, 2022, 2023, 2024]


def get_time_machine(skills: list) -> dict:
    """Return historical demand data for each skill found in resume."""
    timeline = {}
    rising = []
    falling = []
    stable = []

    for skill in skills:
        key = skill.lower()
        if key in SKILL_TIMELINE:
            data = SKILL_TIMELINE[key]
            series = [data.get(y, 0) for y in YEARS]
            timeline[skill] = {"years": YEARS, "demand": series}

            # Trend: compare 2020 vs 2024
            old = data.get(2020, 0)
            new = data.get(2024, 0)
            delta = new - old
            if delta >= 20:
                rising.append({"skill": skill, "delta": f"+{delta}", "trend": "🚀 Rising Fast"})
            elif delta <= -10:
                falling.append({"skill": skill, "delta": str(delta), "trend": "📉 Declining"})
            else:
                stable.append({"skill": skill, "delta": f"+{delta}" if delta >= 0 else str(delta), "trend": "➡️ Stable"})

    return {
        "timeline": timeline,
        "rising": rising,
        "falling": falling,
        "stable": stable,
        "years": YEARS,
    }
