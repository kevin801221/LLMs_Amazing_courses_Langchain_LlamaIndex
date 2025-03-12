"""
說話者識別模組 - 負責識別不同的說話者並管理會議轉錄內容
"""
import datetime
from typing import Dict, List, Any, Optional

class SpeakerRecognition:
    """說話者識別和會議記錄管理類"""
    
    def __init__(self):
        """初始化說話者識別器"""
        self.speaker_profiles = {}  # 說話者標籤到ID的映射
        self.current_speaker_id = 0  # 當前最大說話者ID
        
        # 會議記錄相關
        self.transcript_entries = []  # 完整轉錄記錄
        self.current_sentence_parts = []  # 當前句子的部分
        self.current_speaker = None  # 當前說話者
        
        # 會議元數據
        self.meeting_title = "未命名會議"
        self.participants = []
        self.meeting_start_time = datetime.datetime.now()
        self.meeting_summary = None
        self.action_items = []
    
    def assign_speaker_id(self, speaker_tag: str) -> str:
        """將Deepgram說話者標籤映射到人類可讀的ID
        
        Args:
            speaker_tag: Deepgram返回的說話者標籤
            
        Returns:
            str: 分配的說話者ID (如 "說話者 1")
        """
        if not speaker_tag:
            return "未知說話者"
            
        if speaker_tag not in self.speaker_profiles:
            self.current_speaker_id += 1
            self.speaker_profiles[speaker_tag] = f"說話者 {self.current_speaker_id}"
        
        return self.speaker_profiles[speaker_tag]
    
    def handle_transcript(self, transcript_data: Dict[str, Any]) -> Dict[str, Any]:
        """處理轉錄結果，更新內部狀態
        
        Args:
            transcript_data: 轉錄數據
            
        Returns:
            Dict: 處理後的轉錄條目
        """
        # 提取數據
        text = transcript_data.get("text", "")
        speaker_tag = transcript_data.get("speaker_tag")
        is_final = transcript_data.get("is_final", False)
        timestamp = transcript_data.get("timestamp", datetime.datetime.now().strftime("%H:%M:%S"))
        timestamp_iso = transcript_data.get("timestamp_iso", datetime.datetime.now().isoformat())
        confidence = transcript_data.get("confidence", 0)
        
        # 分配說話者ID
        if speaker_tag:
            speaker_id = self.assign_speaker_id(speaker_tag)
            self.current_speaker = speaker_id
        else:
            speaker_id = self.current_speaker if self.current_speaker else "未知說話者"
        
        # 創建轉錄條目
        entry = {
            "timestamp": timestamp,
            "timestamp_iso": timestamp_iso,
            "speaker": speaker_id,
            "text": text,
            "confidence": confidence,
            "speaker_tag": speaker_tag  # 保留原始標籤用於調試
        }
        
        # 根據是否是最終結果決定處理方式
        if not is_final:
            # 非最終結果，保存到當前句子部分
            self.current_sentence_parts.append(text)
        else:
            # 最終結果，添加到完整記錄
            if text.strip():
                self.transcript_entries.append(entry)
                print(f"{speaker_id}: {text}")
            
            # 清空當前句子部分
            self.current_sentence_parts = []
        
        return entry
    
    def get_full_transcript(self) -> List[Dict[str, Any]]:
        """獲取完整轉錄記錄
        
        Returns:
            List: 轉錄條目列表
        """
        return self.transcript_entries
    
    def get_formatted_transcript(self) -> str:
        """獲取格式化的完整轉錄文本
        
        Returns:
            str: 格式化的轉錄文本
        """
        formatted = []
        for entry in self.transcript_entries:
            formatted.append(f"[{entry['timestamp']}] {entry['speaker']}: {entry['text']}")
        return "\n".join(formatted)
    
    def get_speaker_statistics(self) -> Dict[str, Dict[str, Any]]:
        """計算說話者統計數據
        
        Returns:
            Dict: 說話者統計字典
        """
        stats = {}
        
        for entry in self.transcript_entries:
            speaker = entry.get('speaker', '未知說話者')
            text = entry.get('text', '')
            
            if speaker not in stats:
                stats[speaker] = {
                    "sentences": 0,
                    "total_words": 0,
                    "speaking_time": 0
                }
            
            # 更新統計
            stats[speaker]["sentences"] += 1
            word_count = len(text.split())
            stats[speaker]["total_words"] += word_count
            # 估算說話時間 (假設平均每個單詞0.5秒)
            stats[speaker]["speaking_time"] += word_count * 0.5
        
        return stats
    
    def get_meeting_duration(self) -> str:
        """獲取會議持續時間
        
        Returns:
            str: 格式化的會議持續時間
        """
        duration = datetime.datetime.now() - self.meeting_start_time
        minutes, seconds = divmod(duration.seconds, 60)
        hours, minutes = divmod(minutes, 60)
        return f"{hours:02d}:{minutes:02d}:{seconds:02d}"
    
    def set_meeting_info(self, title: str, participants: List[str]):
        """設置會議信息
        
        Args:
            title: 會議標題
            participants: 參與者列表
        """
        self.meeting_title = title
        self.participants = participants
        
    def reset(self):
        """重置所有會議數據"""
        self.transcript_entries = []
        self.current_sentence_parts = []
        self.current_speaker = None
        self.meeting_start_time = datetime.datetime.now()
        self.meeting_summary = None
        self.action_items = []