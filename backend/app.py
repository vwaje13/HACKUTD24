from flask import Flask, request, jsonify
from flask_cors import CORS
from werkzeug.utils import secure_filename
import os
import logging
from documenthandler import DocumentHandler
from extraction import InvestmentExtractor

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize Flask app
app = Flask(__name__)
CORS(app)

# Configure upload settings
UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'uploads')
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)
VECTOR_DB_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'vectordb')
ALLOWED_EXTENSIONS = {'pdf'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

def init_directories():
    """Create necessary directories if they don't exist"""
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    os.makedirs(VECTOR_DB_FOLDER, exist_ok=True)

def allowed_file(filename: str) -> bool:
    """Check if file extension is allowed"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/api/upload', methods=['POST'])
def upload_file():
    """Handle document uploads and process them into the vector database"""
    if not request.files:
        return jsonify({'error': 'No files in the request'}), 400
    
    try:
        processed_files = []
        doc_handler = DocumentHandler()
        extractor = InvestmentExtractor()
        
        for key in request.files:
            file = request.files[key]
            if file.filename == '' or not allowed_file(file.filename):
                continue
                
            # Save and process file
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            
            # Debug logging
            logger.info(f"Saving file to: {filepath}")
            file.save(filepath)
            
            # Verify file exists
            if not os.path.exists(filepath):
                logger.error(f"File not saved successfully: {filepath}")
                return jsonify({'error': 'File upload failed'}), 500
            
            try:
                # Extract investment data and store in vector database
                documents = doc_handler.process_pdf(filepath)
                text_content = "\n".join([doc.page_content for doc in documents])
                investment_data = extractor.extract_investment_info(text_content)
                doc_handler.process_document(filepath, investment_data)
                processed_files.append(filename)
                
            except Exception as e:
                logger.error(f"Error processing file {filename}: {str(e)}")
                return jsonify({'error': f"Error processing file {filename}: {str(e)}"}), 500
            finally:
                # Clean up uploaded file
                if os.path.exists(filepath):
                    os.remove(filepath)
            
        return jsonify({
            'message': f'Successfully processed {len(processed_files)} files',
            'processed_files': processed_files
        }), 200
        
    except Exception as e:
        logger.error(f"Error processing files: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/portfolio', methods=['GET'])
def analyze_portfolio():
    """Retrieve and analyze all stocks from the vector database"""
    try:
        doc_handler = DocumentHandler()
        portfolio_data = doc_handler.get_all_investment_data()
        
        # Format the portfolio data
        formatted_portfolio = {
            'stocks': [
                {
                    'symbol': stock['symbol'],
                    'shares': stock['shares'],
                    'average_price': stock['average_price'],
                    'current_value': stock['current_value'],
                    'sector': stock['sector'],
                    'purchase_date': stock['purchase_date']
                }
                for stock in portfolio_data
            ],
            'total_value': sum(stock['current_value'] for stock in portfolio_data),
            'total_stocks': len(portfolio_data)
        }
        
        return jsonify(formatted_portfolio), 200
        
    except Exception as e:
        logger.error(f"Error analyzing portfolio: {str(e)}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    init_directories()
    app.run(debug=True)