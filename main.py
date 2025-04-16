import logging
import re
import json
import pytz
import dingtalk_stream
import uuid
from config import knowledge_message, qwen_model, agent, client_id, client_secret
from dingtalk_stream import AckMessage
 
# 日志配置
def setup_logger():
    logger = logging.getLogger()
    handler = logging.StreamHandler()
    handler.setFormatter(
        logging.Formatter('%(asctime)s %(name)-8s %(levelname)-8s %(message)s [%(filename)s:%(lineno)d]'))
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)
    return logger
 
 
class mychatBot_Handler(dingtalk_stream.ChatbotHandler):
    def __init__(self, logger: logging.Logger = None):
        super().__init__()
        if logger:
            self.logger = logger
 
    async def process(self, callback: dingtalk_stream.CallbackMessage):
        incoming_message = dingtalk_stream.ChatbotMessage.from_dict(callback.data)
        agent.update_memory(knowledge_message, "user")
        assistant_response = agent.step(incoming_message.text.content)
        res_content = assistant_response.msgs[0].content
        self.reply_markdown("机器人回复", res_content, incoming_message)
        return AckMessage.STATUS_OK, 'OK'
 
 
def main():
    logger = setup_logger()
    credential = dingtalk_stream.Credential(client_id, client_secret)
    client = dingtalk_stream.DingTalkStreamClient(credential)
    client.register_callback_handler(dingtalk_stream.chatbot.ChatbotMessage.TOPIC, mychatBot_Handler(logger))
    client.start_forever()
 
 
if __name__ == '__main__':
    main()
