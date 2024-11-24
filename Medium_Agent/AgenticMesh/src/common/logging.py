# src/common/logging.py
import logging
import sys
from pathlib import Path
from datetime import datetime
from typing import Optional
import json

class AgentLogger:
    """集中式代理日誌系統"""
    
    def __init__(self, name: str, log_dir: Optional[str] = None):
        self.name = name
        self.log_dir = Path(log_dir) if log_dir else Path("logs")
        self.log_dir.mkdir(parents=True, exist_ok=True)
        
        # 創建logger
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.DEBUG)
        
        # 創建文件處理器
        log_file = self.log_dir / f"{name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
        file_handler = logging.FileHandler(log_file, encoding='utf-8')
        file_handler.setLevel(logging.DEBUG)
        
        # 創建控制台處理器
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(logging.INFO)
        
        # 設置格式
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)
        
        # 添加處理器
        self.logger.addHandler(file_handler)
        self.logger.addHandler(console_handler)
        
    def log_agent_action(self, action_type: str, details: dict):
        """記錄代理行為"""
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "action": action_type,
            "details": details
        }
        self.logger.info(json.dumps(log_entry))
        
    def log_collaboration(self, agent_id: str, action: str, status: str, details: dict):
        """記錄協作行為"""
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "agent_id": agent_id,
            "action": action,
            "status": status,
            "details": details
        }
        self.logger.info(json.dumps(log_entry))
        
    def log_error(self, error_type: str, error_message: str, details: dict = None):
        """記錄錯誤"""
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "error_type": error_type,
            "error_message": error_message,
            "details": details or {}
        }
        self.logger.error(json.dumps(log_entry))

# 創建全局logger實例
agent_logger = AgentLogger("agent_system")