import os
import pandas as pd
from sqlalchemy import text
from app.db.connection.sql_alchemy import SqlAlchemyBuilder


def load_iot_readings():
    sql_server = os.getenv('MYSQL_HOST')
    sql_database = os.getenv('MYSQL_DATABASE')
    engine = SqlAlchemyBuilder(sql_server, sql_database).engine

    query = text("""
        SELECT 
            id,
            timestamp,
            humidity,
            ph,
            phosphorus,
            potassium,
            pump_on
        FROM iot_reading
        ORDER BY timestamp ASC
    """)

    df = pd.read_sql(query, engine)
    return df


def compute_statistics(df: pd.DataFrame):
    stats = {"humidity": {
        "mean": round(df["humidity"].mean(), 2),
        "min": round(df["humidity"].min(), 2),
        "max": round(df["humidity"].max(), 2),
        "std": round(df["humidity"].std(), 2),
    }, "ph": {
        "mean": round(df["ph"].mean(), 2),
        "min": round(df["ph"].min(), 2),
        "max": round(df["ph"].max(), 2),
        "std": round(df["ph"].std(), 2),
    }, "pump_on": float(df["pump_on"].mean() * 100), "nutrients": {
        "phosphorus_ok": float(df["phosphorus"].mean() * 100),
        "potassium_ok": float(df["potassium"].mean() * 100),
    }}

    return stats
