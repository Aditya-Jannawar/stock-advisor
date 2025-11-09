from fastapi import FastAPI
from app.routes import stock_routes
from app.database import Base, engine
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

# Initialize DB
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Stock Advisor Backend")

app.include_router(stock_routes.router, prefix="/api", tags=["Stock"])


@app.get("/")
def root():
    return {"message": "🚀 Stock Advisor Backend is running"}



# Allow frontend calls
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Serve frontend folder
app.mount("/frontend", StaticFiles(directory="frontend"), name="frontend")