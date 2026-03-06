import os
import json
from google import genai
from dotenv import load_dotenv

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))


def generate_mcq_questions():

    prompt = """
    Generate an IELTS Academic Reading simulation.

    First generate a realistic academic passage (400–600 words).
    Then generate 5 multiple choice questions based strictly on the passage.

    Format strictly as JSON:

    {
      "passage": "Full academic passage here...",
      "questions": [
        {
          "question": "Question text",
          "options": {
            "A": "Option A",
            "B": "Option B",
            "C": "Option C",
            "D": "Option D"
          },
          "correct_answer": "A"
        }
      ]
    }

    Rules:
    - Questions must depend on the passage.
    - Do NOT mention 'according to the passage' unless the passage exists.
    - Do NOT include explanations.
    - Return ONLY valid JSON.
    """

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )

    try:
        text = response.text.strip()

        # Clean markdown wrapping
        if text.startswith("```"):
            text = text.replace("```json", "")
            text = text.replace("```", "")
            text = text.strip()

        data = json.loads(text)
        return data

    except Exception:
        return {
            "error": "Failed to parse MCQ response",
            "raw_output": response.text
        }