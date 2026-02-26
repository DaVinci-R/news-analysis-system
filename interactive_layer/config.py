import os

# 数据库配置
DB_HOST = "localhost"
DB_PORT = 3306
DB_USER = "root"
DB_PASSWORD = "yourpassword"
DB_NAME = "news_analysis"
TABLE_NAME = "all_news"
SUMMARY_TABLE_NAME = "news_summary"


def get_db_url():
    return f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# API 服务配置
API_HOST = "0.0.0.0"
API_PORT = 8001
CHAT_PATH = "/chat"  # 智能问答接口路径

# LLM 模型配置映射
# 不同的模型可以对应不同的 API Key 和 Base URL
LLM_CONFIGS = {
    "deepseek-chat": {
        "api_key": "your_api_key",
        "base_url": "https://api.deepseek.com",
    },
    "gpt-4o": {
        "api_key": "your_api_key",
        "base_url": "https://api.openai.com/v1",
    },
    # 可以根据需要添加更多模型配置
}

# 默认模型名称
DEFAULT_MODEL_NAME = "deepseek-chat"

# 资产大类映射（辅助智能体判断）
ASSET_CLASSES = ['商品', '股票', '债券', '利率', '外汇', '数字货币', '房地产', '衍生品', '其他']


