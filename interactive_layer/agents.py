from .llm_client import agent_template

from .config import DEFAULT_MODEL_NAME
from .prompt import get_sql_prompt, get_summary_prompt

def sql_agent(query, model_name=DEFAULT_MODEL_NAME):
    """
    SQL 生成智能体
    """
    return agent_template(get_sql_prompt(), query, model_name)

def summary_agent(query, data_context, model_name=DEFAULT_MODEL_NAME):
    """
    结果总结智能体
    query: 用户的原始问题
    data_context: 从数据库查询到的数据内容
    """
    user_input = f"用户问题: {query}\n\n数据库查询结果: {data_context}"
    return agent_template(get_summary_prompt(), user_input, model_name)

