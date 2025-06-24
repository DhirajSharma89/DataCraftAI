import React from 'react';
import './About.css';

function About() {
  return (
    <div className="about-page">
      <div className="about-card">
        <h1>📊 About DataCraft AI</h1>
        <p>
          <strong>DataCraft AI</strong> is an AI-powered tool that transforms your raw CSV data into meaningful visual insights.
          It leverages local LLMs (like Mistral via Ollama) to:
        </p>
        <ul>
          <li>🧠 Understand your prompt</li>
          <li>📁 Process and clean your dataset</li>
          <li>📈 Suggest charts & dashboards</li>
        </ul>
        <p>
          Whether you're analyzing sales, trends, or patterns — DataCraft AI gives you a head start on your reports.
        </p>
        <p className="signature">🚀 Built by Dhiraj Sharma</p>
      </div>
    </div>
  );
}

export default About;
