from flask import Flask, jsonify
from flask_cors import CORS
from reddit_pipeline import scrape_subreddits, compute_features, cluster_topics
from prophet import Prophet

app = Flask(__name__)
CORS(app)

df_global = None

@app.route("/refresh", methods=["GET"])
def refresh():
    global df_global
    print("🔄 Refreshing data from Reddit...")
    df = scrape_subreddits(["news", "technology"], 100)
    df = compute_features(df)
    df = cluster_topics(df, n_clusters=5)
    df_global = df
    print("✅ Data refreshed and processed.")
    return jsonify({"status": "refreshed", "count": len(df_global)})

@app.route("/clusters", methods=["GET"])
def get_clusters():
    if df_global is None:
        return jsonify({})

    clusters = {}
    for cluster_id, group in df_global.groupby("cluster"):
        clusters[str(cluster_id)] = {
            "name": group["cluster_name"].iloc[0],
            "posts": group["title"].tolist()
        }
    return jsonify(clusters)

@app.route("/cluster-names", methods=["GET"])
def get_cluster_names():
    if df_global is None:
        return jsonify({})

    cluster_names = df_global.groupby("cluster")["cluster_name"].first().to_dict()
    return jsonify(cluster_names)

@app.route("/forecast/<int:cluster_id>/<metric>", methods=["GET"])
def forecast(cluster_id, metric):
    if df_global is None:
        return jsonify([])

    cluster_df = df_global[df_global["cluster"] == cluster_id]
    ts = cluster_df.groupby("timestamp")[metric].mean().reset_index()
    ts.columns = ["ds", "y"]

    if ts["y"].count() < 2:
        return jsonify([])

    model = Prophet()
    model.fit(ts)
    future = model.make_future_dataframe(periods=30)
    forecast = model.predict(future)
    forecast["ds"] = forecast["ds"].astype(str)
    return forecast[["ds", "yhat"]].to_dict(orient="records")

@app.route("/forecast-multi/<int:cluster_id>", methods=["GET"])
def forecast_multi(cluster_id):
    if df_global is None:
        return jsonify({})

    cluster_df = df_global[df_global["cluster"] == cluster_id]
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
    if df_global is None:
        return jsonify([])

    top_posts = df_global.nlargest(10, "engagement_score")[["title", "engagement_score"]]
    return top_posts.to_dict(orient="records")

@app.route("/wordcloud", methods=["GET"])
def get_wordcloud():
    global DATAFRAME
    if DATAFRAME is None:
        return jsonify({"error": "Data not loaded"}), 400

    img_io = generate_wordcloud_image(DATAFRAME)
    return send_file(img_io, mimetype='image/png')

if __name__ == "__main__":
    app.run(debug=True)