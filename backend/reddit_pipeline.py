import praw
import pandas as pd
from datetime import datetime
from textblob import TextBlob
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from transformers import pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
from prophet import Prophet
import numpy as np

# === CONFIG ===
SUBREDDITS = ["technology"]
LIMIT = 100
N_CLUSTERS = 5

# === SCRAPE REDDIT ===
def get_reddit_instance():
    return praw.Reddit(
        client_id='YVJ32KpFG4ZNiQmG66hY8w',
        client_secret='46IGTKQKTi1aiZ_Dx4Ak98tTrM5L8g',
        user_agent = 'script:Trendsetters:1.0 (by u/Aggravating-Steak128)'
    )

def scrape_subreddits(subreddits, limit):
    reddit = get_reddit_instance()
    data = []
    for sub in subreddits:
        # for post in reddit.subreddit(sub).search(query="*", sort="new", time_filter="month", limit=limit):
        for post in reddit.subreddit(sub).search(query="*", sort="new", time_filter="month", limit=limit):

            data.append({
                "id": post.id,
                "title": post.title,
                "subreddit": sub,
                "created_utc": datetime.utcfromtimestamp(post.created_utc),
                "upvotes": post.score,
                "comments": post.num_comments,
                "awards": post.total_awards_received
            })
    return pd.DataFrame(data)

# === SENTIMENT ANALYSIS ===
analyzer = SentimentIntensityAnalyzer()
bert_pipe = pipeline("sentiment-analysis")

def get_sentiment(text):
    vader = analyzer.polarity_scores(text)["compound"]
    textblob = TextBlob(text).sentiment.polarity
    bert_result = bert_pipe(text[:512])[0]["label"]
    bert_score = 1 if bert_result == "POSITIVE" else -1
    return 0.4 * vader + 0.3 * textblob + 0.3 * bert_score

# === FEATURE ENGINEERING ===
def compute_features(df):
    df["timestamp"] = pd.to_datetime(df["created_utc"])
    df["hours_since_posted"] = (datetime.utcnow() - df["timestamp"]).dt.total_seconds() / 3600
    df["engagement_score"] = df["upvotes"] + (0.75 * df["comments"]) + (10 * df["awards"])
    # df["engagement_score"] += np.random.normal(0, 0.5, size=len(df))
    df["sentiment"] = df["title"].apply(get_sentiment)
    return df

# === TOPIC CLUSTERING ===
def cluster_topics(df, n_clusters):
    tfidf = TfidfVectorizer(stop_words='english')
    X = tfidf.fit_transform(df["title"])
    kmeans = KMeans(n_clusters=n_clusters, random_state=42)
    df["cluster"] = kmeans.fit_predict(X)
    return df

# === FORECASTING ===
# def forecast_cluster(df, metric="engagement_score"):
#     cluster_ids = df["cluster"].unique()
#     for cluster_id in cluster_ids:
#         cluster_df = df[df["cluster"] == cluster_id]
#         ts = cluster_df.groupby("timestamp")[metric].mean().reset_index()
#         ts.columns = ["ds", "y"]
#         model = Prophet()
#         model.fit(ts)
#         future = model.make_future_dataframe(periods=30)
#         forecast = model.predict(future)
#         print(f"\n=== Forecast for Cluster {cluster_id} ({metric}) ===")
#         print(forecast[["ds", "yhat"]].tail())

def forecast_cluster(df, metric="engagement_score"):
    cluster_ids = df["cluster"].unique()
    for cluster_id in cluster_ids:
        cluster_df = df[df["cluster"] == cluster_id]
        ts = cluster_df.groupby("timestamp")[metric].mean().reset_index()
        ts.columns = ["ds", "y"]

        # Skip if not enough data
        if ts["y"].count() < 2:
            print(f"⚠️ Skipping cluster {cluster_id} — not enough data for forecasting.")
            continue

        model = Prophet()
        model.fit(ts)
        future = model.make_future_dataframe(periods=30)
        forecast = model.predict(future)
        print(f"\n=== Forecast for Cluster {cluster_id} ({metric}) ===")
        print(forecast[["ds", "yhat"]].tail())


# === MAIN PIPELINE ===
def main():
    print("🚀 Scraping Reddit...")
    df = scrape_subreddits(SUBREDDITS, LIMIT)

    print("🔍 Computing Features...")
    df = compute_features(df)

    print("🧠 Clustering Topics...")
    df = cluster_topics(df, N_CLUSTERS)

    df.to_csv("final_dataset.csv", index=False)
    print("✅ Data saved to final_dataset.csv")

    print("📈 Running Forecasts...")
    forecast_cluster(df, metric="engagement_score")
    forecast_cluster(df, metric="sentiment")

if __name__ == "__main__":
    main()
