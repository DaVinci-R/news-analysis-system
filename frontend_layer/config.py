# 前端展示层配置
WEB_HOST = "0.0.0.0"
WEB_PORT = 8501

DB_HOST = "localhost"
DB_PORT = 3306
DB_USER = "root"
DB_PASSWORD = "yourpassword"
DB_NAME = "news_analysis"
TABLE_NAME = "all_news"
SUMMARY_TABLE = "news_summary"
# 交互层 API 配置
INTERACTIVE_API_HOST = "localhost" # 如果想实现同一局域网内访问，需要将该url改成后端所在主机的IP地址
INTERACTIVE_API_PORT = 8001
INTERACTIVE_CHAT_PATH = "/chat"
INTERACTIVE_API_URL = f"http://{INTERACTIVE_API_HOST}:{INTERACTIVE_API_PORT}{INTERACTIVE_CHAT_PATH}"

def get_db_url():
    return f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
