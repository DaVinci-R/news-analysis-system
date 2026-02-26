import json
from .models.llm_client import BaseLLMClient

SUMMARY_PROMPT_TEMPLATE = """
# 角色
你是一个资深的宏观经济与金融策略分析师。

# 任务
请根据我提供的多条新闻内容，针对“{asset_class}”这一特定的资产大类，撰写一份精炼的市场综述分析。

# 包含内容
1. **核心趋势总结**：一句话概括这段时间内该资产类别的整体表现或核心驱动力。
2. **关键驱动事件**：列举 2-3 个影响该资产类别最显著的新闻事件，并说明逻辑。
3. **市场情绪评价**：综合判断目前该类别的市场情绪（看多、看空、观望）。

# 约束项
- 必须基于提供的新闻内容进行总结，不要虚构不存在的事实。
- 语言风格要求专业、客观、言简意赅。
- 如果提供的新闻内容为空或不足以总结，请返回“该时间段内暂无显著影响事件”。
- 总字数控制在 200-300 字以内。

# 输入的新闻标题与摘要如下：
{news_content}
"""

def generate_asset_summary(llm_client: BaseLLMClient, asset_class, news_list):
    """
    为特定资产大类生成总结
    news_list: 包含 title 和 content 的字典列表
    """
    if not news_list:
        return "该时间段内暂无相关新闻记录。"

    # 构造新闻文本块
    formatted_news = ""
    for i, news in enumerate(news_list):
        formatted_news += f"{i+1}. 标题：{news['title']}\n   内容：{news['content'][:150]}...\n\n"

    # 构造 Prompt
    prompt = SUMMARY_PROMPT_TEMPLATE.format(
        asset_class=asset_class,
        news_content=formatted_news
    )

    # 调用 LLM
    response = llm_client.chat("你是一个金融分析助手。", prompt)
    
    return response if response else "生成总结失败。"
