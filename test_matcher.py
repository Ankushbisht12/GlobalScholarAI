from utils.university_matcher import UniversityMatcher

matcher = UniversityMatcher()

student_profile = """
Student wants to study Data Science.
Has GPA 8.5, IELTS 7.5.
Looking for research-oriented university in Germany or UK.
Strong academic background.
"""

results = matcher.match_universities(student_profile)

print(results[["university_name", "country", "world_rank"]])