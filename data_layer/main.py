import time
import os
import sys

# 将当前项目的根目录添加到 sys.path 中，以便可以基于模块名层级导入
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from data_layer.config import SPIDER_INTERVAL
from data_layer.db_init import init_db
from data_layer.api_client import fetch_news
from data_layer.db_ops import filter_new_hashes, save_news_to_db

def run():
    print("=== 数据层(Data Layer)启动 ===")
    
    # 1. 自动创建表结构
    print("正在初始化数据库连接与表结构...")
    init_db()
    
    # 2. 循环爬取
    print(f"开始爬取财联社新闻，间隔时间为 {SPIDER_INTERVAL} 秒。")
    while True:
        try:
            # 3. 通过财联社API获取新闻数据
            news_df = fetch_news()
            
            if news_df is not None and not news_df.empty:
                # 4. 过滤已存在的数据
                new_news_df = filter_new_hashes(news_df)
                
                # 5. 将新闻数据保存到数据库的A表中
                save_news_to_db(new_news_df)
            else:
                print("未获取到任何新闻数据。")
                
        except Exception as e:
            print(f"运行过程中遇到错误: {e}")
            
        print(f"等待 {SPIDER_INTERVAL} 秒后再次抓取...\n")
        time.sleep(SPIDER_INTERVAL)

if __name__ == "__main__":
    run()
