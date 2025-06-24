DataCraft AI
DataCraft AI is an intelligent application designed to streamline the data preparation process for analysis and visualization, especially for tools like Tableau. It allows users to upload a CSV file and provide natural language prompts for data transformations. The AI then processes the request, generates a transformed CSV file, and offers insights and suggestions for visualization.

Features
CSV Upload: Easily upload your raw CSV datasets.

Natural Language Processing: Describe your desired data transformations and analyses using plain English prompts.

AI-Powered Data Transformation: The backend, powered by Ollama (Mistral), generates Python (Pandas) scripts to clean, filter, aggregate, or select data based on your prompt.

Transformed CSV Download: Download the cleaned and transformed CSV file, ready for direct import into Tableau or other visualization tools.

Tableau Visualization Suggestions: Receive AI-generated suggestions and notes on how to best visualize your transformed data in Tableau Desktop.

Local History: Your interaction history (prompts and results) is stored locally in your browser for easy access.

Screenshots
Main Dashboard & Input/Output
The main dashboard where users can upload CSVs, enter prompts, and view the generated output and download the processed CSV.

Transformed CSV Output in Spreadsheet
An example of the transformed CSV output opened in a spreadsheet application, showing the results of an AI-driven data transformation.

Technologies Used
Frontend
React: For building the user interface.

Axios: For making HTTP requests to the backend.

CSS: For styling, including responsive design.

Local Storage: For client-side history persistence.

Backend
FastAPI: A modern, fast (high-performance) web framework for building APIs with Python.

Ollama (Mistral): Used as the Large Language Model (LLM) to interpret user prompts and generate data transformation instructions and visualization suggestions.

Pandas: A powerful Python library for data manipulation and analysis, used to execute the AI-generated transformation scripts.

uuid: For generating unique identifiers for temporary files.

shutil & os: For file system operations and managing temporary file storage.

Getting Started
To get DataCraft AI up and running on your local machine, follow these steps.

Prerequisites
Python 3.8+

Node.js and npm (or Yarn)

Git

Ollama installed and running with the mistral model (or deepseek-coder if you switch models in ollama_handler.py).

Download Ollama from ollama.ai.

Pull the mistral model: ollama pull mistral

Installation
Clone the repository:

git clone https://github.com/DhirajSharma89/DataCraftAI.git
cd DataCraftAI

Backend Setup:

cd backend
python -m venv .venv_hyper # Create a virtual environment named .venv_hyper
.\.venv_hyper\Scripts\activate # Activate on Windows PowerShell
# For Git Bash/Linux/macOS: source ./.venv_hyper/bin/activate

pip install -r requirements.txt

Your requirements.txt should contain:

fastapi
uvicorn
python-multipart
ollama
pandas
# If you are working with .hyper files for Tableau directly:
# tableauhyperapi

Note on tableauhyperapi: If your backend logic uses tableauhyperapi (as seen in some previous discussions), ensure it's in your requirements.txt. It's a binary dependency and might require specific system setup for installation. If you are only outputting CSVs, you can omit it.

Frontend Setup:

cd ../frontend # Go back to the DataCraftAI root, then into frontend
npm install

Running the Application
Start the Backend Server:
Open a new terminal, navigate to the backend directory, activate its virtual environment, and start the FastAPI server:

cd E:\Projects\DataCraftAI\backend
.\.venv_hyper\Scripts\activate # For Windows PowerShell
# For Git Bash/Linux/macOS: source ./.venv_hyper/bin/activate
uvicorn main:app --reload

(The --reload flag is useful for development as it restarts the server on code changes).

Start the Frontend Development Server:
Open another new terminal, navigate to the frontend directory, and start the React development server:

cd E:\Projects\DataCraftAI\frontend
npm run dev

Access the Application:
Once both servers are running, open your web browser and go to the address displayed by the frontend server (usually http://localhost:5173/ or similar).

Project Structure
DataCraftAI/
├── backend/
│   ├── main.py                     # FastAPI application entry point
│   ├── ollama_handler.py           # Handles communication with Ollama and prompt engineering
│   ├── pbip_generator.py (or hyper_generator.py) # Logic for generating PBIP/Hyper files if applicable
│   ├── requirements.txt            # Python dependencies
│   ├── .venv_hyper/                # Python virtual environment (ignored by Git)
│   ├── __pycache__/                # Python cache files (ignored by Git)
│   ├── uploads/                    # Temporary storage for uploaded CSVs (ignored by Git)
│   └── output/                     # Generated CSVs/Hyper/PBIP files (ignored by Git)
├── frontend/
│   ├── public/                     # Static assets
│   ├── src/
│   │   ├── App.jsx                 # Main React component
│   │   ├── App.css                 # Global CSS for the app
│   │   ├── main.jsx (or index.jsx) # React entry point
│   │   └── components/
│   │       ├── About.jsx           # About page component (NEW)
│   │       ├── About.css           # Styling for the About page (NEW)
│   │       ├── Sidebar.jsx         # Sidebar navigation component
│   │       └── Sidebar.css         # Styling for the Sidebar
│   ├── index.html                  # HTML template for the React app
│   ├── package.json                # Frontend dependencies and scripts
│   ├── package-lock.json
│   ├── vite.config.js              # Vite configuration
│   └── node_modules/               # Frontend dependencies (ignored by Git)
├── .gitignore                      # Specifies files/folders to ignore in Git
├── README.md                       # This file
└── (other project-level files, e.g., license, docs)

Contributing
(Add information on how others can contribute to your project, e.g., fork the repository, create a new branch, make changes, submit a pull request.)

License
(Specify your project's license, e.g., MIT, Apache 2.0, etc.)

Contact
For questions or feedback, please contact [Your Name/Email/GitHub Profile Link]
