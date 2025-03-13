# """
# 智能會議記錄助手 - 主程式
# """
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
        """處理會議結果，生成摘要和行動項目
        
        Returns:
            Dict: 包含會議數據的字典
        """
        # 獲取會議記錄
        transcript_entries = self.speaker_recognition.transcript_entries
        
        if not transcript_entries:
            print("沒有記錄到任何對話")
            return None
        
        # 計算會議時長
        start_time = transcript_entries[0]["timestamp"]
        end_time = transcript_entries[-1]["timestamp"]
        duration = end_time - start_time
        
        # 計算每個說話者的統計數據
        speaker_statistics = {}
        for entry in transcript_entries:
            speaker = entry.get("speaker", "未知")
            if speaker not in speaker_statistics:
                speaker_statistics[speaker] = {
                    "speech_count": 0,
                    "total_words": 0,
                    "total_duration": 0
                }
            
            speaker_statistics[speaker]["speech_count"] += 1
            speaker_statistics[speaker]["total_words"] += len(entry["text"].split())
            # 假設每個條目有持續時間，如果沒有則假設為0
            speaker_statistics[speaker]["total_duration"] += entry.get("duration", 0)
        
        # 將記錄格式化為純文本
        transcript_text = ""
        for entry in transcript_entries:
            speaker = entry.get("speaker", "未知")
            timestamp = time.strftime("%H:%M:%S", time.localtime(entry["timestamp"]))
            transcript_text += f"[{timestamp}] {speaker}: {entry['text']}\n"
        
        # 使用AI處理器分析會議記錄
        try:
            # 使用OpenAI處理器進行更詳細的分析
            analysis_results = self.ai_processor.analyze_meeting(transcript_text)
            
            # 增強分析結果：添加關鍵主題分析
            try:
                key_topics = self.ai_processor.extract_key_topics(transcript_text)
                analysis_results["key_topics"] = key_topics
            except Exception as e:
                print(f"提取關鍵主題時出錯: {e}")
                analysis_results["key_topics"] = []
            
            # 增強分析結果：添加情感分析
            try:
                sentiment_analysis = self.ai_processor.analyze_sentiment(transcript_text)
                analysis_results["sentiment"] = sentiment_analysis
            except Exception as e:
                print(f"進行情感分析時出錯: {e}")
                analysis_results["sentiment"] = {"overall": "中性"}
            
            # 增強分析結果：添加決策點分析
            try:
                decisions = self.ai_processor.extract_decisions(transcript_text)
                analysis_results["decisions"] = decisions
            except Exception as e:
                print(f"提取決策點時出錯: {e}")
                analysis_results["decisions"] = []
                
        except Exception as e:
            print(f"分析會議記錄時出錯: {e}")
            import traceback
            traceback.print_exc()
            # 提供一個默認值
            analysis_results = {
                "summary": "無法生成摘要",
                "action_items": [],
                "key_topics": [],
                "sentiment": {"overall": "未知"},
                "decisions": []
            }
        
        # 創建會議數據
        meeting_data = {
            "meeting_title": self.command_parser.app_state["meeting_title"],
            "timestamp": time.time(),
            "date": time.strftime("%Y-%m-%d", time.localtime()),
            "participants": self.command_parser.app_state["participants"],
            "transcript_entries": transcript_entries,
            "speaker_statistics": speaker_statistics,
            "duration": duration,
            "summary": analysis_results["summary"],
            "action_items": analysis_results.get("action_items", []),
            "key_topics": analysis_results.get("key_topics", []),
            "sentiment": analysis_results.get("sentiment", {"overall": "中性"}),
            "decisions": analysis_results.get("decisions", [])
        }
        
        # 保存會議數據到數據庫
        try:
            self.database.save_meeting(meeting_data)
            print("會議記錄已保存到數據庫")
        except Exception as e:
            print(f"保存會議記錄到數據庫時出錯: {e}")
        
        return {"meeting_data": meeting_data}
    
    def display_meeting_report(self, meeting_data: Dict[str, Any]):
        """顯示會議報告
        
        Args:
            meeting_data: 會議數據
        """
        print("\n" + "="*60)
        print(f"會議報告: {meeting_data['meeting_title']}")
        print("="*60)
        
        # 顯示基本信息
        print(f"日期: {meeting_data['date']}")
        print(f"時長: {int(meeting_data['duration'] // 60)}分{int(meeting_data['duration'] % 60)}秒")
        print(f"參與者: {', '.join(meeting_data['participants'])}")
        print("\n" + "-"*60)
        
        # 顯示摘要
        print("會議摘要:")
        print(meeting_data['summary'])
        print("\n" + "-"*60)
        
        # 顯示關鍵主題
        if "key_topics" in meeting_data and meeting_data["key_topics"]:
            print("關鍵主題:")
            for topic in meeting_data["key_topics"]:
                print(f"• {topic}")
            print("\n" + "-"*60)
        
        # 顯示決策點
        if "decisions" in meeting_data and meeting_data["decisions"]:
            print("決策點:")
            for decision in meeting_data["decisions"]:
                print(f"• {decision}")
            print("\n" + "-"*60)
        
        # 顯示行動項目
        if meeting_data['action_items']:
            print("行動項目:")
            for item in meeting_data['action_items']:
                assignee = f"({item['assignee']})" if item.get('assignee') else ""
                deadline = f"截止日期: {item['deadline']}" if item.get('deadline') else ""
                print(f"• {item['action']} {assignee} {deadline}")
            print("\n" + "-"*60)
        else:
            print("沒有發現行動項目")
            print("\n" + "-"*60)
        
        # 顯示情感分析
        if "sentiment" in meeting_data:
            print(f"整體情感: {meeting_data['sentiment'].get('overall', '中性')}")
            if "details" in meeting_data["sentiment"]:
                print("詳細情感分析:")
                for detail in meeting_data["sentiment"]["details"]:
                    print(f"• {detail}")
            print("\n" + "-"*60)
        
        # 顯示說話者統計
        print("說話者統計:")
        for speaker, stats in meeting_data['speaker_statistics'].items():
            print(f"• {speaker}: {stats['speech_count']}次發言, {stats['total_words']}個詞")
        
        print("\n" + "="*60)
        print("會議記錄已保存。使用 'export' 命令匯出完整報告。")
        print("="*60 + "\n")
    
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