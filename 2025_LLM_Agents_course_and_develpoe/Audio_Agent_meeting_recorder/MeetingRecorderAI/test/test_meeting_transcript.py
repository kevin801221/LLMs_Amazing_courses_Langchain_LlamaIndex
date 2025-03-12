import os
import asyncio
from dotenv import load_dotenv
from deepgram import (
    DeepgramClient,
    DeepgramClientOptions,
    LiveOptions,
    LiveTranscriptionEvents,
    Microphone
)

# 載入環境變數
load_dotenv()
API_KEY = os.getenv("DEEPGRAM_API_KEY")

# 創建一個簡單的回調函數來顯示轉錄結果
async def process_audio():
    print("開始錄音和即時轉寫...")
    
    # 設置 Deepgram 客戶端
    dg_config = DeepgramClientOptions(options={"keepalive": "true"})
    deepgram = DeepgramClient(API_KEY, dg_config)
    dg_connection = deepgram.listen.asynclive.v("1")
    
    # 轉錄收到時的處理函數
    async def on_message(self, result, **kwargs):
        # 只在句子完成時輸出
        if result.speech_final:
            sentence = result.channel.alternatives[0].transcript
            if sentence.strip():
                print(f"轉錄: {sentence}")
                
                # 如果有說話者信息則顯示
                if hasattr(result.channel, 'metadata') and hasattr(result.channel.metadata, 'speaker'):
                    speaker_tag = result.channel.metadata.speaker
                    print(f"說話者: {speaker_tag}")
    
    # 錯誤處理函數
    async def on_error(self, error, **kwargs):
        print(f"錯誤: {error}")
    
    # 註冊事件處理函數
    dg_connection.on(LiveTranscriptionEvents.Transcript, on_message)
    dg_connection.on(LiveTranscriptionEvents.Error, on_error)
    
    # 設置轉錄選項
    options = LiveOptions(
        model="nova-2",
        language="zh-TW",
        encoding="linear16",
        channels=1,
        sample_rate=16000,
        smart_format=True,
        diarize=True,
        endpointing=380,
        interim_results=True
    )
    
    # 啟動連接
    await dg_connection.start(options)
    
    # 啟動麥克風
    microphone = Microphone(dg_connection.send)
    microphone.start()
    
    # 繼續錄音直到按下 Ctrl+C
    try:
        print("開始錄音中... 請說話 (按 Ctrl+C 停止)")
        while True:
            await asyncio.sleep(0.1)
    except KeyboardInterrupt:
        print("\n停止錄音...")
    finally:
        # 清理資源
        microphone.finish()
        await dg_connection.finish()
        print("錄音已結束")

# 運行測試
if __name__ == "__main__":
    asyncio.run(process_audio())