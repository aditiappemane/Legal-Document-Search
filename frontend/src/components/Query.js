import React, { useState } from 'react';

function Query({ onQuery, loading }) {
  const [input, setInput] = useState('');

  const handleSubmit = (e) => {
    e.preventDefault();
    if (input.trim()) {
      onQuery(input);
    }
  };

  return (
    <form onSubmit={handleSubmit} style={{ marginBottom: 24 }}>
      <h2>Search Query</h2>
      <input
        type="text"
        value={input}
        onChange={e => setInput(e.target.value)}
        placeholder="Enter your legal query..."
        style={{ width: 400, padding: 8, fontSize: 16 }}
        disabled={loading}
      />
      <button type="submit" style={{ marginLeft: 12, padding: '8px 16px', fontSize: 16 }} disabled={loading}>
        {loading ? 'Searching...' : 'Search'}
      </button>
    </form>
  );
}

export default Query; 