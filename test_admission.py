from utils.admission_predictor import AdmissionPredictor

predictor = AdmissionPredictor()

probability = predictor.predict_probability(
    gpa=8.5,
    ielts=7.5,
    experience=2,
    research=1
)

print(f"Admission Probability: {probability}%")