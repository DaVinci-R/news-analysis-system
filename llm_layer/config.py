import os

# LLM处理层配置

# 数据库配置
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = int(os.getenv("DB_PORT", 3306))
DB_USER = os.getenv("DB_USER", "root")
DB_PASSWORD = os.getenv("DB_PASSWORD", "yourpassword")
DB_NAME = os.getenv("DB_NAME", "news_analysis")
TABLE_NAME = "all_news"

# 在线 LLM 配置
ONLINE_API_KEY = os.getenv("ONLINE_API_KEY", "your_api_key")
ONLINE_BASE_URL = os.getenv("ONLINE_BASE_URL", "https://api.deepseek.com")
ONLINE_MODEL = os.getenv("ONLINE_MODEL", "deepseek-chat")

# 处理参数
BATCH_SIZE = int(os.getenv("BATCH_SIZE", 10))
CONCURRENCY = int(os.getenv("CONCURRENCY", 2))
PROCESS_INTERVAL = int(os.getenv("PROCESS_INTERVAL", 600))

# --- 分类总结配置 ---
SUMMARY_TRIGGER_MODE = os.getenv("SUMMARY_TRIGGER_MODE", "fixed")  # 控制触发模式 fixed | interval
SUMMARY_FIXED_TIME = os.getenv("SUMMARY_FIXED_TIME", "00:01")  # 定点执行时间
SUMMARY_INTERVAL = int(os.getenv("SUMMARY_INTERVAL", 3600))  # 间隔执行时间
SUMMARY_DEFAULT_WINDOW_HOURS = int(os.getenv("SUMMARY_DEFAULT_WINDOW_HOURS", 24))  # 默认窗口时间
SUMMARY_CUSTOM_WINDOW = None 

# 资产大类列表 (固定)
ASSET_CLASSES = ['商品', '股票', '债券', '利率', '外汇', '数字货币', '房地产', '衍生品', '其他']

def get_db_url():
    return f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
