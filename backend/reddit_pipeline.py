import praw
import pandas as pd
from datetime import datetime
from textblob import TextBlob
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from transformers import pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
from prophet import Prophet
import matplotlib.pyplot as plt
import numpy as np
from collections import Counter
import re

# === CONFIG ===
SUBREDDITS = ["technology", "news", "politics"]
LIMIT = 300
N_CLUSTERS = 5

# === SCRAPE REDDIT ===
def get_reddit_instance():
    return praw.Reddit(
        client_id='YVJ32KpFG4ZNiQmG66hY8w',
        client_secret='46IGTKQKTi1aiZ_Dx4Ak98tTrM5L8g',
        user_agent='script:Trendsetters:1.0 (by u/Aggravating-Steak128)'
    )

def scrape_subreddits(subreddits, limit):
    reddit = get_reddit_instance()
    data = []
    for sub in subreddits:
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
    return 0.3 * vader + 0.3 * textblob + 0.4 * bert_score

# === FEATURE ENGINEERING ===
def compute_features(df):
    df["timestamp"] = pd.to_datetime(df["created_utc"])
    df["hours_since_posted"] = (datetime.utcnow() - df["timestamp"]).dt.total_seconds() / 3600
    df["growth_rate"] = df["upvotes"] / df["hours_since_posted"].replace(0, 1)
    df["engagement_score"] = df["upvotes"] + (0.75 * df["comments"]) + (10 * df["awards"])
    df["sentiment"] = df["title"].apply(get_sentiment)
    return df

# === CLUSTER NAMING FUNCTION ===
def name_clusters(df, tfidf_vectorizer, kmeans_model, top_n=3):
    terms = tfidf_vectorizer.get_feature_names_out()
    cluster_names = {}

    for i in range(kmeans_model.n_clusters):
        centroid = kmeans_model.cluster_centers_[i]
        top_indices = centroid.argsort()[-top_n:][::-1]
        top_tfidf_terms = [terms[ind] for ind in top_indices]

        titles = df[df["cluster"] == i]["title"]
        words = re.findall(r'\b\w+\b', " ".join(titles).lower())
        common_words = [word for word, _ in Counter(words).most_common(top_n)]

        combined = list(dict.fromkeys(top_tfidf_terms + common_words))
        cluster_names[i] = " / ".join(word.title() for word in combined[:top_n])

    return cluster_names

# === TOPIC CLUSTERING ===
def cluster_topics(df, n_clusters):
    tfidf = TfidfVectorizer(stop_words='english')
    X = tfidf.fit_transform(df["title"])
    kmeans = KMeans(n_clusters=n_clusters, random_state=42)
    df["cluster"] = kmeans.fit_predict(X)

    cluster_names = name_clusters(df, tfidf, kmeans)
    df["cluster_name"] = df["cluster"].map(cluster_names)

    return df

# === MAIN ===
def main():
    all_dfs = []
    for sub in SUBREDDITS:
        print(f"\n🚀 Scraping r/{sub}...")
        df = scrape_subreddits([sub], LIMIT)
        df = compute_features(df)
        df = cluster_topics(df, N_CLUSTERS)
        df["subreddit"] = sub
        all_dfs.append(df)

    df_full = pd.concat(all_dfs, ignore_index=True)
    df_full.to_csv("final_dataset.csv", index=False)
    print("✅ Data saved to final_dataset.csv")

if __name__ == "__main__":
    main()
