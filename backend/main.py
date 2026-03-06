from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os
from pydantic import BaseModel

from pydantic import BaseModel
from backend.services.admission_service import predict_admission
from backend.services.scholarship_service import predict_scholarship

from backend.services.ielts.mcq_service import generate_mcq_questions
from pydantic import BaseModel

load_dotenv()

app = FastAPI(title="GlobalScholarAI API")

# Allow frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Later restrict
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"message": "GlobalScholarAI Backend Running"}


class AdmissionRequest(BaseModel):
    gpa: float
    ielts: float
    experience: int
    research: int


@app.post("/predict/admission")
def admission_prediction(data: AdmissionRequest):
    probability = predict_admission(
        data.gpa,
        data.ielts,
        data.experience,
        data.research
    )

    return {
        "admission_probability": probability
    }



class ScholarshipRequest(BaseModel):
    gpa: float
    ielts: float
    income: float
    research: int
    leadership: int


@app.post("/predict/scholarship")
def scholarship_prediction(data: ScholarshipRequest):
    probability = predict_scholarship(
        data.gpa,
        data.ielts,
        data.income,
        data.research,
        data.leadership
    )

    return {
        "scholarship_probability": probability
    }

from backend.services.university_service import match_universities


class UniversityRequest(BaseModel):
    field: str
    preferred_country: str
    gpa: float
    ielts: float


from backend.services.strategy_service import generate_strategy

@app.post("/match/universities")
def university_match(data: UniversityRequest):

    recommendations = match_universities(
        data.field,
        data.preferred_country,
        data.gpa,
        data.ielts
    )

    # If message returned (no universities found)
    if isinstance(recommendations, list) and "message" in recommendations[0]:
        return {
            "recommended_universities": recommendations,
            "strategy": "No strategy available due to no university match."
        }

    student_profile = {
        "gpa": data.gpa,
        "ielts": data.ielts,
        "field": data.field,
        "country": data.preferred_country
    }

    strategy = generate_strategy(student_profile, recommendations)

    return {
        "recommended_universities": recommendations,
        "strategy": strategy
    }

class MCQSubmission(BaseModel):
    answers: list  # Example: ["A", "C", "B", "D", "A"]
    questions: list

@app.post("/ielts/mcq/start")
def start_mcq():
    questions = generate_mcq_questions()
    return questions


@app.post("/ielts/mcq/submit")
def submit_mcq(submission: MCQSubmission):

    correct_count = 0
    total = len(submission.questions)

    for i, question in enumerate(submission.questions):
        if i < len(submission.answers):
            if submission.answers[i].upper() == question["correct_answer"].upper():
                correct_count += 1

    # IELTS Reading Band Approximation (more realistic mapping)
    score_ratio = correct_count / total

    if score_ratio >= 0.9:
        band = 9.0
    elif score_ratio >= 0.8:
        band = 8.0
    elif score_ratio >= 0.7:
        band = 7.0
    elif score_ratio >= 0.6:
        band = 6.0
    elif score_ratio >= 0.5:
        band = 5.0
    else:
        band = 4.0

    return {
        "section": "Reading",
        "correct_answers": correct_count,
        "total_questions": total,
        "estimated_reading_band": band
    }


from backend.services.ielts.writing_service import generate_writing_topic, evaluate_writing

class WritingSubmission(BaseModel):
    essay: str

@app.post("/ielts/writing/topic")
def get_writing_topic():
    return generate_writing_topic()


@app.post("/ielts/writing/evaluate")
def evaluate_writing_task(submission: WritingSubmission):
    return evaluate_writing(submission.essay)


from backend.services.ielts.speaking_service import (
    start_speaking_session,
    continue_speaking_session,
    evaluate_speaking
)

class SpeakingResponse(BaseModel):
    session_id: str
    answer: str

@app.post("/ielts/speaking/start")
def start_speaking():
    return start_speaking_session()


@app.post("/ielts/speaking/respond")
def respond_speaking(response: SpeakingResponse):
    return continue_speaking_session(response.session_id, response.answer)


@app.post("/ielts/speaking/evaluate")
def evaluate_speaking_test(response: SpeakingResponse):
    return evaluate_speaking(response.session_id)


from backend.services.ielts.final_score_service import calculate_final_score    
class FinalScoreRequest(BaseModel):
    reading: float
    writing: float
    speaking: float

@app.post("/ielts/final-score")
def final_score(data: FinalScoreRequest):
    return calculate_final_score(
        data.reading,
        data.writing,
        data.speaking
    )


from backend.services.documents.sop_service import generate_sop
class SOPRequest(BaseModel):
    name: str
    field: str
    country: str
    academic_background: str
    experience: str
    career_goals: str
    why_country: str

@app.post("/documents/sop")
def create_sop(data: SOPRequest):
    return generate_sop(data.dict())


from backend.services.documents.lor_service import generate_lor
class LORRequest(BaseModel):
    type: str  # academic or professional
    student_name: str
    recommender_name: str
    duration: str
    field: str
    strengths: str
    achievements: str
    country: str


@app.post("/documents/lor")
def create_lor(data: LORRequest):
    return generate_lor(data.dict())        


from backend.services.documents.roadmap_service import generate_application_roadmap
class RoadmapRequest(BaseModel):
    country: str
    intake: str  # Fall or Spring
    year: int
    ielts_band: float

@app.post("/documents/roadmap")
def application_roadmap(data: RoadmapRequest):
    return generate_application_roadmap(data.dict())    



from backend.services.ielts.result_service import generate_performance_summary
class PerformanceSummary(BaseModel):
    reading: str
    writing: str
    speaking: str
    overall: str


@app.post("/ielts/performance-summary")
def performance_summary(data: PerformanceSummary):
    return generate_performance_summary(data)