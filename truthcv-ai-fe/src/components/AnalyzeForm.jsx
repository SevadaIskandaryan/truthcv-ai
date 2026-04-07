import React, { useState } from 'react';

const AnalyzeForm = ({ onSubmit, isLoading }) => {
  const [file, setFile] = useState(null);
  const [githubLink, setGithubLink] = useState('');
  const [error, setError] = useState('');

  const handleFileChange = (e) => {
    const selectedFile = e.target.files[0];
    if (selectedFile && selectedFile.type !== 'application/pdf') {
      setError('Please select a valid PDF file.');
      setFile(null);
    } else {
      setError('');
      setFile(selectedFile);
    }
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    if (!file) {
      setError('PDF file is required.');
      return;
    }
    
    const formData = new FormData();
    formData.append('file', file);
    if (githubLink.trim()) {
      formData.append('github_link', githubLink.trim());
    }
    
    onSubmit(formData);
  };

  return (
    <div className="card form-container">
      <h2>Analyze Developer</h2>
      {error && <div className="error-message">{error}</div>}
      <form onSubmit={handleSubmit}>
        <div className="form-group">
          <label htmlFor="resume-upload">Upload Resume (PDF only)*</label>
          <input
            id="resume-upload"
            type="file"
            accept=".pdf"
            onChange={handleFileChange}
            disabled={isLoading}
            required
          />
        </div>
        <div className="form-group">
          <label htmlFor="github-link">GitHub Username or Link (Optional)</label>
          <input
            id="github-link"
            type="text"
            placeholder="e.g. torvalds or https://github.com/torvalds"
            value={githubLink}
            onChange={(e) => setGithubLink(e.target.value)}
            disabled={isLoading}
          />
        </div>
        <button type="submit" disabled={isLoading || !file} className="submit-btn">
          {isLoading ? <span className="spinner"></span> : 'Analyze'}
        </button>
      </form>
    </div>
  );
};

export default AnalyzeForm;
