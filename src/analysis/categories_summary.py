from sqlalchemy import create_engine
import pandas as pd
from tqdm import tqdm
from transformers import AutoModelForCausalLM, AutoTokenizer
import torch
import os
import schedule
import time
from datetime import datetime, timedelta
from ..config.config import DATABASE_URL

# 模型路径
MODEL_NAME = "Qwen/Qwen3-4B"

print("加载模型中...")
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
model = AutoModelForCausalLM.from_pretrained(
    MODEL_NAME,
    torch_dtype="auto",
    device_map="auto"
)
print("模型加载完成。")

# 数据库连接
engine = create_engine(DATABASE_URL)


def get_summary(date):
    query = 'SELECT date, category, summary FROM analysis_results WHERE date = %s'
    return pd.read_sql(query, engine, params=(date,))


def generate_summary(input_text, system_prompt, user_template):
    """通用生成函数"""
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_template.format(content=input_text)}
    ]

    try:
        text = tokenizer.apply_chat_template(
            messages,
            tokenize=False,
            add_generation_prompt=True,
            enable_thinking=False
        )

        inputs = tokenizer([text], return_tensors="pt").to(model.device)

        outputs = model.generate(
            **inputs,
            max_new_tokens=1024,
            temperature=0.1,
            top_p=0.95,
            do_sample=True
        )

        output_text = tokenizer.decode(outputs[0][len(inputs["input_ids"][0]):], skip_special_tokens=True).strip()
        return output_text
    except Exception as e:
        print(f"[ERROR] 生成摘要失败：{e}")
        return f"[ERROR] {e}"


def summarize_category_in_chunks(date, category, summaries, chunk_size=100):
    """
    分段生成每类新闻摘要，并进行二次归纳。
    """
    system_prompt = "你是一个专业的金融新闻分析归纳总结师，你会首先对同一类别的新闻进行归纳汇总，并作总结分析。"

    user_template_stage1 = """请对以下新闻进行200字左右的综合摘要，仅输出正文，不要包含任何其他说明：

{content}
"""

    user_template_stage2 = """请对以下多个小摘要进行再次归纳总结，生成一个200字左右的最终综合摘要：

{content}
"""

    print(f"正在处理类别：{category}，总摘要数：{len(summaries)}")

    # 分段处理小摘要
    chunks = [summaries[i:i+chunk_size] for i in range(0, len(summaries), chunk_size)]
    chunk_summaries = []

    for idx, chunk in enumerate(tqdm(chunks, desc=f"处理中 {category}")):
        chunk_text = "\n".join([f"【{i+1}】{s}" for i, s in enumerate(chunk)])
        summary = generate_summary(chunk_text, system_prompt, user_template_stage1)
        chunk_summaries.append(summary)

    # 二次归纳
    combined_chunk_text = "\n".join([f"【小摘要{i+1}】{s}" for i, s in enumerate(chunk_summaries)])
    final_summary = generate_summary(combined_chunk_text, system_prompt, user_template_stage2)

    return {
        "date": date,
        "category": category,
        "summary": final_summary
    }


def main():
    print("========== 开始执行 main() ==========")

    # 设置需要总结分析新闻的日期
    # 获取当天日期
    date = datetime.today().strftime('%Y-%m-%d')

    # 获取前一天的日期
    # date = (datetime.today() - timedelta(days=1)).strftime('%Y-%m-%d')


    print(f"读取 {date} 的分析数据...")
    df = get_summary(date)

    results = []
    for category, group in df.groupby("category"):
        summaries = group['summary'].fillna('').tolist()
        result = summarize_category_in_chunks(date, category, summaries)
        results.append(result)

    # 结果转 DataFrame
    results_df = pd.DataFrame(results)

    # 写入本地文件
    now_str = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    output_dir = '../../data/summary_results'
    filename = f'data_{now_str}.txt'
    filepath = os.path.join(output_dir, filename)
    os.makedirs(output_dir, exist_ok=True)
    results_df.to_csv(filepath, sep='\t', index=False)
    print(f"[保存成功] 文件已保存至 {filepath}")

    # 写入数据库
    try:
        results_df.to_sql('summary', engine, if_exists='append', index=False)
        print("[写入成功] 已写入数据库表 summary")
    except Exception as e:
        print(f"[ERROR] 写入数据库失败：{e}")

    # 打印输出
    print("=== 摘要结果如下 ===")
    for res in results:
        print(f"【{res['category']}】{res['summary']}")
    print("========== main() 执行完毕 ==========")


if __name__ == "__main__":
    # 安排每天固定时间执行
    schedule.every().day.at("09:56").do(main)

    print("程序已启动，等待每天09:36定时执行 main()...", flush=True)

    while True:
        schedule.run_pending()
        time.sleep(1)
