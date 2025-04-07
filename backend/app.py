from flask import Flask, jsonify, request
from reddit_pipeline import (
    scrape_subreddits,
    compute_features,
    cluster_topics,
    init_sentiment_models  # 👈 import the init function
)
import pandas as pd

app = Flask(__name__)

# Global cache
DATAFRAME = pd.DataFrame()

def refresh_data(subreddits=["technology"], limit=100):
    try:
        df = scrape_subreddits(subreddits, limit=limit)
        df = compute_features(df)
        df = cluster_topics(df)
        return df
    except Exception as e:
        print(f"Error refreshing data: {e}")
        return pd.DataFrame()

# === Initialize models + data once at startup ===
init_sentiment_models()  # 👈 this is critical
DATAFRAME = refresh_data()

@app.route("/")
def index():
    return jsonify({"message": "Reddit Trend Analyzer API is running."})

@app.route("/refresh", methods=["POST"])
def refresh():
    global DATAFRAME
    subreddits = request.json.get("subreddits", ["technology"])
    limit = request.json.get("limit", 100)
    DATAFRAME = refresh_data(subreddits, limit)
    return jsonify({"status": "Data refreshed", "subreddits": subreddits, "count": len(DATAFRAME)})

@app.route("/top-posts", methods=["GET"])
def get_top_posts():
    metric = request.args.get("metric", "engagement_score")
    top_n = int(request.args.get("top_n", 10))

    if metric not in DATAFRAME.columns:
        return jsonify({"error": f"Invalid metric: {metric}"}), 400

    sorted_df = DATAFRAME.sort_values(by=metric, ascending=False).head(top_n)
    posts = sorted_df[["title", "subreddit", "upvotes", "comments", "awards", metric]].to_dict(orient="records")
    return jsonify(posts)

if __name__ == "__main__":
    app.run(debug=True)
