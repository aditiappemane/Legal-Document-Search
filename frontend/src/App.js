import React, { useState, useEffect } from 'react';
import axios from 'axios';
import Upload from './components/Upload';
import Query from './components/Query';
import ResultsTable from './components/ResultsTable';
import MetricsDashboard from './components/MetricsDashboard';

function App() {
  const [uploadStatus, setUploadStatus] = useState('');
  const [query, setQuery] = useState('');
  const [results, setResults] = useState(null);
  const [loading, setLoading] = useState(false);
  const [evalQuery, setEvalQuery] = useState('');
  const [evalRelevant, setEvalRelevant] = useState('');
  const [metrics, setMetrics] = useState(null);
  const [evalLoading, setEvalLoading] = useState(false);
  const [availableFilenames, setAvailableFilenames] = useState([]);

  useEffect(() => {
    axios.get('/filenames/').then(res => {
      setAvailableFilenames(res.data.filenames || []);
      setEvalRelevant('');
    });
  }, []);

  const handleUpload = async (file) => {
    setUploadStatus('Uploading...');
    const formData = new FormData();
    formData.append('file', file);
    try {
      const res = await axios.post('/upload/', formData, {
        headers: { 'Content-Type': 'multipart/form-data' },
      });
      setUploadStatus(`Uploaded: ${res.data.filename}`);
    } catch (err) {
      setUploadStatus('Upload failed');
    }
  };

  const handleQuery = async (q) => {
    setQuery(q);
    setLoading(true);
    try {
      const res = await axios.post('/search/', { query: q });
      setResults(res.data);
    } catch (err) {
      setResults({ error: 'Search failed' });
    }
    setLoading(false);
  };

  const handleEvaluate = async (e) => {
    e.preventDefault();
    setEvalLoading(true);
    setMetrics(null);
    try {
      const res = await axios.post('/evaluate/', {
        query: evalQuery,
        relevant: evalRelevant.split(',').map(s => s.trim()).filter(Boolean)
      });
      setMetrics(res.data.metrics);
    } catch (err) {
      setMetrics({ error: 'Evaluation failed' });
    }
    setEvalLoading(false);
  };

  return (
    <div style={{ maxWidth: 1200, margin: '0 auto', padding: 32, fontFamily: 'sans-serif' }}>
      <h1>Indian Legal Document Search System</h1>
      <Upload onUpload={handleUpload} status={uploadStatus} />
      <Query onQuery={handleQuery} loading={loading} />
      <ResultsTable results={results} />
      <div style={{ marginTop: 32, marginBottom: 32, border: '1px solid #eee', borderRadius: 8, padding: 24 }}>
        <h2>Evaluate Metrics</h2>
        <form onSubmit={handleEvaluate}>
          <div style={{ marginBottom: 12 }}>
            <label>Query:&nbsp;
              <input
                type="text"
                value={evalQuery}
                onChange={e => setEvalQuery(e.target.value)}
                style={{ width: 400, padding: 8 }}
                disabled={evalLoading}
              />
            </label>
          </div>
          <div style={{ marginBottom: 12 }}>
            <label>Relevant Filenames:&nbsp;
              <select
                multiple
                value={evalRelevant.split(',').map(s => s.trim()).filter(Boolean)}
                onChange={e => {
                  const selected = Array.from(e.target.selectedOptions).map(opt => opt.value);
                  setEvalRelevant(selected.join(', '));
                }}
                style={{ width: 400, height: 100, padding: 8 }}
                disabled={evalLoading}
              >
                {availableFilenames.map(fname => (
                  <option key={fname} value={fname}>{fname}</option>
                ))}
              </select>
            </label>
          </div>
          <button type="submit" disabled={evalLoading} style={{ padding: '8px 16px', fontSize: 16 }}>
            {evalLoading ? 'Evaluating...' : 'Evaluate'}
          </button>
        </form>
      </div>
      <MetricsDashboard metrics={metrics} />
    </div>
  );
}

export default App; 