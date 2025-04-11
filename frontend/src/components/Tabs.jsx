import React from 'react';

const Tabs = ({ activeTab, setActiveTab }) => (
  <div style={{ marginBottom: 20 }}>
    <button
      onClick={() => setActiveTab("forecast")}
      style={{
        marginRight: 10,
        padding: "8px 16px",
        background: activeTab === "forecast" ? "#007bff" : "#444",
        color: "white",
        border: "none",
        borderRadius: 5
      }}
    >
      📈 Forecasted Trends
    </button>
    <button
      onClick={() => setActiveTab("top")}
      style={{
        marginRight: 10,
        padding: "8px 16px",
        background: activeTab === "top" ? "#007bff" : "#444",
        color: "white",
        border: "none",
        borderRadius: 5
      }}
    >
      🔝 Top Posts
    </button>
  </div>
);

export default Tabs;
