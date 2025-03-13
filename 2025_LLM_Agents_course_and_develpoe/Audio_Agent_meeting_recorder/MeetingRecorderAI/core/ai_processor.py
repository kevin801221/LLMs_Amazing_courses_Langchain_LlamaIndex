"""
AI處理模組 - 負責生成會議摘要和提取行動項目
"""
from typing import Dict, List, Any, Optional
from langchain_openai import ChatOpenAI
from langchain.prompts import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate
)
from langchain.chains import create_extraction_chain
from langchain_core.output_parsers import StrOutputParser
from pydantic import BaseModel, Field  # 添加 Pydantic 導入

class AIProcessor:
    """AI處理類 - 負責使用GPT-4o分析會議內容"""
    
    def __init__(self, openai_api_key: str):
        """初始化AI處理器
        
        Args:
            openai_api_key: OpenAI API金鑰
        """
        self.llm = ChatOpenAI(
            model="gpt-4o",
            api_key=openai_api_key,
            temperature=0.1
        )
    
    def generate_summary(self, transcript: str) -> str:
        """生成會議摘要
        
        Args:
            transcript: 會議記錄文本
            
        Returns:
            str: 生成的摘要
        """
        print("正在生成會議摘要...")
        
        system = SystemMessagePromptTemplate.from_template(
            """
            你是一個專業的會議記錄助手。
            請根據提供的會議記錄生成一個簡潔但全面的摘要。
            摘要應包括：
            1. 會議的主要主題
            2. 討論的關鍵點
            3. 達成的任何決定或結論
            
            請使用繁體中文回答。
            """
        )
        human = HumanMessagePromptTemplate.from_template("{text}")
        
        prompt = ChatPromptTemplate.from_messages([
            system,
            human
        ])
        
        chain = prompt | self.llm | StrOutputParser()
        
        response = chain.invoke({"text": transcript})
        
        return response
    
    def extract_action_items(self, transcript: str) -> List[Dict[str, Any]]:
        """提取行動項目"""
        print("正在提取行動項目...")
        
        # 定義輸出結構
        class ActionItem(BaseModel):
            action: str = Field(description="需要執行的行動")
            assignee: Optional[str] = Field(None, description="負責人，如果有指定的話")
            deadline: Optional[str] = Field(None, description="截止日期，如果有指定的話")
        
        class ActionItems(BaseModel):
            action_items: List[ActionItem]
        
        # 使用新的結構化輸出方法
        structured_llm = self.llm.with_structured_output(ActionItems)
        
        system_prompt = """
        你是一個專業的會議記錄助手。
        請從提供的會議記錄中提取所有行動項目。
        行動項目通常是會議期間分配給特定人員的任務或責任。
        請注意任何提到的截止日期。
        
        請使用繁體中文回答。
        """
        
        messages = [
            ("system", system_prompt),
            ("human", transcript)
        ]
        
        result = structured_llm.invoke(messages)
        return result.action_items
    
    def analyze_meeting(self, transcript: str) -> Dict[str, Any]:
        """分析會議記錄，生成摘要和提取行動項目
        
        Args:
            transcript: 會議記錄文本
            
        Returns:
            Dict: 包含摘要和行動項目的字典
        """
        try:
            summary = self.generate_summary(transcript)
            action_items = self.extract_action_items(transcript)
            
            return {
                "summary": summary,
                "action_items": action_items
            }
        except Exception as e:
            print(f"分析會議記錄時出錯: {e}")
            import traceback
            traceback.print_exc()
            # 提供一個默認值
            return {
                "summary": "無法生成摘要",
                "action_items": []
            }
# 在處理會議結果的方法中添加錯誤處理
# try:
#     analysis_results = self.ai_processor.analyze_meeting(transcript_text)
# except Exception as e:
#     print(f"分析會議記錄時出錯: {e}")
#     import traceback
#     traceback.print_exc()
#     # 提供一個默認值
#     analysis_results = {
#         "summary": "無法生成摘要",
#         "action_items": []
#     }