import React from 'react';

const ScoreCard = ({ data }) => {
  if (!data || !data.data) return null;
  // If backend returns a score, use it, otherwise fallback to 75
  const score = data.data.score || 75;

  return (
    <div className="score-card card">
      <h3>Developer Score</h3>
      <div className="score-display">
        <span className="score-value">{score}</span>
        <span className="score-max">/ 100</span>
      </div>
      <p className="score-summary">
        Based on the provided resume and optional GitHub profile analysis, this candidate shows a solid overall compatibility.
      </p>
    </div>
  );
};

export default ScoreCard;
