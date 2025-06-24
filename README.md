## DataCraft AI 🚀
A full-stack application leveraging React.js (frontend) and Python (backend) for AI-driven data transformation and visualization insights, powered by Ollama for local AI model execution.

# ✨ Features
CSV Data Upload: Securely upload your raw Comma Separated Values (CSV) datasets.

Natural Language Prompting: Describe your desired data transformations, aggregations, and analytical goals using intuitive natural language.

AI-Powered Data Transformation: Utilizes Ollama (with the Mistral model) to interpret prompts and generate precise Python (Pandas) scripts for data cleaning, filtering, aggregation, and selection.

Transformed CSV Download: Download the cleaned and transformed CSV file, perfectly prepared for direct import into Tableau Desktop or other BI tools.

Tableau Visualization Suggestions: Receive intelligent, AI-generated recommendations on how to visualize your processed data.

Local History Persistence: Your interaction history (prompts and results) is conveniently stored locally in your browser, allowing you to revisit previous sessions.

## 📸 Demo Screenshots
![Screenshot 2025-06-24 135029](https://github.com/user-attachments/assets/50ad0e1c-e612-48dd-a4d0-e955c00bf19c)
An overview of the DataCraft AI dashboard, showcasing the CSV upload and prompt input on the left, and the dynamically updated AI-generated output with the download option on the right.

# Transformed Data in Spreadsheet
![Screenshot 2025-06-24 140443](https://github.com/user-attachments/assets/0f51b854-8108-4899-8aef-3f94b05fd532)
A glimpse of the AI-transformed CSV file opened in a spreadsheet application, demonstrating the precise data manipulation based on a user's prompt (e.g., specific columns and filtered data).

# 🛠️ Technologies Used
Frontend (React.js)
React: JavaScript library for building user interfaces.

Axios: Promise-based HTTP client for API requests.

CSS: For custom styling and responsive design.

Local Storage: Browser API used for client-side persistence of interaction history.

Backend (FastAPI Python API)
FastAPI: Modern, high-performance web framework for Python APIs.

Ollama (Mistral): Large Language Model (LLM) backend for prompt interpretation and script generation.

Pandas: Python library for data manipulation and analysis.

uuid: For generating unique identifiers for temporary files.

shutil & os: Python modules for high-level file operations and interacting with the operating system.

# 🚀 Getting Started
Follow these instructions to get DataCraft AI up and running on your local machine.

Prerequisites
Before you begin, ensure you have the following installed:

Python 3.8+: python.org

Node.js & npm (or Yarn): nodejs.org

Git: git-scm.com

Ollama:

Download and install Ollama from ollama.ai.

After installation, pull the mistral model (this is crucial for the backend's AI functionality):

ollama pull mistral

Installation
Clone the DataCraft AI Repository:
Navigate to your desired directory in your terminal and clone the project:

git clone https://github.com/DhirajSharma89/DataCraftAI.git
cd DataCraftAI

Backend Setup (Python & Ollama):
Navigate into the backend directory, create and activate a Python virtual environment, and install dependencies.

cd backend
python -m venv .venv_hyper # Create virtual environment
.\.venv_hyper\Scripts\activate # Activate on Windows PowerShell
# For Git Bash / Linux / macOS: source ./.venv_hyper/bin/activate

pip install -r requirements.txt

Your backend/requirements.txt should contain:

fastapi
uvicorn
python-multipart
ollama
pandas

If using Tableau Hyper API: tableauhyperapi

(Note: tableauhyperapi is optional if your current focus is solely on CSV output, but good to include if .hyper generation is a future feature.)

Frontend Setup (React.js):
Navigate into the frontend directory and install Node.js dependencies.

cd ../frontend # Go back to the DataCraftAI root, then into frontend
npm install

Running the Application
You will need two separate terminal windows.

Start the Backend Server:
In your first terminal, navigate to the backend directory, activate its virtual environment, and start the FastAPI server:

cd E:\Projects\DataCraftAI\backend
.\.venv_hyper\Scripts\activate # For Windows PowerShell
#For Git Bash/Linux/macOS: source ./.venv_hyper/bin/activate

uvicorn main:app --reload

(The --reload flag automatically restarts the server on code changes.)

Start the Frontend Development Server:
In your second terminal, navigate to the frontend directory and start the React development server:

cd E:\Projects\DataCraftAI\frontend
npm run dev

Access the Application:
After both servers are running, open your web browser and go to the address displayed by the frontend server (typically http://localhost:5173/).

# 📂 Project Structure
We have uploaded all the core files to the main branch. For clarity and easier navigation during development, separate backend and frontend branches might exist or be created to focus on specific parts. The general structure looks like this:

# 👥 Contributors
Dhiraj Sharma


# 📄 License
This project is open-source. Feel free to modify and improve it! 🚀

# 📧 Contact
For any questions or feedback, please reach out to Dhiraj Sharma:

GitHub: DhirajSharma89

(Optional:rhombahu@gmail.com)
