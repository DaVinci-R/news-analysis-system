import os

# 数据库配置
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = int(os.getenv("DB_PORT", 3306))
DB_USER = os.getenv("DB_USER", "root")
DB_PASSWORD = os.getenv("DB_PASSWORD", "yourpassword")
DB_NAME = os.getenv("DB_NAME", "news_analysis")
TABLE_NAME = "all_news"

# 新闻爬取间隔时间（秒）
SPIDER_INTERVAL = int(os.getenv("SPIDER_INTERVAL", 60))

# 数据库连接URL
def get_db_url():
    return f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
