from sqlalchemy import create_engine, MetaData, Table, Column, String, Text, DateTime, Date, Time, text, Integer
from .config import get_db_url, TABLE_NAME, DB_USER, DB_PASSWORD, DB_HOST, DB_PORT, DB_NAME

def init_db():
    # 1. 连接MySQL服务，检查并创建数据库
    server_url = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/"
    server_engine = create_engine(server_url)
    
    with server_engine.connect() as conn:
        conn.execute(text(f"CREATE DATABASE IF NOT EXISTS `{DB_NAME}` CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci"))
    
    print(f"数据库 {DB_NAME} 确保存在。")

    # 2. 连接到具体数据库，创建表结构
    engine = create_engine(get_db_url())
    metadata = MetaData()

    # 自动创建表结构，A表的名称为cls_news
    from sqlalchemy import Float
    news_table = Table(
        TABLE_NAME, metadata,
        Column('id', Integer, primary_key=True, autoincrement=True, comment='自增ID'),
        Column('content_hash', String(64), unique=True, comment='内容哈希值'),
        
        # --- 原始数据列 ---
        Column('title', String(255), comment='标题'),
        Column('content', Text, comment='原文内容'),
        Column('publish_date', Date, comment='发布日期'),
        Column('publish_time', Time, comment='发布时间'),
        Column('create_time', DateTime, comment='入库时间'),

        # --- 结构化数据列 (允许为空) ---
        Column('source', String(100), comment='来源'),
        Column('region', String(50), comment='地区'),
        Column('subject', String(100), comment='主体'),
        Column('asset_class', String(50), comment='资产类别'),
        Column('sector', String(100), comment='行业板块'),
        Column('sentiment_score', Float, comment='情感评分'),
        Column('impact_weight', Integer, comment='影响权重'),
        Column('trend_signal', Integer, comment='趋势信号'),
        Column('event_type', String(100), comment='事件类型'),
        Column('driver_factor', Text, comment='驱动因素'),
        Column('key_metrics', Text, comment='核心指标'),
        Column('processed_at', DateTime, comment='分析处理时间')
    )
    
    # 3. 创建分类总结表 news_summary
    summary_table = Table(
        'news_summary', metadata,
        Column('summary_id', Integer, primary_key=True, autoincrement=True, comment='摘要自增ID'),
        Column('asset_class', String(50), comment='资产大类'),
        Column('summary_text', Text, comment='总结正文'),
        Column('window_start', DateTime, comment='窗口开始时间'),
        Column('window_end', DateTime, comment='窗口结束时间'),
        Column('news_count', Integer, comment='新闻样本数量'),
        Column('created_at', DateTime, comment='生成时间')
    )
    
    # 创建所有表（如果不存在）
    metadata.create_all(engine)
    print(f"数据库表 {TABLE_NAME} 和 news_summary 初始化完成。")

if __name__ == "__main__":
    init_db()
