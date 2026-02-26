from sqlalchemy import create_engine, text
from .config import get_db_url, TABLE_NAME
import pandas as pd

def get_engine():
    return create_engine(get_db_url())

def filter_new_hashes(df):
    """过滤掉已经存在的 hash"""
    if df is None or df.empty:
        return df

    hashes = tuple(df['content_hash'].unique())
    if not hashes:
        return df
        
    engine = get_engine()
    with engine.connect() as conn:
        if len(hashes) == 1:
            query = text(f"SELECT content_hash FROM {TABLE_NAME} WHERE content_hash = :h")
            result = conn.execute(query, {"h": hashes[0]})
        else:
            query = text(f"SELECT content_hash FROM {TABLE_NAME} WHERE content_hash IN :hashes")
            result = conn.execute(query, {"hashes": hashes})
        existing_hashes = {row[0] for row in result.fetchall()}

    # 筛选出未存在的 hash
    return df[~df['content_hash'].isin(existing_hashes)]

def save_news_to_db(new_news_df):
    """将新闻数据保存到数据库的A表中"""
    if new_news_df is None or len(new_news_df) == 0:
        print("没有新新闻需要写入数据库")
        return
    
    engine = get_engine()
    # 使用 to_sql 批量写入
    new_news_df.to_sql(name=TABLE_NAME, con=engine, if_exists='append', index=False)
    print(f"成功写入 {len(new_news_df)} 条新新闻到数据库表 {TABLE_NAME} 中")
