import React, { useState } from 'react';
import Navbar from '../components/Navbar';
import AnalyzeForm from '../components/AnalyzeForm';
import ResultCard from '../components/ResultCard';
import PdfViewer from '../components/PdfViewer';
import ScoreCard from '../components/ScoreCard';
import InsightsCard from '../components/InsightsCard';
import { analyzeDeveloper } from '../services/api';

const Home = () => {
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);
  const [result, setResult] = useState(null);
  const [uploadedFile, setUploadedFile] = useState(null);

  const handleAnalyze = async (formData) => {
    setIsLoading(true);
    setError(null);
    setResult(null);
    
    // Store the file so we can explicitly pass it to the PdfViewer
    const file = formData.get('file');
    setUploadedFile(file);

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
    <>
      <Navbar />
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
          
          {result && (
            <div className="results-container">
              <div className="left">
                <PdfViewer file={uploadedFile} />
              </div>
              <div className="right">
                <ScoreCard data={result} />
                <InsightsCard data={result} />
                <ResultCard result={result} />
              </div>
            </div>
          )}
        </main>
      </div>
    </>
  );
};

export default Home;
