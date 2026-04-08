import React, { useEffect, useState } from 'react';

const PdfViewer = ({ file }) => {
  const [url, setUrl] = useState('');

  useEffect(() => {
    if (file) {
      const objectUrl = URL.createObjectURL(file);
      setUrl(objectUrl);
      return () => URL.revokeObjectURL(objectUrl);
    }
  }, [file]);

  if (!file) return null;

  // Enhance URL to disable default PDF viewer toolbars
  const iframeSrc = url ? `${url}#toolbar=0&navpanes=0&scrollbar=0` : '';

  return (
    <div className="pdf-viewer-card card">
      <div className="pdf-header">
        <h3>Resume Preview</h3>
        {url && (
          <a href={url} target="_blank" rel="noopener noreferrer" className="pdf-open-link">
            Open Full PDF ↗
          </a>
        )}
      </div>
      
      <p className="pdf-hint">
        Preview your resume while reviewing insights &rarr;
      </p>

      <div className="pdf-container">
        {iframeSrc && (
          <iframe 
            className="pdf-iframe"
            src={iframeSrc} 
            title="PDF Preview" 
          />
        )}
      </div>
    </div>
  );
};

export default PdfViewer;
