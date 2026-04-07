import React from 'react';

const ResultCard = ({ result }) => {
  if (!result || !result.data) return null;

  const { cv_data, github_data, insights } = result.data;

  return (
    <div className="card result-container">
      <h2>Analysis Results</h2>
      
      {/* CV Data Section */}
      <div className="result-section">
        <h3>Resume Information</h3>
        <ul className="info-list">
          {cv_data?.email && <li><strong>Email:</strong> {cv_data.email}</li>}
          {cv_data?.phone && <li><strong>Phone:</strong> {cv_data.phone}</li>}
          <li><strong>Raw Content Length:</strong> {cv_data?.raw_text?.length || 0} characters</li>
        </ul>
      </div>

      {/* GitHub Data Section */}
      {github_data && (
        <div className="result-section">
          <h3>GitHub Profile</h3>
          <ul className="info-list">
            <li><strong>Public Repositories:</strong> {github_data.repo_count || 0}</li>
            {github_data.languages && Object.keys(github_data.languages).length > 0 && (
              <li>
                <strong>Languages:</strong> {Object.keys(github_data.languages).join(', ')}
              </li>
            )}
          </ul>
        </div>
      )}

      {/* Insights Section */}
      {insights && insights.length > 0 && (
        <div className="result-section highlight-section">
          <h3>AI Insights</h3>
          <ul className="insight-list">
            {insights.map((insight, idx) => (
              <li key={idx} className="insight-item">{insight}</li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
};

export default ResultCard;
