from fastapi import FastAPI
from sqlalchemy import create_engine
import pandas as pd
import os
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

app = FastAPI(title="Medical Telegram Analytics API")

# Database connection using env vars
user = os.getenv("POSTGRES_USER", "postgres")
password = os.getenv("POSTGRES_PASSWORD", "postgres")
db = os.getenv("POSTGRES_DB", "medical_dw")
host = os.getenv("POSTGRES_HOST", "localhost")
port = os.getenv("POSTGRES_PORT", "5432")

engine = create_engine(f"postgresql://{user}:{password}@{host}:{port}/{db}")

# Root route
@app.get("/")
def root():
    return {"message": "Medical Telegram Analytics API is running"}

# Analytics endpoint: Top product words
@app.get("/api/reports/top-products")
def top_products(limit: int = 10):
    query = """
    select word, count(*) as freq
    from (
        select unnest(string_to_array(message_text,' ')) as word
        from analytics.fct_messages
    ) t
    where word <> ''
    group by word
    order by freq desc
    limit %(limit)s
    """
    df = pd.read_sql(query, engine, params={"limit": limit})
    return df.to_dict("records")
