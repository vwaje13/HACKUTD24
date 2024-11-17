import logging
from typing import Dict, Any
from utils.model_wrappers.api_gateway import APIGateway
import config
from prompts import INVESTMENT_EXTRACTION_PROMPT, PORTFOLIO_QUERY_PROMPT, SPECIFIC_STOCK_PROMPT

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class InvestmentExtractor:
    def __init__(self):
        """Initialize the investment extractor with LLM"""
        self.llm = APIGateway.load_chat(
            type=config.LLM_CONFIG["api"],
            model=config.LLM_CONFIG["model"],
            temperature=config.LLM_CONFIG["temperature"],
            do_sample=config.LLM_CONFIG["do_sample"],
            max_tokens=config.LLM_CONFIG["max_tokens"]
        )

    def extract_investment_info(self, text: str) -> Dict[str, Any]:
        """Extract investment information from text using LLM"""
        try:
            logger.info("Extracting investment information")
            
            chain = INVESTMENT_EXTRACTION_PROMPT | self.llm
            response = chain.invoke({"text": text})
            
            return response
            
        except Exception as e:
            logger.error(f"Error extracting investment info: {str(e)}")
            raise

    def query_portfolio(self, query: str) -> Dict[str, Any]:
        """Query portfolio information"""
        try:
            logger.info(f"Querying portfolio: {query}")
            
            chain = PORTFOLIO_QUERY_PROMPT | self.llm
            response = chain.invoke({"query": query})
            
            return response
            
        except Exception as e:
            logger.error(f"Error querying portfolio: {str(e)}")
            raise

    def get_stock_details(self, stock_symbol: str) -> Dict[str, Any]:
        """Get detailed information about a specific stock"""
        try:
            logger.info(f"Getting details for stock: {stock_symbol}")
            
            chain = SPECIFIC_STOCK_PROMPT | self.llm
            response = chain.invoke({"stock_symbol": stock_symbol})
            
            return response
            
        except Exception as e:
            logger.error(f"Error getting stock details: {str(e)}")
            raise