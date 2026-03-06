import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))


def generate_lor(data):

    lor_type = data["type"]  # academic or professional

    if lor_type.lower() == "academic":
        role_context = "professor or academic supervisor"
        focus_points = """
        - Academic performance
        - Research ability
        - Analytical skills
        - Classroom participation
        - Intellectual curiosity
        """
    else:
        role_context = "manager or workplace supervisor"
        focus_points = """
        - Professional performance
        - Technical skills
        - Leadership
        - Team collaboration
        - Problem-solving ability
        """

    prompt = f"""
    You are a professional recommendation letter writer.

    Write a strong and realistic Letter of Recommendation.

    Recommender Role: {role_context}
    Student Name: {data['student_name']}
    Recommender Name: {data['recommender_name']}
    Relationship Duration: {data['duration']}
    Field of Study: {data['field']}
    Key Strengths: {data['strengths']}
    Achievements: {data['achievements']}
    Target Country: {data['country']}

    Focus on:
    {focus_points}

    Requirements:
    - Formal tone
    - 500–700 words
    - Realistic and personalized
    - Suitable for Master's admission
    - No generic phrases
    - Ready to submit

    Sign off professionally at the end.
    """

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": "You are an expert LOR writer."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.6
    )

    return {
        "lor": response.choices[0].message.content
    }