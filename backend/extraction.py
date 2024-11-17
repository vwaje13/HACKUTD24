import logging
from typing import Dict, Any, List
from utils.model_wrappers.api_gateway import APIGateway
import config
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate

logger = logging.getLogger(__name__)

class InvestmentExtractor:
    def __init__(self):
        """Initialize the investment extractor with LLM"""
        self.llm = APIGateway.load_chat(
            type=config.LLM_CONFIG["type"],
            model=config.LLM_CONFIG.get("model", "Meta-Llama-3.1-70B-Instruct"),
            streaming=True,
            # coe=config.LLM_CONFIG["coe"],
            do_sample=config.LLM_CONFIG["do_sample"],
            max_tokens=config.LLM_CONFIG["max_tokens_to_generate"],  # Note: changed from max_tokens_to_generate
            temperature=config.LLM_CONFIG["temperature"],
            # select_expert=config.LLM_CONFIG["select_expert"]
        )

    def extract_investment_info(self, text: str) -> Dict[str, Any]:
        """Extract investment information from text"""
        try:
            logger.info("Extracting investment information")
            
            prompt = ChatPromptTemplate.from_template("""
                Analyze the following text and extract all investment-related information.
                Focus on:
                - Stock symbols and company names
                - Number of shares
                - Purchase prices and dates
                - Current values
                - Portfolio percentages
                
                Text: {text}
                
                Format the output as a structured JSON.
            """)
            
            chain = prompt | self.llm | StrOutputParser()
            response = chain.invoke({"text": text})
            
            return response
            
        except Exception as e:
            logger.error(f"Error extracting investment info: {str(e)}")
            raise

    def get_stock_details(self, symbol: str) -> Dict[str, Any]:
        """Get detailed information about a specific stock"""
        try:
            logger.info(f"Getting details for stock: {symbol}")
            
            prompt = ChatPromptTemplate.from_template("""
                Extract all information about {symbol} stock from the documents.
                Include:
                - Entry price and date
                - Number of shares
                - Current value
                - Portfolio percentage
                - Any relevant news or analysis
                
                Return only factual information as JSON.
            """)
            
            chain = prompt | self.llm | StrOutputParser()
            response = chain.invoke({"symbol": symbol})
            
            return response
            
        except Exception as e:
            logger.error(f"Error getting stock details: {str(e)}")
            raise

    def query_portfolio(self, query: str) -> List[Dict[str, Any]]:
        """Search portfolio with specific query"""
        try:
            logger.info(f"Querying portfolio: {query}")
            
            prompt = ChatPromptTemplate.from_template("""
                Based on the following query, analyze the investment portfolio:
                {query}
                
                Provide:
                1. Direct answer to the query
                2. Relevant portfolio statistics
                3. Any related investment insights
                
                Format as JSON with clear data structure.
            """)
            
            chain = prompt | self.llm | StrOutputParser()
            response = chain.invoke({"query": query})
            
            return response
            
        except Exception as e:
            logger.error(f"Error querying portfolio: {str(e)}")
            raise