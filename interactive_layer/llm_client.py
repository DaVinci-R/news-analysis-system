from openai import OpenAI
from .config import LLM_CONFIGS, DEFAULT_MODEL_NAME

class LLMClient:
    def __init__(self, model_name=DEFAULT_MODEL_NAME):
        config = LLM_CONFIGS.get(model_name)
        if not config:
            raise ValueError(f"Model {model_name} not configured in config.py")
        
        self.model_name = model_name
        self.api_key = config["api_key"]
        self.base_url = config["base_url"]
        self.client = OpenAI(api_key=self.api_key, base_url=self.base_url)

    def chat(self, system_prompt, user_query):
        """
        基础的对话接口
        """
        try:
            response = self.client.chat.completions.create(
                model=self.model_name,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_query},
                ],
                stream=False
            )
            return response.choices[0].message.content
        except Exception as e:
            print(f"LLM Client Error ({self.model_name}): {e}")
            return f"Error: {str(e)}"

def agent_template(system_prompt, user_query, model_name=DEFAULT_MODEL_NAME):
    """
    智能体模板函数
    输入：提示词 (system_prompt)、用户输入 (user_query)、LLM名称 (model_name)
    """
    client = LLMClient(model_name=model_name)
    return client.chat(system_prompt, user_query)
