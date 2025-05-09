import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Groq API configurations
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_MODEL = "llama3-70b-8192"  # You can change this

# Project paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")
MODELS_DIR = os.path.join(BASE_DIR, "models")

# Ensure directories exist
os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(MODELS_DIR, exist_ok=True)

# Dataset configurations
DATASET_NAME = "codeparrot/github-code"
LANGUAGES = ["python", "javascript", "java"]
MAX_SAMPLES = 10000