"""
命令解析器模組 - 處理終端機指令輸入
"""
import re
import sys
import os
import argparse
from typing import Dict, Any, List, Optional

class CommandParser:
    """命令解析器類 - 處理使用者在終端機輸入的指令"""
    
    def __init__(self):
        """初始化命令解析器"""
        self.commands = {
            "help": self._help_command,
            "start": self._start_command,
            "stop": self._stop_command,
            "speaker": self._speaker_command,
            "summary": self._summary_command,
            "export": self._export_command,
            "exit": self._exit_command
        }
        
        # 應用狀態
        self.app_state = {
            "is_recording": False,
            "speaker_recognition_enabled": False,
            "meeting_title": "未命名會議",
            "participants": [],
            "summary_enabled": True
        }
        
        # 命令回調函數
        self.callbacks = {}
    
    def register_callback(self, command: str, callback):
        """註冊命令回調函數
        
        Args:
            command: 指令名稱
            callback: 回調函數
        """
        self.callbacks[command] = callback
    
    def parse_arguments(self):
        """解析命令行參數"""
        parser = argparse.ArgumentParser(
            description="智能會議記錄助手 - 用於記錄會議並識別說話者"
        )
        
        parser.add_argument(
            "--no-speaker",
            action="store_true",
            help="啟動時預設不啟用說話者識別"
        )
        
        parser.add_argument(
            "--title",
            type=str,
            help="會議標題"
        )
        
        parser.add_argument(
            "--participants",
            type=str,
            help="參與者列表 (逗號分隔)"
        )
        
        parser.add_argument(
            "--no-summary",
            action="store_true",
            help="不生成會議摘要和行動項目"
        )
        
        args = parser.parse_args()
        
        # 更新應用狀態
        if args.no_speaker:
            self.app_state["speaker_recognition_enabled"] = False
        
        if args.title:
            self.app_state["meeting_title"] = args.title
        
        if args.participants:
            self.app_state["participants"] = [
                p.strip() for p in args.participants.split(",") if p.strip()
            ]
        
        if args.no_summary:
            self.app_state["summary_enabled"] = False
        
        return self.app_state
    
    def process_command(self, command_line: str) -> Dict[str, Any]:
        """處理指令
        
        Args:
            command_line: 使用者輸入的指令行
            
        Returns:
            Dict: 處理結果
        """
        command_line = command_line.strip()
        
        if not command_line:
            return {"success": False, "message": "請輸入指令"}
        
        # 解析指令和參數
        parts = command_line.split(' ')
        command = parts[0].lower()
        args = parts[1:] if len(parts) > 1 else []
        
        # 尋找並執行對應的指令處理函數
        if command in self.commands:
            return self.commands[command](args)
        else:
            return {"success": False, "message": f"未知指令: {command}. 輸入 'help' 獲取幫助。"}
    
    def _help_command(self, args: List[str]) -> Dict[str, Any]:
        """顯示幫助信息
        
        Args:
            args: 指令參數
            
        Returns:
            Dict: 處理結果
        """
        help_text = """
可用指令:
  help                      - 顯示此幫助信息
  start                     - 開始錄音
  stop                      - 停止錄音
  speaker on|off           - 開啟/關閉說話者識別
  summary on|off           - 開啟/關閉會議摘要生成
  export [markdown|json]    - 匯出會議記錄
  exit                      - 退出程式
  
示例:
  speaker on                - 開啟說話者識別
  export markdown           - 匯出為Markdown格式
        """
        
        return {"success": True, "message": help_text}
    
    def _start_command(self, args: List[str]) -> Dict[str, Any]:
        """開始錄音
        
        Args:
            args: 指令參數
            
        Returns:
            Dict: 處理結果
        """
        if self.app_state["is_recording"]:
            return {"success": False, "message": "已經在錄音中"}
        
        self.app_state["is_recording"] = True
        
        # 呼叫回調函數
        if "start" in self.callbacks:
            self.callbacks["start"](self.app_state)
        
        message = "開始錄音"
        if self.app_state["speaker_recognition_enabled"]:
            message += " (說話者識別已啟用)"
        else:
            message += " (說話者識別已關閉)"
        
        return {"success": True, "message": message}
    
    def _stop_command(self, args: List[str]) -> Dict[str, Any]:
        """停止錄音
        
        Args:
            args: 指令參數
            
        Returns:
            Dict: 處理結果
        """
        if not self.app_state["is_recording"]:
            return {"success": False, "message": "尚未開始錄音"}
        
        self.app_state["is_recording"] = False
        
        # 呼叫回調函數
        if "stop" in self.callbacks:
            self.callbacks["stop"](self.app_state)
        
        return {"success": True, "message": "停止錄音"}
    
    def _speaker_command(self, args: List[str]) -> Dict[str, Any]:
        """控制說話者識別
        
        Args:
            args: 指令參數 [on|off]
            
        Returns:
            Dict: 處理結果
        """
        if not args:
            current_state = "啟用" if self.app_state["speaker_recognition_enabled"] else "關閉"
            return {"success": True, "message": f"當前說話者識別狀態: {current_state}"}
        
        action = args[0].lower()
        
        if action == "on":
            self.app_state["speaker_recognition_enabled"] = True
            
            # 呼叫回調函數
            if "speaker" in self.callbacks:
                self.callbacks["speaker"](True)
            
            return {"success": True, "message": "說話者識別已啟用"}
            
        elif action == "off":
            self.app_state["speaker_recognition_enabled"] = False
            
            # 呼叫回調函數
            if "speaker" in self.callbacks:
                self.callbacks["speaker"](False)
            
            return {"success": True, "message": "說話者識別已關閉"}
            
        else:
            return {"success": False, "message": "無效參數。使用 'speaker on' 或 'speaker off'"}
    
    def _summary_command(self, args: List[str]) -> Dict[str, Any]:
        """控制會議摘要生成
        
        Args:
            args: 指令參數 [on|off]
            
        Returns:
            Dict: 處理結果
        """
        if not args:
            current_state = "啟用" if self.app_state["summary_enabled"] else "關閉"
            return {"success": True, "message": f"當前會議摘要生成狀態: {current_state}"}
        
        action = args[0].lower()
        
        if action == "on":
            self.app_state["summary_enabled"] = True
            
            # 呼叫回調函數
            if "summary" in self.callbacks:
                self.callbacks["summary"](True)
            
            return {"success": True, "message": "會議摘要生成已啟用"}
            
        elif action == "off":
            self.app_state["summary_enabled"] = False
            
            # 呼叫回調函數
            if "summary" in self.callbacks:
                self.callbacks["summary"](False)
            
            return {"success": True, "message": "會議摘要生成已關閉"}
            
        else:
            return {"success": False, "message": "無效參數。使用 'summary on' 或 'summary off'"}
    
    def _export_command(self, args: List[str]) -> Dict[str, Any]:
        """匯出會議記錄
        
        Args:
            args: 指令參數 [markdown|json]
            
        Returns:
            Dict: 處理結果
        """
        if not self.app_state.get("meeting_processed", False):
            return {"success": False, "message": "尚未有可匯出的會議記錄。請先錄音並停止。"}
        
        format_type = "markdown"
        if args and args[0].lower() in ["markdown", "json"]:
            format_type = args[0].lower()
        
        # 呼叫回調函數
        if "export" in self.callbacks:
            result = self.callbacks["export"](format_type)
            return {"success": True, "message": f"已匯出 {format_type} 格式會議記錄", "data": result}
        
        return {"success": False, "message": "匯出功能尚未實現"}
    
    def _exit_command(self, args: List[str]) -> Dict[str, Any]:
        """退出程式
        
        Args:
            args: 指令參數
            
        Returns:
            Dict: 處理結果
        """
        # 呼叫回調函數
        if "exit" in self.callbacks:
            self.callbacks["exit"]()
        
        return {"success": True, "message": "正在退出程式...", "exit": True}
    
    def interactive_mode(self):
        """進入互動模式"""
        print("歡迎使用智能會議記錄助手!")
        print("輸入 'help' 獲取幫助，輸入 'exit' 退出程式")
        
        while True:
            try:
                command_line = input("\n> ").strip()
                
                # 處理指令
                result = self.process_command(command_line)
                
                # 顯示結果
                if "message" in result:
                    print(result["message"])
                
                # 檢查是否退出
                if result.get("exit", False):
                    break
                    
            except KeyboardInterrupt:
                print("\n程式已中斷")
                break
            except Exception as e:
                print(f"錯誤: {e}")