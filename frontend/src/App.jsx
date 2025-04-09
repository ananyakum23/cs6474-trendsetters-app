// import React, { useEffect, useState } from 'react';
// import axios from 'axios';
// import { Bar } from 'react-chartjs-2';
// import {
//   Chart,
//   BarElement,
//   CategoryScale,
//   LinearScale,
//   Tooltip,
//   Legend
// } from 'chart.js';

// Chart.register(BarElement, CategoryScale, LinearScale, Tooltip, Legend);

// const App = () => {
//   const [forecastData, setForecastData] = useState([]);
//   const [metric, setMetric] = useState("engagement_score");
//   const [clusterId, setClusterId] = useState(0); // default cluster

//   useEffect(() => {
//     axios
//       .get(`http://localhost:5000/forecast/${clusterId}/${metric}`)
//       .then(res => setForecastData(res.data))
//       .catch(err => console.error(err));
//   }, [metric, clusterId]);

//   const data = {
//     labels: forecastData.map(point => point.ds),
//     datasets: [
//       {
//         label: `Forecasted ${metric.replace("_", " ").toUpperCase()}`,
//         data: forecastData.map(point => point.yhat),
//         backgroundColor: 'rgba(75, 192, 192, 0.6)',
//       }
//     ]
//   };

//   const options = {
//     responsive: true,
//     plugins: {
//       legend: { display: true },
//       tooltip: { enabled: true },
//     },
//     scales: {
//       x: { title: { display: true, text: 'Date' } },
//       y: { beginAtZero: true },
//     }
//   };

//   return (
//     <div style={{ padding: 40, fontFamily: 'sans-serif' }}>
//       <h1>Forecasted Reddit Trends</h1>

//       <div style={{ marginBottom: 20 }}>
//         <label style={{ marginRight: 10 }}>Select Metric:</label>
//         <select value={metric} onChange={(e) => setMetric(e.target.value)}>
//           <option value="engagement_score">Engagement Score</option>
//           <option value="growth_rate">Growth Rate</option>
//         </select>
//       </div>

//       <div style={{ marginBottom: 20 }}>
//         <label style={{ marginRight: 10 }}>Select Cluster ID:</label>
//         <select value={clusterId} onChange={(e) => setClusterId(Number(e.target.value))}>
//           {[0, 1, 2, 3, 4].map(id => (
//             <option key={id} value={id}>Cluster {id}</option>
//           ))}
//         </select>
//       </div>

//       <Bar data={data} options={options} />
//     </div>
//   );
// };

// export default App;

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
  const [topPosts, setTopPosts] = useState([]);

  useEffect(() => {
    axios
      .get('http://127.0.0.1:5000/top-engagement')
      .then(res => {
        console.log("✅ Top posts fetched:", res.data); // 👈 Add this
        setTopPosts(res.data);
      })
      .catch(err => {
        console.error("❌ Axios error:", err);
        if (err.response) {
          console.error("Status:", err.response.status);
          console.error("Data:", err.response.data);
        } else if (err.request) {
          console.error("No response received:", err.request);
        } else {
          console.error("Error setting up request:", err.message);
        }
      });
  }, []);

  const data = {
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

  const options = {
    responsive: true,
    plugins: {
      legend: { display: true },
      tooltip: { enabled: true },
    },
    indexAxis: 'y', // horizontal bar chart
    scales: {
      x: {
        beginAtZero: true,
        title: {
          display: true,
          text: 'Engagement Score'
        }
      },
      y: {
        title: {
          display: true,
          text: 'Post Title'
        }
      }
    }
  };

  return (
    <div style={{ padding: 40, fontFamily: 'sans-serif' }}>
      <h1>Top 10 Reddit Posts by Engagement</h1>
      <Bar data={data} options={options} />
    </div>
  );
};

export default App;