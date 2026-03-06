import numpy as np
import pandas as pd
import joblib
import os


MODEL_PATH = "backend/models/admission_model.pkl"


def load_model():
    if os.path.exists(MODEL_PATH):
        return joblib.load(MODEL_PATH)
    else:
        raise Exception("Admission model not found.")


model = load_model()


def predict_admission(gpa: float, ielts: float, experience: int, research: int):

    # Normalize
    gpa_norm = (gpa - 5) / 5
    ielts_norm = (ielts - 5) / 4
    exp_norm = experience / 5
    research_norm = research / 2

    # Weighted score
    score = (
        gpa_norm * 0.35 +
        ielts_norm * 0.30 +
        exp_norm * 0.20 +
        research_norm * 0.15
    )

    # Convert to percentage
    probability = score * 100

    # Add smoothing (no extreme values)
    if probability < 20:
        probability += 15
    if probability > 90:
        probability = 90

    return round(probability, 2)