from flask import Flask, request, jsonify
from flask_cors import CORS
from werkzeug.utils import secure_filename
import os
import logging
import PyPDF2
import re
from typing import List, Dict, Any
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize Flask app
app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "http://localhost:3000"}})  # Update port if your React app uses a different one


# Configure upload settings
UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'uploads')
ALLOWED_EXTENSIONS = {'pdf'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Create uploads folder if it doesn't exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def allowed_file(filename: str) -> bool:
    """Check if file extension is allowed"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def extract_text_from_pdf(filepath: str) -> str:
    """Extract text content from PDF file"""
    try:
        with open(filepath, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            text = ''
            for page in reader.pages:
                text += page.extract_text() + '\n'
            return text
    except Exception as e:
        logger.error(f"Error extracting text from PDF: {str(e)}")
        raise

def extract_stock_info(text: str) -> List[Dict[str, Any]]:
    """
    Extract stock information using SambaNova API
    """
    try:
        # SambaNova API configuration
        url = os.getenv('SAMBANOVA_URL', 'https://api.sambanova.ai/v1/chat/completions')
        api_key = os.getenv('SAMBANOVA_API_KEY')
        
        if not api_key:
            raise ValueError("SAMBANOVA_API_KEY not found in environment variables")

        # Prepare the prompt
        prompt = f"""
        Extract all stock information from the following text. Look for:
        1. Stock symbols/tickers
        2. Company names
        3. Number of shares
        4. Share prices
        5. Purchase dates
        6. Any relevant financial metrics

        Format the response as a list of JSON objects, with each object containing:
        {{
            "symbol": "ticker symbol",
            "company_name": "company name",
            "shares": number of shares (if found),
            "price": price (if found),
            "date": "date" (if found),
            "metrics": "any additional metrics"
        }}

        Text content:
        {text}
        """

        # Make API request
        response = requests.post(
            url,
            headers={
                'Authorization': f'Bearer {api_key}',
                'Content-Type': 'application/json'
            },
            json={
                'model': 'Meta-Llama-3.1-70B-Instruct',
                'messages': [
                    {'role': 'system', 'content': 'You are a financial document analyzer.'},
                    {'role': 'user', 'content': prompt}
                ],
                'temperature': 0.0,
                'max_tokens': 1000
            }
        )

        if response.status_code != 200:
            raise Exception(f"API request failed: {response.text}")

        # Parse the response
        result = response.json()
        extracted_info = result['choices'][0]['message']['content']
        
        # Convert string response to JSON if necessary
        if isinstance(extracted_info, str):
            import json
            try:
                extracted_info = json.loads(extracted_info)
            except json.JSONDecodeError:
                logger.warning("Could not parse API response as JSON, returning raw text")
                return [{"raw_text": extracted_info}]

        return extracted_info

    except Exception as e:
        logger.error(f"Error extracting stock information: {str(e)}")
        return []

@app.route('/api/upload', methods=['POST'])
def upload_file():
    """Handle document uploads and extract stock information"""
    logger.info("Received upload request")  # Add this for debugging
    
    if not request.files:
        logger.error("No files in request")  # Add this for debugging
        return jsonify({'error': 'No files in the request'}), 400
    
    try:
        results = []
        
        logger.info(f"Files in request: {request.files}")  # Add this for debugging
        
        for key in request.files:
            file = request.files[key]
            if file.filename == '' or not allowed_file(file.filename):
                continue
                
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            
            logger.info(f"Processing file: {filename}")  # Add this for debugging
            
            try:
                file.save(filepath)
                logger.info(f"File saved to: {filepath}")  # Add this for debugging
                
                # Extract text from PDF
                text_content = extract_text_from_pdf(filepath)
                
                # Extract stock information
                stock_info = extract_stock_info(text_content)
                
                results.append({
                    'filename': filename,
                    'stocks': stock_info
                })
                
            except Exception as e:
                logger.error(f"Error processing file {filename}: {str(e)}")  # Add this for debugging
                return jsonify({'error': f"Error processing file {filename}: {str(e)}"}), 500
            finally:
                # Clean up uploaded file
                if os.path.exists(filepath):
                    os.remove(filepath)
        
        logger.info(f"Successfully processed {len(results)} files")  # Add this for debugging
        return jsonify({
            'message': f'Successfully processed {len(results)} files',
            'results': results
        }), 200
        
    except Exception as e:
        logger.error(f"Error processing files: {str(e)}")  # Add this for debugging
        return jsonify({'error': str(e)}), 500

@app.route('/api/portfolio', methods=['GET'])
def get_portfolio():
    """Get current portfolio analysis"""
    try:
        # You can modify this to return whatever portfolio data you need
        return jsonify({
            'stocks': [
                {
                    'symbol': 'AAPL',
                    'company_name': 'Apple Inc.',
                    'shares': 100,
                    'current_price': 150.23,
                    'total_value': 15023.00
                }
                # Add more stocks as needed
            ],
            'total_value': 15023.00,
            'total_stocks': 1
        }), 200
    except Exception as e:
        logger.error(f"Error retrieving portfolio: {str(e)}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)