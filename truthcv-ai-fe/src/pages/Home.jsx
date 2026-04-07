import React, { useState } from 'react';
import AnalyzeForm from '../components/AnalyzeForm';
import ResultCard from '../components/ResultCard';
import { analyzeDeveloper } from '../services/api';

const Home = () => {
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);
  const [result, setResult] = useState(null);

  const handleAnalyze = async (formData) => {
    setIsLoading(true);
    setError(null);
    setResult(null);

    try {
      const response = await analyzeDeveloper(formData);
      setResult(response);
    } catch (err) {
      setError(err.message || 'Failed to analyze developer.');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="home-page">
      <header className="page-header">
        <h1>TruthCV AI</h1>
        <p>Your Developer Analysis Tool</p>
      </header>
      
      <main className="main-content">
        <AnalyzeForm onSubmit={handleAnalyze} isLoading={isLoading} />
        
        {error && (
          <div className="alert error-alert">
            <strong>Error:</strong> {error}
          </div>
        )}
        
        {isLoading && (
          <div className="loading-state">
            <div className="spinner lg"></div>
            <p>Analyzing developer profile... This might take a few moments.</p>
          </div>
        )}
        
        {result && <ResultCard result={result} />}
      </main>
    </div>
  );
};

export default Home;
