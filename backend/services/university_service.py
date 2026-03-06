import pandas as pd
import numpy as np
from sentence_transformers import SentenceTransformer
import faiss
import os

DATA_PATH = "backend/data/clean_universities.csv"

class UniversityMatcher:

    def __init__(self):
        self.df = pd.read_csv(DATA_PATH)
        self.model = SentenceTransformer("all-MiniLM-L6-v2")
        self.index = None
        self._build_index()

    def _build_index(self):

        texts = self.df.apply(
            lambda row: f"{row['university_name']} in {row['country']} "
                        f"Teaching score {row['teaching']} "
                        f"Research score {row['research']} "
                        f"Citations {row['citations']} "
                        f"Overall rank {row['world_rank']}",
            axis=1
        ).tolist()

        embeddings = self.model.encode(texts)
        dimension = embeddings.shape[1]

        self.index = faiss.IndexFlatL2(dimension)
        self.index.add(np.array(embeddings))

    def match(self, query_text, top_k=5):
        query_embedding = self.model.encode([query_text])
        distances, indices = self.index.search(np.array(query_embedding), top_k)
        
        results = self.df.iloc[indices[0]].copy()
        
        #IMPORTANT FIX — Replace NaN with safe values
        results = results.replace({np.nan: None})
        
        return results.to_dict(orient="records")


matcher = UniversityMatcher()


def match_universities(field: str, preferred_country: str, gpa: float, ielts: float):

    df = matcher.df.copy()

    #Step 1: Strict country filter first
    if preferred_country:
        country_map = {
            "uk": "united kingdom",
            "usa": "united states of america",
            "us": "united states of america",
            "canada": "canada",
            "germany": "germany",
            "australia": "australia"
            }
        preferred = preferred_country.lower().strip()
        if preferred in country_map:
            preferred = country_map[preferred]

        df_country = df[
            df["country"]
            .str.lower()
            .str.contains(preferred, na=False)
        ]

        if df_country.empty:
            df = matcher.df.copy()

        df = df_country

    # 🔥 Step 2: Semantic ranking inside filtered dataset
    texts = df.apply(
        lambda row: f"{row['university_name']} in {row['country']} "
                    f"Teaching score {row['teaching']} "
                    f"Research score {row['research']} "
                    f"Citations {row['citations']} "
                    f"Overall rank {row['world_rank']}",
        axis=1
    ).tolist()

    embeddings = matcher.model.encode(texts)
    dimension = embeddings.shape[1]

    index = faiss.IndexFlatL2(dimension)
    index.add(np.array(embeddings))

    query = f"{field} program with strong research focus"
    query_embedding = matcher.model.encode([query])

    distances, indices = index.search(np.array(query_embedding), 5)

    results = df.iloc[indices[0]].copy()
    results = results.replace({np.nan: None})

    recommendations = []

    for _, row in results.iterrows():

        rank_str = str(row["world_rank"]).replace("=", "")
        rank = int(rank_str) if rank_str.isdigit() else 999

        if gpa >= 9 and rank <= 50:
            category = "Dream"
        elif gpa >= 8 and rank <= 150:
            category = "Target"
        else:
            category = "Safe"

        recommendations.append({
            "university_name": row["university_name"],
            "country": row["country"],
            "world_rank": row["world_rank"],
            "category": category
        })

    return {
    "recommended_universities": recommendations,
    "strategy": "Apply to a mix of Dream, Target and Safe universities for better chances."
}