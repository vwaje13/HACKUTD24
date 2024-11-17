# main.py

import os
from dotenv import load_dotenv
from agents import StockAnalysisAgent
from typing import List, Dict

class TradeTrends:
    def __init__(self):
        load_dotenv()
        self.agent = StockAnalysisAgent(
            serper_api_key=os.getenv('SERPER_API_KEY'),
            openai_api_key=os.getenv('OPENAI_API_KEY')
        )

    def analyze_portfolio(self, tickers: List[str]) -> Dict:
        """Analyze multiple stocks in a portfolio."""
        portfolio_analysis = {"stocks": []}
        
        for ticker in tickers:
            try:
                analysis = self.agent.get_stock_analysis(ticker)
                formatted_analysis = {
                    "symbol": ticker,
                    "price": analysis['price'],
                    "change": {
                        "value": analysis['change'],
                        "percentage": analysis['change_percent']
                    },
                    "news": []
                }
                
                for article in analysis['articles']:
                    formatted_article = {
                        "source": article['source'],
                        "title": article['title'],
                        "time": article['time_ago'],
                        "impact": {
                            "percentage": article['effect_percentage'],
                            "effect": article['effect_type'],
                            "description": article['explanation']
                        }
                    }
                    formatted_analysis["news"].append(formatted_article)
                
                portfolio_analysis["stocks"].append(formatted_analysis)
                
            except Exception as e:
                print(f"Error analyzing {ticker}: {e}")
                continue
            
        return portfolio_analysis

    def format_output(self, portfolio_analysis: Dict) -> None:
        """Format and print the analysis in TradeTrends style."""
        import json
        print(json.dumps(portfolio_analysis, indent=2))

def main():
    try:
        # Initialize TradeTrends
        app = TradeTrends()
        
        # Example portfolio
        portfolio = ["CMG", "NVDA"]
        
        # Get analysis
        analysis = app.analyze_portfolio(portfolio)
        
        # Display results
        app.format_output(analysis)
        
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()