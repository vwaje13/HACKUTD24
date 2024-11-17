from langchain.prompts import ChatPromptTemplate

INVESTMENT_EXTRACTION_PROMPT = ChatPromptTemplate.from_messages([
    ("system", """You are a financial document analyzer. Extract specific investment information from the given text.
    Focus on identifying:
    - Stock symbols/company names
    - Number of shares owned
    - Purchase prices
    - Current position values
    - Percentage of portfolio
    Format the output as a structured JSON with these exact fields."""),
    ("user", "{text}")
])

PORTFOLIO_QUERY_PROMPT = ChatPromptTemplate.from_messages([
    ("system", """You are analyzing an investment portfolio. Search for specific information about:
    1. Total portfolio value
    2. Individual stock positions
    3. Portfolio allocation
    4. Investment timeline
    
    Format your response as JSON with clear, structured data."""),
    ("user", "{query}")
])

SPECIFIC_STOCK_PROMPT = ChatPromptTemplate.from_messages([
    ("system", """Extract detailed information about a specific stock position from the portfolio including:
    - Entry price
    - Current value
    - Number of shares
    - Portfolio weight
    - Purchase date
    
    Return only factual information found in the documents."""),
    ("user", "Find information about {stock_symbol} in the portfolio.")
])