from app.database import SessionLocal, engine, Base
from app.models import StockList

# Create tables if not exist
Base.metadata.create_all(bind=engine)
db = SessionLocal()

# Top Indian stocks (can expand later)
stocks = [
    {"ticker": "RELIANCE.NS", "name": "Reliance Industries", "sector": "Energy"},
    {"ticker": "TCS.NS", "name": "Tata Consultancy Services", "sector": "IT"},
    {"ticker": "INFY.NS", "name": "Infosys", "sector": "IT"},
    {"ticker": "HDFCBANK.NS", "name": "HDFC Bank", "sector": "Banking"},
    {"ticker": "ICICIBANK.NS", "name": "ICICI Bank", "sector": "Banking"},
    {"ticker": "SBIN.NS", "name": "State Bank of India", "sector": "Banking"},
    {"ticker": "BHARTIARTL.NS", "name": "Bharti Airtel", "sector": "Telecom"},
    {"ticker": "ASIANPAINT.NS", "name": "Asian Paints", "sector": "Consumer"},
    {"ticker": "ITC.NS", "name": "ITC Limited", "sector": "FMCG"},
    {"ticker": "LT.NS", "name": "Larsen & Toubro", "sector": "Infrastructure"},
]

for s in stocks:
    exists = db.query(StockList).filter_by(ticker=s["ticker"]).first()
    if not exists:
        db.add(StockList(**s))

db.commit()
db.close()
print("✅ Stock list seeded successfully!")
