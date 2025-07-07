import React from 'react';

function MetricsDashboard({ metrics }) {
  const methods = ['cosine', 'euclidean', 'mmr', 'hybrid'];
  if (!metrics) return null;
  return (
    <div style={{ marginTop: 32 }}>
      <h2>Performance Metrics</h2>
      <table style={{ width: '100%', borderCollapse: 'collapse' }}>
        <thead>
          <tr>
            <th style={{ border: '1px solid #ccc', padding: 8 }}>Method</th>
            <th style={{ border: '1px solid #ccc', padding: 8 }}>Precision@5</th>
            <th style={{ border: '1px solid #ccc', padding: 8 }}>Recall</th>
            <th style={{ border: '1px solid #ccc', padding: 8 }}>Diversity</th>
          </tr>
        </thead>
        <tbody>
          {methods.map(method => (
            <tr key={method}>
              <td style={{ border: '1px solid #ccc', padding: 8 }}>{method.charAt(0).toUpperCase() + method.slice(1)}</td>
              <td style={{ border: '1px solid #ccc', padding: 8 }}>{metrics[method]?.precision ?? '-'}</td>
              <td style={{ border: '1px solid #ccc', padding: 8 }}>{metrics[method]?.recall ?? '-'}</td>
              <td style={{ border: '1px solid #ccc', padding: 8 }}>{metrics[method]?.diversity ?? '-'}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

export default MetricsDashboard; 