from google import genai
import json


class IELTSEvaluator:
    def __init__(self, api_key):
        self.client = genai.Client(api_key=api_key)

    def evaluate_writing(self, essay_text):
        prompt = f"""
You are a strict IELTS examiner.

Evaluate the following IELTS Writing Task 2 essay.

Return ONLY valid JSON in this exact structure:

{{
  "band_score": number,
  "grammar_score": number,
  "vocabulary_score": number,
  "coherence_score": number,
  "task_response_score": number,
  "strengths": "text",
  "weaknesses": "text",
  "improvement_suggestions": "text"
}}

Essay:
{essay_text}
"""

        response = self.client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )

        text = response.text.strip()
        # Remove markdown formatting
        if text.startswith("```"):
            text = text.replace("```json", "").replace("```", "").strip()
        
        # Sometimes Gemini returns JSON inside a string — clean it
        text = text.strip()
        try:
            return json.loads(text)
        except json.JSONDecodeError:
            try:
                # Try to fix escaped JSON
                cleaned = text.replace('\n', '').replace('\\"', '"')
                return json.loads(cleaned)
            except:
                return {
            "error": "Could not parse response",
            "raw_output": text
        }