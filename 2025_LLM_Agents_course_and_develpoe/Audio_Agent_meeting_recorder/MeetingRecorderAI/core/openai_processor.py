"""
OpenAI 處理模組 - 直接使用 OpenAI API 生成會議摘要和提取行動項目
"""
import json
from typing import Dict, List, Any
import openai
from openai import OpenAI

class OpenAIProcessor:
    """OpenAI處理類 - 直接使用OpenAI API分析會議內容"""
    
    def __init__(self, openai_api_key: str):
        """初始化OpenAI處理器
        
        Args:
            openai_api_key: OpenAI API金鑰
        """
        self.openai_api_key = openai_api_key
        self.client = OpenAI(api_key=openai_api_key)
    
    def generate_summary(self, transcript: str) -> str:
        """生成會議摘要
        
        Args:
            transcript: 會議記錄文本
            
        Returns:
            str: 生成的摘要
        """
        print("正在使用OpenAI API生成會議摘要...")
        
        try:
            response = self.client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": """
                        你是一個專業的會議記錄助手。
                        請根據提供的會議記錄生成一個簡潔但全面的摘要。
                        摘要應包括：
                        1. 會議的主要主題
                        2. 討論的關鍵點
                        3. 達成的任何決定或結論
                        
                        請使用繁體中文回答。
                    """},
                    {"role": "user", "content": transcript}
                ],
                temperature=0.1
            )
            
            return response.choices[0].message.content
        
        except Exception as e:
            print(f"生成摘要時出錯: {e}")
            return f"由於技術問題，無法生成摘要。錯誤: {str(e)}"
    
    def extract_action_items(self, transcript: str) -> List[Dict[str, Any]]:
        """提取行動項目
        
        Args:
            transcript: 會議記錄文本
            
        Returns:
            List: 行動項目列表
        """
        print("正在使用OpenAI API提取行動項目...")
        
        try:
            system_prompt = """
            你是一個專業的會議記錄助手。請從提供的會議記錄中提取所有行動項目。
            行動項目通常是會議期間分配給特定人員的任務或責任。
            請注意任何提到的截止日期。
            
            請以JSON格式返回行動項目列表，格式如下：
            [
                {
                    "action": "需要執行的行動",
                    "assignee": "負責人，如果有指定的話",
                    "deadline": "截止日期，如果有指定的話"
                },
                ...
            ]
            
            如果沒有找到任何行動項目，請返回空列表 []。
            確保返回的JSON格式正確，可以被解析。
            請使用繁體中文回答。
            """
            
            response = self.client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": transcript}
                ],
                temperature=0.1
            )
            
            result_text = response.choices[0].message.content
            
            # 提取JSON部分
            try:
                # 尋找JSON部分的開始和結束
                start_idx = result_text.find('[')
                end_idx = result_text.rfind(']') + 1
                
                if start_idx >= 0 and end_idx > start_idx:
                    json_str = result_text[start_idx:end_idx]
                    return json.loads(json_str)
                else:
                    # 嘗試解析整個回覆
                    return json.loads(result_text)
            except json.JSONDecodeError:
                # 如果解析失敗，嘗試用更寬容的方式解析
                print(f"JSON解析失敗，原始回覆: {result_text}")
                return []
        
        except Exception as e:
            print(f"提取行動項目時出錯: {e}")
            return []
    
    def analyze_meeting(self, transcript: str) -> Dict[str, Any]:
        """分析會議記錄，生成摘要和提取行動項目
        
        Args:
            transcript: 會議記錄文本
            
        Returns:
            Dict: 包含摘要和行動項目的字典
        """
        # 先獲取摘要
        try:
            summary = self.generate_summary(transcript)
        except Exception as e:
            print(f"生成摘要過程中出錯: {e}")
            summary = f"由於技術問題，無法生成摘要。錯誤: {str(e)}"
        
        # 然後提取行動項目
        try:
            action_items = self.extract_action_items(transcript)
        except Exception as e:
            print(f"提取行動項目過程中出錯: {e}")
            action_items = []
        
        return {
            "summary": summary,
            "action_items": action_items
        }