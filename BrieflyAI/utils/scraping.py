from urllib.parse import quote_plus
from dotenv import load_dotenv
import requests
from fastapi import FastAPI, HTTPException
from bs4 import BeautifulSoup
from datetime import datetime
from config import BRIGHTDATA_API_KEY, WEB_UNLOCKER_ZONE
class MCPOverloadedError(Exception):
    """Custom exception for MCP service overloads"""
    pass


def generate_valid_news_url(keyword: str) -> str:
    """
    Generate a Google News search URL for a keyword with optional sorting by latest
    
    Args:
        keyword: Search term to use in the news search
        
    Returns:
        str: Constructed Google News search URL
    """
    q = quote_plus(keyword)
    return f"https://news.google.com/search?q={q}&tbs=sbd:1"


def generate_news_urls_to_scrape(list_of_keywords):
    valid_urls_dict = {}
    for keyword in list_of_keywords:
        valid_urls_dict[keyword] = generate_valid_news_url(keyword)
    
    return valid_urls_dict


def scrape_with_brightdata(url: str) -> str:
    """Scrape a URL using BrightData with improved error handling"""
    
    # Validate environment variables
    api_key = BRIGHTDATA_API_KEY
    zone = WEB_UNLOCKER_ZONE
    
    if not api_key:
        raise ValueError("BRIGHTDATA_API_KEY environment variable is not set")
    if not zone:
        raise ValueError("BRIGHTDATA_WEB_UNLOCKER_ZONE environment variable is not set")
    
    # Validate URL
    if not url or not url.startswith(('http://', 'https://')):
        raise ValueError("Invalid URL provided")
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    # Updated payload based on BrightData API documentation
    payload = {
        "zone": zone,
        "url": url,
        "format": "raw",
        "country": "US",  # Add country if required
        "render": False   # Set to True if you need JavaScript rendering
    }
    
    try:
        print(f"Attempting to scrape: {url}")
        print(f"Using zone: {zone}")
        
        response = requests.post(
            "https://api.brightdata.com/request", 
            json=payload, 
            headers=headers,
            timeout=30  # Add timeout
        )
        
        # Log response details for debugging
        print(f"Response status: {response.status_code}")
        print(f"Response headers: {dict(response.headers)}")
        
        if response.status_code == 400:
            # Try to get more specific error details
            try:
                error_detail = response.json()
                print(f"BrightData error details: {error_detail}")
                raise HTTPException(
                    status_code=500, 
                    detail=f"BrightData API error: {error_detail.get('message', 'Bad Request')}"
                )
            except:
                print(f"Response text: {response.text}")
                raise HTTPException(
                    status_code=500, 
                    detail=f"BrightData API error: 400 Bad Request - {response.text}"
                )
        
        response.raise_for_status()
        return response.text
        
    except requests.exceptions.RequestException as e:
        print(f"Request exception: {str(e)}")
        raise HTTPException(status_code=500, detail=f"BrightData error: {str(e)}")


def clean_html_to_text(html_content: str) -> str:
    """Clean HTML content to plain text"""
    soup = BeautifulSoup(html_content, "html.parser")
    text = soup.get_text(separator="\n")
    return text.strip()


def extract_headlines(cleaned_text: str) -> str:
    """
    Extract and concatenate headlines from cleaned news text content.
    
    Args:
        cleaned_text: Raw text from news page after HTML cleaning
        
    Returns:
        str: Combined headlines separated by newlines
    """
    headlines = []
    current_block = []
    
    # Split text into lines and remove empty lines
    lines = [line.strip() for line in cleaned_text.split('\n') if line.strip()]
    
    # Process lines to find headline blocks
    for line in lines:
        if line == "More":
            if current_block:
                # First line of block is headline
                headlines.append(current_block[0])
                current_block = []
        else:
            current_block.append(line)
    
    # Add any remaining block at end of text
    if current_block:
        headlines.append(current_block[0])
    
    return "\n".join(headlines)