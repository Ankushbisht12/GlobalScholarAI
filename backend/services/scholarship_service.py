def predict_scholarship(gpa: float, ielts: float, income: float, research: int, leadership: int):

    # Normalize
    gpa_norm = (gpa - 5) / 5
    ielts_norm = (ielts - 5) / 4
    research_norm = research / 2
    leadership_norm = leadership / 3

    # Income logic (lower income = higher chance)
    max_income = 2000000
    income_norm = 1 - (income / max_income)
    if income_norm < 0:
        income_norm = 0

    # Weighted scoring
    score = (
        gpa_norm * 0.30 +
        ielts_norm * 0.20 +
        research_norm * 0.20 +
        leadership_norm * 0.15 +
        income_norm * 0.15
    )

    probability = score * 100

    # Smooth boundaries
    if probability < 15:
        probability += 10
    if probability > 92:
        probability = 92

    return round(probability, 2)