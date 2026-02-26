import json
import re
from .agents import sql_agent, summary_agent
from .db_utils import execute_sql
from .config import DEFAULT_MODEL_NAME

def extract_json(text):
    """从文本中提取 JSON"""
    try:
        match = re.search(r'(\{.*\})', text, re.DOTALL)
        if match:
            return json.loads(match.group(1))
        return json.loads(text)
    except:
        return None

class InteractiveService:
    def __init__(self, model_name=DEFAULT_MODEL_NAME):
        self.model_name = model_name

    def ask(self, user_question):
        print(f"用户提问: {user_question} (Model: {self.model_name})")
        
        # 1. 第一个智能体：拆解问题生成 SQL
        sql_response_raw = sql_agent(user_question, model_name=self.model_name)
        sql_data = extract_json(sql_response_raw)
        
        if not sql_data or "sql" not in sql_data:
            print(f"SQL Agent response raw: {sql_response_raw}")
            return "对不起，我暂时无法理解您的查询需求。请换个方式提问。"
        
        sql_query = sql_data.get("sql")
        target_table = sql_data.get("table", "unknown")
        print(f"智能体 1 生成针对 [{target_table}] 的 SQL: {sql_query}")
        
        # 2. 从数据库执行查询
        try:
            db_results = execute_sql(sql_query, table_name=target_table)
            print(f"数据库返回 {len(db_results)} 条结果。")

            # 处理 db_results 中的 datetime, date, timedelta 对象，使其可序列化
            for row in db_results:
                for key, value in row.items():
                    if hasattr(value, 'isoformat'):
                        row[key] = value.isoformat()
                    elif hasattr(value, 'total_seconds'): # 处理 timedelta
                        row[key] = str(value)
        except Exception as e:

            print(f"Database Error: {e}")
            return f"在执行数据查询时出错: {str(e)}"

        # 3. 第二个智能体：整合结果生成总结
        data_context = json.dumps(db_results, ensure_ascii=False)
        final_answer = summary_agent(user_question, data_context, model_name=self.model_name)
        
        return final_answer

