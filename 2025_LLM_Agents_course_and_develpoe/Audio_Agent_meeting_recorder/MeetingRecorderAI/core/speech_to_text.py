"""
語音轉文字模組 - 負責處理音訊輸入並轉換為文字
"""
import os
import asyncio
import datetime
from typing import Callable, Dict, Any, Optional
from deepgram import (
    DeepgramClient,
    DeepgramClientOptions,
    LiveOptions,
    LiveTranscriptionEvents,
    Microphone
)

class SpeechToText:
    """語音轉文字處理類"""
    
    def __init__(self, api_key: str):
        """初始化語音轉文字處理器
        
        Args:
            api_key: Deepgram API金鑰
        """
        self.api_key = api_key
        self.is_recording = False
        self.microphone = None
        self.dg_connection = None
        
    async def start_recording(self, callback: Callable[[Dict[str, Any]], None]):
        """開始錄音並進行實時轉錄"""
        self.is_recording = True
        
        try:
            # 設置Deepgram客戶端
            dg_config = DeepgramClientOptions(options={"keepalive": "true"})
            deepgram = DeepgramClient(self.api_key, dg_config)
            self.dg_connection = deepgram.listen.asynclive.v("1")
            
            # 轉錄回調函數
            async def on_message(self, result, **kwargs):
                if not result.channel.alternatives[0].transcript.strip():
                    return
                    
                # 獲取轉錄文本
                sentence = result.channel.alternatives[0].transcript
                
                # 獲取信心值
                confidence = 0
                if hasattr(result.channel.alternatives[0], 'confidence'):
                    confidence = result.channel.alternatives[0].confidence
                
                # 創建當前時間戳
                timestamp = datetime.datetime.now().strftime("%H:%M:%S")
                timestamp_iso = datetime.datetime.now().isoformat()
                
                # 獲取說話者標籤（如果有）
                speaker_tag = None
                if hasattr(result.channel, 'metadata') and hasattr(result.channel.metadata, 'speaker'):
                    speaker_tag = result.channel.metadata.speaker
                
                # 創建轉錄結果對象
                transcript_data = {
                    "timestamp": timestamp,
                    "timestamp_iso": timestamp_iso,
                    "speaker_tag": speaker_tag,
                    "text": sentence,
                    "confidence": confidence,
                    "is_final": result.speech_final
                }
                
                # 調用回調函數
                callback(transcript_data)
            
            # 錯誤處理回調
            async def on_error(self, error, **kwargs):
                print(f"錯誤: {error}")
            
            # 註冊事件處理
            self.dg_connection.on(LiveTranscriptionEvents.Transcript, on_message)
            self.dg_connection.on(LiveTranscriptionEvents.Error, on_error)
            
            # 配置轉錄選項
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
            await self.dg_connection.start(options)
            
            # 啟動麥克風
            self.microphone = Microphone(self.dg_connection.send)
            self.microphone.start()
            
            # 保持執行直到停止錄音
            while self.is_recording:
                await asyncio.sleep(0.1)
                
        except Exception as e:
            print(f"錄音過程中發生錯誤: {e}")
        finally:
            # 確保資源被釋放
            try:
                if self.microphone:
                    self.microphone.finish()
                    self.microphone = None
                    
                if self.dg_connection:
                    await self.dg_connection.finish()
                    self.dg_connection = None
            except Exception as e:
                print(f"關閉錄音資源時發生錯誤: {e}")
            
            self.is_recording = False
            print("錄音已停止")
    
    @staticmethod
    async def process_audio_file(api_key: str, audio_file_path: str, 
                                num_speakers: Optional[int] = None):
        """處理預先錄製的音頻文件
        
        Args:
            api_key: Deepgram API金鑰
            audio_file_path: 音頻文件路徑
            num_speakers: 預估說話者數量
            
        Returns:
            Dict: Deepgram API的響應
        """
        try:
            from deepgram import PrerecordedOptions
            
            deepgram = DeepgramClient(api_key)
            
            # 讀取音頻文件
            with open(audio_file_path, "rb") as audio:
                audio_data = audio.read()
                
            # 配置轉錄選項
            options = PrerecordedOptions(
                model="nova-2",
                language="zh-TW",
                smart_format=True,
                diarize=True,
                summarize=True,
                detect_topics=True,
                utterances=True
            )
            
            if num_speakers:
                options.diarize_version = "latest"
                options.diarize_num_speakers = num_speakers
            
            # 執行轉錄
            response = deepgram.listen.prerecorded.v("1").transcribe_file(
                {"buffer": audio_data}, 
                options
            )
            
            return response
            
        except Exception as e:
            print(f"音頻文件處理錯誤: {e}")
            return None