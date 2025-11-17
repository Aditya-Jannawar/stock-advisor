from fastapi import APIRouter, Query
from app.database import SessionLocal
from app.models import StockAnalysis
from app.services.ai_engine import client  # you already have this Groq client

import json

router = APIRouter()

@router.get("/api/chat")
def chat_with_ai(query: str, ticker: str = Query(None)):
    """
    Chat with the AI about any analyzed stock.
    If ticker provided, include latest context from DB.
    """
    db = SessionLocal()
    context = ""

    if ticker:
        latest = db.query(StockAnalysis).filter(StockAnalysis.ticker == ticker).order_by(StockAnalysis.analyzed_at.desc()).first()
        if latest:
            context = f"""
            Latest analysis for {ticker}:
            Summary: {latest.summary}
            Risk: {latest.risk}
            Suggestion: {latest.suggestion}
            Predicted next-day price: ₹{latest.predicted_next_day_close}
            """

    prompt = f"""
    You are a helpful financial assistant AI.
    Use the following context if available:
    {context}

    User question: {query}

    Reply clearly and conversationally, giving reasoning and insights.
    """

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.5,
        max_tokens=400,
    )

    answer = response.choices[0].message.content.strip()
    return {"response": answer}
