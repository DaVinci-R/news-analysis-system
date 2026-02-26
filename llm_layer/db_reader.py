import pandas as pd
from sqlalchemy import create_engine, text
from .config import get_db_url, TABLE_NAME

def read_unprocessed_news(last_hash=None):
    """读取尚未进行结构化分析的新闻数据"""
    engine = create_engine(get_db_url())
    
    # 策略：直接读取 processed_at 为空的数据
    query = f"SELECT * FROM {TABLE_NAME} WHERE processed_at IS NULL ORDER BY create_time ASC"
    df = pd.read_sql(query, con=engine)
    
    return df
