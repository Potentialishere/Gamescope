import pandas as pd
import plotly.express as px
from app.analytics import load_games

df = load_games()

# 1. Horizontal Bar Chart: Top 10 Games
top = df.dropna(subset=["rating"]).nlargest(10, "rating")
px.bar(top, x="rating", y="name", orientation="h",
       title="Top Rated Games",
       labels={"rating": "RAWG rating", "name": "Game"}).show()

# 2. Line Chart: Monthly Release Trend
df["released"] = pd.to_datetime(df["released"], errors="coerce")
df["month"] = df["released"].dt.to_period("M").astype(str)
monthly = df.groupby("month").size().reset_index(name="games")
px.line(monthly, x="month", y="games", markers=True,
        title="Video Game Release Trends").show()

# 3. Histogram: Rating Distribution
px.histogram(df.dropna(subset=["rating"]), x="rating",
             nbins=20,
             title="Distribution of Game Ratings").show()
