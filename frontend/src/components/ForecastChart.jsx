import React, { useRef, useEffect } from 'react';
import { Chart as ChartJS, registerables } from 'chart.js';
import { Chart } from 'react-chartjs-2';

ChartJS.register(...registerables);

const ForecastChart = ({ data, clusterId }) => {
  const chartRef = useRef(null);

  useEffect(() => {
    return () => {
      if (chartRef.current && chartRef.current.chartInstance) {
        chartRef.current.chartInstance.destroy();
      }
    };
  }, [data, clusterId]);

  const labels = data?.engagement_score?.map(item => item.ds) || [];

  const chartData = {
    labels,
    datasets: [
      {
        label: 'Forecasted Engagement Score',
        data: data?.engagement_score?.map(item => item.yhat) || [],
        borderColor: 'rgba(75, 192, 192, 1)',
        backgroundColor: 'rgba(75, 192, 192, 0.4)',
        tension: 0.3
      },
      {
        label: 'Forecasted Growth Rate',
        data: data?.growth_rate?.map(item => item.yhat) || [],
        borderColor: 'rgba(255, 99, 132, 1)',
        backgroundColor: 'rgba(255, 99, 132, 0.4)',
        tension: 0.3
      },
      {
        label: 'Forecasted Sentiment',
        data: data?.sentiment?.map(item => item.yhat) || [],
        borderColor: 'rgba(255, 206, 86, 1)',
        backgroundColor: 'rgba(255, 206, 86, 0.4)',
        tension: 0.3
      }
    ]
  };

  const options = {
    responsive: true,
    plugins: {
      legend: { display: true },
      tooltip: { enabled: true }
    },
    scales: {
      x: { title: { display: true, text: 'Date' } },
      y: { beginAtZero: true, title: { display: true, text: 'Metric Value' } }
    }
  };

  return (
  <div style={{ width: '100%', height: '500px' }}> {/* You can adjust this */}
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

export default ForecastChart;
