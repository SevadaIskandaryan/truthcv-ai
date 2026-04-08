import React from 'react';

const InsightsCard = ({ data }) => {
  if (!data || !data.data) return null;

  const { insights } = data.data;

  if (!insights || insights.length === 0) return null;

  return (
    <div className="insights-card card highlight-section">
      <h3>AI Insights</h3>
      <ul className="insight-list">
        {insights.map((item, idx) => (
          <li key={idx} className="insight-item">{item}</li>
        ))}
      </ul>
    </div>
  );
};

export default InsightsCard;
