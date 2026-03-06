import pandas as pd
import numpy as np

def clean_university_data(input_path, output_path):
    # Load dataset
    df = pd.read_csv(input_path)

    # Keep only latest year data
    latest_year = df["year"].max()
    df = df[df["year"] == latest_year]

    # Replace '-' with NaN
    df.replace("-", np.nan, inplace=True)

    # Convert numeric columns
    numeric_cols = [
        "teaching", "international", "research",
        "citations", "income", "total_score",
        "num_students", "student_staff_ratio"
    ]

    for col in numeric_cols:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    # Drop rows with missing total_score
    df = df.dropna(subset=["total_score"])

    # Select useful columns
    df_clean = df[[
        "university_name",
        "country",
        "world_rank",
        "teaching",
        "research",
        "citations",
        "international",
        "total_score",
        "num_students"
    ]]

    # Reset index
    df_clean.reset_index(drop=True, inplace=True)

    # Save cleaned file
    df_clean.to_csv(output_path, index=False)

    print("✅ Cleaned dataset saved successfully!")
    print(f"Total universities: {len(df_clean)}")


if __name__ == "__main__":
    clean_university_data(
        "data/timesData.csv",
        "data/clean_universities.csv"
    )