# encoding:utf-8

import json
import logging
import os
import pickle
import copy
import asyncio
from pydantic import BaseModel, Field
from camel.loaders import Firecrawl
from camel.configs import QwenConfig, MistralConfig
from camel.models import ModelFactory
from camel.types import ModelPlatformType, ModelType
from camel.models.openai_compatible_model import OpenAICompatibleModel
from camel.agents import ChatAgent
from camel.messages import BaseMessage
import asyncio
from crawl4ai import AsyncWebCrawler, CacheMode

client_id = "dingi1yzricklujz9rji" 
client_secret = "8NHYRiKFqxzpE4b9uHIvrEKtDNr6WBD_jEzlMM1AzR-_WaF32KchG2VSNOrkKYcB"

qwen_model = ModelFactory.create(
            model_platform=ModelPlatformType.OPENAI_COMPATIBLE_MODEL,
            model_type="Qwen/Qwen2.5-32B-Instruct",
            api_key="9b16f530-adcd-4711-a998-20e070d1265d",
            url="https://api-inference.modelscope.cn/v1",
            model_config_dict=QwenConfig(temperature=0.2).as_dict(),
        )
agent = ChatAgent(
            system_message="You're a helpful assistant",
            message_window_size=10,
            model=qwen_model
        )
async def search():
    async with AsyncWebCrawler(verbose=True) as crawler:
        result = await crawler.arun(url="https://help.aliyun.com/zh/model-studio/getting-started/what-is-model-studio?spm=a2c4g.11186623.help-menu-2400256.d_0_0.41f9253asmiZKt&scm=20140722.H_2579562._.OR_help-T_cn~zh-V_1")
        # Soone will be change to result.markdown
        return result
    

knowledge = asyncio.run(search()).markdown
knowledge_message = BaseMessage.make_user_message(
            role_name="User", content=f"Based on the following knowledge: {knowledge}"
        )
# print(knowledge)
# 全局配置，用于存放全局生效的状态
    
    
# # 配置 API 密钥
# os.environ["FIRECRAWL_API_KEY"] = "YOUR API"
# # 爬取知识并存储到本地
# os.makedirs('local_data', exist_ok=True)
# firecrawl = Firecrawl()
# knowledge = firecrawl.crawl(url="Knowledge base URL")
# with open('local_data/qdrant_overview.md', 'w') as file:
#     file.write(knowledge["data"][0]["markdown"])
# qwen_model = ModelFactory.create(
#             model_platform=ModelPlatformType.OPENAI_COMPATIBLE_MODEL,
#             model_type="Qwen/Qwen2.5-32B-Instruct",
#             api_key="YOUR API",
#             url="Model path",
#             model_config_dict=QwenConfig(temperature=0.2).as_dict(),
#         )
# agent = ChatAgent(
#             system_message="You're a helpful assistant",
#             message_window_size=10,
#             model=qwen_model
#         )
