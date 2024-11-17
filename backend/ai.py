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
        portfolio_analysis = {}
        
        for ticker in tickers:
            try:
                analysis = self.agent.get_stock_analysis(ticker)
                portfolio_analysis[ticker] = analysis
            except Exception as e:
                print(f"Error analyzing {ticker}: {e}")
                continue
            
        return portfolio_analysis

    def format_output(self, portfolio_analysis: Dict) -> None:
        """Format and print the analysis in TradeTrends style."""
        print("\n=== Briefing ===")
        
        for ticker, analysis in portfolio_analysis.items():
            print(f"\nStock: {ticker}")
            print(f"Price: ${analysis['price']:.2f}")
            print(f"Change: ${analysis['change']:.2f} ({analysis['change_percent']:.1f}%)")
            
            print("\nRecent News and Impact:")
            for article in analysis['articles']:
                print(f"\nSource: {article['source']}")
                print(f"Title: {article['title']}")
                print(f"Time: {article['time_ago']}")
                print(f"{article['effect_percentage']}% {article['effect_type']}")
                print(f"Impact: {article['explanation']}")

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