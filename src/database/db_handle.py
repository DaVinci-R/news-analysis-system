import json
import pymysql
import pandas as pd
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from ..config.config import DATABASE_URL

engine = create_engine(DATABASE_URL)

def get_last_processed_news_id():
    """获取 processed_hashes 表中最新一条 hash 对应的 news.id"""
    sql = """
    SELECT n.id 
    FROM processed_hashes p
    JOIN news n ON p.hash = n.content_hash
    ORDER BY p.id DESC 
    LIMIT 1
    """
    df = pd.read_sql(sql, engine)
    return df['id'].iloc[0] if not df.empty else None

def load_news_after_last_processed():
    """从最后处理的新闻之后开始加载"""
    last_id = get_last_processed_news_id()
    if last_id is not None:
        sql = "SELECT id, publish_date, content, content_hash FROM news WHERE id > %s ORDER BY id"
        params = (last_id,)
    else:
        sql = "SELECT id, publish_date, content, content_hash FROM news ORDER BY id"
        params = ()
    df = pd.read_sql(sql, engine, params=params)
    df['formatted_content'] = df.apply(lambda row: f"id:{row['id']};date:{row['publish_date']};{row['content']}", axis=1)
    return df[['id', 'content_hash', 'formatted_content']]


def import_results(results, last_hash):
    try:
        df_results = pd.DataFrame([json.loads(list(item)[0]) for item in results])
        df_hashes = pd.DataFrame({'hash': [last_hash]})

        with engine.begin() as connection:
            # 在一个事务中写入两张表
            df_results.to_sql('analysis_results', con=connection, if_exists='append', index=False)
            df_hashes.to_sql('processed_hashes', con=connection, if_exists='append', index=False, method='multi')

    except Exception as e:
        print(f"导入数据时出错: {e}")
        # 注意：engine.begin() 自动 rollback 出错事务，这里不用手动 rollback
        raise
