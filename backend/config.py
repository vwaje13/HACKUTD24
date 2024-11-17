import os
from dotenv import load_dotenv

load_dotenv()

# Vector Database Configuration
VECTOR_DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'vectordb')
UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'uploads')

# Document Processing Configuration
MAX_CHARACTERS = 2000
NEW_AFTER_N_CHARS = 1500
COMBINE_TEXT_UNDER_N_CHARS = 500
K_RETRIEVED_DOCUMENTS = 5

# LLM Configuration
LLM_CONFIG = {
    "type": "sncloud",
    "model": "Meta-Llama-3.1-70B-Instruct",
    "coe": False,
    "do_sample": False,
    "max_tokens_to_generate": 1200,
    "temperature": 0.0,
    "select_expert": None,
    "streaming": True
}

# Embedding Configuration
EMBEDDING_CONFIG = {
    "type": "cpu",
    "batch_size": 1,
    "coe": True,
    "select_expert": "e5-mistral-7b-instruct"
}

ALLOWED_EXTENSIONS = {'pdf'}