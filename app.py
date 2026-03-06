import streamlit as st
from utils.university_matcher import UniversityMatcher
from utils.admission_predictor import AdmissionPredictor
from utils.scholarship_predictor import ScholarshipPredictor
from utils.ielts_evaluator import IELTSEvaluator

st.set_page_config(page_title="GlobalScholarAI", layout="wide")

st.title("🎓 GlobalScholarAI – Study Abroad Advisor")

# Sidebar Inputs
st.sidebar.header("Student Profile")

gpa = st.sidebar.slider("GPA", 5.0, 10.0, 8.0)
ielts = st.sidebar.slider("IELTS Score", 5.0, 9.0, 7.0)
experience = st.sidebar.slider("Work Experience (years)", 0, 5, 1)
research = st.sidebar.slider("Research Papers", 0, 3, 0)
income = st.sidebar.number_input("Family Income (INR)", 200000, 2000000, 600000)
leadership = st.sidebar.slider("Leadership Activities", 0, 3, 1)

field = st.sidebar.text_input("Field of Study", "Data Science")
preferred_country = st.sidebar.text_input("Preferred Country", "Germany")

# Initialize Models
matcher = UniversityMatcher()
admission_model = AdmissionPredictor()
scholarship_model = ScholarshipPredictor()

# Admission Probability
admission_prob = admission_model.predict_probability(
    gpa, ielts, experience, research
)

# Scholarship Probability
scholarship_prob = scholarship_model.predict_probability(
    gpa, ielts, income, research, leadership
)

st.subheader("📊 Admission Prediction")
st.metric("Admission Probability", f"{admission_prob}%")

st.subheader("💰 Scholarship Prediction")
st.metric("Scholarship Probability", f"{scholarship_prob}%")

# University Matching
student_profile_text = f"""
Student wants to study {field}.
Has GPA {gpa}, IELTS {ielts}.
Looking for university in {preferred_country}.
Work experience {experience} years.
"""

results = matcher.match_universities(student_profile_text)

st.subheader("🏫 Recommended Universities")
st.dataframe(results[["university_name", "country", "world_rank"]])

# IELTS Evaluation
st.subheader("✍ IELTS Writing Evaluation")

essay = st.text_area("Paste your IELTS essay here")

api_key = st.text_input("Enter Gemini API Key", type="password")

if st.button("Evaluate Essay"):
    if essay and api_key:
        evaluator = IELTSEvaluator(api_key)
        result = evaluator.evaluate_writing(essay)

        if "error" in result:
            st.error(result["error"])
        else:
            st.success(f"Overall Band Score: {result['band_score']}")
            st.write("Grammar:", result["grammar_score"])
            st.write("Vocabulary:", result["vocabulary_score"])
            st.write("Coherence:", result["coherence_score"])
            st.write("Task Response:", result["task_response_score"])

            st.subheader("Strengths")
            st.write(result["strengths"])

            st.subheader("Weaknesses")
            st.write(result["weaknesses"])

            st.subheader("Improvement Suggestions")
            st.write(result["improvement_suggestions"])