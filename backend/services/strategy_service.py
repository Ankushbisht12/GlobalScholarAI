import os
from google import genai
from dotenv import load_dotenv

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))


def generate_strategy(student_profile, recommendations):

    universities_summary = "\n".join(
        [
            f"{u['university_name']} ({u['category']}, Rank: {u['world_rank']})"
            for u in recommendations
            if "university_name" in u
        ]
    )

    prompt = f"""
    Student Profile:
    GPA: {student_profile['gpa']}
    IELTS: {student_profile['ielts']}
    Field: {student_profile['field']}
    Preferred Country: {student_profile['country']}

    Recommended Universities:
    {universities_summary}

    Provide:
    1. Overall admission strategy.
    2. Whether profile is competitive.
    3. How to improve chances.
    4. Suggested application distribution (Dream/Target/Safe ratio).
    Keep it structured and professional.
    """

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )

    return response.text