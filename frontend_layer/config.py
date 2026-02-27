import os

# 前端展示层配置
WEB_HOST = "0.0.0.0"
WEB_PORT = 8501

DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = int(os.getenv("DB_PORT", 3306))
DB_USER = os.getenv("DB_USER", "root")
DB_PASSWORD = os.getenv("DB_PASSWORD", "yourpassword")
DB_NAME = os.getenv("DB_NAME", "news_analysis")
TABLE_NAME = "all_news"
SUMMARY_TABLE = "news_summary"

# 交互层 API 配置
INTERACTIVE_API_HOST = os.getenv("INTERACTIVE_API_HOST", "localhost")
INTERACTIVE_API_PORT = int(os.getenv("INTERACTIVE_API_PORT", 8001))
INTERACTIVE_CHAT_PATH = "/chat"
INTERACTIVE_API_URL = f"http://{INTERACTIVE_API_HOST}:{INTERACTIVE_API_PORT}{INTERACTIVE_CHAT_PATH}"

def get_db_url():
    return f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
