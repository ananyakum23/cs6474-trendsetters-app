import React, { useRef, useEffect } from 'react';
import { Chart as ChartJS, registerables } from 'chart.js';
import { Chart } from 'react-chartjs-2';

ChartJS.register(...registerables);

const TopPostsChart = ({ posts }) => {
  const chartRef = useRef(null);

  useEffect(() => {
    return () => {
      if (chartRef.current && chartRef.current.chartInstance) {
        chartRef.current.chartInstance.destroy();
      }
    };
  }, [posts]);

  const data = {
    labels: posts.map(post =>
      post.title.length > 50 ? post.title.slice(0, 50) + '...' : post.title
    ),
    datasets: [
      {
        label: 'Engagement Score',
        data: posts.map(post => post.engagement_score),
        backgroundColor: 'rgba(54, 162, 235, 0.6)',
        borderColor: 'rgba(54, 162, 235, 1)',
        borderWidth: 1
      }
    ]
  };

  const options = {
    responsive: true,
    indexAxis: 'y',
    plugins: {
      legend: { display: true },
      tooltip: { enabled: true }
    },
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

  return <Chart ref={chartRef} type="bar" data={data} options={options} />;
};

export default TopPostsChart;
