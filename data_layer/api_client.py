import akshare as ak
import pandas as pd
import hashlib
from datetime import datetime

def generate_hash(row):
    """根据新闻标题和内容生成唯一哈希"""
    combined = str(row.get('title', '')) + str(row.get('content', ''))
    return hashlib.md5(combined.encode('utf-8')).hexdigest()

def fetch_news():
    """通过财联社API获取新闻数据"""
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

        return news_df
    except Exception as e:
        print(f"抓取失败: {e}")
        return pd.DataFrame()