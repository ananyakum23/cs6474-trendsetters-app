# === socialcomputingbackend.py ===
from flask import Flask, jsonify, request
from flask_cors import CORS
from reddit_pipeline import scrape_subreddits, compute_features, cluster_topics
from prophet import Prophet
import pandas as pd

app = Flask(__name__)
CORS(app)

df_global = None

@app.route("/refresh", methods=["GET"])
def refresh():
    global df_global
    subreddits = ["technology", "news", "politics"]
    all_dfs = []
    for sub in subreddits:
        df = scrape_subreddits([sub], 100)
        df = compute_features(df)
        df = cluster_topics(df, n_clusters=5)
        df["subreddit"] = sub
        all_dfs.append(df)
    df_global = pd.concat(all_dfs, ignore_index=True)
    return jsonify({"status": "refreshed", "count": len(df_global)})

@app.route("/cluster-names", methods=["GET"])
def get_cluster_names():
    subreddit = request.args.get("subreddit")
    if df_global is None or subreddit is None:
        return jsonify({})
    filtered = df_global[df_global["subreddit"] == subreddit]
    names = filtered.groupby("cluster")["cluster_name"].first().to_dict()
    return jsonify(names)

@app.route("/forecast-multi/<subreddit>/<int:cluster_id>", methods=["GET"])
def forecast_multi(subreddit, cluster_id):
    if df_global is None:
        return jsonify({})
    cluster_df = df_global[(df_global["subreddit"] == subreddit) & (df_global["cluster"] == cluster_id)]
    result = {}
    for metric in ["engagement_score", "growth_rate", "sentiment"]:
        ts = cluster_df.groupby("timestamp")[metric].mean().reset_index()
        ts.columns = ["ds", "y"]
        if ts["y"].count() < 2:
            result[metric] = []
            continue
        model = Prophet()
        model.fit(ts)
        future = model.make_future_dataframe(periods=30)
        forecast = model.predict(future)
        forecast["ds"] = forecast["ds"].astype(str)
        result[metric] = forecast[["ds", "yhat"]].to_dict(orient="records")
    return jsonify(result)

@app.route("/top-engagement", methods=["GET"])
def top_engagement():
    subreddit = request.args.get("subreddit")
    if df_global is None or subreddit is None:
        return jsonify([])
    filtered = df_global[df_global["subreddit"] == subreddit]
    top_posts = filtered.nlargest(10, "engagement_score")[["title", "engagement_score"]]
    return top_posts.to_dict(orient="records")

if __name__ == "__main__":
    app.run(debug=True)
