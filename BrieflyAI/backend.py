from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from datetime import datetime
from models import NewsRequest
from services.news_scraper import NewsScraper
from services.reddit_scraper import scrape_reddit_topics
from utils.summarization import generate_structured_news_summary, summarize_with_groq_structured
from config import GROQ_API_KEY

app = FastAPI(title="NewsNinja API", description="News and Reddit Analysis API")

@app.get("/")
async def root():
    return {"message": "NewsNinja API is running!", "version": "2.0", "features": ["news_analysis", "reddit_analysis", "structured_summaries"]}


@app.get("/health")
async def health_check():
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}


@app.post("/generate-news-summary")
async def generate_news_summary(request: NewsRequest):
    """
    Generate a comprehensive structured news summary for UI display
    """
    try:
        # Initialize results storage
        results = {}
        raw_data = {}
        
        # Scrape news sources if requested
        if request.source_type in ["news", "both"]:
            try:
                news_scraper = NewsScraper()
                news_results = await news_scraper.scrape_news(request.topics)
                results["news"] = news_results
                raw_data["news"] = news_results
            except Exception as e:
                print(f"News scraping error: {e}")
                results["news"] = {}

        # Scrape Reddit sources if requested
        if request.source_type in ["reddit", "both"]:
            try:
                reddit_results = await scrape_reddit_topics(request.topics)
                results["reddit"] = reddit_results
                raw_data["reddit"] = reddit_results
            except Exception as e:
                print(f"Reddit scraping error: {e}")
                results["reddit"] = {}

        # Check if we have any data to work with
        news_data = results.get("news", {})
        reddit_data = results.get("reddit", {})
        
        if not news_data and not reddit_data:
            raise HTTPException(
                status_code=404, 
                detail="No data could be retrieved for the specified topics and sources"
            )

        # Generate comprehensive structured summary
        try:
            main_summary = generate_structured_news_summary(
                api_key=GROQ_API_KEY,
                news_data=news_data,
                reddit_data=reddit_data,
                topics=request.topics
            )
        except Exception as e:
            print(f"Summary generation error: {e}")
            main_summary = "Summary generation failed. Please check the logs for more details."

        # Generate individual topic analyses
        individual_analyses = {}
        for topic in request.topics:
            try:
                # Collect data for this specific topic
                topic_news = news_data.get("news_analysis", {}).get(topic, "") if news_data else ""
                topic_reddit = reddit_data.get("reddit_analysis", {}).get(topic, "") if reddit_data else ""
                
                if topic_news or topic_reddit:
                    # Create focused analysis for this topic
                    topic_content = f"Topic: {topic}\n\n"
                    if topic_news:
                        topic_content += f"News Analysis:\n{topic_news}\n\n"
                    if topic_reddit:
                        topic_content += f"Reddit Analysis:\n{topic_reddit}\n\n"
                    
                    # Generate structured analysis for this topic
                    topic_analysis = summarize_with_groq_structured(
                        api_key=GROQ_API_KEY,
                        headlines=topic_content
                    )
                    individual_analyses[topic] = topic_analysis
                else:
                    individual_analyses[topic] = f"No data available for topic: {topic}"
                    
            except Exception as e:
                print(f"Individual topic analysis error for {topic}: {e}")
                individual_analyses[topic] = f"Analysis failed for topic: {topic}"

        # Prepare response data
        response_data = {
            "topics": request.topics,
            "source_type": request.source_type,
            "timestamp": datetime.now().isoformat(),
            "summary": main_summary,
            "individual_topics": individual_analyses,
            "raw_data": raw_data,
            "metadata": {
                "total_topics": len(request.topics),
                "sources_used": request.source_type,
                "has_news_data": bool(news_data),
                "has_reddit_data": bool(reddit_data),
                "analysis_generated": True
            }
        }

        return JSONResponse(content=response_data)

    except HTTPException:
        raise
    except Exception as e:
        print(f"Unexpected error in generate_news_summary: {e}")
        raise HTTPException(
            status_code=500, 
            detail=f"Internal server error: {str(e)}"
        )


@app.post("/quick-summary")
async def quick_summary(request: NewsRequest):
    """
    Generate a quick summary without individual topic breakdown
    """
    try:
        results = {}
        
        # Scrape sources based on request
        if request.source_type in ["news", "both"]:
            news_scraper = NewsScraper()
            results["news"] = await news_scraper.scrape_news(request.topics)
        
        if request.source_type in ["reddit", "both"]:
            results["reddit"] = await scrape_reddit_topics(request.topics)

        # Generate quick summary
        news_data = results.get("news", {})
        reddit_data = results.get("reddit", {})
        
        summary = generate_structured_news_summary(
            api_key=GROQ_API_KEY,
            news_data=news_data,
            reddit_data=reddit_data,
            topics=request.topics
        )

        return {
            "topics": request.topics,
            "source_type": request.source_type,
            "timestamp": datetime.now().isoformat(),
            "summary": summary
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "backend:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )