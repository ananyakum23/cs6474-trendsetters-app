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
      🔝 Top Current Posts
    </button>

    <button
        onClick={() => setActiveTab("lifetime")}
        style={{
            marginRight: 10,
            padding: "8px 16px",
            background: activeTab === "lifetime" ? "#007bff" : "#444",
            color: "white",
            border: "none",
            borderRadius: 5
        }}
    >
        ⏳ Past Trend Lifetimes
    </button>
    
    <button
        onClick={() => setActiveTab("popularity")}
        style={{
            marginRight: 10,
            padding: "8px 16px",
            background: activeTab === "popularity" ? "#007bff" : "#444",
            color: "white",
            border: "none",
            borderRadius: 5
        }}
        >
        📊 Past Topic Popularity
    </button>
  </div>
);

export default Tabs;
