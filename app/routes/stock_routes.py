from fastapi import APIRouter, Depends
from app.services.ai_engine import analyze_stock
from app.database import SessionLocal
from app import models
from app.models import StockList


router = APIRouter()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/analyze/{ticker}")
def analyze_ticker(ticker: str, db=Depends(get_db)):
    """
    Analyze a stock and return ML + LLM insights.
    Also save the result to the database.
    """
    result = analyze_stock(ticker)

    stock = models.StockResult(
        ticker=ticker,
        predicted_next_day_close=result["predicted_next_day_close"],
        mae=result.get("mae", None),
        r2_score=result.get("r2_score", None),
        summary=result["llm_summary"],
        risk=result["risk_level"],
        suggestion=result["suggestion"],
    )
    db.add(stock)
    db.commit()
    db.refresh(stock)

    return {"status": "success", "data": result}

@router.get("/recent")
def get_recent_results(db=Depends(get_db)):
    """
    Get the latest 10 analyses from the database.
    Useful for showing previous predictions in frontend.
    """
    results = db.query(models.StockResult).order_by(models.StockResult.id.desc()).limit(10).all()
    return results




@router.get("/stocks")
def get_all_stocks(db=Depends(get_db)):
    """
    Get all available stock tickers (for dropdown in frontend)
    """
    stocks = db.query(StockList).all()
    return [{"ticker": s.ticker, "name": s.name, "sector": s.sector} for s in stocks]
