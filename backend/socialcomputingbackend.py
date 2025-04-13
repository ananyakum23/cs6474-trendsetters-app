# === socialcomputingbackend.py ===
from flask import Flask, jsonify, request
from flask_cors import CORS
from reddit_pipeline import scrape_subreddits, compute_features, cluster_topics
from prophet import Prophet
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

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
# def forecast_multi(subreddit, cluster_id):
#     if df_global is None:
#         return jsonify({})
#     cluster_df = df_global[(df_global["subreddit"] == subreddit) & (df_global["cluster"] == cluster_id)]
#     result = {}
#     for metric in ["engagement_score", "growth_rate", "sentiment"]:
#         ts = cluster_df.groupby("timestamp")[metric].mean().reset_index()
#         ts.columns = ["ds", "y"]
#         if ts["y"].count() < 2:
#             result[metric] = []
#             continue
#         model = Prophet()
#         model.fit(ts)
#         future = model.make_future_dataframe(periods=30)
#         forecast = model.predict(future)
#         forecast["ds"] = forecast["ds"].astype(str)
#         result[metric] = forecast[["ds", "yhat"]].to_dict(orient="records")
#     return jsonify(result)
@app.route("/forecast-multi/<subreddit>/<int:cluster_id>", methods=["GET"])
# def forecast_multi(subreddit, cluster_id):
#     if df_global is None:
#         return jsonify({})

#     cluster_df = df_global[
#         (df_global["subreddit"] == subreddit) & (df_global["cluster"] == cluster_id)
#     ].copy()
#     cluster_df["ds"] = cluster_df["timestamp"].dt.floor("D")

#     result = {}

#     for metric in ["engagement_score", "growth_rate", "sentiment"]:
#         if metric == "sentiment":
#             ts_raw = cluster_df[["ds", "sentiment"]].copy()
#             ts = ts_raw.groupby("ds")["sentiment"].sum().rolling(window=2, min_periods=1).sum().reset_index()
#             ts["sentiment_scaled"] = (ts["sentiment"] - ts["sentiment"].mean()) * 100
#             ts = ts[["ds", "sentiment_scaled"]].rename(columns={"sentiment_scaled": "y"})
#         else:
#             ts = cluster_df.groupby("ds")[metric].mean().reset_index()
#             ts.columns = ["ds", "y"]

#         ts.replace([np.inf, -np.inf], pd.NA, inplace=True)
#         ts.dropna(inplace=True)

#         if ts["y"].count() < 2:
#             result[metric] = []
#             continue

#         model = Prophet(daily_seasonality=True, weekly_seasonality=True)
#         model.fit(ts)
#         future = model.make_future_dataframe(periods=30)
#         forecast = model.predict(future)
#         forecast["ds"] = forecast["ds"].astype(str)
#         result[metric] = forecast[["ds", "yhat"]].to_dict(orient="records")

#     return jsonify(result)

#best so far
@app.route("/forecast-multi/<subreddit>/<int:cluster_id>", methods=["GET"])
# def forecast_multi(subreddit, cluster_id):
#     if df_global is None:
#         return jsonify({})

#     cluster_df = df_global[
#         (df_global["subreddit"] == subreddit) & (df_global["cluster"] == cluster_id)
#     ].copy()
#     cluster_df["ds"] = cluster_df["timestamp"].dt.floor("D")

#     result = {}

#     for metric in ["engagement_score", "growth_rate", "sentiment"]:
#         if metric == "sentiment":
#             ts_raw = cluster_df[["ds", "sentiment"]].copy()
#             ts = ts_raw.groupby("ds")["sentiment"].sum().rolling(window=2, min_periods=1).sum().reset_index()
#             ts["sentiment_scaled"] = (ts["sentiment"] - ts["sentiment"].mean()) * 100
#             ts = ts[["ds", "sentiment_scaled"]].rename(columns={"sentiment_scaled": "y"})
        
#         else:
#             ts = cluster_df.groupby("ds")[metric].mean().reset_index()
#             ts.columns = ["ds", "y"]

#         # Clean and validate
#         ts.replace([np.inf, -np.inf], pd.NA, inplace=True)
#         ts.dropna(inplace=True)

#         if ts["y"].count() < 2:
#             result[metric] = []
#             continue

#         # Customize Prophet model
#         if metric == "engagement_score":
#             model = Prophet(
#                 seasonality_mode='multiplicative',
#                 daily_seasonality=False,
#                 weekly_seasonality=False,
#                 yearly_seasonality=False
#             )
#             model.add_seasonality(name='custom_week', period=7, fourier_order=3)
#         else:
#             model = Prophet(daily_seasonality=True, weekly_seasonality=True)

#         model.fit(ts)
#         future = model.make_future_dataframe(periods=30)
#         forecast = model.predict(future)
#         forecast["ds"] = forecast["ds"].astype(str)
#         result[metric] = forecast[["ds", "yhat"]].to_dict(orient="records")

