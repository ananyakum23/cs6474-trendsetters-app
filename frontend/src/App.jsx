import React, { useEffect, useState } from 'react';
import Tabs from './components/Tabs';
import TopPostsChart from './components/TopPostsChart';
import ForecastChart from './components/ForecastChart';
import {
  fetchTopPosts,
  fetchClusterNames,
  fetchForecastForCluster
} from './services/api';

const App = () => {
  const [topPosts, setTopPosts] = useState([]);
  const [forecastData, setForecastData] = useState(null);
  const [clusterId, setClusterId] = useState(0);
  const [clusterNames, setClusterNames] = useState({});
  const [activeTab, setActiveTab] = useState("forecast");

  // Fetch top posts and cluster names on load
  useEffect(() => {
    fetchTopPosts().then(res => setTopPosts(res.data));
    fetchClusterNames().then(res => setClusterNames(res.data));
  }, []);

  // Fetch forecast when clusterId changes
  useEffect(() => {
    fetchForecastForCluster(clusterId).then(res => setForecastData(res.data));
  }, [clusterId]);

  return (
    <div style={{ padding: 40, fontFamily: 'sans-serif', maxWidth: 1200, margin: '0 auto' }}>
      {/* MAIN DASHBOARD TITLE */}
      <h1 style={{ textAlign: 'center', fontSize: '2.5rem', marginBottom: 20 }}>
        Technology Subreddit Trends
      </h1>

      {/* Tab Controls */}
      <Tabs activeTab={activeTab} setActiveTab={setActiveTab} />

      {/* Top Posts Tab */}
      {activeTab === "top" && (
        <>
          <h2>🔝 Top 10 Reddit Posts by Engagement</h2>
          <TopPostsChart posts={topPosts} />
        </>
      )}

      {/* Forecast Tab */}
      {activeTab === "forecast" && (
        <div style={{ marginTop: 30 }}>
          <h2>
            📈 Forecasted Trends for{' '}
            {clusterNames[clusterId] || `Cluster ${clusterId}`}
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
    </div>
  );
};

export default App;