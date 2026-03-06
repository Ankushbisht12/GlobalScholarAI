from utils.ielts_evaluator import IELTSEvaluator

api_key = "AIzaSyDpEYyZaZkDjT9coJ138g3Mbb8wZVYOZBs"

evaluator = IELTSEvaluator(api_key)

essay = """
In recent years, technology has become an essential part of our daily lives. 
Many people argue that it has made life more convenient by improving communication, transportation, and access to information. 
However, others believe that excessive reliance on technology has created social and psychological problems.

On one hand, technological advancements have simplified many tasks. 
For instance, online banking and digital payments save time and reduce the need for physical visits to banks. 
Moreover, communication tools such as smartphones and social media enable people to stay connected across long distances. 
This has significantly improved global interaction and business opportunities.

On the other hand, technology has also introduced certain drawbacks. 
Many individuals have become addicted to social media and online games, which negatively affects mental health and productivity. 
Additionally, automation has reduced employment opportunities in some sectors, leading to economic concerns.

In my opinion, although technology presents some challenges, its advantages outweigh the disadvantages. 
The key lies in using it responsibly and maintaining a balance between digital and real-life interactions.
"""

result = evaluator.evaluate_writing(essay)

print(result)