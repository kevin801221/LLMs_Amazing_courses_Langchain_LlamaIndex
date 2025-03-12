"""
資料庫模組 - 負責儲存和讀取會議記錄
"""
import os
import json
import datetime
import uuid
from typing import List, Dict, Any, Optional

class ConversationDatabase:
    """對話資料庫管理類"""
    
    def __init__(self, db_directory: str = "./conversation_db"):
        """初始化對話資料庫
        
        Args:
            db_directory: 儲存JSON檔案的目錄
        """
        self.db_directory = db_directory
        
        # 確保資料庫目錄存在
        if not os.path.exists(db_directory):
            os.makedirs(db_directory)
    
    def save_meeting(self, meeting_data: Dict[str, Any]) -> str:
        """將會議資料儲存為JSON檔案
        
        Args:
            meeting_data: 包含會議資訊的字典
            
        Returns:
            str: 儲存的檔案路徑
        """
        # 確保會議有一個唯一ID
        if 'meeting_id' not in meeting_data:
            meeting_data['meeting_id'] = str(uuid.uuid4())
        
        # 確保有時間戳記
        if 'timestamp' not in meeting_data:
            meeting_data['timestamp'] = datetime.datetime.now().isoformat()
        
        # 構建檔案名稱：meeting_日期_ID.json
        date_str = datetime.datetime.now().strftime("%Y%m%d")
        file_name = f"meeting_{date_str}_{meeting_data['meeting_id']}.json"
        file_path = os.path.join(self.db_directory, file_name)
        
        # 寫入JSON檔案
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(meeting_data, f, ensure_ascii=False, indent=2)
        
        print(f"已儲存會議記錄至: {file_path}")
        return file_path
    
    def load_meeting(self, meeting_id: str) -> Optional[Dict[str, Any]]:
        """根據會議ID載入會議資料
        
        Args:
            meeting_id: 會議唯一識別ID
            
        Returns:
            Dict 或 None: 會議資料字典，若未找到則回傳None
        """
        # 列出資料庫目錄中的所有檔案
        for file_name in os.listdir(self.db_directory):
            if file_name.endswith('.json') and meeting_id in file_name:
                file_path = os.path.join(self.db_directory, file_name)
                with open(file_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
        
        print(f"找不到會議ID: {meeting_id}")
        return None
    
    def list_meetings(self, start_date: Optional[str] = None, 
                      end_date: Optional[str] = None) -> List[Dict[str, Any]]:
        """列出指定日期範圍內的所有會議
        
        Args:
            start_date: 起始日期 (格式: YYYY-MM-DD)
            end_date: 結束日期 (格式: YYYY-MM-DD)
            
        Returns:
            List: 符合條件的會議概要列表
        """
        meetings = []
        
        # 轉換日期字串為datetime對象進行比較
        start_datetime = None
        end_datetime = None
        
        if start_date:
            start_datetime = datetime.datetime.strptime(start_date, "%Y-%m-%d")
        if end_date:
            # 設為當天結束
            end_datetime = datetime.datetime.strptime(end_date, "%Y-%m-%d")
            end_datetime = end_datetime.replace(hour=23, minute=59, second=59)
        
        # 列出所有JSON檔案
        for file_name in os.listdir(self.db_directory):
            if file_name.endswith('.json'):
                file_path = os.path.join(self.db_directory, file_name)
                
                with open(file_path, 'r', encoding='utf-8') as f:
                    meeting_data = json.load(f)
                
                # 檢查日期範圍
                if 'timestamp' in meeting_data:
                    meeting_time = datetime.datetime.fromisoformat(meeting_data['timestamp'])
                    
                    if start_datetime and meeting_time < start_datetime:
                        continue
                    if end_datetime and meeting_time > end_datetime:
                        continue
                
                # 只添加摘要信息，而非完整會議記錄
                meetings.append({
                    'meeting_id': meeting_data.get('meeting_id', ''),
                    'title': meeting_data.get('title', '未命名會議'),
                    'timestamp': meeting_data.get('timestamp', ''),
                    'duration': meeting_data.get('duration', ''),
                    'participants': meeting_data.get('participants', []),
                    'has_summary': 'summary' in meeting_data
                })
        
        # 按時間戳排序，最新的在前
        meetings.sort(key=lambda x: x.get('timestamp', ''), reverse=True)
        return meetings

    def create_meeting_schema(self, 
                             title: str,
                             participants: List[str],
                             transcript_entries: List[Dict[str, Any]],
                             speaker_statistics: Dict[str, Dict[str, Any]],
                             duration: str,
                             summary: Optional[str] = None,
                             action_items: Optional[List[Dict[str, Any]]] = None) -> Dict[str, Any]:
        """創建標準的會議記錄JSON結構
        
        Args:
            title: 會議標題
            participants: 參與者列表
            transcript_entries: 轉錄記錄列表
            speaker_statistics: 說話者統計數據
            duration: 會議持續時間
            summary: 會議摘要
            action_items: 行動項目列表
            
        Returns:
            Dict: 格式化的會議記錄字典
        """
        meeting_id = str(uuid.uuid4())
        now = datetime.datetime.now()
        
        # 構建會議記錄結構
        meeting_data = {
            "meeting_id": meeting_id,
            "title": title,
            "timestamp": now.isoformat(),
            "date": now.strftime("%Y-%m-%d"),
            "start_time": now.strftime("%H:%M:%S"),
            "duration": duration,
            "participants": participants,
            "transcript": transcript_entries,
            "speaker_statistics": speaker_statistics,
        }
        
        # 添加摘要信息（如果有）
        if summary:
            meeting_data["summary"] = summary
        
        # 添加行動項目（如果有）
        if action_items:
            meeting_data["action_items"] = action_items
        
        return meeting_data

    def export_meeting_record(self, meeting_data: Dict[str, Any], 
                              format: str = "markdown") -> str:
        """匯出會議記錄為特定格式
        
        Args:
            meeting_data: 會議資料字典
            format: 匯出格式 ("markdown" 或 "json")
            
        Returns:
            str: 格式化的會議記錄內容
        """
        title = meeting_data.get("title", "未命名會議")
        date = meeting_data.get("date", "未知日期")
        duration = meeting_data.get("duration", "未知")
        participants = meeting_data.get("participants", [])
        summary = meeting_data.get("summary", "未生成摘要")
        action_items = meeting_data.get("action_items", [])
        transcript = meeting_data.get("transcript", [])
        speakers = meeting_data.get("speaker_statistics", {})
        
        if format == "markdown":
            # 生成Markdown格式的會議記錄
            md_content = f"# {title}\n\n"
            md_content += f"日期: {date}\n"
            md_content += f"持續時間: {duration}\n"
            md_content += f"參與者: {', '.join(participants)}\n\n"
            
            md_content += "## 摘要\n\n"
            md_content += f"{summary}\n\n"
            
            md_content += "## 行動項目\n\n"
            for item in action_items:
                assignee = f" (@{item.get('assignee', '未分配')})" if item.get('assignee') else ""
                deadline = f" - 截止日期: {item.get('deadline')}" if item.get('deadline') else ""
                md_content += f"- {item.get('action')}{assignee}{deadline}\n"
            
            md_content += "\n## 說話者統計\n\n"
            for speaker, stats in speakers.items():
                md_content += f"### {speaker}\n"
                md_content += f"- 發言次數: {stats['sentences']}\n"
                md_content += f"- 總字數: {stats['total_words']}\n"
                md_content += f"- 發言時間: {stats['speaking_time']:.1f} 秒\n\n"
            
            md_content += "## 完整記錄\n\n"
            md_content += "```\n"
            # 格式化記錄
            for entry in transcript:
                md_content += f"[{entry['timestamp']}] {entry['speaker']}: {entry['text']}\n"
            md_content += "```\n"
            
            return md_content
        
        elif format == "json":
            # 直接返回JSON字符串
            return json.dumps(meeting_data, ensure_ascii=False, indent=2)
        
        else:
            return "不支持的格式"