import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))


def generate_performance_summary(data):

    prompt = f"""
    You are an expert IELTS mentor and international admissions consultant.

    A student has completed IELTS practice with:

    Reading Band: {data.reading}
    Writing Band: {data.writing}
    Speaking Band: {data.speaking}
    Overall Band: {data.overall}

    Based on this score, provide:

    1. Overall Performance Analysis
    2. University & Country Suggestions (realistic)
    3. Minimum IELTS Band Requirements for those countries
    4. Step-by-step Admission Roadmap
    5. Section-wise Improvement Plan (Reading, Writing, Speaking)
    6. Estimated real IELTS exam potential

    Be realistic, structured, professional and motivational.

    Return STRICT JSON format:

    {{
        "performance_analysis": "...",
        "university_suggestions": "...",
        "minimum_band_requirements": "...",
        "admission_roadmap": "...",
        "improvement_plan": "...",
        "exam_potential": "..."
    }}
    """

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": "You are a professional IELTS and Study Abroad advisor."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.4
    )

    try:
        import json
        result_text = response.choices[0].message.content.strip()

        if result_text.startswith("```"):
            result_text = result_text.replace("```json", "").replace("```", "").strip()

        return json.loads(result_text)

    except Exception:
        return {
            "error": "Failed to parse performance summary",
            "raw_output": response.choices[0].message.content
        }