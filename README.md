# 📈 Stock Advisor Project

An AI-powered stock analysis dashboard built using **FastAPI**, **Groq LLM**, and **Tailwind CSS**.

### Features
- Real-time and historical Indian stock data via Yahoo Finance
- Linear Regression–based price prediction
- LLM-driven risk & suggestion analysis (Buy/Hold/Sell)
- Beautiful Tailwind dashboard with chart visualization

### Tech Stack
- **Backend:** FastAPI, SQLite, SQLAlchemy
- **AI Engine:** Groq (Llama 3)
- **Frontend:** Tailwind CSS + Chart.js

### Run Locally
```bash
uvicorn app.main:app --reload
python -m http.server 5500