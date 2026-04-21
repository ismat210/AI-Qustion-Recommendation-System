"AI-Qustion-Recommendation-System"

# Download the project

First, download the repository from GitHub as a ZIP file and extract it on your local machine. Then open the extracted folder in a terminal or a code editor like VS Code.

# Create a virtual environment

Create an isolated Python environment to manage dependencies.
python -m venv .venv

Activate it:

Windows -- .venv\Scripts\activate
Mac/Linux -- source .venv/bin/activate

# Install dependencies

Since this project already contains a uv.lock file, install dependencies using: 
uv sync

# Run the backend (FastAPI)

Start the backend server first:

uvicorn backend.app.main:app --reload

# Run the frontend (Streamlit)
Open a new terminal and run:

streamlit run frontend/streamlit_app.py

#  Use the system

After both services are running:

Upload a PDF / DOCX / Image file
Process the file to extract questions
Store data in database automatically
Enter a question in the recommendation box
Get similar AI-generated questions