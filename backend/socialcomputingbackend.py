# from flask import Flask, jsonify, request
# import pandas as pd
# from scraper import scrape_subreddits
# from features import compute_features
# from clustering import cluster_topics
# from forecasting import forecast_trend

# app = Flask(__name__)
# df_global = None

# @app.route("/refresh", methods=["GET"])
# def refresh_data():
#     global df_global
#     df = scrape_subreddits(["news", "technology"])
#     df = compute_features(df)
#     df = cluster_topics(df)
#     df_global = df
#     return jsonify({"status": "data refreshed", "rows": len(df)})

# @app.route("/forecast/<int:cluster_id>/<metric>", methods=["GET"])
# def get_forecast(cluster_id, metric):
#     forecast = forecast_trend(df_global, metric, cluster_id)
#     forecast["ds"] = forecast["ds"].astype(str)
#     return forecast[["ds", "yhat"]].to_dict(orient="records")

# @app.route("/clusters", methods=["GET"])
# def get_clusters():
#     clusters = df_global.groupby("cluster")["title"].apply(list).to_dict()
#     return jsonify(clusters)

# if __name__ == "__main__":
#     app.run(debug=True)

# app.py (Flask backend)

from flask import Flask, jsonify
from flask_cors import CORS
from reddit_pipeline import scrape_subreddits
from reddit_pipeline import compute_features
from reddit_pipeline import cluster_topics
from reddit_pipeline import forecast_cluster

app = Flask(__name__)
CORS(app)

# Global dataframe
df_global = None

@app.route("/refresh", methods=["GET"])
def refresh():
    global df_global
    df = scrape_subreddits(["news", "technology"], 100)
    df = compute_features(df)
    df = cluster_topics(df, n_clusters=5)
    df_global = df
    return jsonify({"status": "refreshed", "count": len(df_global)})

@app.route("/clusters", methods=["GET"])
def get_clusters():
    if df_global is None:
        return jsonify({})
    grouped = df_global.groupby("cluster")["title"].apply(list).to_dict()
    return jsonify(grouped)

@app.route("/forecast/<int:cluster_id>/<metric>", methods=["GET"])
def forecast(cluster_id, metric):
    if df_global is None:
        return jsonify([])
    forecast_df = forecast_cluster(df_global, cluster_id, metric)
    return forecast_df.to_dict(orient="records")

if __name__ == "__main__":
    app.run(debug=True)
