# web scraping functions
import requests
import streamlit as st

# ScraperAPI Key
SCRAPERAPI_KEY = "df2cc6999b7e073dfc974034d1658c04"

def perform_scraperapi_search(query):
    """
    Performs a web search using ScraperAPI.
    
    Args:
        query (str): The search query.
        
    Returns:
        str: The HTML response as text or an error message.
    """
    url = "http://api.scraperapi.com"
    params = {
        "api_key": SCRAPERAPI_KEY,
        "url": f"https://www.google.com/search?q={query}"
    }
    try:
        response = requests.get(url, params=params)
        if response.status_code == 200:
            return response.text  # Return HTML content
        else:
            st.warning(f"ScraperAPI returned status code {response.status_code}")
            return None
    except Exception as e:
        st.warning(f"Error with ScraperAPI: {e}")
        return None
