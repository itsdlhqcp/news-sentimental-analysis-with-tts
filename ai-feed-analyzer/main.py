from fastapi import FastAPI
from fastapi.responses import FileResponse
import requests
import nltk
from nltk.sentiment import SentimentIntensityAnalyzer
from openai import OpenAI
from gtts import gTTS
import os
from pydantic import BaseModel

class TextRequest(BaseModel):
    text: str

nltk.download('vader_lexicon')

app = FastAPI()
sia = SentimentIntensityAnalyzer()

# API Keys
NEWS_API_KEY = "492910a2d3eb4024a0d2c79dda65d0a6"
OPENROUTER_API_KEY = "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"

# OpenRouter Client
client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=OPENROUTER_API_KEY
)

# Fetch News from NewsAPI
async def fetch_newsapi(company: str):
    url = f"https://newsapi.org/v2/everything?q={company}&sortBy=publishedAt&apiKey={NEWS_API_KEY}"
    response = requests.get(url)
    articles = response.json().get("articles", [])
    return articles[:6]  # Limit to 6 articles

# Fetch News from Local API
async def fetch_local_news(company: str):
    url = "http://localhost:3000/fetch-articles"
    try:
        response = requests.get(url, params={"company": company})
        response.raise_for_status()
        articles = response.json().get("articles", [])
        return articles[:4]
    except requests.RequestException as e:
        print(f"Error fetching local news: {e}")
        return []

# Fetch Combined News
@app.get("/news/{company}")
async def fetch_news(company: str):
    newsapi_articles = await fetch_newsapi(company)
    local_articles = await fetch_local_news(company)
    combined_articles = newsapi_articles + local_articles
    return {"Company": company, "Articles": combined_articles}

# Perform Sentiment Analysis
@app.post("/analyze_sentiment/")
async def analyze_sentiment(company: str):
    news_data = await fetch_news(company)
    articles = news_data["Articles"]

    results = []
    sentiment_counts = {"Positive": 0, "Negative": 0, "Neutral": 0}
    
    for article in articles:
        text = article.get("content") or article.get("description") or ""
        sentiment_score = sia.polarity_scores(text)
        sentiment = "Positive" if sentiment_score["compound"] > 0 else "Negative" if sentiment_score["compound"] < 0 else "Neutral"
        
        # Increment the sentiment count
        sentiment_counts[sentiment] += 1

        results.append({
            "Title": article.get("title"),
            "Summary": article.get("description"),
            "Sentiment": sentiment,
            "Topics": []  # Can be extracted using NLP topic modeling
        })
    
    # Determine the most frequent sentiment
    most_frequent_sentiment = max(sentiment_counts, key=sentiment_counts.get)
    
    # Create the comparative sentiment score
    comparative_sentiment = {
        "Comparative Sentiment Score": {
            "Sentiment Distribution": sentiment_counts
        }
    }
    
    # Add the final summary statement
    sentiment_summary = f"{company} latest news coverage is mostly {most_frequent_sentiment.lower()}"

    return {
        "Company": company, 
        "Articles": results,
        "SentimentSummary": sentiment_summary,
        "ComparativeSentiment": comparative_sentiment
    }

# Generate Report from Articles
@app.post("/generate_report/")
async def generate_report(company: str):
    news_data = await fetch_news(company)
    articles = news_data["Articles"]

    report = f"{company} के लिए समाचार रिपोर्ट:\n\n"
    
    sentiment_counts = {"सकारात्मक": 0, "नकारात्मक": 0, "तटस्थ": 0}
    english_sentiment_map = {"सकारात्मक": "Positive", "नकारात्मक": "Negative", "तटस्थ": "Neutral"}
    
    if not articles:
        report += "कोई समाचार नहीं मिला।"
    else:
        for idx, article in enumerate(articles, 1):
            text = article.get("content") or article.get("description") or ""
            sentiment_score = sia.polarity_scores(text)
            sentiment = "सकारात्मक" if sentiment_score["compound"] > 0 else "नकारात्मक" if sentiment_score["compound"] < 0 else "तटस्थ"
            
            # Increment the sentiment count
            sentiment_counts[sentiment] += 1
            
            report += f"{idx}. {article.get('title')}\n"
            report += f"   - सारांश: {article.get('description')}\n"
            report += f"   - भावना: {sentiment}\n\n"
    
    # Add sentiment summary to the report
    most_frequent_sentiment_hindi = max(sentiment_counts, key=sentiment_counts.get)
    most_frequent_sentiment_english = english_sentiment_map[most_frequent_sentiment_hindi]
    
    report += f"\nविश्लेषण परिणाम: {company} के नवीनतम समाचार कवरेज मुख्य रूप से {most_frequent_sentiment_hindi} हैं।\n"
    report += f"\nभावना वितरण:\n"
    report += f"- सकारात्मक: {sentiment_counts['सकारात्मक']}\n"
    report += f"- नकारात्मक: {sentiment_counts['नकारात्मक']}\n"
    report += f"- तटस्थ: {sentiment_counts['तटस्थ']}\n"

    comparative_sentiment = {
        "Comparative Sentiment Score": {
            "Sentiment Distribution": {
                "Positive": sentiment_counts["सकारात्मक"],
                "Negative": sentiment_counts["नकारात्मक"],
                "Neutral": sentiment_counts["तटस्थ"]
            }
        }
    }

    return {
        "report": report,
        "sentiment_summary": f"{company} latest news coverage is mostly {most_frequent_sentiment_english.lower()}",
        "comparative_sentiment": comparative_sentiment
    }

# Convert Report to Hindi Speech
@app.post("/tts/")
async def text_to_speech(request: TextRequest):
    try:
        filename = "report_hindi.mp3"
        
        # Generate TTS audio in Hindi
        tts = gTTS(request.text, lang="hi")
        tts.save(filename)

        # Ensure the file exists before returning
        if os.path.exists(filename):
            return FileResponse(filename, media_type="audio/mpeg", filename=filename)
        else:
            return {"error": "Failed to generate audio."}
    
    except Exception as e:
        return {"error": str(e)}