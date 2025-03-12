# """
# 智能會議記錄助手 - 主程式
# """
# import os
# import asyncio
# import threading
# import time
# import json
# from typing import List, Dict, Any, Optional
# from dotenv import load_dotenv

# # 導入核心模組
# from core.speech_to_text import SpeechToText
# from core.speaker_recognition import SpeakerRecognition
# from core.database import ConversationDatabase
# from core.ai_processor import AIProcessor
# from core.command_parser import CommandParser

# # 載入環境變數
# load_dotenv()
# DEEPGRAM_API_KEY = os.getenv("DEEPGRAM_API_KEY")
# OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# class MeetingRecorder:
#     """會議記錄管理器類"""
    
#     def __init__(self):
#         """初始化會議記錄器"""
#         # 檢查API金鑰
#         if not DEEPGRAM_API_KEY:
#             raise ValueError("缺少DEEPGRAM_API_KEY環境變數")
#         if not OPENAI_API_KEY:
#             raise ValueError("缺少OPENAI_API_KEY環境變數")
            
#         # 初始化核心組件
#         self.speech_to_text = SpeechToText(DEEPGRAM_API_KEY)
#         self.speaker_recognition = SpeakerRecognition()
#         self.database = ConversationDatabase()
#         self.ai_processor = AIProcessor(OPENAI_API_KEY)
        
#         # 會議狀態
#         self.is_recording = False
#         self.recording_task = None
#         self.current_meeting_data = None
#         self.command_parser = CommandParser()
        
#         # 註冊命令回調
#         self._register_command_callbacks()
    
#     def _register_command_callbacks(self):
#         """註冊命令回調函數"""
#         self.command_parser.register_callback("start", self._handle_start_command)
#         self.command_parser.register_callback("stop", self._handle_stop_command)
#         self.command_parser.register_callback("speaker", self._handle_speaker_command)
#         self.command_parser.register_callback("summary", self._handle_summary_command)
#         self.command_parser.register_callback("export", self._handle_export_command)
#         self.command_parser.register_callback("exit", self._handle_exit_command)
    
#     def _handle_start_command(self, app_state: Dict[str, Any]):
#         """處理開始命令
        
#         Args:
#             app_state: 應用狀態
#         """
#         self.is_recording = True
        
#         # 設置會議信息
#         self.speaker_recognition.set_meeting_info(
#             app_state["meeting_title"],
#             app_state["participants"]
#         )
        
#         # 設置說話者識別狀態
#         self._update_speaker_recognition(app_state["speaker_recognition_enabled"])
        
#         # 開始錄音
#         self.start_recording_task()
    
#     def _handle_stop_command(self, app_state: Dict[str, Any]):
#         """處理停止命令
        
#         Args:
#             app_state: 應用狀態
#         """
#         self.is_recording = False
#         self.stop_recording_task()
        
#         # 如果有記錄到對話且啟用了摘要生成，則處理會議記錄
#         if app_state["summary_enabled"] and self.speaker_recognition.transcript_entries:
#             results = self.process_meeting_results()
#             if results:
#                 self.current_meeting_data = results["meeting_data"]
#                 self.display_meeting_report(self.current_meeting_data)
#                 self.command_parser.app_state["meeting_processed"] = True
#         else:
#             print("錄音已停止，未生成摘要")
    
#     def _handle_speaker_command(self, enabled: bool):
#         """處理說話者識別命令
        
#         Args:
#             enabled: 是否啟用說話者識別
#         """
#         self._update_speaker_recognition(enabled)
    
#     def _handle_summary_command(self, enabled: bool):
#         """處理摘要生成命令
        
#         Args:
#             enabled: 是否啟用摘要生成
#         """
#         print(f"會議摘要生成已{'啟用' if enabled else '關閉'}")
    
#     def _handle_export_command(self, format_type: str):
#         """處理匯出命令
        
#         Args:
#             format_type: 匯出格式
            
#         Returns:
#             str: 匯出檔案路徑
#         """
#         if not self.current_meeting_data:
#             return "沒有可匯出的會議記錄"
        
#         return self.export_report(self.current_meeting_data, format_type)
    
#     def _handle_exit_command(self):
#         """處理退出命令"""
#         if self.is_recording:
#             self.stop_recording_task()
    
#     def _update_speaker_recognition(self, enabled: bool):
#         """更新說話者識別設定
        
