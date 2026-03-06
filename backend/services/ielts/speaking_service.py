import os
import uuid
import json
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# In-memory session storage (prototype)
speaking_sessions = {}

MAX_TURNS = 6  # Total answers allowed


def start_speaking_session():
    session_id = str(uuid.uuid4())

    intro_prompt = """
    You are an IELTS Speaking examiner.

    Start Part 1 of the IELTS Speaking test.
    Ask only ONE simple introduction question about:
    - Name
    - Hometown
    - Studies or Job
    - Hobbies

    Ask only ONE question.
    Do not explain anything.
    """

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": "You are a professional IELTS examiner."},
            {"role": "user", "content": intro_prompt}
        ],
        temperature=0.5
    )

    question = response.choices[0].message.content.strip()

    speaking_sessions[session_id] = {
        "history": [
            {"role": "assistant", "content": question}
        ],
        "stage": "part1",
        "turns": 1
    }

    return {
        "session_id": session_id,
        "question": question,
        "stage": "part1"
    }


def continue_speaking_session(session_id, user_answer):

    if session_id not in speaking_sessions:
        return {"error": "Invalid session ID"}

    session = speaking_sessions[session_id]

    # Save user answer
    session["history"].append({"role": "user", "content": user_answer})
    session["turns"] += 1

    # 🚀 Stop and evaluate after MAX_TURNS answers
    if session["turns"] > MAX_TURNS:
        return evaluate_speaking(session_id)

    # Stage transition logic
    if session["turns"] == 4:
        stage_prompt = """
        Now move to Part 2 (Cue Card).

        Give ONE cue card topic.
        Include:
        - Short description
        - 3-4 bullet points
        Ask the candidate to speak for 1-2 minutes.
        """
        session["stage"] = "part2"

    elif session["turns"] == 6:
        stage_prompt = """
        Now move to Part 3.

        Ask ONE deeper analytical discussion question
        related to the cue card topic.
        """
        session["stage"] = "part3"

    else:
        stage_prompt = """
        Continue IELTS Speaking Part 1.
        Ask ONE natural follow-up question.
        """

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=session["history"] + [
            {"role": "system", "content": stage_prompt}
        ],
        temperature=0.5
    )

    next_question = response.choices[0].message.content.strip()

    session["history"].append({"role": "assistant", "content": next_question})

    return {
        "session_id": session_id,
        "question": next_question,
        "stage": session["stage"],
        "turns_remaining": MAX_TURNS - session["turns"]
    }


def evaluate_speaking(session_id):

    if session_id not in speaking_sessions:
        return {"error": "Invalid session ID"}

    session = speaking_sessions[session_id]

    conversation_text = "\n".join(
        [f"{msg['role']}: {msg['content']}" for msg in session["history"]]
    )

    evaluation_prompt = f"""
    Evaluate this IELTS Speaking test conversation.

    Score separately:
    - Fluency & Coherence
    - Lexical Resource
    - Grammatical Range & Accuracy
    - Pronunciation (assume average since text-based)

    Return STRICT JSON:

    {{
      "overall_band": 7.0,
      "fluency": 7,
      "lexical_resource": 7,
      "grammar": 7,
      "pronunciation": 7,
      "strengths": "...",
      "weaknesses": "...",
      "improvement_suggestions": "..."
    }}

    Be strict like a real IELTS examiner.

    Conversation:
    {conversation_text}
    """

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": "You are an official IELTS examiner."},
            {"role": "user", "content": evaluation_prompt}
        ],
        temperature=0.3
    )

    try:
        result_text = response.choices[0].message.content.strip()

        # Remove markdown wrapping if present
        if result_text.startswith("```"):
            result_text = result_text.replace("```json", "").replace("```", "").strip()

        result_json = json.loads(result_text)

        # ✅ Clean session after evaluation (important)
        del speaking_sessions[session_id]

        return result_json

    except Exception:
        return {
            "error": "Failed to parse speaking evaluation",
            "raw_output": response.choices[0].message.content
        }