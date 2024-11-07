import requests
from typing import Dict, Any

class WolframAPI:
    """Wolfram API 處理類"""
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "http://api.wolframalpha.com/v2/query"
    
    def query(self, input_text: str, params: Dict[str, Any] = None) -> Dict[str, Any]:
        """執行 API 查詢"""
        default_params = {
            "appid": self.api_key,
            "input": input_text,
            "format": "plaintext,image",
            "output": "json"
        }
        if params:
            default_params.update(params)
            
        try:
            response = requests.get(self.base_url, params=default_params)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            return {"error": str(e)}
    
    def format_result(self, result: Dict[str, Any]) -> Dict[str, Any]:
        """格式化 API 響應結果"""
        if "error" in result:
            return {"error": result["error"]}
            
        try:
            queryresult = result.get("queryresult", {})
            pods = queryresult.get("pods", [])
            
            formatted_result = {
                "success": queryresult.get("success", False),
                "pods": []
            }
            
            for pod in pods:
                pod_data = {
                    "title": pod.get("title", ""),
                    "content": []
                }
                
                for subpod in pod.get("subpods", []):
                    if "plaintext" in subpod:
                        pod_data["content"].append(subpod["plaintext"])
                    if "img" in subpod:
                        pod_data["content"].append(subpod["img"]["src"])
                        
                formatted_result["pods"].append(pod_data)
                
            return formatted_result
        except Exception as e:
            return {"error": f"結果解析錯誤: {str(e)}"}