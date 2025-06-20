import os
from openai import OpenAI
from tqdm import tqdm
import pandas as pd



def qwen3_model_by_api(news_batch, api_key=None):
    """
    使用阿里云 DashScope 的 Qwen API 批量处理新闻，直接返回模型原始输出（不尝试解析 JSON）

    Args:
        news_batch: 包含新闻内容的 DataFrame，每行至少包含 'content' 字段
        api_key: DashScope API 密钥（可选，若未传入则从环境变量获取）

    Returns:
        List: 每个元素包含原始新闻索引和模型输出的 raw text
    """
    results = []

    # 设置 API_KEY
    client = OpenAI(
        api_key=api_key,
        base_url="https://dashscope.aliyuncs.com/compatible-mode/v1"
    )

    # 分类体系提示词
    system_prompt = """你是一个专业的金融新闻分析师，专注于为期货量化交易提供新闻分类和分析服务。你需要将每条新闻准确分类，并提取有价值的信息。

分类体系如下：
1. 宏观经济类：央行政策、经济数据、政府财政政策、就业数据等
2. 商品期货相关：农产品、能源、金属、工业品等
3. 金融市场类：股市动态、债券市场、外汇市场、其他期货市场情况
4. 地缘政治类：国际冲突、贸易争端、重大国际事件
5. 行业政策类：监管变化、产业政策调整、环保政策
6. 非金融类：天气、自然灾害、非经济类社会新闻等"""

    for _, row in tqdm(news_batch.iterrows(), total=len(news_batch), desc="Processing News"):
        content = row['content']

        user_prompt = """请对以下新闻进行分类和分析：

                        新闻内容: {content}

                        不包含任何其他内容,并严格按照以下json格式进行输出：
                          "news_index": "新闻序号"(与输入新闻的id号相同),
                          "date": "发布日期"(与输入新闻内容中的date相同),
                          "category": "主分类(从上述6类中选择一个)",
                          "subcategory": "子分类(具体说明该新闻属于主分类中的哪一小类)",
                          "is_market_relevant": true/false, (是否与金融市场相关)
                          "keywords": "关键词1,关键词2, 关键词3,关键词4",
                          "sentiment": 0.0, (情感得分,范围为-1~1，-1表示极度负面，0表示中性，1表示极度正面)
                          "impact_markets": "市场,品种"（可能受到影响的市场或品种）,
                          "summary": "一句话总结这条新闻的核心内容"

                        现在请你处理当前新闻。
                        """
        user_prompt = user_prompt.replace("{content}", content)

        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ]

        try:
            completion = client.chat.completions.create(
                model="qwen3-4b",
                messages=messages,
                temperature=0.1,
                top_p=0.95,
                stream=True,
                extra_body={
                    "enable_thinking": False
                }
            )

            # 收集流式输出内容
            content_text = ""
            for chunk in completion:
                # 判断是否有内容输出
                if len(chunk.choices) > 0 and chunk.choices[0].delta.content is not None:
                    content_text += chunk.choices[0].delta.content

            content_text = content_text.strip()


            # 直接保存模型输出原文
            results.append({
                 content_text
            })

        except Exception as e:
            print(f"处理新闻时出错: {e}")
            results.append({
                "error": str(e)
            })

    return results
