import pandas as pd
from tqdm import tqdm
from transformers import AutoModelForCausalLM, AutoTokenizer

# 模型路径或 HuggingFace ID
MODEL_NAME = "Qwen/Qwen3-4B"

# 加载模型和分词器
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
model = AutoModelForCausalLM.from_pretrained(
    MODEL_NAME,
    torch_dtype="auto",
    device_map="auto"
)

def qwen3_model_by_local(news_batch):
    """
    使用本地加载的 Qwen3-4B 模型批量处理新闻，返回模型生成的原始文本。

    Args:
        news_batch (pd.DataFrame): 包含新闻内容的 DataFrame，每行至少包含 'content' 字段

    Returns:
        List[Dict]: 每个元素包含原始新闻索引和模型输出的 raw text
    """
    results = []

    # 分类体系提示词（保持不变）
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
            # 使用 chat template 构造输入（关闭 thinking mode）
            text = tokenizer.apply_chat_template(
                messages,
                tokenize=False,
                add_generation_prompt=True,
                enable_thinking=False
            )

            # Tokenize 输入
            inputs = tokenizer([text], return_tensors="pt").to(model.device)

            # 模型生成
            outputs = model.generate(
                **inputs,
                max_new_tokens=1024,     # 控制最大输出长度
                temperature=0.1,         # 更确定性的输出
                top_p=0.95,
                do_sample=True
            )

            # 解码生成内容
            output_text = tokenizer.decode(outputs[0][len(inputs["input_ids"][0]):], skip_special_tokens=True).strip()

            # 保存结果
            results.append({
            output_text
            })

        except Exception as e:
            print(f"处理新闻时出错: {e}")
            results.append({
                "error": str(e)
            })

    return results