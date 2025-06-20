import akshare as ak
import pandas as pd
import hashlib
from datetime import datetime
from sqlalchemy import create_engine, text
import time
from ..config.config import DATABASE_URL

# 初始化数据库引擎
engine = create_engine(DATABASE_URL)

def generate_hash(row):
    """根据新闻标题和内容生成唯一哈希"""
    combined = row['title'] + row['content']
    return hashlib.md5(combined.encode('utf-8')).hexdigest()

def filter_new_hashes(df):
    """过滤掉已经存在的 hash"""
    existing_hashes = set()
    with engine.connect() as conn:
        result = conn.execute(text("SELECT content_hash FROM news WHERE content_hash IN :hashes"),
                              {"hashes": tuple(df['content_hash'].unique())})
        existing_hashes = {row[0] for row in result.fetchall()}

    # 筛选出未存在的 hash
    return df[~df['content_hash'].isin(existing_hashes)]

def fetch_and_store_news():
    print(f"[{datetime.now()}] 开始抓取财联社新闻...")
    try:
        news_df = ak.stock_info_global_cls(symbol="全部")
        print(f"成功获取 {len(news_df)} 条新闻")
        # 重命名列
        news_df = news_df.rename(columns={
            '标题': 'title',
            '内容': 'content',
            '发布日期': 'publish_date',
            '发布时间': 'publish_time'
        })

        # 添加 hash 列
        news_df['content_hash'] = news_df.apply(generate_hash, axis=1)

        # 添加入库时间
        news_df['create_time'] = datetime.now()

        # 过滤掉已存在的 hash
        new_news_df = filter_new_hashes(news_df)
        if len(new_news_df) == 0:
            print("没有新新闻需要写入数据库")
            return

        # 使用 to_sql 批量写入
        new_news_df.to_sql(name='news', con=engine, if_exists='append', index=False)
        print(f"成功写入 {len(new_news_df)} 条新新闻到数据库")

    except Exception as e:
        print(f"抓取或写入失败: {e}")


if __name__ == "__main__":

    while True:
        fetch_and_store_news()
        print("等待 1 分钟后再次抓取...\n")
        time.sleep(60)  # 每1分钟执行一次