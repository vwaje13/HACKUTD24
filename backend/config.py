import os
from dotenv import load_dotenv

load_dotenv()

# API Configuration
SAMBANOVA_API_KEY = os.getenv('SAMBANOVA_API_KEY')

# Vector Database Configuration
VECTOR_DB_PATH = "vectordb"
COLLECTION_NAME = "investment_documents"

# Document Processing Configuration
CHUNK_SIZE = 1000
CHUNK_OVERLAP = 200

# LLM Configuration
LLM_CONFIG = {
    "api": "sncloud",
    "temperature": 0.0,
    "do_sample": False,
    "max_tokens": 1200,
    "model": "Meta-Llama-3.1-70B-Instruct"
}

# Embedding Configuration
EMBEDDING_CONFIG = {
    "type": "cpu",
    "batch_size": 1,
    "coe": True,
    "select_expert": "e5-mistral-7b-instruct"
}

# File Storage
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'pdf'}