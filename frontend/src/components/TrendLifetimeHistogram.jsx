import React from "react";
import { Bar } from "react-chartjs-2";
import {
  Chart,
  BarElement,
  CategoryScale,
  LinearScale,
  Tooltip,
  Legend,
} from "chart.js";

Chart.register(BarElement, CategoryScale, LinearScale, Tooltip, Legend);

const TrendLifetimeHistogram = ({ data }) => {
  const labels = data.map(d => d.cluster_name);
  const counts = data.map(d =>
    Math.round(d.lifetimes.reduce((acc, hr) => acc + hr, 0) / d.lifetimes.length)
  );

  const chartData = {
    labels,
    datasets: [
      {
        label: "Avg Lifetime (hrs)",
        data: counts,
        backgroundColor: "rgba(75,192,192,0.6)",
      },
    ],
  };

  return (
    <div style={{ marginTop: 30 }}>
      <Bar data={chartData} options={{ responsive: true }} />
    </div>
  );
};

export default TrendLifetimeHistogram;
