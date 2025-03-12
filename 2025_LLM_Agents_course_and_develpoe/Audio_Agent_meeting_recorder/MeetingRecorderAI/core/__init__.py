"""
核心模組初始化檔案
"""
# 使用絕對導入避免問題
from core.speech_to_text import SpeechToText
from core.speaker_recognition import SpeakerRecognition
from core.database import ConversationDatabase
from core.ai_processor import AIProcessor
from core.command_parser import CommandParser

__all__ = [
    'SpeechToText',
    'SpeakerRecognition',
    'ConversationDatabase',
    'AIProcessor',
    'CommandParser'
]