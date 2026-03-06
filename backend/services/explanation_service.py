import os
from google import genai
from dotenv import load_dotenv

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))


def generate_university_explanation(student_profile, university):

    prompt = f"""
    Student Profile:
    GPA: {student_profile['gpa']}
    IELTS: {student_profile['ielts']}
    Field: {student_profile['field']}

    University:
    Name: {university['university_name']}
    Country: {university['country']}
    World Rank: {university['world_rank']}
    Category: {university['category']}

    Explain:
    1. Why this university suits the student.
    2. Why it is categorized as Dream/Target/Safe.
    3. What the student should improve to increase chances.
    Keep it concise and professional.
    """

    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=prompt
    )

    return response.text