import re

def decide_action(query: str):
    """
    Decide which tool to use based on user query.
    Returns tool name and extracted parameters.
    """
    query = query.lower()

    if "weather" in query:
        city = extract_city(query)
        return "weather_forecast", {"city": city} if city else {}
    
    if "usd" in query or "inr" in query or "dollar" in query or "rupee" in query:
        return "usd_to_inr", {}
    
    if "gold" in query:
        return "gold_price", {}
    
    # Default: send to LLM
    return "llm", {}

def extract_city(query: str) -> str:
    """
    Extract city name from query using regex.
    Example: "What is the weather in Paris?"
    """
    pattern = r"weather in ([a-zA-Z\s]+)"
    match = re.search(pattern, query, re.IGNORECASE)
    if match:
        return match.group(1).strip()
    return None
