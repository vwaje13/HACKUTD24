# documenthandler.py
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
import os
import re

class DocumentHandler:
    def __init__(self):
        self.embeddings = HuggingFaceEmbeddings(
            model_name="all-MiniLM-L6-v2",
            model_kwargs={'device': 'cpu'}
        )
        self.vector_store = None
        
    def process_pdf(self, file_path):
        """Process PDF file and return documents"""
        loader = PyPDFLoader(file_path)
        return loader.load()
        
    def process_document(self, file_path, metadata=None):
        """Process document and store in vector database"""
        documents = self.process_pdf(file_path)
        
        if metadata:
            for doc in documents:
                doc.metadata.update(metadata)
        
        if self.vector_store is None:
            self.vector_store = FAISS.from_documents(documents, self.embeddings)
        else:
            self.vector_store.add_documents(documents)
            
        return len(documents)
    
    def search_documents(self, query, k=5):
        """Search documents with a query"""
        if self.vector_store is None:
            return []
            
        results = self.vector_store.similarity_search(query, k=k)
        return [{"content": doc.page_content, "metadata": doc.metadata} for doc in results]
    
    def get_all_investment_data(self):
        """Retrieve all stored investment data"""
        if self.vector_store is None:
            return []
            
        return self.search_documents("investment", k=100)

# extraction.py
class InvestmentExtractor:
    def __init__(self):
        self.investment_patterns = {
            'stock_symbol': r'\b[A-Z]{1,5}\b',  # Basic pattern for stock symbols
            'amount': r'\$\d+(?:,\d{3})*(?:\.\d{2})?',  # Currency amounts
            'percentage': r'\d+(?:\.\d+)?%'  # Percentage values
        }
    
    def extract_investment_info(self, text):
        """Extract investment information from text"""
        investment_data = {
            'symbols': self._extract_pattern(text, self.investment_patterns['stock_symbol']),
            'amounts': self._extract_pattern(text, self.investment_patterns['amount']),
            'percentages': self._extract_pattern(text, self.investment_patterns['percentage'])
        }
        
        return investment_data
    
    def _extract_pattern(self, text, pattern):
        """Helper method to extract patterns from text"""
        matches = re.findall(pattern, text)
        return list(set(matches))  # Remove duplicates
    
    def get_stock_details(self, symbol):
        """Get information about a specific stock symbol"""
        # This is a placeholder - you might want to integrate with a real stock API
        return {
            'symbol': symbol,
            'found_in_documents': True if symbol in self.portfolio_data else False
        }
    
    def query_portfolio(self, query):
        """Search portfolio with specific query"""
        # Implement your specific search logic here
        results = []
        
        # Add your search implementation
        return results