#         Args:
#             enabled: 是否啟用說話者識別
#         """
#         # 實際的說話者識別邏輯可以在這裡實現
#         print(f"說話者識別已{'啟用' if enabled else '關閉'}")
    
#     def handle_transcript(self, transcript_data: Dict[str, Any]):
#         """處理轉錄結果
        
#         Args:
#             transcript_data: 轉錄數據
#         """
#         # 如果啟用了說話者識別，則正常處理
#         if self.command_parser.app_state["speaker_recognition_enabled"]:
#             processed_entry = self.speaker_recognition.handle_transcript(transcript_data)
#         else:
#             # 否則，將所有說話者標記為未知
#             transcript_data["speaker_tag"] = None
#             processed_entry = self.speaker_recognition.handle_transcript(transcript_data)
        
#         # 檢查是否有停止指令（只檢查最終結果）
#         if transcript_data.get("is_final", False):
#             text = transcript_data.get("text", "").lower()
            
#             # 檢查是否包含停止關鍵詞
#             stop_keywords = ["停止", "停止錄音", "結束", "結束錄音", "stop", "end"]
#             for keyword in stop_keywords:
#                 if keyword in text:
#                     print(f"檢測到停止指令: '{text}'")
#                     # 使用命令解析器停止錄音
#                     self.command_parser.process_command("stop")
#                     break
    
#     async def start_recording(self):
#         """開始錄音"""
#         self.speaker_recognition.reset()
#         await self.speech_to_text.start_recording(self.handle_transcript)
    
#     def start_recording_task(self):
#         """在背景啟動錄音任務"""
#         def run_async_recording():
#             loop = asyncio.new_event_loop()
#             asyncio.set_event_loop(loop)
#             try:
#                 loop.run_until_complete(self.start_recording())
#             finally:
#                 loop.close()
        
#         print("\n開始錄音...")
#         print("說「停止錄音」或使用 'stop' 指令停止錄音")
        
#         self.recording_task = threading.Thread(target=run_async_recording, daemon=True)
#         self.recording_task.start()
    
#     def stop_recording_task(self):
#         """停止錄音任務"""
#         if not self.is_recording:
#             return
        
#         print("\n正在停止錄音...")
#         self.is_recording = False
        
#         # 設置speech_to_text的狀態為非錄音
#         self.speech_to_text.is_recording = False
        
#         # 不要嘗試在這裡異步停止錄音
#         # 讓錄音線程自己處理結束流程
        
#         # 只是等待錄音線程結束
#         if self.recording_task and self.recording_task.is_alive():
#             # 設置最大等待時間，避免永久等待
#             self.recording_task.join(timeout=5)
#             if self.recording_task.is_alive():
#                 print("警告: 錄音線程未能及時結束")
#             self.recording_task = None
    
#     def process_meeting_results(self):
#         """處理會議結果，生成摘要和行動項目"""
#         print("\n處理會議記錄中...")
        
#         # 確保Deepgram連接已完全關閉，但不要嘗試在這裡再次關閉它
#         # 只是確認一下狀態
#         if hasattr(self.speech_to_text, 'is_recording') and self.speech_to_text.is_recording:
#             print("警告: 錄音似乎仍在進行中，可能會導致連接問題")
        
#         # 獲取完整記錄文本
#         transcript_text = self.speaker_recognition.get_formatted_transcript()
        
#         if not transcript_text.strip():
#             print("錄音結果為空，無法生成分析")
#             return None
        
#         # 使用try-except包裝AI處理部分
#         try:
#             # 使用AI處理器分析會議
#             analysis_results = self.ai_processor.analyze_meeting(transcript_text)
#         except Exception as e:
#             print(f"分析會議記錄時出錯: {e}")
#             import traceback
#             traceback.print_exc()
#             # 提供一個默認值
#             analysis_results = {
#                 "summary": "由於技術問題，無法生成摘要。",
#                 "action_items": []
#             }
        
#         # 獲取會議數據
#         transcript_entries = self.speaker_recognition.get_full_transcript()
#         speaker_statistics = self.speaker_recognition.get_speaker_statistics()
#         duration = self.speaker_recognition.get_meeting_duration()
        
