# LLM处理层配置

# 数据库配置 (保持与 data_layer 一致，或独立配置)
DB_HOST = "localhost"
DB_PORT = 3306
DB_USER = "root"
DB_PASSWORD = "yourpassword"
DB_NAME = "news_analysis"
TABLE_NAME = "all_news"   # 合并后的单表名称

# 在线 LLM 配置 (OpenAI 协议，如 DeepSeek)
ONLINE_API_KEY = "your_api_key" # 示例 Key
ONLINE_BASE_URL = "https://api.deepseek.com"
ONLINE_MODEL = "deepseek-chat"


# 处理参数
BATCH_SIZE = 10      # 一次处理的数据条数
CONCURRENCY = 2       # 并发处理个数 (协程或线程)
PROCESS_INTERVAL = 600 # 轮询间隔时间 (秒)

# --- 分类总结配置 ---
# 触发模式: 'fixed' (定点触发) 或 'interval' (循环触发)
SUMMARY_TRIGGER_MODE = "fixed" 

# 定点触发时间 (仅在 fixed 模式下生效, 格式 HH:MM)
SUMMARY_FIXED_TIME = "00:01"

# 循环触发间隔 (仅在 interval 模式下生效, 单位：秒)
SUMMARY_INTERVAL = 3600 

# 默认时间窗口 (小时)
SUMMARY_DEFAULT_WINDOW_HOURS = 24

# 自定义时间窗口 (格式: [开始时间, 结束时间])
# 例如: ["2026-02-23 13:00:00", "2026-02-24 14:00:00"]
SUMMARY_CUSTOM_WINDOW = None 

# 资产大类列表 (固定)
ASSET_CLASSES = ['商品', '股票', '债券', '利率', '外汇', '数字货币', '房地产', '衍生品', '其他']

def get_db_url():
    return f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
