import React, { useEffect, useState } from 'react';
import Tabs from './components/Tabs';
import TopPostsChart from './components/TopPostsChart';
import ForecastChart from './components/ForecastChart';
import TrendLifetimeHistogram from './components/TrendLifetimeHistogram';
import TopicPopularityChart from './components/TopicPopularityChart'; // ⬅️ new

import {
  fetchTopPosts,
  fetchClusterNames,
  fetchForecastForCluster,
  fetchTrendLifetimes,
  fetchTopicPopularity // ⬅️ new
} from './services/api';

const App = () => {
  const [selectedSubreddit, setSelectedSubreddit] = useState("technology");
  const [topPosts, setTopPosts] = useState([]);
  const [forecastData, setForecastData] = useState(null);
  const [clusterId, setClusterId] = useState(0);
  const [clusterNames, setClusterNames] = useState({});
  const [lifetimeData, setLifetimeData] = useState([]);
  const [popularityData, setPopularityData] = useState({}); // ⬅️ new
  const [activeTab, setActiveTab] = useState("forecast");

  // Fetch top posts, cluster names, lifetimes, and popularity on subreddit change
  useEffect(() => {
    fetchTopPosts(selectedSubreddit).then(res => setTopPosts(res.data));
    fetchClusterNames(selectedSubreddit).then(res => setClusterNames(res.data));
    fetchTrendLifetimes(selectedSubreddit).then(res => setLifetimeData(res.data));
    fetchTopicPopularity(selectedSubreddit).then(res => setPopularityData(res.data)); // ⬅️ new
    setClusterId(0);
  }, [selectedSubreddit]);

  // Fetch forecast data when cluster or subreddit changes
  useEffect(() => {
    fetchForecastForCluster(clusterId, selectedSubreddit).then(res =>
      setForecastData(res.data)
    );
  }, [clusterId, selectedSubreddit]);

  return (
    <div style={{ padding: 40, fontFamily: 'sans-serif', maxWidth: 1200, margin: '0 auto' }}>
      {/* MAIN DASHBOARD TITLE */}
      <h1 style={{ textAlign: 'center', fontSize: '2.5rem', marginBottom: 20 }}>
        {selectedSubreddit.charAt(0).toUpperCase() + selectedSubreddit.slice(1)} Subreddit Trends
      </h1>

      {/* SUBREDDIT SELECTOR */}
      <div style={{ marginBottom: 20 }}>
        <label>Select Subreddit: </label>
        <select value={selectedSubreddit} onChange={(e) => setSelectedSubreddit(e.target.value)}>
          <option value="technology">Technology</option>
          <option value="news">News</option>
          <option value="politics">Politics</option>
        </select>
      </div>

      {/* TAB CONTROLS */}
      <Tabs activeTab={activeTab} setActiveTab={setActiveTab} />

      {/* TOP POSTS TAB */}
      {activeTab === "top" && (
        <>
          <h2>🔝 Top 10 Reddit Posts by Engagement</h2>
          <TopPostsChart posts={topPosts} />
        </>
      )}

      {/* FORECAST TAB */}
      {activeTab === "forecast" && (
        <div style={{ marginTop: 30 }}>
          <h2>
            📈 Forecasted Trends for {clusterNames[clusterId] || `Cluster ${clusterId}`}
          </h2>

          {Object.keys(clusterNames).length === 0 ? (
            <p>⏳ Loading cluster names...</p>
          ) : (
            <>
              <label style={{ marginRight: 10 }}>Select Cluster:</label>
              <select
                value={clusterId}
                onChange={(e) => setClusterId(Number(e.target.value))}
              >
                {Object.entries(clusterNames).map(([id, name]) => (
                  <option key={id} value={id}>
                    {name}
                  </option>
                ))}
              </select>
            </>
          )}

          {forecastData ? (
            <div style={{ marginTop: 30 }}>
              <ForecastChart data={forecastData} clusterId={clusterId} />
            </div>
          ) : (
            <p>⏳ Loading forecast...</p>
          )}
        </div>
      )}

      {/* LIFETIME HISTOGRAM TAB */}
      {activeTab === "lifetime" && (
        <div style={{ marginTop: 30 }}>
          <h2>⏳ Trend Lifetimes (Avg Hours Active Per Cluster in the Last Month)</h2>
          {lifetimeData.length === 0 ? (
            <p>⏳ Loading lifetime data...</p>
          ) : (
            <TrendLifetimeHistogram data={lifetimeData} />
          )}
        </div>
      )}

      {/* TOPIC POPULARITY TAB */}
      {activeTab === "popularity" && (
        <div style={{ marginTop: 30 }}>
          <h2>📊 Topic Popularity Over Time (Cluster Post Volume)</h2>
          {Object.keys(popularityData).length === 0 ? (
            <p>⏳ Loading popularity data...</p>
          ) : (
            <TopicPopularityChart data={popularityData} />
          )}
        </div>
      )}
    </div>
  );
};

export default App;
