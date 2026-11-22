import pandas as pd
from app.database import get_connection

def load_games():
    with get_connection() as conn:
        return pd.read_sql_query("SELECT * FROM games", conn)

if __name__ == "__main__":
    df = load_games()
    df["released"] = pd.to_datetime(df["released"], errors="coerce")

    # 1. Highest-rated games
    top_rated = (df.dropna(subset=["rating"])
                   .sort_values("rating", ascending=False)
                   .head(10))
    print("Top Rated Games:")
    print(top_rated[["name", "rating"]])

    # 2. Monthly releases
    df["release_month"] = df["released"].dt.to_period("M")
    monthly = (df.groupby("release_month").size()
                 .reset_index(name="number_of_games"))
    print("\nMonthly Releases:")
    print(monthly.head(10))

    # 3. Rating distribution
    print("\nAverage rating:", df["rating"].mean())
    print("Median rating:", df["rating"].median())
