import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { Bar } from 'react-chartjs-2';
import {
  Chart,
  BarElement,
  CategoryScale,
  LinearScale,
  Tooltip,
  Legend
} from 'chart.js';

Chart.register(BarElement, CategoryScale, LinearScale, Tooltip, Legend);

const App = () => {
  const [posts, setPosts] = useState([]);
  const [metric, setMetric] = useState("engagement_score");

  useEffect(() => {
    axios.get(`http://localhost:5000/top-posts?metric=${metric}&top_n=10`)
      .then(res => setPosts(res.data))
      .catch(err => console.error(err));
  }, [metric]);

  const data = {
    labels: posts.map(post =>
      post.title.length > 50 ? post.title.slice(0, 47) + '...' : post.title
    ),
    datasets: [
      {
        label: metric.replace("_", " ").toUpperCase(),
        data: posts.map(post => post[metric]),
        backgroundColor: 'rgba(54, 162, 235, 0.6)',
      }
    ]
  };

  const options = {
    indexAxis: 'y',
    responsive: true,
    plugins: {
      legend: { display: false },
      tooltip: { enabled: true },
    },
    scales: {
      x: { beginAtZero: true },
    }
  };

  return (
    <div style={{ padding: 40, fontFamily: 'sans-serif' }}>
      <h1>Top Reddit Posts by {metric.replace("_", " ")}</h1>
      <select value={metric} onChange={(e) => setMetric(e.target.value)} style={{ marginBottom: 20 }}>
        <option value="engagement_score">Engagement Score</option>
        <option value="growth_rate">Growth Rate</option>
      </select>
      <Bar data={data} options={options} />
    </div>
  );
};

export default App;
