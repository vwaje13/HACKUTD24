from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename
import os
import logging
from documenthandler import DocumentHandler
from extraction import InvestmentExtractor
from ai import TradeTrends
import config

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize Flask app
app = Flask(__name__)


# Configure upload settings
UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'uploads')
VECTOR_DB_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'vectordb')
ALLOWED_EXTENSIONS = {'pdf'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

def init_directories():
    """Create necessary directories if they don't exist"""
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    os.makedirs(VECTOR_DB_FOLDER, exist_ok=True)
    logger.info(f"Initialized directories: {UPLOAD_FOLDER}, {VECTOR_DB_FOLDER}")

def allowed_file(filename: str) -> bool:
    """Check if file extension is allowed"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

init_directories()

@app.route('/api/analyze_portfolio', methods=['POST'])
def analyze_portfolio():
    """Analyze portfolio of stocks"""
    # Validate input
    if not request.is_json:
        return jsonify({'error': 'Request must be JSON'}), 400
    
    tickers = request.json.get('tickers', [])
    if not tickers:
        return jsonify({'error': 'No stock tickers provided'}), 400
    
    try:
        # Initialize TradeTrends
        app = TradeTrends()
        portfolio_analysis = app.analyze_portfolio(tickers)
        app.format_output(portfolio_analysis)
        
        return jsonify(portfolio_analysis), 200
        
    except Exception as e:
        logger.error(f"Error analyzing portfolio: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/upload', methods=['POST'])
def upload_file():
    """Handle document upload and processing"""
    # Check if file was included in request
    if 'file' not in request.files:
        return jsonify({'error': 'No file part in the request'}), 400
    
    file = request.files['file']
    
    # Check if file was selected
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
    
    # Validate file type
    if not allowed_file(file.filename):
        return jsonify({'error': 'Invalid file type. Only PDF files are allowed'}), 400
    
    try:
        # Save file with secure filename
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        
        logger.info(f"Saving file to: {filepath}")
        file.save(filepath)
        
        # Process document
        doc_handler = DocumentHandler()
        extractor = InvestmentExtractor()
        
        # Extract text and get investment information
        documents = doc_handler.process_pdf(filepath)
        combined_text = "\n".join([doc.page_content for doc in documents])
        investment_data = extractor.extract_investment_info(combined_text)
        
        # Store in vector database
        doc_handler.process_document(filepath, investment_data)
        
        # Clean up uploaded file
        os.remove(filepath)
        
        return jsonify({
            'message': 'File processed successfully',
            'filename': filename,
            'investments': investment_data
        }), 200
        
    except Exception as e:
        logger.error(f"Error processing file: {str(e)}")
        # Clean up file if it exists
        if 'filepath' in locals() and os.path.exists(filepath):
            os.remove(filepath)
        return jsonify({'error': f'Error processing file: {str(e)}'}), 500

@app.route('/api/portfolio', methods=['GET'])
def get_portfolio():
    """Retrieve all portfolio information"""
    try:
        doc_handler = DocumentHandler()
        portfolio_data = doc_handler.get_all_investment_data()
        return jsonify({
            'portfolio': portfolio_data,
            'count': len(portfolio_data)
        }), 200
        
    except Exception as e:
        logger.error(f"Error retrieving portfolio: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/stock/<symbol>', methods=['GET'])
def get_stock_info(symbol):
    """Get information about a specific stock"""
    try:
        extractor = InvestmentExtractor()
        stock_data = extractor.get_stock_details(symbol)
        return jsonify({
            'symbol': symbol,
            'stock_data': stock_data
        }), 200
        
    except Exception as e:
        logger.error(f"Error retrieving stock info: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/search', methods=['POST'])
def search_portfolio():
    """Search portfolio with specific query"""
    # Validate input
    if not request.is_json:
        return jsonify({'error': 'Request must be JSON'}), 400
    
    query = request.json.get('query', '')
    if not query:
        return jsonify({'error': 'No search query provided'}), 400
    
    try:
        doc_handler = DocumentHandler()
        extractor = InvestmentExtractor()
        
        # Search documents
        search_results = doc_handler.search_documents(query)
        
        # Extract relevant information
        portfolio_info = extractor.query_portfolio(query)
        
        return jsonify({
            'query': query,
            'search_results': search_results,
            'portfolio_info': portfolio_info
        }), 200
        
    except Exception as e:
        logger.error(f"Error searching portfolio: {str(e)}")
        return jsonify({'error': str(e)}), 500



if __name__ == '__main__':
    # Initialize directories
    init_directories()
    
    # Run Flask app
    app.run(debug=True)