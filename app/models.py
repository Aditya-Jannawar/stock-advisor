from sqlalchemy import Column, Integer, String, Float, DateTime
from datetime import datetime
from app.database import Base
from sqlalchemy.sql import func


class StockResult(Base):
    __tablename__ = "stock_results"

    id = Column(Integer, primary_key=True, index=True)
    ticker = Column(String, index=True)
    # sector = Column(String, nullable=True)   # 🔹 Added for future use
    predicted_next_day_close = Column(Float)
    mae = Column(Float)
    r2_score = Column(Float)
    summary = Column(String)
    risk = Column(String)
    suggestion = Column(String)
    analyzed_at = Column(DateTime, default=datetime.utcnow)

class StockList(Base):
    __tablename__ = "stock_list"

    id = Column(Integer, primary_key=True, index=True)
    ticker = Column(String, unique=True, index=True)
    name = Column(String)
    sector = Column(String)

class StockAnalysis(Base):
    __tablename__ = "stock_analysis"

    id = Column(Integer, primary_key=True, index=True)
    ticker = Column(String, nullable=False)
    summary = Column(String)
    risk = Column(String)
    suggestion = Column(String)
    predicted_next_day_close = Column(Float)
    mae = Column(Float, nullable=True)
    r2_score = Column(Float, nullable=True)
    analyzed_at = Column(DateTime(timezone=True), server_default=func.now())