from ..models.local_model import qwen3_model_by_local
from ..database.db_handle import load_news_after_last_processed, import_results
import pandas as pd
import json
import schedule
import time
import os
from datetime import datetime

def job():
    df_unprocessed = load_news_after_last_processed()
    if df_unprocessed.empty:
        print("无新数据，等待下次运行。", flush=True)
        return

    # 创建新闻数据批次
    news_batch = pd.DataFrame([{"content": content} for content in df_unprocessed['formatted_content']])
    # 使用本地模型进行分析
    results = qwen3_model_by_local(news_batch)
    # 获取最后一条新闻的 content_hash
    last_hash = df_unprocessed['content_hash'].iloc[-1]

    # 保存 results 到本地 JSON 文件
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"analysis_results_{timestamp}_{last_hash}.json"
    save_path = os.path.join("../../data/backup_results", filename)

    # 确保目录存在
    os.makedirs("../../data/backup_results", exist_ok=True)

    try:
        # 保存为 JSON 文件
        with open(save_path, "w", encoding="utf-8") as f:
            json.dump([list(item)[0] for item in results], f, ensure_ascii=False, indent=2)
        print(f"分析结果已备份到：{save_path}", flush=True)
    except Exception as e:
        print(f"保存分析结果 JSON 文件失败: {e}", flush=True)

    # 尝试导入到数据库
    try:
        import_results(results, [last_hash])
    except Exception as e:
        print(f"写入数据库失败: {e}", flush=True)
        print("请稍后使用备份文件手动恢复。", flush=True)


# 每120分钟执行一次，可以替换成固定间隔时间启动
# schedule.every(120).minutes.do(job)

# 每天凌晨1点执行，可以修改成你具体需要启动的时间
schedule.every().day.at("09:27").do(job)

# 启动时是否立即执行一次（如果需要，可以保留这句）
# job()

# 开始调度循环
print("开始任务调度，每天01:00执行一次任务", flush=True)
while True:
    schedule.run_pending()
    time.sleep(1)