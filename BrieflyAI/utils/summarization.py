from langchain_groq import ChatGroq
from langchain_core.messages import SystemMessage, HumanMessage
from fastapi import HTTPException
from config import GROQ_API_KEY, LLAMA_70b_model, TEMPERATURE, MAX_TOKEN_1, MAX_TOKEN_2


def generate_structured_news_summary(api_key, news_data, reddit_data, topics):
    """Generate a structured news summary for UI display using GROQ"""
    system_prompt = """
    You are a professional news analyst. Create a well-structured, comprehensive summary for web display.

    For each topic, organize the information as follows:
    1. **Topic Overview**: Brief context and importance
    2. **Key Developments**: Main news points if available
    3. **Public Sentiment**: Reddit discussions and reactions if available
    4. **Impact & Analysis**: What this means and potential implications

    Formatting guidelines:
    - Use clear headings and subheadings
    - Present information in digestible bullet points
    - Include relevant quotes when available
    - Maintain neutral, professional tone
    - Focus on factual accuracy and clarity
    - Make each section informative but concise

    Structure each topic clearly with proper headings and organize information logically.
    """

    try:
        topic_blocks = []
        for topic in topics:
            news_content = news_data.get("news_analysis", {}).get(topic, '') if news_data else ''
            reddit_content = reddit_data.get("reddit_analysis", {}).get(topic, '') if reddit_data else ''
            
            context = []
            if news_content:
                context.append(f"NEWS SOURCES:\n{news_content}")
            if reddit_content:
                context.append(f"REDDIT DISCUSSIONS:\n{reddit_content}")
            
            if context:  # Only include topics with actual content
                topic_blocks.append(
                    f"TOPIC: {topic}\n\n" +
                    "\n\n".join(context)
                )

        user_prompt = (
            "Create a comprehensive structured summary for these topics using available sources:\n\n" +
            "\n\n--- NEXT TOPIC ---\n\n".join(topic_blocks) +
            "\n\nPlease format this as a well-structured report suitable for web display with clear headings, bullet points, and organized sections."
        )

        llm = ChatGroq(
            model=LLAMA_70b_model,
            api_key=api_key,
            temperature=TEMPERATURE,
            max_tokens=MAX_TOKEN_2,
        )

        response = llm.invoke([
            SystemMessage(content=system_prompt),
            HumanMessage(content=user_prompt)
        ])

        return response.content

    except Exception as e:
        raise e


def summarize_with_groq_structured(api_key: str, headlines: str) -> str:
    """
    Summarize headlines into a structured format for UI display using GROQ.
    """
    system_prompt = """
    You are a professional news analyst creating structured summaries for web display.

    Transform the provided headlines into a well-organized, comprehensive summary with:

    1. **Executive Summary**: Brief overview of the main themes
    2. **Key Stories**: Major headlines with detailed explanations
    3. **Analysis**: What these stories mean and their significance
    4. **Trends**: Patterns or connections between different stories

    Format guidelines:
    - Use clear markdown headings (##, ###)
    - Present key points as bullet points
    - Include specific details and context
    - Maintain professional, informative tone
    - Focus on clarity and readability
    - Make it comprehensive but digestible

    Create a structured report that would be suitable for display on a news dashboard or summary page.
    """

    try:
        llm = ChatGroq(
            model=LLAMA_70b_model,
            api_key=api_key,
            temperature=TEMPERATURE,
            max_tokens=MAX_TOKEN_1
        )

        response = llm.invoke([
            SystemMessage(content=system_prompt),
            HumanMessage(content=f"Headlines to analyze:\n\n{headlines}")
        ])

        return response.content
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"GROQ error: {str(e)}")