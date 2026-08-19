def analyze_resume(text):

    skills = [
        "Python",
        "SQL",
        "Excel",
        "Power BI",
        "Tableau",
        "Machine Learning",
        "Statistics",
        "Pandas",
        "NumPy",
        "Git"
    ]

    found_skills = []

    for skill in skills:
        if skill.lower() in text.lower():
            found_skills.append(skill)

    missing_skills = []

    for skill in skills:
        if skill not in found_skills:
            missing_skills.append(skill)

    return found_skills, missing_skills