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

  return (
    <div className="pdf-viewer-card card">
      <h3>Uploaded Document</h3>
      <div className="pdf-container">
        {url && (
          <iframe 
            src={url} 
            title="PDF Viewer" 
            width="100%" 
            height="600px" 
            style={{ border: 'none', borderRadius: '4px' }}
          />
        )}
      </div>
    </div>
  );
};

export default PdfViewer;
