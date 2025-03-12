# 測試導入
import sys
print("Python 路徑:", sys.path)

try:
    from core.speaker_recognition import SpeakerRecognition
    print("成功導入 SpeakerRecognition 類!")
except ImportError as e:
    print(f"導入失敗: {e}")