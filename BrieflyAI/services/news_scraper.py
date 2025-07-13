import asyncio
from typing import Dict, List

from aiolimiter import AsyncLimiter
from langchain_groq import ChatGroq
from tenacity import retry, stop_after_attempt, wait_exponential
from config import GROQ_API_KEY
from utils.scraping import (
    generate_news_urls_to_scrape,
    scrape_with_brightdata,
    clean_html_to_text,
    extract_headlines
)
from utils.summarization import (
    summarize_with_groq_structured
)
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from langchain_mcp_adapters.tools import load_mcp_tools

class NewsScraper:
    _rate_limiter = AsyncLimiter(5, 1)  # 5 requests/second

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=2, max=10)
    )
    async def scrape_news(self, topics: List[str]) -> Dict[str, str]:
        """Scrape and analyze news articles with structured summaries"""
        results = {}
        raw_headlines = {}  # Store raw headlines for debugging
        
        for topic in topics:
            async with self._rate_limiter:
                try:
                    # Generate news URLs for the topic
                    urls = generate_news_urls_to_scrape([topic])
                    
                    # Scrape the news page
                    search_html = scrape_with_brightdata(urls[topic])
                    clean_text = clean_html_to_text(search_html)
                    headlines = extract_headlines(clean_text)
                    
                    # Store raw headlines for potential debugging
                    raw_headlines[topic] = headlines
                    
                    # Generate structured summary using the updated function
                    if headlines.strip():
                        summary = summarize_with_groq_structured(
                            api_key=GROQ_API_KEY,
                            headlines=headlines
                        )
                        results[topic] = summary
                    else:
                        results[topic] = f"No headlines found for topic: {topic}"
                        
                except Exception as e:
                    print(f"Error scraping news for topic '{topic}': {str(e)}")
                    results[topic] = f"Error analyzing {topic}: {str(e)}"
                
                # Rate limiting to be respectful to news sites
                await asyncio.sleep(1)

        return {
            "news_analysis": results,
            "raw_headlines": raw_headlines,  # Include raw data for debugging
            "metadata": {
                "total_topics": len(topics),
                "successful_scrapes": len([r for r in results.values() if not r.startswith("Error")]),
                "scraping_method": "brightdata"
            }
        }

    @retry(
        stop=stop_after_attempt(2),
        wait=wait_exponential(multiplier=1, min=1, max=5)
    )
    async def scrape_single_topic(self, topic: str) -> Dict[str, str]:
        """Scrape a single topic for more focused analysis"""
        try:
            async with self._rate_limiter:
                urls = generate_news_urls_to_scrape([topic])
                search_html = scrape_with_brightdata(urls[topic])
                clean_text = clean_html_to_text(search_html)
                headlines = extract_headlines(clean_text)
                
                if headlines.strip():
                    summary = summarize_with_groq_structured(
                        api_key=GROQ_API_KEY,
                        headlines=headlines
                    )
                    return {
                        "topic": topic,
                        "summary": summary,
                        "raw_headlines": headlines,
                        "status": "success"
                    }
                else:
                    return {
                        "topic": topic,
                        "summary": f"No current news found for: {topic}",
                        "raw_headlines": "",
                        "status": "no_data"
                    }
                    
        except Exception as e:
            print(f"Error in single topic scrape for '{topic}': {str(e)}")
            return {
                "topic": topic,
                "summary": f"Error: {str(e)}",
                "raw_headlines": "",
                "status": "error"
            }

    async def get_news_health_check(self) -> Dict[str, str]:
        """Test if news scraping is working properly"""
        test_topic = "technology"
        try:
            result = await self.scrape_single_topic(test_topic)
            return {
                "status": "healthy" if result["status"] == "success" else "degraded",
                "test_topic": test_topic,
                "details": result["status"]
            }
        except Exception as e:
            return {
                "status": "unhealthy",
                "test_topic": test_topic,
                "details": str(e)
            }