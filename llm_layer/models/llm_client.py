import os
import time
from abc import ABC, abstractmethod
from openai import OpenAI

class BaseLLMClient(ABC):
    @abstractmethod
    def chat(self, system_prompt, user_input):
        pass

class OnlineLLMClient(BaseLLMClient):
    def __init__(self, api_key, base_url, model):
        self.client = OpenAI(api_key=api_key, base_url=base_url)
        self.model = model

    def chat(self, system_prompt, user_input):
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_input},
                ],
                stream=False
            )
            return response.choices[0].message.content
        except Exception as e:
            print(f"Online LLM Error: {e}")
            return None

def get_llm_client(config):
    # 统一采用SDK即openai通讯协议的方式加载模型
    return OnlineLLMClient(
        api_key=config.ONLINE_API_KEY,
        base_url=config.ONLINE_BASE_URL,
        model=config.ONLINE_MODEL
    )

