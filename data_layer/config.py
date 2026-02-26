DB_HOST = "localhost"
DB_PORT = 3306
DB_USER = "root"
DB_PASSWORD = "yourpassword"
DB_NAME = "news_analysis"
TABLE_NAME = "all_news"

# 新闻爬取间隔时间（秒）
SPIDER_INTERVAL = 60

# 数据库连接URL
def get_db_url():
    return f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
