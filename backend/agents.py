# agents.py

from openai import OpenAI
import requests
import json
from datetime import datetime
from typing import Dict, List, Optional
from flask import Flask, url_for, request

class StockAnalysisAgent:
    def __init__(self, serper_api_key: str, openai_api_key: str):
        self.serper_api_key = 'c20983719a234f567382ff9bbd1b9d6e6c933c97'
        self.client = OpenAI(
            api_key='dc4d7e8c-98c0-4dc6-b6c6-67879269d31f',
            base_url="https://api.sambanova.ai/v1",
        )
        
    def fetch_stock_price(self, ticker: str) -> Dict:
        """Fetch current stock price and change."""
        url = f"https://google.serper.dev/search"
        payload = json.dumps({
            "q": f"{ticker} stock price real time"
        })
        headers = {
            'X-API-KEY': self.serper_api_key,
            'Content-Type': 'application/json'
        }
        try:
            response = requests.post(url, headers=headers, data=payload)
            data = response.json()
            # Extract price from search results
            return {
                "price": 0.0,  # Replace with actual parsing
                "change": 0.0,
                "change_percent": 0.0
            }
        except Exception as e:
            print(f"Error fetching stock price: {e}")
            return {
                "price": 0.0,
                "change": 0.0,
                "change_percent": 0.0
            }

    def fetch_news_articles(self, ticker: str) -> List[Dict]:
        """Fetch news articles for a given stock."""
        url = "https://google.serper.dev/news"  
        payload = json.dumps({
            "q": f"{ticker} stock news",
            "num": 5
        })
        headers = {
            'X-API-KEY': self.serper_api_key,
            'Content-Type': 'application/json'
        }
        try:
            response = requests.post(url, headers=headers, data=payload)
            return response.json().get('news', [])
        except Exception as e:
            print(f"Error fetching news: {e}")
            return []

    def analyze_article_impact(self, ticker: str, article: Dict) -> Dict:
        """Analyze the impact of an article on the stock price."""
        try:
            prompt = f"""Analyze this article about {ticker} stock and determine its impact.
            
            Article Title: {article.get('title', '')}
            Source: {article.get('source', '')}
            Date: {article.get('date', '')}
            
            Provide the following in your analysis:
            1. Effect percentage (between -100 and 100)
            2. Whether this is a "Positive Effect" or "Negative Effect"
            3. Brief explanation of impact
            
            Format your response EXACTLY like this example:
            {{
                "effect_percentage": 45,
                "effect_type": "Negative Effect",
                "explanation": "Lawsuit over portion sizes could impact revenue"
            }}"""

            response = self.client.chat.completions.create(
                model='Meta-Llama-3.1-405B-Instruct',
                messages=[
                    {"role": "system", "content": "You are a financial analyst expert."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3
            )
            
            # Ensure the response is valid JSON
            try:
                return json.loads(response.choices[0].message.content.strip())
            except json.JSONDecodeError:
                # Fallback response if JSON parsing fails
                return {
                    "effect_percentage": 0,
                    "effect_type": "Neutral Effect",
                    "explanation": "Unable to determine impact"
                }
                
        except Exception as e:
            print(f"Error analyzing article impact: {e}")
            return {
                "effect_percentage": 0,
                "effect_type": "Neutral Effect",
                "explanation": "Analysis failed"
            }

    def get_stock_analysis(self, ticker: str) -> Dict:
        """Get comprehensive stock analysis including news and impact."""
        price_info = self.fetch_stock_price(ticker)
        articles = self.fetch_news_articles(ticker)
        
        analyzed_articles = []
        for article in articles[:5]:
            impact = self.analyze_article_impact(ticker, article)
            analyzed_articles.append({
                "source": article.get('source', ''),
                "title": article.get('title', ''),
                "time_ago": article.get('date', ''),
                "link": article.get('link', ''),
                "effect_percentage": impact['effect_percentage'],
                "effect_type": impact['effect_type'],
                "explanation": impact['explanation']
            })
        
        return {
            "ticker": ticker,
            "price": price_info['price'],
            "change": price_info['change'],
            "change_percent": price_info['change_percent'],
            "articles": analyzed_articles
        }