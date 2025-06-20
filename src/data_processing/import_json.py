import json
import pandas as pd
from sqlalchemy import create_engine
from ..config.config import DATABASE_URL

# 1. 加载原始 JSON（是一个字符串列表）
json_file = '../../data/backup_results/xxxx.json'
with open(json_file, 'r', encoding='utf-8') as f:
    raw_data = json.load(f)

# 2. 如果每个元素是字符串形式的 JSON，先解析成字典
if isinstance(raw_data, list) and isinstance(raw_data[0], str):
    data = [json.loads(item) for item in raw_data]
else:
    data = raw_data  # 正常结构化的字典列表

# 3. 转成 DataFrame
df = pd.DataFrame(data)

# 4. 创建数据库连接

engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,
    pool_recycle=3600,
    connect_args={'connect_timeout': 10}
)

# 5. 分批写入
def write_in_batches(df, batch_size=500):
    total = len(df)
    for i in range(0, total, batch_size):
        batch_df = df.iloc[i:i + batch_size]
        batch_df.to_sql(
            name=table_name,
            con=engine,
            if_exists='append',
            index=False
        )
        print(f'已写入第 {i} 到 {i + len(batch_df) - 1} 行')

write_in_batches(df)

print("✅ 所有数据已成功写入数据库！")
