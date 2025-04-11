import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { Bar, Line } from 'react-chartjs-2';
import {
  Chart,
  BarElement,
  LineElement,
  PointElement,
  CategoryScale,
  LinearScale,
  Tooltip,
  Legend
} from 'chart.js';

Chart.register(
  BarElement,
  LineElement,
  PointElement,
  CategoryScale,
  LinearScale,
  Tooltip,
  Legend
);

const App = () => {
  const [topPosts, setTopPosts] = useState([]);
  const [forecastData, setForecastData] = useState(null);
  const [clusterId, setClusterId] = useState(0);

  // Fetch top posts for bar chart
  useEffect(() => {
    axios
      .get('http://127.0.0.1:5000/top-engagement')
      .then(res => {
        console.log("✅ Top posts fetched:", res.data);
        setTopPosts(res.data);
      })
      .catch(err => {
        console.error("❌ Axios error:", err);
      });
  }, []);

  // Fetch forecast data for selected cluster
  useEffect(() => {
    axios
      .get(`http://127.0.0.1:5000/forecast-multi/${clusterId}`)
      .then(res => {
        console.log("📈 Forecast data:", res.data);
        setForecastData(res.data);
      })
      .catch(err => {
        console.error("❌ Forecast error:", err);
      });
  }, [clusterId]);

  const barData = {
    labels: topPosts.map(post =>
      post.title.length > 50 ? post.title.slice(0, 50) + '...' : post.title
    ),
    datasets: [
      {
        label: 'Engagement Score',
        data: topPosts.map(post => post.engagement_score),
        backgroundColor: 'rgba(54, 162, 235, 0.6)',
        borderColor: 'rgba(54, 162, 235, 1)',
        borderWidth: 1
      }
    ]
  };

  const barOptions = {
    responsive: true,
    plugins: {
      legend: { display: true },
      tooltip: { enabled: true },
    },
    indexAxis: 'y',
    scales: {
      x: {
        beginAtZero: true,
        title: { display: true, text: 'Engagement Score' }
      },
      y: {
        title: { display: true, text: 'Post Title' }
      }
    }
  };

  const lineLabels = forecastData?.engagement_score?.map(item => item.ds) || [];

  const lineData = {
    labels: lineLabels,
    datasets: [
      {
        label: 'Forecasted Engagement Score',
        data: forecastData?.engagement_score?.map(item => item.yhat) || [],
        borderColor: 'rgba(75, 192, 192, 1)',
        backgroundColor: 'rgba(75, 192, 192, 0.4)',
        tension: 0.3
      },
      {
        label: 'Forecasted Growth Rate',
        data: forecastData?.growth_rate?.map(item => item.yhat) || [],
        borderColor: 'rgba(255, 99, 132, 1)',
        backgroundColor: 'rgba(255, 99, 132, 0.4)',
        tension: 0.3
      },
      {
        label: 'Forecasted Sentiment',
        data: forecastData?.sentiment?.map(item => item.yhat) || [],
        borderColor: 'rgba(255, 206, 86, 1)',
        backgroundColor: 'rgba(255, 206, 86, 0.4)',
        tension: 0.3
      }
    ]
  };

  const lineOptions = {
    responsive: true,
    plugins: {
      legend: { display: true },
      tooltip: { enabled: true }
    },
    scales: {
      x: {
        title: { display: true, text: 'Date' }
      },
      y: {
        beginAtZero: true,
        title: { display: true, text: 'Metric Value' }
      }
    }
  };

  return (
    <div style={{ padding: 40, fontFamily: 'sans-serif' }}>
      <h1>Top 10 Reddit Posts by Engagement</h1>
      <Bar data={barData} options={barOptions} />

      <div style={{ marginTop: 60 }}>
        <h2>📈 Forecasted Trends for Cluster {clusterId}</h2>

        <label style={{ marginRight: 10 }}>Select Cluster:</label>
        <select value={clusterId} onChange={e => setClusterId(Number(e.target.value))}>
          {[0, 1, 2, 3, 4].map(id => (
            <option key={id} value={id}>Cluster {id}</option>
          ))}
        </select>

        {forecastData ? (
          <div style={{ marginTop: 30 }}>
            <Line data={lineData} options={lineOptions} />
          </div>
        ) : (
          <p>⏳ Loading forecast...</p>
        )}
      </div>
    </div>
  );
};

export default App;