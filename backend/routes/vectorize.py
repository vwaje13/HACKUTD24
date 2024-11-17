# vectorize.py

from flask import Blueprint, request, jsonify
import os
import tempfile
import threading
from typing import List, Dict

# Import necessary modules from SambaNova's code
from helpers.document_retrieval import DocumentRetrieval
from helpers.api_gateway import APIGateway

# Initialize the Blueprint
vectorize_bp = Blueprint('vectorize', __name__)

# Initialize the DocumentRetrieval instance
sambanova_api_key = os.environ.get('SAMBANOVA_API_KEY', '')
document_retrieval = DocumentRetrieval(sambanova_api_key=sambanova_api_key)

@vectorize_bp.route('/vectorize', methods=['POST'])
def vectorize_files():
    """
    Route to accept user files, vectorize the information,
    and extract stocks the user is invested in.
    """
    if 'files' not in request.files:
        return jsonify({'error': 'No files part in the request'}), 400

    files = request.files.getlist('files')

    # Create a temporary directory to save uploaded files
    with tempfile.TemporaryDirectory() as tmpdirname:
        file_paths = []
        for file in files:
            file_path = os.path.join(tmpdirname, file.filename)
            file.save(file_path)
            file_paths.append(file_path)

        # Process the files in a separate thread to avoid blocking
        result = []
        processing_thread = threading.Thread(target=process_files, args=(file_paths, result))
        processing_thread.start()
        processing_thread.join()

    # Return the list of stocks
    return jsonify({'stocks': result})

def process_files(file_paths: List[str], result: List):
    """
    Process the uploaded files to extract stocks.
    """
    # Parse the documents
    documents = []
    for file_path in file_paths:
        docs = document_retrieval.parse_doc(file_path)
        documents.extend(docs)

    # Load the embedding model
    embeddings = document_retrieval.load_embedding_model()

    # Create a temporary vector store with user data
    user_vectorstore = document_retrieval.create_vector_store(
        text_chunks=documents,
        embeddings=embeddings,
        output_db=None,  # Not persisting to disk
        collection_name='user_collection'
    )

    # Initialize the retriever with user_vectorstore
    document_retrieval.init_retriever(user_vectorstore)

    # Define the query to extract stocks
    query = "List all the stocks the user is invested in from the provided documents."

    # Get the QA chain
    qa_chain = document_retrieval.get_qa_retrieval_chain(conversational=False)

    # Generate the answer
    response = qa_chain({'question': query})

    # Extract the stocks from the response
    answer = response.get('answer', '')
    stocks = extract_stocks_from_answer(answer)

    # Append the stocks to the result list
    result.extend(stocks)

def extract_stocks_from_answer(answer: str) -> List[str]:
    """
    Extract stock symbols or names from the answer text.
    """
    # Simple placeholder extraction logic
    # In practice, use a more robust method or NLP techniques
    stocks = []

    # Example: Assume stocks are listed in the answer separated by commas
    if answer:
        stocks = [stock.strip() for stock in answer.split(',')]

    return stocks