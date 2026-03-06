import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def generate_sop(data):

    prompt = f"""
    You are an expert study abroad consultant.

    Generate a professional Statement of Purpose (SOP) for Master's admission.

    Student Details:
    Name: {data['name']}
    Field: {data['field']}
    Target Country: {data['country']}
    Academic Background: {data['academic_background']}
    Projects / Experience: {data['experience']}
    Career Goals: {data['career_goals']}
    Why this country: {data['why_country']}

    Structure the SOP properly:

    1. Introduction
    2. Academic Background
    3. Professional Experience / Projects
    4. Why this country and program
    5. Career goals
    6. Conclusion

    Tone:
    - Formal
    - Genuine
    - Strong but not arrogant
    - Suitable for top 100 universities

    Do not write placeholders.
    Write full ready-to-submit SOP.
    """

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": "You are a professional SOP writer."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.6
    )

    return {
        "sop": response.choices[0].message.content
    }