from sqlalchemy import create_engine, text
from .config import get_db_url

def execute_sql(sql_query, table_name="unknown"):
    """执行 SQL 并返回列表字典格式的结果"""
    print(f"执行数据库查询, 目标表: {table_name}")
    engine = create_engine(get_db_url())
    try:
        with engine.connect() as conn:
            result = conn.execute(text(sql_query))
            # 将结果转换为字典列表
            if result.returns_rows:
                return [dict(row._mapping) for row in result.fetchall()]
            return []
    except Exception as e:
        print(f"SQL Execution Error on table {table_name}: {e}")
        return []

