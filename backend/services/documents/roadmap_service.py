import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))


def generate_application_roadmap(data):

    prompt = f"""
    You are a professional study abroad consultant.

    Generate a detailed application roadmap for a Master's student.

    Country: {data['country']}
    Intake: {data['intake']}
    Target Year: {data['year']}
    Current IELTS Band: {data['ielts_band']}

    Provide:

    1. Month-by-month preparation timeline (starting 12 months before intake)
    2. Required document checklist (academic + financial + visa)
    3. Scholarship application guidance
    4. Visa process overview
    5. Common mistakes students make
    6. Strategy to increase admission chances
    7. Minimum IELTS recommended for top universities in that country

    Make it practical, structured, and professional.
    """

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": "You are an expert global education consultant."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.5
    )

    return {
        "roadmap": response.choices[0].message.content
    }