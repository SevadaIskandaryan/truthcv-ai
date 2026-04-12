import React from 'react';

const InsightsCard = ({ data }) => {
  if (!data || !data.data || !data.data.insights) return null;

  const { confident_insights, ambiguity_insights, high_risk } = data.data.insights;

  const hasInsights = 
    (confident_insights && confident_insights.length > 0) || 
    (ambiguity_insights && ambiguity_insights.length > 0) || 
    (high_risk && high_risk.length > 0);

  if (!hasInsights) return null;

  return (
    <div className="insights-card card highlight-section">
      <h3>AI Insights</h3>
      
      {confident_insights && confident_insights.length > 0 && (
        <ul className="insight-list">
          {confident_insights.map((item, idx) => (
            <li key={`conf-${idx}`} className="insight-item">✅ {item}</li>
          ))}
        </ul>
      )}

      {ambiguity_insights && ambiguity_insights.length > 0 && (
        <ul className="insight-list" style={{ marginTop: '1rem' }}>
          {ambiguity_insights.map((item, idx) => (
            <li key={`amb-${idx}`} className="insight-item">⚠️ {item}</li>
          ))}
        </ul>
      )}

      {high_risk && high_risk.length > 0 && (
        <ul className="insight-list" style={{ marginTop: '1rem' }}>
          {high_risk.map((item, idx) => (
            <li key={`risk-${idx}`} className="insight-item">❌ {item}</li>
          ))}
        </ul>
      )}
      
    </div>
  );
};

export default InsightsCard;
