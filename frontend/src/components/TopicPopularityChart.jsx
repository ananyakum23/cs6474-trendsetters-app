import React, { useRef, useEffect } from 'react';
import { Chart as ChartJS, registerables } from 'chart.js';
import { Chart } from 'react-chartjs-2';

ChartJS.register(...registerables);

const TopicPopularityChart = ({ data }) => {
  const chartRef = useRef(null);

  useEffect(() => {
    return () => {
      if (chartRef.current && chartRef.current.chartInstance) {
        chartRef.current.chartInstance.destroy();
      }
    };
  }, [data]);

  const labels = [...new Set(Object.values(data).flatMap(cluster =>
    cluster.data.map(item => item.ds)
  ))].sort();

  const datasets = Object.entries(data).map(([clusterId, cluster]) => ({
    label: cluster.name || `Cluster ${clusterId}`,
    data: labels.map(date => {
      const match = cluster.data.find(d => d.ds === date);
      return match ? match.count : 0;
    }),
    borderWidth: 2,
    tension: 0.3,
    fill: false
  }));

  const chartData = {
    labels,
    datasets
  };

  const options = {
    responsive: true,
    plugins: {
      legend: { display: true },
      tooltip: { enabled: true }
    },
    scales: {
      x: {
        title: { display: true, text: 'Date' },
        ticks: { maxRotation: 45, minRotation: 45 }
      },
      y: {
        beginAtZero: true,
        title: { display: true, text: 'Post Count' }
      }
    }
  };

  return (
    <div style={{ width: '100%', height: '500px' }}>
      <Chart
        ref={chartRef}
        type="line"
        data={chartData}
        options={options}
        height={500}
        width={900}
      />
    </div>
  );
};

export default TopicPopularityChart;