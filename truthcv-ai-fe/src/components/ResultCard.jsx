import React from 'react';

const ResultCard = ({ result }) => {
  if (!result || !result.data) return null;

  const { cv_data, github_data } = result.data;

  const formatDate = (dateString) => {
    if (!dateString) return 'N/A';
    return new Date(dateString).toLocaleDateString('en-US', {
      month: 'short',
      day: 'numeric',
      year: 'numeric'
    });
  };

  const capitalize = (s) => {
    if (!s) return '';
    return s.charAt(0).toUpperCase() + s.slice(1);
  };

  const getStatusLabel = (dateString) => {
    if (!dateString) return null;
    const days = (new Date() - new Date(dateString)) / (1000 * 60 * 60 * 24);
    if (days <= 30) return <span style={{ fontSize: '0.85em', marginLeft: '0.5rem' }}>🟢 Active</span>;
    if (days <= 90) return <span style={{ fontSize: '0.85em', marginLeft: '0.5rem' }}>🟢 Recent</span>;
    return null;
  };

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
          <h3 style={{ marginBottom: '1.5rem' }}>GitHub Profile</h3>
          
          <ul className="info-list" style={{ marginBottom: '1.5rem' }}>
            <li><strong>Repositories:</strong> {github_data.total_repos} ({github_data.original_repos} original)</li>
            <li><strong>Stars:</strong> {github_data.total_stars}</li>
            <li><strong>Primary Language:</strong> {github_data.primary_language || 'N/A'}</li>
          </ul>

          {github_data.top_languages && github_data.top_languages.length > 0 && (
            <div style={{ marginBottom: '1.5rem' }}>
              <h4 style={{ marginBottom: '0.5rem', color: 'var(--text-muted)' }}>Top Languages</h4>
              <ul style={{ listStyle: 'none', padding: '0.75rem 1rem', backgroundColor: 'rgba(255, 255, 255, 0.02)', borderRadius: 'var(--radius-md)' }}>
                {github_data.top_languages.map((l, i) => (
                  <li key={i} style={{ marginBottom: i < github_data.top_languages.length - 1 ? '0.75rem' : '0' }}>
                    <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '0.25rem', fontSize: '0.9rem', fontWeight: '500' }}>
                      <span>{l.language}</span>
                      <span>{l.percentage}%</span>
                    </div>
                    <div style={{ height: '6px', width: '100%', backgroundColor: 'rgba(255,255,255,0.1)', borderRadius: '3px', overflow: 'hidden' }}>
                      <div style={{ height: '100%', width: `${l.percentage}%`, backgroundColor: 'var(--accent-color)', borderRadius: '3px' }}></div>
                    </div>
                  </li>
                ))}
              </ul>
            </div>
          )}

          {github_data.activity && (
            <div style={{ marginBottom: '1.5rem' }}>
              <h4 style={{ marginBottom: '0.5rem', color: 'var(--text-muted)' }}>Activity</h4>
              <ul className="info-list">
                <li><strong>Activity Score:</strong> {github_data.activity.activity_score} ({capitalize(github_data.activity.activity_level)})</li>
                <li><strong>Active Repos:</strong> {github_data.activity.active_repos} / {github_data.total_repos}</li>
                <li><strong>Last Push:</strong> {formatDate(github_data.activity.last_push)}</li>
                <li><strong>Recent Activity:</strong> {capitalize(github_data.activity.recent_activity_level)}</li>
              </ul>
            </div>
          )}

          {github_data.top_projects && github_data.top_projects.length > 0 && (
            <div style={{ marginBottom: '1.5rem' }}>
              <h4 style={{ marginBottom: '0.5rem', color: 'var(--text-muted)' }}>Top Projects</h4>
              <ul className="info-list">
                {github_data.top_projects.map((proj, idx) => (
                  <li key={idx}>
                    • <strong>{proj.name}</strong> {proj.language ? `(${proj.language})` : ''} 
                    {proj.stars > 0 ? ` ⭐${proj.stars}` : ''}
                    {getStatusLabel(proj.last_updated)}
                    <span style={{ color: 'var(--text-muted)', fontSize: '0.9em', marginLeft: '0.5rem' }}>
                      — Updated {formatDate(proj.last_updated)}
                    </span>
                  </li>
                ))}
              </ul>
            </div>
          )}

          <div>
            <h4 style={{ marginBottom: '0.5rem', color: 'var(--text-muted)' }}>Profile Signals</h4>
            <ul className="info-list">
              <li><strong>Total Repo Quality Score:</strong> {github_data.repo_quality_score} / 100</li>
              <li><strong>Language Diversity:</strong> {github_data.language_diversity_score} / 100</li>
            </ul>
          </div>

        </div>
      )}

    </div>
  );
};

export default ResultCard;