#         # 創建會議記錄模式
#         meeting_data = self.database.create_meeting_schema(
#             title=self.command_parser.app_state["meeting_title"],
#             participants=self.command_parser.app_state["participants"],
#             transcript_entries=transcript_entries,
#             speaker_statistics=speaker_statistics,
#             duration=duration,
#             summary=analysis_results["summary"],
#             action_items=analysis_results["action_items"]
#         )
        
#         # 保存到資料庫
#         try:
#             file_path = self.database.save_meeting(meeting_data)
#             meeting_data["file_path"] = file_path
#         except Exception as e:
#             print(f"保存會議記錄時出錯: {e}")
#             import traceback
#             traceback.print_exc()
#             file_path = None
#             meeting_data["file_path"] = "由於錯誤，未能保存檔案"
        
#         return {
#             "meeting_data": meeting_data,
#             "file_path": file_path
#         }
    
#     def display_meeting_report(self, meeting_data: Dict[str, Any]):
#         """顯示會議報告
        
#         Args:
#             meeting_data: 會議數據
#         """
#         print("\n" + "="*50)
#         print(f"會議報告: {meeting_data['title']}")
#         print("="*50)
        
#         print(f"日期: {meeting_data.get('date', '未知')}")
#         print(f"時間: {meeting_data.get('start_time', '未知')}")
#         print(f"持續時間: {meeting_data.get('duration', '未知')}")
#         print(f"參與者: {', '.join(meeting_data.get('participants', ['未知']))}")
        
#         print("\n--- 摘要 ---")
#         print(meeting_data.get("summary", "未生成摘要"))
        
#         print("\n--- 行動項目 ---")
#         for i, item in enumerate(meeting_data.get("action_items", []), 1):
#             assignee = f" (@{item.get('assignee', '未分配')})" if item.get('assignee') else ""
#             deadline = f" - 截止日期: {item.get('deadline')}" if item.get('deadline') else ""
#             print(f"{i}. {item.get('action')}{assignee}{deadline}")
        
#         print("\n--- 說話者統計 ---")
#         for speaker, stats in meeting_data.get("speaker_statistics", {}).items():
#             print(f"{speaker}:")
#             print(f"  發言次數: {stats['sentences']}")
#             print(f"  總字數: {stats['total_words']}")
#             print(f"  發言時間: {stats['speaking_time']:.1f} 秒")
        
#         print("\n會議記錄已保存至:", meeting_data.get("file_path", "未知"))
#         print("="*50)
#         print("\n輸入 'export markdown' 或 'export json' 可匯出報告")
    
#     def export_report(self, meeting_data: Dict[str, Any], format: str = "markdown"):
#         """匯出會議報告
        
#         Args:
#             meeting_data: 會議數據
#             format: 匯出格式 ("markdown" 或 "json")
            
#         Returns:
#             str: 匯出檔案路徑
#         """
#         content = self.database.export_meeting_record(meeting_data, format)
        
#         # 構建檔案名稱
#         title_slug = meeting_data.get("title", "未命名會議").replace(" ", "_")
#         date_str = meeting_data.get("date", time.strftime("%Y%m%d"))
#         ext = "md" if format == "markdown" else "json"
#         file_name = f"{title_slug}_{date_str}.{ext}"
        
#         # 寫入檔案
#         with open(file_name, "w", encoding="utf-8") as f:
#             f.write(content)
        
#         print(f"已匯出 {format.upper()} 報告至: {file_name}")
#         return file_name
    
#     def run_interactive(self):
#         """運行互動模式"""
#         try:
#             # 解析命令行參數
#             initial_state = self.command_parser.parse_arguments()
            
#             # 獲取會議基本信息
#             if not initial_state.get("meeting_title") or not initial_state.get("participants"):
#                 title = input("請輸入會議標題 (預設: 未命名會議): ").strip() or "未命名會議"
#                 participants = input("請輸入參與者 (用逗號分隔): ").strip()
                
#                 self.command_parser.app_state["meeting_title"] = title
#                 self.command_parser.app_state["participants"] = [
#                     p.strip() for p in participants.split(",") if p.strip()
#                 ]
            
#             # 執行互動模式
#             self.command_parser.interactive_mode()
            
#         except KeyboardInterrupt:
#             print("\n程序已中斷")
#         except Exception as e:
#             print(f"\n錯誤: {e}")
#         finally:
#             # 確保錄音已停止
#             if self.is_recording:
#                 self.stop_recording_task()
#             print("\n程序結束")

