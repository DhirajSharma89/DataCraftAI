DataCraft AI
DataCraft AI is an intelligent web application designed to empower users with self-service data preparation and visualization insights. It simplifies the often-complex process of transforming raw CSV data into a clean, analysis-ready format, and provides AI-driven suggestions for creating impactful visualizations in tools like Tableau.

✨ Features
CSV Data Upload: Securely upload your raw Comma Separated Values (CSV) datasets.

Natural Language Prompting: Describe your desired data transformations, aggregations, and analytical goals using intuitive natural language.

AI-Powered Data Transformation: Leverages Ollama (with the Mistral model) on the backend to interpret your prompts and generate precise Python (Pandas) scripts. These scripts perform operations like column selection, filtering, aggregation, and data cleaning.

Transformed CSV Download: Download the resulting clean and transformed CSV file, perfectly prepared for direct import into Tableau Desktop or other business intelligence tools.

Tableau Visualization Suggestions: Receive intelligent, AI-generated recommendations and notes on how to best visualize your newly processed data, tailored to your original prompt.

Local History Persistence: Your past interactions, including prompts, AI suggestions, and download links, are conveniently stored locally in your browser, allowing you to revisit previous sessions.

📸 Screenshots
Main Dashboard & Input/Output Flow
An overview of the DataCraft AI dashboard, showcasing the CSV upload and prompt input on the left, and the dynamically updated AI-generated output with the download option on the right.

Transformed Data in Spreadsheet
A glimpse of the AI-transformed CSV file opened in a spreadsheet application, demonstrating the precise data manipulation based on a user's prompt (e.g., specific columns and filtered data).

🛠️ Technologies Used
Frontend (React Application)
React: A JavaScript library for building user interfaces.

Axios: A promise-based HTTP client for making API requests.

CSS: For custom styling and responsive design.

Local Storage: Browser API used for client-side persistence of interaction history.

Backend (FastAPI Python API)
FastAPI: A modern, fast (high-performance) web framework for building APIs with Python 3.7+.

Ollama (Mistral): Serves as the Large Language Model (LLM) backend, interpreting natural language prompts and generating Python data transformation scripts and visualization insights.

Pandas: The foundational Python library for data manipulation and analysis, used to execute the AI-generated transformation scripts.

uuid: For generating universally unique identifiers for temporary file management.

shutil & os: Python's standard utility modules for high-level file operations and interacting with the operating system.

🚀 Getting Started
Follow these instructions to get a copy of DataCraft AI up and running on your local machine for development and testing purposes.

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

Backend Setup:
Navigate into the backend directory, create and activate a Python virtual environment, and install the necessary dependencies.

cd backend
python -m venv .venv_hyper # Create a virtual environment named .venv_hyper

# Activate the virtual environment:
# On Windows PowerShell:
.\.venv_hyper\Scripts\activate
# On Git Bash / Linux / macOS:
source ./.venv_hyper/bin/activate

pip install -r requirements.txt

Ensure your backend/requirements.txt file contains:

fastapi
uvicorn
python-multipart
ollama
pandas
# If you intend to work with Tableau Hyper API directly (e.g., for .hyper files):
# tableauhyperapi

(Note: tableauhyperapi is optional if your current focus is solely on CSV output, but good to include if .hyper generation is a future feature.)

Frontend Setup:
Navigate into the frontend directory and install the Node.js dependencies:

cd ../frontend # Go back to the DataCraftAI root, then into the frontend folder
npm install

Running the Application
Once both the backend and frontend dependencies are installed, you can start the application. You will need two separate terminal windows.

Start the Backend Server:
In your first terminal, navigate to the backend directory, activate your virtual environment, and start the FastAPI server:

cd E:\Projects\DataCraftAI\backend
.\.venv_hyper\Scripts\activate # For Windows PowerShell
# For Git Bash/Linux/macOS: source ./.venv_hyper/bin/activate

uvicorn main:app --reload

(The --reload flag is recommended during development as it automatically restarts the server when code changes are detected.)

Start the Frontend Development Server:
In your second terminal, navigate to the frontend directory and start the React development server:

cd E:\Projects\DataCraftAI\frontend
npm run dev

Access the Application:
After both servers are successfully running, open your web browser and go to the address displayed by the frontend server (typically http://localhost:5173/).

📂 Project Structure
DataCraftAI/
├── backend/
│   ├── main.py                     # FastAPI application entry point
│   ├── ollama_handler.py           # Handles communication with Ollama and prompt engineering
│   ├── pbip_generator.py (or hyper_generator.py) # Logic for generating PBIP/Hyper files (if implemented)
│   ├── requirements.txt            # Python dependencies list
│   ├── .venv_hyper/                # Python virtual environment (IGNORED by Git)
│   ├── __pycache__/                # Python compiled bytecode cache (IGNORED by Git)
│   ├── uploads/                    # Temporary storage for uploaded CSVs (IGNORED by Git)
│   └── output/                     # Directory for generated CSVs/other output (IGNORED by Git)
├── frontend/
│   ├── public/                     # Static assets (e.g., index.html, favicon)
│   ├── src/
│   │   ├── App.jsx                 # Main React application component
│   │   ├── App.css                 # Global styling for the main application layout
│   │   ├── main.jsx (or index.jsx) # React application entry point (e.g., ReactDOM.createRoot)
│   │   └── components/             # Reusable React components
│   │       ├── About.jsx           # Component for the 'About' page content
│   │       ├── About.css           # Styling for the 'About' page
│   │       ├── Sidebar.jsx         # Navigation sidebar component
│   │       └── Sidebar.css         # Styling for the sidebar
│   ├── index.html                  # Main HTML file for the React app
│   ├── package.json                # Frontend project metadata and dependencies
│   ├── package-lock.json           # Records exact dependency versions
│   ├── vite.config.js              # Configuration for Vite development server and build
│   └── node_modules/               # Installed JavaScript packages (IGNORED by Git)
├── .gitignore                      # Specifies intentionally untracked files/directories
├── README.md                       # This README file
└── (any other project-level documentation, license files, etc.)

🤝 Contributing
Contributions are welcome! If you have suggestions for improvements, new features, or bug fixes, please feel free to:

Fork the repository.

Create a new branch (git checkout -b feature/YourFeatureName).

Make your changes.

Commit your changes (git commit -m 'Add YourFeatureName').

Push to the branch (git push origin feature/YourFeatureName).

Open a Pull Request.

📄 License
This project is licensed under the MIT License - see the LICENSE file (if you create one) for details.

📧 Contact
For any questions or feedback, please reach out to Dhiraj Sharma:

GitHub: DhirajSharma89

(Optional: Add your Email, LinkedIn, etc.)
