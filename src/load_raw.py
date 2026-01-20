import os
import json
import pandas as pd
from sqlalchemy import create_engine, text
from dotenv import load_dotenv
from urllib.parse import quote_plus

# Load environment variables
load_dotenv()

user = os.getenv("POSTGRES_USER")
password = quote_plus(os.getenv("POSTGRES_PASSWORD"))  # encode special chars
db = os.getenv("POSTGRES_DB")
host = os.getenv("POSTGRES_HOST")
port = os.getenv("POSTGRES_PORT")

# Create SQLAlchemy engine
engine = create_engine(
    f"postgresql+psycopg2://{user}:{password}@{host}:{port}/{db}"
)

# Ensure raw schema exists
with engine.connect() as conn:
    conn.execute(text("CREATE SCHEMA IF NOT EXISTS raw;"))
    conn.commit()

BASE = "data/raw/telegram_messages"

for date in os.listdir(BASE):
    for file in os.listdir(f"{BASE}/{date}"):
        with open(f"{BASE}/{date}/{file}", encoding="utf-8") as f:
            data = json.load(f)

        df = pd.DataFrame(data)

        # Append data into raw.telegram_messages
        df.to_sql(
            "telegram_messages",
            engine,
            schema="raw",
            if_exists="append",  # requires table to exist
            index=False
        )

print("✅ Loaded raw data into raw.telegram_messages")
