import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))


def round_band(score):
    decimal = score - int(score)

    if decimal < 0.25:
        return float(int(score))
    elif decimal < 0.75:
        return float(int(score) + 0.5)
    else:
        return float(int(score) + 1)


def calculate_final_score(reading, writing, speaking):

    average = (reading + writing + speaking) / 3
    overall = round_band(average)

    summary_prompt = f"""
    You are an IELTS examiner.

    The student's IELTS scores are:

    Reading: {reading}
    Writing: {writing}
    Speaking: {speaking}
    Overall Band: {overall}

    Provide:

    1. Strength analysis
    2. Weakest area
    3. Clear improvement strategy for each module
    4. Study plan for next 30 days
    5. University admission readiness (for top 100 universities)

    Be realistic and professional.
    """

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": "You are a professional IELTS examiner."},
            {"role": "user", "content": summary_prompt}
        ],
        temperature=0.4
    )

    return {
        "reading": reading,
        "writing": writing,
        "speaking": speaking,
        "overall_band": overall,
        "ai_summary": response.choices[0].message.content
    }