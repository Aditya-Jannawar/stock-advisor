import pandas as pd
import yfinance as yf
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, r2_score
from groq import Groq
import os, json
# from dotenv import load_dotenv


# Load environment variables
# load_dotenv()

# ✅ Initialize Groq client
os.environ["GROQ_API_KEY"] = "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"
client = Groq(api_key=os.environ["GROQ_API_KEY"])

# --------- ML Functions ----------
def prepare_ml_data(df, window_size=5):
    """
    Create feature windows and targets for next-day price prediction.
    """
    # Ensure close_prices is a 1D array, as df['Close'].values can sometimes return (N, 1)
    # if the column itself was selected as a DataFrame or from a MultiIndex structure.
    close_prices = df['Close'].values.ravel()
    X, y = [], []
    for i in range(window_size, len(close_prices)):
        X.append(close_prices[i-window_size:i])
        y.append(close_prices[i])
    return np.array(X), np.array(y)

def train_predict_model(df):
    X, y = prepare_ml_data(df)
    
    # Split into training (80%) and testing (20%)
    split_idx = int(0.8 * len(X))
    X_train, X_test = X[:split_idx], X[split_idx:]
    y_train, y_test = y[:split_idx], y[split_idx:]
    
    # Train model
    model = LinearRegression()
    model.fit(X_train, y_train)
    
    # Predict
    y_pred = model.predict(X_test)
    
    # Evaluate
    mae = mean_absolute_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)
    # print(f"📈 MAE: {mae:.2f}, R²: {r2:.3f}")
    
    # Predict next day's price using last 5 days
    next_input = df['Close'].values[-5:].reshape(1, -1)
    next_pred = model.predict(next_input)[0]
    
    return y_test, y_pred, next_pred


# --------- LLM Functions ----------
def build_prompt(ticker, df):
    recent = df.tail(30)[['Date', 'Close']].copy()

    # More robust way to format dates and closes, avoiding iterrows() quirks
    formatted_dates = recent['Date'].dt.strftime('%d-%b-%Y')
    formatted_closes = recent['Close'].apply(lambda x: f'₹{x:.2f}')

    data_summary = "\n".join([
        f"{date_str}: {close_str}"
        for date_str, close_str in zip(formatted_dates, formatted_closes)
    ])

    prompt = f"""
You Are a financial analyst AI. Analyze the following 30-day stock closing prices for {ticker}.

Data:
{data_summary}

Please respond strictly in JSON with keys:
"summary" → 2-3 sentence overview of trend,
"risk" → Low / Medium / High,
"suggestion" → Buy / Hold / Sell.

Example format:
{{
  "summary": "...",
  "risk": "Medium",
  "suggestion": "Hold"
}}
    """
    return prompt.strip()

def analyze_with_llm(ticker, df):
    prompt = build_prompt(ticker, df)

    # Use the correct, currently supported model
    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3,
        max_tokens=300,
    )

    raw = response.choices[0].message.content.strip()
    print("Raw LLM Response:\n", raw)

    # Try to parse JSON output safely
    try:
        parsed = json.loads(raw)
    except json.JSONDecodeError:
        parsed = {"summary": raw, "risk": "Unknown", "suggestion": "Hold"}

    return parsed

# --------- Main Function ----------
def analyze_stock(ticker="RELIANCE.NS", start="2022-01-01", end="2023-01-01"):
    # 1️⃣ Fetch stock data
    stock_data = yf.Ticker(ticker)
    df = stock_data.history(start=start, end=end, auto_adjust=False)
    df.reset_index(inplace=True)

    if isinstance(df.columns, pd.MultiIndex):
        df.columns = df.columns.get_level_values(-1)
    df = df[['Date', 'Close']].copy()
    df['Date'] = pd.to_datetime(df['Date'])

    # 2️⃣ Run ML Predictor
    _, _, next_price = train_predict_model(df)

    # 3️⃣ Run LLM Summary & Risk Analysis
    llm_result = analyze_with_llm(ticker, df)

    # 4️⃣ Combine Results
    result = {
        "ticker": ticker,
        "predicted_next_day_close": round(float(next_price), 2),
        "llm_summary": llm_result.get("summary", ""),
        "risk_level": llm_result.get("risk", ""),
        "suggestion": llm_result.get("suggestion", ""),
    }

    return result
