📈 Stock Advisor Backend

An end-to-end AI-powered stock analysis engine built using FastAPI, Machine Learning, and Groq LLM.
This backend powers the Stock Advisor Dashboard to fetch stock data, predict trends, and generate intelligent investment insights.

🚀 Features
🔹 1. Real-Time Stock Data

Fetches live & historical Indian stock data using Yahoo Finance (yfinance)

Cleans, prepares, and formats stock datasets

🔹 2. Machine Learning Prediction

Uses Linear Regression to predict next-day closing price

Trains on last N days of closing prices

Includes performance metrics (MAE, R²)

🔹 3. AI-Driven Financial Analysis

Uses Groq Llama-3 models

Generates:

📘 Trend Summary

⚠️ Risk Level (Low/Medium/High)

💰 Investment Suggestion (Buy / Hold / Sell)

Returns results strictly in JSON format

🔹 4. FastAPI Backend

Clean route structure

CORS enabled

Modular architecture (routes, services, database)

🧩 Tech Stack
Backend Framework

FastAPI

Uvicorn (ASGI server)

Machine Learning

Scikit-Learn

NumPy

Pandas

AI & LLM

Groq API (Llama-3 Models)

Database

SQLite (local development)

SQLAlchemy ORM

Other Tools

Python-Dotenv

YFinance

📁 Project Structure
backend/
│
├── app/
│   ├── main.py
│   ├── routes/
│   │   ├── stock_routes.py
│   ├── services/
│   │   ├── ai_engine.py
│   ├── database.py
│
├── .env               # API Keys (ignored from Git)
├── .gitignore
├── requirements.txt
└── README.md

⚙️ Environment Variables

Create a .env file in the backend/ folder:

GROQ_API_KEY=your_api_key_here


⚠️ Never commit .env to GitHub.

🛠️ Setup & Installation
1. Clone Repository
git clone https://github.com/Aditya-Jannawar/stock-advisor-backend.git
cd stock-advisor-backend

2. Create Virtual Environment
python -m venv venv

3. Activate Virtual Environment

Windows:

venv\Scripts\activate

4. Install Dependencies
pip install -r requirements.txt

5. Run FastAPI Server
uvicorn app.main:app --reload

🧪 Test API in Browser

Open:

👉 http://127.0.0.1:8000/docs

You’ll see interactive Swagger UI.

📊 Example API Output
{
  "ticker": "RELIANCE.NS",
  "predicted_next_day_close": 2578.44,
  "llm_summary": "The stock is showing a stable uptrend in the past 30 days...",
  "risk_level": "Medium",
  "suggestion": "Hold"
}

🧠 Future Enhancements

Add ARIMA/LSTM models for better prediction

Multi-stock portfolio analysis

Sentiment analysis using news APIs

Docker support + production deployment

Authentication + rate limiting

🤝 Contributing

Pull requests are welcome!
If you find a bug, feel free to open an issue.

❤️ Support This Project

If you like this project, ⭐ star the repository on GitHub.
It helps a lot!