#     return jsonify(result)

@app.route("/forecast-multi/<subreddit>/<int:cluster_id>", methods=["GET"])
def forecast_multi(subreddit, cluster_id):
    if df_global is None:
        return jsonify({})

    cluster_df = df_global[
        (df_global["subreddit"] == subreddit) & (df_global["cluster"] == cluster_id)
    ].copy()
    cluster_df["ds"] = cluster_df["timestamp"].dt.floor("D")

    result = {}

    for metric in ["engagement_score", "growth_rate", "sentiment"]:
        if metric == "sentiment":
            ts_raw = cluster_df[["ds", "sentiment"]].copy()
            ts = ts_raw.groupby("ds")["sentiment"].sum().rolling(window=2, min_periods=1).sum().reset_index()
            ts["sentiment_scaled"] = (ts["sentiment"] - ts["sentiment"].mean()) * 100
            ts = ts[["ds", "sentiment_scaled"]].rename(columns={"sentiment_scaled": "y"})

        # elif metric == "growth_rate":
        #     ts_raw = cluster_df[["ds", "growth_rate"]].copy()
        #     ts = ts_raw.groupby("ds")["growth_rate"].sum().rolling(window=2, min_periods=1).sum().reset_index()
        #     ts["growth_scaled"] = (ts["growth_rate"] - ts["growth_rate"].mean()) * 10
        #     ts = ts[["ds", "growth_scaled"]].rename(columns={"growth_scaled": "y"})
        elif metric == "growth_rate":
            ts_raw = cluster_df[["ds", "growth_rate"]].copy()

            # Log transform to reduce effect of extreme values
            ts_raw["growth_rate"] = np.log1p(ts_raw["growth_rate"].clip(lower=0))  # only log positive growth

            ts = ts_raw.groupby("ds")["growth_rate"].mean().rolling(window=2, min_periods=1).mean().reset_index()

            # Scale to improve visibility
            ts["growth_scaled"] = (ts["growth_rate"] - ts["growth_rate"].mean()) * 100
            ts = ts[["ds", "growth_scaled"]].rename(columns={"growth_scaled": "y"})


        else:
            ts = cluster_df.groupby("ds")[metric].mean().reset_index()
            ts.columns = ["ds", "y"]

        ts.replace([np.inf, -np.inf], pd.NA, inplace=True)
        ts.dropna(inplace=True)

        if ts["y"].count() < 2:
            result[metric] = []
            continue

        if metric == "engagement_score":
            model = Prophet(
                seasonality_mode='multiplicative',
                daily_seasonality=False,
                weekly_seasonality=False,
                yearly_seasonality=False
            )
            model.add_seasonality(name='custom_week', period=7, fourier_order=3)
        else:
            model = Prophet(daily_seasonality=True, weekly_seasonality=True)

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

@app.route("/trend-lifetimes", methods=["GET"])
def trend_lifetimes():
    subreddit = request.args.get("subreddit")
    if df_global is None or subreddit is None:
        return jsonify([])

    filtered = df_global[df_global["subreddit"] == subreddit].copy()

    # 🔐 Filter to posts from the last 30 days
    one_month_ago = datetime.utcnow() - timedelta(days=30)
    filtered = filtered[filtered["timestamp"] >= one_month_ago]

    filtered["lifetime_hours"] = filtered["hours_since_posted"]

    results = (
        filtered.groupby("cluster")["lifetime_hours"]
        .apply(list)
        .reset_index()
        .rename(columns={"lifetime_hours": "lifetimes"})
    )

    results["cluster_name"] = results["cluster"].map(
        filtered.groupby("cluster")["cluster_name"].first().to_dict()
    )
    return results.to_dict(orient="records")

@app.route("/topic-popularity", methods=["GET"])
def topic_popularity():
    subreddit = request.args.get("subreddit")
    if df_global is None or subreddit is None:
        return jsonify({})

    filtered = df_global[df_global["subreddit"] == subreddit].copy()

    # 🗓 Filter to only the past 7 days
    one_week_ago = datetime.utcnow() - timedelta(days=7)
    filtered = filtered[filtered["timestamp"] >= one_week_ago]

    filtered["ds"] = filtered["timestamp"].dt.floor("D")

    popularity = (
        filtered.groupby(["cluster", "ds"]).size().reset_index(name="count")
    )

    cluster_names = filtered.groupby("cluster")["cluster_name"].first().to_dict()

    result = {}
    for cluster_id, group in popularity.groupby("cluster"):
        result[str(cluster_id)] = {
            "name": cluster_names.get(cluster_id, f"Cluster {cluster_id}"),
            "data": group[["ds", "count"]].to_dict(orient="records")
        }

    return jsonify(result)


if __name__ == "__main__":
    app.run(debug=True)
