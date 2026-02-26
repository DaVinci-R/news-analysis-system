import time
import os
import sys
import pandas as pd
from concurrent.futures import ThreadPoolExecutor

# 添加根目录到路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from llm_layer import config
from llm_layer.db_writer import init_table_b, get_last_processed_hash, save_structured_data
from llm_layer.db_reader import read_unprocessed_news
from llm_layer.llm_processor import process_single_news
from llm_layer.models.llm_client import get_llm_client

def batch_process(client, news_df):
    """并发处理一批新闻"""
    results = []
    with ThreadPoolExecutor(max_workers=config.CONCURRENCY) as executor:
        # 将这一批次的任务交给线程池
        futures = [executor.submit(process_single_news, client, row) for _, row in news_df.iterrows()]
        for future in futures:
            res = future.result()
            if res:
                results.append(res)
    return results

def run():
    print("=== LLM 处理层 (LLM Layer) 启动 ===")
    
    # 1. 初始化 B 表
    init_table_b()
    
    # 2. 加载 LLM 客户端 (如果是本地模型，在此处加载一次)
    client = None
    
    while True:
        try:
            # 3. 获取上次处理到的进度
            last_hash = get_last_processed_hash()
            
            # 4. 读取待处理的新闻
            unprocessed_df = read_unprocessed_news(last_hash)
            
            if not unprocessed_df.empty:
                print(f"发现 {len(unprocessed_df)} 条新数据待处理...")
                
                # 只有发现新数据时才按需加载客户端（如果是本地模型建议在循环外加载）
                if client is None:
                    client = get_llm_client(config)
                
                # 5. 分片处理 (按 BATCH_SIZE)
                total_processed = 0
                for i in range(0, len(unprocessed_df), config.BATCH_SIZE):
                    batch_df = unprocessed_df.iloc[i : i + config.BATCH_SIZE]
                    print(f"正在处理批次 {i // config.BATCH_SIZE + 1}, 包含 {len(batch_df)} 条数据...")
                    
                    structured_results = batch_process(client, batch_df)
                    
                    # 6. 保存结果
                    save_structured_data(structured_results)
                    total_processed += len(structured_results)
                
                print(f"本轮处理结束，成功结构化 {total_processed} 条新闻。")
            else:
                print("暂无新数据。")
                
        except Exception as e:
            print(f"LLM 层运行出错: {e}")
            import traceback
            traceback.print_exc()

        print(f"等待 {config.PROCESS_INTERVAL} 秒后进行下一轮比对...\n")
        time.sleep(config.PROCESS_INTERVAL)

if __name__ == "__main__":
    run()
