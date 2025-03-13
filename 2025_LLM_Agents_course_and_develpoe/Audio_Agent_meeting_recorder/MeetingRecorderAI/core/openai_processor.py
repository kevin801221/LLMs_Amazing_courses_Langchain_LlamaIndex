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
                        請根據提供的會議記錄生成一個詳細且結構化的摘要。
                        摘要應包括：
                        1. 會議的主要主題和目的
                        2. 討論的關鍵點和重要議題
                        3. 達成的任何決定或結論
                        4. 主要參與者的關鍵觀點
                        5. 未解決的問題或需要進一步討論的事項
                        
                        請使用繁體中文回答，並以清晰的段落和條點式列表組織內容，使摘要易於閱讀和理解。
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
            請注意任何提到的截止日期、優先級和負責人。
            
            請以JSON格式返回行動項目列表，格式如下：
            [
                {
                    "action": "需要執行的行動",
                    "assignee": "負責人，如果有指定的話",
                    "deadline": "截止日期，如果有指定的話",
                    "priority": "優先級，如果有指定的話（高/中/低）"
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
    
    def extract_key_topics(self, transcript: str) -> List[str]:
        """提取會議中討論的關鍵主題
        
        Args:
            transcript: 會議記錄文本
            
        Returns:
            List[str]: 關鍵主題列表
        """
        print("正在使用OpenAI API提取關鍵主題...")
        
        try:
            system_prompt = """
            你是一個專業的會議記錄助手。請從提供的會議記錄中提取5-10個關鍵主題或討論點。
            這些主題應該是會議中重點討論的內容，按重要性排序。
            
            請以JSON格式返回主題列表，格式如下：
            ["主題1", "主題2", "主題3", ...]
            
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
                # 如果解析失敗，嘗試提取文本形式的主題
                print(f"JSON解析失敗，嘗試提取文本形式的主題: {result_text}")
                # 簡單地按行分割並清理
                lines = [line.strip() for line in result_text.split('\n') if line.strip()]
                # 過濾掉非主題行（例如標題、說明等）
                topics = [line.strip('•- ') for line in lines if line.strip('•- ')]
                return topics[:10]  # 最多返回10個主題
        
        except Exception as e:
            print(f"提取關鍵主題時出錯: {e}")
            return []
    
    def analyze_sentiment(self, transcript: str) -> Dict[str, Any]:
        """分析會議的整體情感和氛圍
        
        Args:
            transcript: 會議記錄文本
            
        Returns:
            Dict: 情感分析結果
        """
        print("正在使用OpenAI API分析會議情感...")
        
        try:
            system_prompt = """
            你是一個專業的會議記錄助手。請分析提供的會議記錄的整體情感和氛圍。
            
            請以JSON格式返回分析結果，格式如下：
            {
                "overall": "整體情感（積極/中性/消極）",
                "details": [
                    "具體情感觀察點1",
                    "具體情感觀察點2",
                    ...
                ],
                "tone": "會議的語調（正式/非正式/混合）",
                "engagement": "參與度評估（高/中/低）"
            }
            
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
                start_idx = result_text.find('{')
                end_idx = result_text.rfind('}') + 1
                
                if start_idx >= 0 and end_idx > start_idx:
                    json_str = result_text[start_idx:end_idx]
                    return json.loads(json_str)
                else:
                    # 嘗試解析整個回覆
                    return json.loads(result_text)
            except json.JSONDecodeError:
                # 如果解析失敗，返回簡單的結果
                print(f"JSON解析失敗，原始回覆: {result_text}")
                return {"overall": "中性", "details": ["無法解析詳細情感分析"]}
        
        except Exception as e:
            print(f"分析情感時出錯: {e}")
            return {"overall": "未知", "details": [f"分析過程中出錯: {str(e)}"]}
    
    def extract_decisions(self, transcript: str) -> List[str]:
        """提取會議中做出的決策
        
        Args:
            transcript: 會議記錄文本
            
        Returns:
            List[str]: 決策列表
        """
        print("正在使用OpenAI API提取決策點...")
        
        try:
            system_prompt = """
            你是一個專業的會議記錄助手。請從提供的會議記錄中提取所有做出的決策或達成的結論。
            這些決策應該是會議中明確同意或決定的事項。
            
            請以JSON格式返回決策列表，格式如下：
            ["決策1", "決策2", "決策3", ...]
            
            如果沒有找到任何明確的決策，請返回空列表 []。
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
                # 如果解析失敗，嘗試提取文本形式的決策
                print(f"JSON解析失敗，嘗試提取文本形式的決策: {result_text}")
                # 簡單地按行分割並清理
                lines = [line.strip() for line in result_text.split('\n') if line.strip()]
                # 過濾掉非決策行（例如標題、說明等）
                decisions = [line.strip('•- ') for line in lines if line.strip('•- ')]
                return decisions
        
        except Exception as e:
            print(f"提取決策點時出錯: {e}")
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
        
        # 提取關鍵主題
        try:
            key_topics = self.extract_key_topics(transcript)
        except Exception as e:
            print(f"提取關鍵主題過程中出錯: {e}")
            key_topics = []
        
        # 分析情感
        try:
            sentiment = self.analyze_sentiment(transcript)
        except Exception as e:
            print(f"分析情感過程中出錯: {e}")
            sentiment = {"overall": "中性"}
        
        # 提取決策點
        try:
            decisions = self.extract_decisions(transcript)
        except Exception as e:
            print(f"提取決策點過程中出錯: {e}")
            decisions = []
        
        return {
            "summary": summary,
            "action_items": action_items,
            "key_topics": key_topics,
            "sentiment": sentiment,
            "decisions": decisions
        }