import time
import os
import sys
from datetime import datetime, timedelta
import pandas as pd
from sqlalchemy import create_engine, text

# 添加根目录到路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from llm_layer import config
from llm_layer.models.llm_client import get_llm_client
from llm_layer.summary_processor import generate_asset_summary

def get_time_window():
    """计算总结的时间窗口"""
    if config.SUMMARY_CUSTOM_WINDOW:
        start_str, end_str = config.SUMMARY_CUSTOM_WINDOW
        return datetime.strptime(start_str, "%Y-%m-%d %H:%M:%S"), datetime.strptime(end_str, "%Y-%m-%d %H:%M:%S")
    
    end_time = datetime.now()
    start_time = end_time - timedelta(hours=config.SUMMARY_DEFAULT_WINDOW_HOURS)
    return start_time, end_time

def save_summary(asset_class, summary_text, window_start, window_end, news_count):
    """保存总结到 news_summary 表"""
    engine = create_engine(config.get_db_url())
    with engine.connect() as conn:
        stmt = text("""
            INSERT INTO news_summary (asset_class, summary_text, window_start, window_end, news_count, created_at)
            VALUES (:asset_class, :summary_text, :window_start, :window_end, :news_count, :created_at)
        """)
        conn.execute(stmt, {
            "asset_class": asset_class,
            "summary_text": summary_text,
            "window_start": window_start,
            "window_end": window_end,
            "news_count": news_count,
            "created_at": datetime.now()
        })
        conn.commit()

def run_summary_task(client):
    """执行完整的总结任务"""
    start_time, end_time = get_time_window()
    print(f"[{datetime.now()}] 开始生成分类总结记录，窗口: {start_time} 至 {end_time}")
    
    engine = create_engine(config.get_db_url())
    
    for asset in config.ASSET_CLASSES:
        print(f"正在处理 [ {asset} ] 类别...")
        
        # 查询属于该类别且在时间窗口内的新闻
        query = text(f"""
            SELECT title, content FROM {config.TABLE_NAME}
            WHERE asset_class = :asset 
            AND create_time >= :start 
            AND create_time <= :end
        """)
        
        with engine.connect() as conn:
            news_df = pd.read_sql(query, conn, params={"asset": asset, "start": start_time, "end": end_time})
        
        if news_df.empty:
            print(f"  - 暂无新闻数据，跳过内容生成。")
            continue
            
        # 调用 LLM 生成总结
        news_list = news_df.to_dict('records')
        summary = generate_asset_summary(client, asset, news_list)
        
        # 入库
        save_summary(asset, summary, start_time, end_time, len(news_list))
        print(f"  - 总结生成并保存成功 (基于 {len(news_list)} 条新闻)。")

def main():
    print("=== 资产分类总结模块 (Summary Layer) 启动 ===")
    
    client = get_llm_client(config)
    last_fixed_date = None # 用于定点模式，记录今天是否已运行
    
    # 循环触发模式下，启动即执行一次
    if config.SUMMARY_TRIGGER_MODE == "interval":
        run_summary_task(client)
        print(f"首次执行完成，进入循环模式，间隔 {config.SUMMARY_INTERVAL} 秒...")
    else:
        print(f"进入定点模式，等待触发时间: {config.SUMMARY_FIXED_TIME} ...")

    while True:
        try:
            now = datetime.now()
            
            if config.SUMMARY_TRIGGER_MODE == "interval":
                time.sleep(config.SUMMARY_INTERVAL)
                run_summary_task(client)
                
            elif config.SUMMARY_TRIGGER_MODE == "fixed":
                current_time_str = now.strftime("%H:%M")
                current_date_str = now.strftime("%Y-%m-%d")
                
                if current_time_str == config.SUMMARY_FIXED_TIME and last_fixed_date != current_date_str:
                    run_summary_task(client)
                    last_fixed_date = current_date_str
                
                # 定点模式下检查频率可以高一些
                time.sleep(60) 
                
        except Exception as e:
            print(f"总结模块运行出错: {e}")
            time.sleep(60)

if __name__ == "__main__":
    main()
