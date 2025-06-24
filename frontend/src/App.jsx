import React, { useState } from 'react';
import axios from 'axios';
import './App.css';
import Sidebar from './components/Sidebar';
import About from './components/About';

function App() {
  const [csvFile, setCsvFile] = useState(null);
  const [fileName, setFileName] = useState('');
  const [prompt, setPrompt] = useState('');
  const [outputFileName, setOutputFileName] = useState('');
  const [history, setHistory] = useState([]);
  const [activePage, setActivePage] = useState('Dashboard');

  const handleSubmit = async () => {
    if (!csvFile || !prompt) {
      alert("Please upload a CSV and enter a prompt.");
      return;
    }

    const formData = new FormData();
    formData.append('csv_file', csvFile);
    formData.append('user_prompt', prompt);

    try {
      const res = await axios.post(
        'http://localhost:8000/generate-csv/',
        formData,
        { headers: { 'Content-Type': 'multipart/form-data' } }
      );

      const filename = res.data.filename;
      setOutputFileName(filename);

      const suggestions = res.data.tableau_suggestions || '';
      const notes = res.data.notes || '';

      const historyEntry = {
        prompt,
        filename,
        suggestions,
        notes,
        timestamp: new Date().toLocaleString()
      };

      setHistory((prev) => [historyEntry, ...prev]);
    } catch (err) {
      console.error(err);
      alert('Error generating configuration.');
      setOutputFileName('');
    }
  };

  return (
  <div className="app-wrapper">
    <Sidebar activePage={activePage} setActivePage={setActivePage} />
    <div className="main-content">
      {activePage === 'Dashboard' ? (
        <>
          <header>
            <h1 className="title">DataCraft AI</h1>
            <p className="subtitle">Simple, strong, and emphasizes turning data into quantifiable insights.</p>
          </header>

          <div className="content-grid">
            {/* Upload + Prompt */}
            <div className="card">
              <h2>1. Provide Your Data</h2>
              <p className="instruction">Upload a CSV file and write a prompt for your report.</p>

              {fileName && (
                <div className="file-name">
                  <strong>Uploaded file:</strong> {fileName}
                </div>
              )}

              <input
                type="file"
                accept=".csv"
                className="file-input"
                onChange={(e) => {
                  setCsvFile(e.target.files[0]);
                  setFileName(e.target.files[0]?.name || '');
                }}
              />

              <textarea
                className="prompt-input"
                placeholder="e.g., 'Create a bar chart showing total sales by region.'"
                value={prompt}
                onChange={(e) => setPrompt(e.target.value)}
              ></textarea>

              <button className="submit-btn" onClick={handleSubmit}>
                Generate Configuration
              </button>
            </div>

            {/* Output Section */}
            <div className="card">
              <h2>2. Generated Output</h2>
              <p className="instruction">Your AI-generated cleaned CSV will appear here.</p>

              <div className="output-container">
                <div className="output-box">
                  {outputFileName ? (
                    <>
                      <p><strong>Output CSV:</strong> {outputFileName}</p>
                      <a
                        className="download-btn"
                        href={`http://localhost:8000/download/${outputFileName}`}
                        target="_blank"
                        rel="noopener noreferrer"
                        download
                      >
                        ⬇️ Download Cleaned CSV
                      </a>
                    </>
                  ) : (
                    "Waiting for input..."
                  )}
                </div>
              </div>
            </div>
          </div>
        </>
      ) : activePage === 'History' ? (
        // History page
        <div className="history-page">
          <h2 className="history-title">🕘 History</h2>
          {history.length === 0 ? (
            <p className="no-history">No history yet.</p>
          ) : (
            <ul className="history-list">
              {history.map((entry, index) => (
                <li key={index} className="history-entry" style={{ backgroundColor: 'white', color: 'black', padding: '12px 16px', borderRadius: '8px', marginBottom: '10px' }}>
                  <span><strong>{entry.timestamp}</strong> — </span>
                  <span>
                    <a
                      href={`http://localhost:8000/download/${entry.filename}`}
                      target="_blank"
                      rel="noopener noreferrer"
                      download
                      style={{ color: 'black', textDecoration: 'underline', fontWeight: '500' }}
                    >
                      {entry.filename}
                    </a>
                  </span>
                  <span> — {entry.prompt}</span>
                </li>
              ))}
            </ul>
          )}
        </div>
      ) : activePage === 'About' ? (
        <About />
      ) : null}
    </div>
  </div>
);

}

export default App;
