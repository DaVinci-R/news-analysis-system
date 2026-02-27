import os

# 数据库配置
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = int(os.getenv("DB_PORT", 3306))
DB_USER = os.getenv("DB_USER", "root")
DB_PASSWORD = os.getenv("DB_PASSWORD", "yourpassword")
DB_NAME = os.getenv("DB_NAME", "news_analysis")
TABLE_NAME = "all_news"
SUMMARY_TABLE_NAME = "news_summary"

def get_db_url():
    return f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# API 服务配置
API_HOST = "0.0.0.0"
API_PORT = 8001
CHAT_PATH = "/chat"

# LLM 模型配置映射
LLM_CONFIGS = {
    os.getenv("ONLINE_MODEL", "deepseek-chat"): {
        "api_key": os.getenv("ONLINE_API_KEY", "your_api_key"),
        "base_url": os.getenv("ONLINE_BASE_URL", "https://api.deepseek.com"),
    }
}

# 默认模型名称
DEFAULT_MODEL_NAME = os.getenv("ONLINE_MODEL", "deepseek-chat")

# 资产大类映射
ASSET_CLASSES = ['商品', '股票', '债券', '利率', '外汇', '数字货币', '房地产', '衍生品', '其他']
