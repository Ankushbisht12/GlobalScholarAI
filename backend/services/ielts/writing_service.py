import os
import json
from google import genai
from dotenv import load_dotenv

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))


def generate_writing_topic():

    prompt = """
    Generate one IELTS Academic Writing Task 2 topic.

    It should:
    - Be realistic
    - Require discussion / opinion
    - Be suitable for Band 7+ level

    Return strictly in JSON format:

    {
      "task_type": "Opinion / Discussion / Problem-Solution / Advantage-Disadvantage",
      "question": "Full IELTS Task 2 question here"
    }

    Return only valid JSON.
    """

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )

    try:
        text = response.text.strip()

        if text.startswith("```"):
            text = text.replace("```json", "")
            text = text.replace("```", "")
            text = text.strip()

        return json.loads(text)

    except Exception:
        return {
            "error": "Failed to parse writing topic",
            "raw_output": response.text
        }


def evaluate_writing(essay_text):

    prompt = f"""
    Evaluate the following IELTS Writing Task 2 essay.

    Score the following criteria separately:
    - Task Response
    - Coherence and Cohesion
    - Lexical Resource
    - Grammatical Range and Accuracy

    Also provide:
    - Overall Band Score (0-9)
    - Strengths
    - Weaknesses
    - Improvement Suggestions

    IMPORTANT:
    - Penalize if word count is below 250.
    - Be strict like a real IELTS examiner.
    - Return strictly in JSON format.

    Format:

    {{
      "overall_band": 7.0,
      "task_response": 7,
      "coherence": 7,
      "lexical_resource": 7,
      "grammar": 7,
      "word_count": 0,
      "strengths": "...",
      "weaknesses": "...",
      "improvement_suggestions": "..."
    }}

    Essay:
    {essay_text}
    """

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )

    try:
        text = response.text.strip()

        if text.startswith("```"):
            text = text.replace("```json", "")
            text = text.replace("```", "")
            text = text.strip()

        return json.loads(text)

    except Exception:
        return {
            "error": "Failed to parse writing evaluation",
            "raw_output": response.text
        }