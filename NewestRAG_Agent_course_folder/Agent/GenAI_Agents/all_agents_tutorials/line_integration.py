import os
from linebot import LineBotApi
from linebot.models import TextSendMessage
from langdetect import detect
from langconv import Converter

class LineMessenger:
    def __init__(self):
        self.line_bot_api = LineBotApi(os.getenv('LINE_CHANNEL_ACCESS_TOKEN'))

    def convert_to_traditional_chinese(self, text):
        if detect(text) == 'zh-cn':
            return Converter('zh-hant').convert(text)
        return text

    def send_message(self, message):
        traditional_chinese_msg = self.convert_to_traditional_chinese(message)
        message_obj = TextSendMessage(text=traditional_chinese_msg)
        self.line_bot_api.push_message(os.getenv('LINE_USER_ID'), message_obj)