# def main():
#     """主程序"""
#     # 歡迎信息
#     print("="*60)
#     print("                智能會議記錄助手")
#     print("      自動記錄會議內容，識別說話者，並生成摘要")
#     print("="*60)
    
#     # 檢查環境變數
#     if not DEEPGRAM_API_KEY or not OPENAI_API_KEY:
#         print("錯誤: 請在 .env 檔案中設定 DEEPGRAM_API_KEY 和 OPENAI_API_KEY")
#         return
    
#     # 初始化並運行記錄器
#     recorder = MeetingRecorder()
#     recorder.run_interactive()

# if __name__ == "__main__":
#     # 運行主程序
#     main()

"""
智能會議記錄助手 - 主程式
"""
import os
import asyncio
import threading
import time
import json
from typing import List, Dict, Any, Optional
from dotenv import load_dotenv

# 導入核心模組
from core.speech_to_text import SpeechToText
from core.speaker_recognition import SpeakerRecognition
from core.database import ConversationDatabase
# 使用新的OpenAI處理器替代原有的AI處理器
from core.openai_processor import OpenAIProcessor
from core.command_parser import CommandParser

# 載入環境變數
load_dotenv()
DEEPGRAM_API_KEY = os.getenv("DEEPGRAM_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

class MeetingRecorder:
    """會議記錄管理器類"""
    
    def __init__(self):
        """初始化會議記錄器"""
        # 檢查API金鑰
        if not DEEPGRAM_API_KEY:
            raise ValueError("缺少DEEPGRAM_API_KEY環境變數")
        if not OPENAI_API_KEY:
            raise ValueError("缺少OPENAI_API_KEY環境變數")
            
        # 初始化核心組件
        self.speech_to_text = SpeechToText(DEEPGRAM_API_KEY)
        self.speaker_recognition = SpeakerRecognition()
        self.database = ConversationDatabase()
        # 使用新的OpenAI處理器
        self.ai_processor = OpenAIProcessor(OPENAI_API_KEY)
        
        # 會議狀態
        self.is_recording = False
        self.recording_task = None
        self.current_meeting_data = None
        self.command_parser = CommandParser()
        
        # 註冊命令回調
        self._register_command_callbacks()
    
    def _register_command_callbacks(self):
        """註冊命令回調函數"""
        self.command_parser.register_callback("start", self._handle_start_command)
        self.command_parser.register_callback("stop", self._handle_stop_command)
        self.command_parser.register_callback("speaker", self._handle_speaker_command)
        self.command_parser.register_callback("summary", self._handle_summary_command)
        self.command_parser.register_callback("export", self._handle_export_command)
        self.command_parser.register_callback("exit", self._handle_exit_command)
    
    def _handle_start_command(self, app_state: Dict[str, Any]):
        """處理開始命令
        
        Args:
            app_state: 應用狀態
        """
        self.is_recording = True
        
        # 設置會議信息
        self.speaker_recognition.set_meeting_info(
            app_state["meeting_title"],
            app_state["participants"]
        )
        
        # 設置說話者識別狀態
        self._update_speaker_recognition(app_state["speaker_recognition_enabled"])
        
        # 開始錄音
        self.start_recording_task()
    
    def _handle_stop_command(self, app_state: Dict[str, Any]):
        """處理停止命令
        
        Args:
            app_state: 應用狀態
        """
        self.is_recording = False
        self.stop_recording_task()
        
        # 如果有記錄到對話且啟用了摘要生成，則處理會議記錄
        if app_state["summary_enabled"] and self.speaker_recognition.transcript_entries:
            results = self.process_meeting_results()
            if results:
                self.current_meeting_data = results["meeting_data"]
                self.display_meeting_report(self.current_meeting_data)
                self.command_parser.app_state["meeting_processed"] = True
        else:
            print("錄音已停止，未生成摘要")
    
    def _handle_speaker_command(self, enabled: bool):
        """處理說話者識別命令
        
        Args:
            enabled: 是否啟用說話者識別
        """
        self._update_speaker_recognition(enabled)
    
    def _handle_summary_command(self, enabled: bool):
        """處理摘要生成命令
        
        Args:
            enabled: 是否啟用摘要生成
        """
        print(f"會議摘要生成已{'啟用' if enabled else '關閉'}")
    
    def _handle_export_command(self, format_type: str):
        """處理匯出命令
        
        Args:
            format_type: 匯出格式
            
        Returns:
            str: 匯出檔案路徑
        """
        if not self.current_meeting_data:
            return "沒有可匯出的會議記錄"
        
        return self.export_report(self.current_meeting_data, format_type)
    
    def _handle_exit_command(self):
        """處理退出命令"""
        if self.is_recording:
            self.stop_recording_task()
    
    def _update_speaker_recognition(self, enabled: bool):
        """更新說話者識別設定
        
        Args:
            enabled: 是否啟用說話者識別
        """
        print(f"說話者識別已{'啟用' if enabled else '關閉'}")
    
    def handle_transcript(self, transcript_data: Dict[str, Any]):
        """處理轉錄結果
        
        Args:
            transcript_data: 轉錄數據
        """
        # 如果啟用了說話者識別，則正常處理
        if self.command_parser.app_state["speaker_recognition_enabled"]:
            processed_entry = self.speaker_recognition.handle_transcript(transcript_data)
        else:
            # 否則，將所有說話者標記為未知
            transcript_data["speaker_tag"] = None
            processed_entry = self.speaker_recognition.handle_transcript(transcript_data)
        
        # 檢查是否有停止指令（只檢查最終結果）
        if transcript_data.get("is_final", False):
            text = transcript_data.get("text", "").lower()
            
            # 檢查是否包含停止關鍵詞
            stop_keywords = ["停止", "停止錄音", "結束", "結束錄音", "stop", "end"]
            for keyword in stop_keywords:
                if keyword in text:
                    print(f"檢測到停止指令: '{text}'")
                    # 使用命令解析器停止錄音
                    self.command_parser.process_command("stop")
                    break
    
    async def start_recording(self):
        """開始錄音"""
        self.speaker_recognition.reset()
        await self.speech_to_text.start_recording(self.handle_transcript)
    
    def start_recording_task(self):
        """在背景啟動錄音任務"""
        def run_async_recording():
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            try:
                loop.run_until_complete(self.start_recording())
            finally:
                loop.close()
        
        print("\n開始錄音...")
        print("說「停止錄音」或使用 'stop' 指令停止錄音")
        
        self.recording_task = threading.Thread(target=run_async_recording, daemon=True)
        self.recording_task.start()
    
    def stop_recording_task(self):
        """停止錄音任務"""
        if not self.is_recording:
            return
        
        print("\n正在停止錄音...")
        self.is_recording = False
        
        # 設置speech_to_text的狀態為非錄音
        if hasattr(self.speech_to_text, 'is_recording'):
            self.speech_to_text.is_recording = False
        
        # 只是等待錄音線程結束
        if self.recording_task and self.recording_task.is_alive():
            # 設置最大等待時間，避免永久等待
            self.recording_task.join(timeout=5)
            if self.recording_task.is_alive():
                print("警告: 錄音線程未能及時結束")
            self.recording_task = None
    
    def process_meeting_results(self):
        """處理會議結果，生成摘要和行動項目"""
        print("\n處理會議記錄中...")
        
        # 獲取完整記錄文本
        transcript_text = self.speaker_recognition.get_formatted_transcript()
        
        if not transcript_text.strip():
            print("錄音結果為空，無法生成分析")
            return None
        
        # 使用try-except包裝AI處理部分
        try:
            # 使用AI處理器分析會議
            analysis_results = self.ai_processor.analyze_meeting(transcript_text)
        except Exception as e:
            print(f"分析會議記錄時出錯: {e}")
            import traceback
            traceback.print_exc()
            # 提供一個默認值
            analysis_results = {
                "summary": "由於技術問題，無法生成摘要。",
                "action_items": []
            }
        
        # 獲取會議數據
        transcript_entries = self.speaker_recognition.get_full_transcript()
        speaker_statistics = self.speaker_recognition.get_speaker_statistics()
        duration = self.speaker_recognition.get_meeting_duration()
        
        # 創建會議記錄模式
        meeting_data = self.database.create_meeting_schema(
            title=self.command_parser.app_state["meeting_title"],
            participants=self.command_parser.app_state["participants"],
            transcript_entries=transcript_entries,
            speaker_statistics=speaker_statistics,
            duration=duration,
            summary=analysis_results["summary"],
            action_items=analysis_results["action_items"]
        )
        
        # 保存到資料庫
        try:
            file_path = self.database.save_meeting(meeting_data)
            meeting_data["file_path"] = file_path
        except Exception as e:
            print(f"保存會議記錄時出錯: {e}")
            import traceback
            traceback.print_exc()
            file_path = None
            meeting_data["file_path"] = "由於錯誤，未能保存檔案"
        
        return {
            "meeting_data": meeting_data,
            "file_path": file_path
        }
    
    def display_meeting_report(self, meeting_data: Dict[str, Any]):
        """顯示會議報告
        
        Args:
            meeting_data: 會議數據
        """
        print("\n" + "="*50)
        print(f"會議報告: {meeting_data['title']}")
        print("="*50)
        
        print(f"日期: {meeting_data.get('date', '未知')}")
        print(f"時間: {meeting_data.get('start_time', '未知')}")
        print(f"持續時間: {meeting_data.get('duration', '未知')}")
        print(f"參與者: {', '.join(meeting_data.get('participants', ['未知']))}")
        
        print("\n--- 摘要 ---")
        print(meeting_data.get("summary", "未生成摘要"))
        
        print("\n--- 行動項目 ---")
        for i, item in enumerate(meeting_data.get("action_items", []), 1):
            assignee = f" (@{item.get('assignee', '未分配')})" if item.get('assignee') else ""
            deadline = f" - 截止日期: {item.get('deadline')}" if item.get('deadline') else ""
            print(f"{i}. {item.get('action')}{assignee}{deadline}")
        
        print("\n--- 說話者統計 ---")
        for speaker, stats in meeting_data.get("speaker_statistics", {}).items():
            print(f"{speaker}:")
            print(f"  發言次數: {stats['sentences']}")
            print(f"  總字數: {stats['total_words']}")
            print(f"  發言時間: {stats['speaking_time']:.1f} 秒")
        
        print("\n會議記錄已保存至:", meeting_data.get("file_path", "未知"))
        print("="*50)
        print("\n輸入 'export markdown' 或 'export json' 可匯出報告")
    
    def export_report(self, meeting_data: Dict[str, Any], format: str = "markdown"):
        """匯出會議報告
        
        Args:
            meeting_data: 會議數據
            format: 匯出格式 ("markdown" 或 "json")
            
        Returns:
            str: 匯出檔案路徑
        """
        content = self.database.export_meeting_record(meeting_data, format)
        
        # 構建檔案名稱
        title_slug = meeting_data.get("title", "未命名會議").replace(" ", "_")
        date_str = meeting_data.get("date", time.strftime("%Y%m%d"))
        ext = "md" if format == "markdown" else "json"
        file_name = f"{title_slug}_{date_str}.{ext}"
        
        # 寫入檔案
        with open(file_name, "w", encoding="utf-8") as f:
            f.write(content)
        
        print(f"已匯出 {format.upper()} 報告至: {file_name}")
        return file_name
    
    def run_interactive(self):
        """運行互動模式"""
        try:
            # 解析命令行參數
            initial_state = self.command_parser.parse_arguments()
            
            # 獲取會議基本信息
            if not initial_state.get("meeting_title") or not initial_state.get("participants"):
                title = input("請輸入會議標題 (預設: 未命名會議): ").strip() or "未命名會議"
                participants = input("請輸入參與者 (用逗號分隔): ").strip()
                
                self.command_parser.app_state["meeting_title"] = title
                self.command_parser.app_state["participants"] = [
                    p.strip() for p in participants.split(",") if p.strip()
                ]
            
            # 執行互動模式
            self.command_parser.interactive_mode()
            
        except KeyboardInterrupt:
            print("\n程序已中斷")
        except Exception as e:
            print(f"\n錯誤: {e}")
            import traceback
            traceback.print_exc()
        finally:
            # 確保錄音已停止
            if self.is_recording:
                self.stop_recording_task()
            print("\n程序結束")

def main():
    """主程序"""
    # 歡迎信息
    print("="*60)
    print("                智能會議記錄助手")
    print("      自動記錄會議內容，識別說話者，並生成摘要")
    print("="*60)
    
    # 檢查環境變數
    if not DEEPGRAM_API_KEY or not OPENAI_API_KEY:
        print("錯誤: 請在 .env 檔案中設定 DEEPGRAM_API_KEY 和 OPENAI_API_KEY")
        return
    
    # 初始化並運行記錄器
    recorder = MeetingRecorder()
    recorder.run_interactive()

if __name__ == "__main__":
    # 運行主程序
    main()