import aiohttp
import asyncio
from typing import Dict
import json
from datetime import datetime
import os
import ssl

# ANSI colors for output
PINK = "\033[95m"
YELLOW = "\033[93m"
CYAN = "\033[96m"
RESET_COLOR = "\033[0m"

class JinaReader:
    def __init__(self, api_key: str):
        self.headers = {
            'Authorization': f'Bearer {api_key}',
            'X-Return-Format': 'markdown'
        }
        # 建立 SSL context
        self.ssl_context = ssl.create_default_context()
        self.ssl_context.check_hostname = False
        self.ssl_context.verify_mode = ssl.CERT_NONE

    async def fetch_url(self, session: aiohttp.ClientSession, url: str) -> Dict:
        """非同步讀取單一 URL 的內容"""
        try:
            # 確保 URL 正確編碼
            jina_url = f'https://r.jina.ai/{url}'
            
            # 添加延遲以避免過多並發請求
            await asyncio.sleep(1)
            
            async with session.get(jina_url, headers=self.headers, ssl=self.ssl_context) as response:
                content = await response.text()
                return {
                    'url': url,
                    'content': content,
                    'status': response.status,
                    'timestamp': datetime.now().isoformat()
                }
        except Exception as e:
            return {
                'url': url,
                'content': str(e),
                'status': 'error',
                'timestamp': datetime.now().isoformat()
            }

    async def process_urls(self, urls_dict: Dict[str, str]) -> Dict:
        """處理多個 URL 並返回結果字典"""
        # 設定 connector 以處理 SSL
        connector = aiohttp.TCPConnector(ssl=self.ssl_context)
        
        async with aiohttp.ClientSession(connector=connector) as session:
            processed_results = {}
            
            # 改為循序處理而不是並行，以避免過多並發請求
            for name, url in urls_dict.items():
                print(f"{CYAN}開始處理: {name}{RESET_COLOR}")
                result = await self.fetch_url(session, url)
                
                processed_results[name] = {
                    'url': result['url'],
                    'content': result['content'],
                    'status': result['status'],
                    'timestamp': result['timestamp']
                }
                
                # 輸出處理狀態
                if result['status'] == 200:
                    print(f"{CYAN}✓ {name} 處理完成{RESET_COLOR}")
                else:
                    print(f"{PINK}✗ {name} 處理失敗: {result['status']}{RESET_COLOR}")
                
                # 在每次請求之間添加短暫延遲
                await asyncio.sleep(1)
            
            return processed_results

    def save_to_json(self, results: Dict, filename: str = None):
        """將結果儲存為 JSON 檔案"""
        if filename is None:
            filename = f"jina_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        # 確保 results 目錄存在
        os.makedirs('results', exist_ok=True)
        filepath = os.path.join('results', filename)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(results, f, ensure_ascii=False, indent=2)
        
        print(f"{CYAN}結果已儲存至: {filepath}{RESET_COLOR}")

    def print_results(self, results: Dict):
        """美化輸出結果"""
        for name, result in results.items():
            print(f"\n{YELLOW}{'='*50}{RESET_COLOR}")
            print(f"{CYAN}Name: {name}{RESET_COLOR}")
            print(f"{CYAN}URL: {result['url']}{RESET_COLOR}")
            print(f"{CYAN}Status: {result['status']}{RESET_COLOR}")
            print(f"{CYAN}Timestamp: {result['timestamp']}{RESET_COLOR}")
            content_preview = result['content'][:500] + "..." if len(result['content']) > 500 else result['content']
            print(f"{PINK}Content Preview:{RESET_COLOR}\n{content_preview}")
            print(f"{YELLOW}{'='*50}{RESET_COLOR}\n")

async def main():
    # Jina API Key
    api_key = ""
    
    # 反詐騙相關網站字典
    urls_dict = {
        "165反詐騙官網首頁": "https://165.npa.gov.tw/#/",
        "165新聞快訊": "https://165.npa.gov.tw/#/articles/1",
        "165反詐騙LINE ID資料集": "https://data.gov.tw/dataset/78432",
        "常見詐騙手法": "https://165.npa.gov.tw/#/articles/C",
        "常見問答集": "https://165.npa.gov.tw/#/articles/A",
        "165檔案下載": "https://165.npa.gov.tw/#/articles/6"
    }
    
    # 創建 JinaReader 實例
    reader = JinaReader(api_key=api_key)
    
    # 處理 URLs
    print(f"{CYAN}開始處理 URLs...{RESET_COLOR}")
    results = await reader.process_urls(urls_dict)
    
    # 輸出結果
    reader.print_results(results)
    
    # 儲存結果
    reader.save_to_json(results)

if __name__ == "__main__":
    asyncio.run(main())