from sqlalchemy import create_engine, text
from .config import get_db_url, TABLE_NAME
from datetime import datetime

def init_table_b():
    # 现在表结构由 data_layer 统一初始化，这里只需要确保主表存在即可
    # 实际上由于 main.py 调用了它，我们可以留个空或做个简单检查
    print(f"数据表 {TABLE_NAME} 已由数据层统一管理。")

def get_last_processed_hash():
    engine = create_engine(get_db_url())
    with engine.connect() as conn:
        # 获取最新的已处理记录的 hash
        query = text(f"SELECT content_hash FROM {TABLE_NAME} WHERE processed_at IS NOT NULL ORDER BY processed_at DESC LIMIT 1")
        result = conn.execute(query).fetchone()
        return result[0] if result else None

def save_structured_data(data_list):
    if not data_list:
        return
    
    engine = create_engine(get_db_url())
    
    with engine.connect() as conn:
        for data in data_list:
            # 执行更新操作
            update_stmt = text(f"""
                UPDATE {TABLE_NAME} 
                SET source = :source,
                    region = :region,
                    subject = :subject,
                    asset_class = :asset_class,
                    sector = :sector,
                    sentiment_score = :sentiment_score,
                    impact_weight = :impact_weight,
                    trend_signal = :trend_signal,
                    event_type = :event_type,
                    driver_factor = :driver_factor,
                    key_metrics = :key_metrics,
                    processed_at = :processed_at
                WHERE content_hash = :content_hash
            """)
            
            # 补充处理时间
            data['processed_at'] = datetime.now()
            
            conn.execute(update_stmt, data)
        
        conn.commit()
    
    print(f"成功更新 {len(data_list)} 条结构化分析数据到 {TABLE_NAME}")
