import React from 'react';

function ResultsTable({ results }) {
  if (!results) return null;
  if (results.error) return <div style={{ color: 'red' }}>{results.error}</div>;

  const columns = [
    { key: 'cosine_top5', label: 'Cosine Similarity' },
    { key: 'euclidean_top5', label: 'Euclidean Distance' },
    { key: 'mmr_top5', label: 'MMR' },
    { key: 'hybrid_top5', label: 'Hybrid' },
  ];

  return (
    <div>
      <h2>Results Comparison</h2>
      <div style={{ display: 'flex', gap: 16 }}>
        {columns.map(col => (
          <div key={col.key} style={{ flex: 1, border: '1px solid #ccc', borderRadius: 8, padding: 12 }}>
            <h3 style={{ textAlign: 'center' }}>{col.label}</h3>
            <ol>
              {(results[col.key] || []).map(([fname, score], idx) => (
                <li key={fname} style={{ marginBottom: 8 }}>
                  <div><b>{fname}</b></div>
                  <div style={{ color: '#555' }}>Score: {score.toFixed(4)}</div>
                </li>
              ))}
            </ol>
          </div>
        ))}
      </div>
    </div>
  );
}

export default ResultsTable; 