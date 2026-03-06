from utils.scholarship_predictor import ScholarshipPredictor

predictor = ScholarshipPredictor()

probability = predictor.predict_probability(
    gpa=8.7,
    ielts=8.0,
    income=500000,
    research=1,
    leadership=1
)

print(f"Scholarship Probability: {probability}%")