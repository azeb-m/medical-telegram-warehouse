# from fastapi import FastAPI
# from sqlalchemy import create_engine
# import pandas as pd

# app = FastAPI(title="Medical Telegram Analytics API")

# engine = create_engine(
#     "postgresql://postgres:postgres@localhost:5432/medical_dw"
# )

# @app.get("/api/reports/top-products")
# def top_products(limit: int = 10):
#     query = f"""
#     select word, count(*) as freq
#     from (
#         select unnest(string_to_array(message_text,' ')) as word
#         from analytics.fct_messages
#     ) t
#     group by word
#     order by freq desc
#     limit {limit}
#     """
#     return pd.read_sql(query, engine).to_dict("records")
