import React, { useRef } from 'react';

function Upload({ onUpload, status }) {
  const fileInput = useRef();

  const handleChange = (e) => {
    if (e.target.files && e.target.files.length > 0) {
      Array.from(e.target.files).forEach(file => onUpload(file));
      fileInput.current.value = '';
    }
  };

  return (
    <div style={{ marginBottom: 24 }}>
      <h2>Upload Legal Document(s)</h2>
      <input type="file" accept=".pdf,.docx" ref={fileInput} onChange={handleChange} multiple />
      <div style={{ marginTop: 8, color: '#555' }}>{status}</div>
    </div>
  );
}

export default Upload; 