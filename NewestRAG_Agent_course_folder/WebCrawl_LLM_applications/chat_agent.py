import os
import json
import time
from dotenv import load_dotenv
from openai import OpenAI
from firecrawl import FirecrawlApp
from termcolor import colored
from transformers import AutoTokenizer
import logging
import traceback

# 設定詳細的日誌記錄
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("scraper_debug.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# 載入環境變數
load_dotenv()
logger.info("環境變數已載入")

# 變更為地端 Ollama deepseek-r1:8b
MODEL = "deepseek-r1:8b"
OLLAMA_API_URL = "http://localhost:11434/v1/chat/completions"  # 修改為本地端 API
logger.info(f"使用模型: {MODEL}, API URL: {OLLAMA_API_URL}")

# 讀取 Firecrawl API Key
FIRECRAWL_API_KEY = os.getenv("FIRECRAWL_API_KEY")
if not FIRECRAWL_API_KEY:
    logger.error("找不到 FIRECRAWL_API_KEY 環境變數")
    raise ValueError("FIRECRAWL_API_KEY is required")
else:
    logger.info("Firecrawl API Key 已讀取成功")

# 設定目標公司與其網站
company = "Discord"
website = "https://discord.com"
logger.info(f"目標公司: {company}, 網站: {website}")

# 需要抓取的數據點，每個數據點包含名稱、值（初始化為 None）和參考來源
data_points = [
    {"name": "catering_offering_for_employees", "value": None, "reference": None},
    {"name": "num_employees", "value": None, "reference": None},
    {"name": "office_locations", "value": None, "reference": None},
]
logger.info(f"需要抓取的數據點: {[dp['name'] for dp in data_points]}")

def get_data_keys():
    """
    取得尚未獲取數據的數據點名稱列表
    """
    missing_keys = [obj["name"] for obj in data_points if obj["value"] is None]
    logger.info(f"尚未找到的數據點: {missing_keys}")
    return missing_keys

def update_data_point(name, value, reference):
    """
    更新找到的數據點
    """
    for dp in data_points:
        if dp["name"] == name and dp["value"] is None:
            dp["value"] = value
            dp["reference"] = reference
            logger.info(f"已更新數據點: {name} = {value} (來源: {reference})")
            return True
    return False

def scrape(url):
    """
    使用 Firecrawl 進行網頁爬取，並回傳爬取的內容。
    """
    logger.info(f"開始爬取URL: {url}")
    try:
        app = FirecrawlApp(api_key=FIRECRAWL_API_KEY)
        logger.debug("Firecrawl 實例已創建")
        
        start_time = time.time()
        scraped_data = app.scrape_url(url)
        end_time = time.time()
        
        logger.info(f"爬取完成，耗時: {end_time - start_time:.2f}秒")
        logger.debug(f"爬取資料類型: {type(scraped_data)}")
        
        # 如果回傳的數據是字典且包含 markdown 格式的內容，則回傳 markdown
        if isinstance(scraped_data, dict) and "markdown" in scraped_data:
            content_preview = scraped_data["markdown"][:200] + "..." if len(scraped_data["markdown"]) > 200 else scraped_data["markdown"]
            logger.info(f"爬取到 markdown 內容，預覽: {content_preview}")
            return scraped_data["markdown"]
        
        # 如果是其他類型，轉為字串
        content_preview = str(scraped_data)[:200] + "..." if len(str(scraped_data)) > 200 else str(scraped_data)
        logger.info(f"爬取到一般內容，預覽: {content_preview}")
        return str(scraped_data)
    except Exception as error:
        logger.error(f"爬取URL失敗: {url}")
        logger.error(f"異常詳情: {error}")
        logger.error(traceback.format_exc())
        return f"Error scraping {url}: {str(error)}"

def chunk_data(data, max_tokens):
    """
    將長文本拆分成較小的部分，以符合模型的 token 限制。
    """
    logger.info(f"開始分割數據，數據長度: {len(str(data))}")
    
    if not isinstance(data, str):
        logger.warning(f"數據不是字串類型，而是 {type(data)}，轉換為字串")
        data = str(data)
    
    chunks = [data[i:i + max_tokens] for i in range(0, len(data), max_tokens)]
    logger.info(f"數據已分割為 {len(chunks)} 個區塊")
    
    for i, chunk in enumerate(chunks):
        logger.debug(f"區塊 {i+1} 長度: {len(chunk)}")
    
    return chunks

def create_tool_message(url, chunk, tool_call_id):
    """
    格式化工具返回的訊息，供 AI 解析。
    """
    logger.debug(f"為工具呼叫 {tool_call_id} 創建回應訊息")
    message = {
        "role": "tool",
        "content": json.dumps({
            "url": url,
            "scraped_data": chunk,
        }),
        "tool_call_id": tool_call_id,
    }
    logger.debug(f"工具回應訊息已創建，URL: {url}, 內容長度: {len(chunk)}")
    return message

def extract_findings_from_response(response_content):
    """
    從 AI 回應中提取發現的數據點
    """
    logger.info("從AI回應中提取數據")
    
    # 尋找可能的數據點更新
    found_data = {}
    
    try:
        # 試著解析 JSON 格式的回應
        if response_content.strip().startswith('{') and response_content.strip().endswith('}'):
            try:
                json_data = json.loads(response_content)
                logger.info("發現JSON格式回應")
                
                for key in [dp["name"] for dp in data_points]:
                    if key in json_data and json_data[key]:
                        found_data[key] = json_data[key]
                        logger.info(f"從JSON中找到數據: {key} = {json_data[key]}")
            except json.JSONDecodeError:
                logger.warning("JSON解析失敗，將使用文本分析")
        
        # 如果沒有找到JSON或JSON解析失敗，嘗試從文本中解析
        if not found_data:
            lines = response_content.split("\n")
            
            for line in lines:
                for dp in data_points:
                    key = dp["name"]
                    if key in line.lower() and ":" in line:
                        value = line.split(":", 1)[1].strip()
                        found_data[key] = value
                        logger.info(f"從文本中找到數據: {key} = {value}")
        
        return found_data
    except Exception as e:
        logger.error(f"提取數據時發生錯誤: {e}")
        logger.error(traceback.format_exc())
        return {}

def call_ollama(messages):
    """
    與本地端 Ollama deepseek-r1:8b 進行對話。
    """
    logger.info(f"發送請求給 Ollama，訊息數量: {len(messages)}")
    try:
        import requests
        
        # 顯示發送給模型的消息
        for i, msg in enumerate(messages[-3:] if len(messages) > 3 else messages):
            role = msg.get("role", "unknown")
            content_preview = str(msg.get("content", ""))[:100] + "..." if len(str(msg.get("content", ""))) > 100 else str(msg.get("content", ""))
            logger.debug(f"訊息 {i+1} - 角色: {role}, 內容預覽: {content_preview}")
        
        start_time = time.time()
        response = requests.post(
            OLLAMA_API_URL,
            json={"model": MODEL, "messages": messages}
        )
        end_time = time.time()
        
        logger.info(f"Ollama 回應時間: {end_time - start_time:.2f}秒")
        
        if response.status_code != 200:
            logger.error(f"Ollama API 返回錯誤狀態碼: {response.status_code}")
            logger.error(f"錯誤內容: {response.text}")
            return {"error": response.text}
        
        response_data = response.json()
        
        if "choices" in response_data and len(response_data["choices"]) > 0:
            content_preview = response_data["choices"][0]["message"].get("content", "")[:100] + "..." if len(response_data["choices"][0]["message"].get("content", "")) > 100 else response_data["choices"][0]["message"].get("content", "")
            logger.info(f"Ollama 回應內容預覽: {content_preview}")
        else:
            logger.warning("Ollama 回應中沒有 choices 或是 choices 為空")
        
        return response_data
    except Exception as e:
        logger.error(f"調用 Ollama 時發生錯誤: {e}")
        logger.error(traceback.format_exc())
        return {"error": str(e)}

def process_additional_urls(current_messages, max_iterations=3):
    """
    處理 AI 建議的其他 URL
    """
    iterations = 0
    findings = {}
    
    while iterations < max_iterations and get_data_keys():
        iterations += 1
        logger.info(f"開始額外 URL 處理迭代 {iterations}/{max_iterations}")
        
        # 請求 AI 推薦更多 URL
        suggestion_prompt = {
            "role": "user", 
            "content": f"基於當前情況，請推薦下一個應該爬取的 URL 來找尋這些數據點: {get_data_keys()}。請直接回傳一個 JSON 格式的回應，包含 url 字段和理由 reason 字段。"
        }
        
        messages = current_messages + [suggestion_prompt]
        response = call_ollama(messages)
        
        if "error" in response:
            logger.error(f"獲取建議 URL 時出錯: {response['error']}")
            break
            
        try:
            ai_message = response["choices"][0]["message"]["content"]
            logger.info(f"AI 建議回應: {ai_message}")
            
            # 嘗試從回應中提取 URL
            suggested_url = None
            
            # 嘗試解析 JSON
            try:
                json_data = json.loads(ai_message)
                if "url" in json_data:
                    suggested_url = json_data["url"]
                    reason = json_data.get("reason", "無提供理由")
                    logger.info(f"從 JSON 中提取的建議 URL: {suggested_url}")
                    logger.info(f"建議理由: {reason}")
            except json.JSONDecodeError:
                # 如果不是 JSON，嘗試直接從文本中提取 URL
                import re
                urls = re.findall(r'https?://(?:[-\w.]|(?:%[\da-fA-F]{2}))+[/\w\.-]*(?:\?\S+)?', ai_message)
                if urls:
                    suggested_url = urls[0]
                    logger.info(f"從文本中提取的建議 URL: {suggested_url}")
            
            if not suggested_url:
                logger.warning("無法從 AI 回應中提取 URL")
                break
                
            # 爬取建議的 URL
            logger.info(f"爬取建議的 URL: {suggested_url}")
            scraped_data = scrape(suggested_url)
            
            # 將爬取的數據發送給 AI 分析
            analysis_prompt = {
                "role": "user", 
                "content": f"以下是從 {suggested_url} 爬取的數據。請分析並提取關於 {get_data_keys()} 的資訊。請以 JSON 格式回傳結果。\n\n{scraped_data[:1000]}..."
            }
            
            # 加入新的訊息到對話中
            messages = current_messages + [analysis_prompt]
            analysis_response = call_ollama(messages)
            
            if "error" in analysis_response:
                logger.error(f"分析爬取數據時出錯: {analysis_response['error']}")
                continue
                
            analysis_content = analysis_response["choices"][0]["message"]["content"]
            logger.info(f"AI 分析回應預覽: {analysis_content[:200]}...")
            
            # 從分析中提取發現
            new_findings = extract_findings_from_response(analysis_content)
            
            # 更新數據點
            for key, value in new_findings.items():
                update_data_point(key, value, suggested_url)
                findings[key] = {"value": value, "reference": suggested_url}
            
            # 檢查是否已找到所有數據點
            if not get_data_keys():
                logger.info("已找到所有數據點，結束額外 URL 處理")
                break
                
            # 加入分析結果到當前對話
            current_messages.append({
                "role": "assistant",
                "content": f"我已經從 {suggested_url} 找到了以下資訊: {json.dumps(new_findings, ensure_ascii=False)}"
            })
            
        except Exception as e:
            logger.error(f"處理建議 URL 時發生錯誤: {e}")
            logger.error(traceback.format_exc())
            continue
    
    return findings

def main():
    """
    主執行函數，負責驅動 Ollama 交互與爬取流程。
    """
    logger.info("=== 開始執行爬蟲任務 ===")
    
    # 獲取需要查找的數據點
    data_keys_to_search = get_data_keys()
    
    # 系統提示詞，指導 AI 如何運作
    system_prompt = f"""
    你是一位世界級的網頁爬蟲專家，擅長從網站上尋找資訊。
    你的任務是爬取多個 URL 直到找到所有需要的數據點。
    當你發現任何一個數據點，請在回應中明確標示出來，格式為: "<數據點名稱>: <值>"
    不要停止搜尋，直到所有缺失的數據點都找到為止。
    你將盡全力在網上搜尋有關 {company} 公司的資訊。
    你需要尋找的數據點有: {data_keys_to_search}。
    當解析爬取到的數據時，請分析其中的有用資訊，並以清晰的 JSON 格式回傳包含所有找到數據點的結果。
    """

    # 用戶提示詞，請求 AI 查詢指定公司與網站資訊
    user_prompt = f"""
    請搜尋以下公司資訊: {company}
    從這個網站開始: {website}
    查找這些數據點: {data_keys_to_search}
    
    當你找到任何數據點時，請明確標出，例如:
    "catering_offering_for_employees: Discord 提供員工免費早餐、午餐和晚餐"
    "num_employees: 約1200名"
    "office_locations: 舊金山（總部）、紐約、多倫多、倫敦"
    
    如果你需要訪問其他頁面獲取資訊，請告訴我你需要訪問的 URL，並說明理由。
    """

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt}
    ]

    max_iterations = 5
    iteration_count = 0
    all_findings = {}
    
    try:
        logger.info("開始與 Ollama 進行初次對話")
        
        # 呼叫本地端 Ollama 進行對話
        response = call_ollama(messages)
        
        if "error" in response:
            logger.error(f"初次對話失敗: {response['error']}")
            return
            
        logger.info("初次對話成功，處理回應")
        print(colored(f"初次 AI 回應: {json.dumps(response, indent=2, ensure_ascii=False)}", "white", "on_blue"))

        if not response.get("choices"):
            logger.error("回應中沒有 choices")
            return

        message = response["choices"][0]["message"]
        
        # 檢查初次回應中是否有任何發現
        initial_findings = extract_findings_from_response(message.get("content", ""))
        for key, value in initial_findings.items():
            update_data_point(key, value, website)
            all_findings[key] = {"value": value, "reference": website}
        
        # 如果回應中有工具呼叫，則處理這些呼叫
        if message.get("tool_calls"):
            logger.info(f"發現 {len(message['tool_calls'])} 個工具呼叫")
            
            for tool_call in message["tool_calls"]:
                try:
                    tool_call_id = tool_call["id"]
                    logger.info(f"處理工具呼叫 ID: {tool_call_id}")
                    
                    arguments = json.loads(tool_call["function"]["arguments"])
                    logger.info(f"工具呼叫參數: {arguments}")
                    
                    url = arguments.get("url")
                    if not url:
                        logger.warning("參數中沒有 URL")
                        continue

                    # 執行網頁爬取
                    logger.info(f"開始爬取 URL: {url}")
                    scraped_data = scrape(url)
                    
                    # 記錄爬取到的數據預覽
                    data_preview = scraped_data[:200] + "..." if len(scraped_data) > 200 else scraped_data
                    logger.info(f"爬取到的數據預覽: {data_preview}")
                    print(colored(f"爬取的數據: {data_preview}", "yellow"))
                    
                    # 使用 transformers 進行分詞，準備分割數據
                    logger.info("使用 transformers 進行分詞")
                    tokenizer = AutoTokenizer.from_pretrained("deepseek-ai/deepseek-llm-7b")
                    
                    # 分割數據為更小的塊，以便 LLM 處理
                    chunks = chunk_data(scraped_data, 2000)
                    logger.info(f"數據已分割為 {len(chunks)} 個區塊")
                    
                    # 處理每個數據塊
                    for i, chunk in enumerate(chunks):
                        logger.info(f"處理數據區塊 {i+1}/{len(chunks)}")
                        
                        # 創建工具回應訊息
                        tool_message = create_tool_message(url, chunk, tool_call_id)
                        messages.append(tool_message)
                        
                        # 檢查訊息總數或 token 數量是否過多
                        token_count = len(tokenizer.tokenize(chunk))
                        logger.info(f"區塊 token 數量: {token_count}")
                        
                        if len(messages) > 4 or token_count > 8192:
                            logger.info("訊息數量或 token 數量過多，使用最新的訊息")
                            latest_messages = messages[-4:]
                            logger.info(f"使用最新的 {len(latest_messages)} 條訊息進行對話")
                            
                            # 與 LLM 進行對話
                            logger.info("發送訊息給 Ollama")
                            chat_response = call_ollama(latest_messages)
                            
                            if "error" in chat_response:
                                logger.error(f"對話失敗: {chat_response['error']}")
                                continue
                                
                            # 獲取回應內容
                            response_content = chat_response["choices"][0]["message"]["content"]
                            logger.info(f"回應內容預覽: {response_content[:200]}...")
                            print(colored("{}".format(response_content), "black", "on_blue"))
                            
                            # 從回應中提取發現
                            findings = extract_findings_from_response(response_content)
                            logger.info(f"從回應中提取的發現: {findings}")
                            
                            # 更新數據點
                            for key, value in findings.items():
                                update_data_point(key, value, url)
                                all_findings[key] = {"value": value, "reference": url}
                
                except Exception as e:
                    logger.error(f"處理工具呼叫時發生錯誤: {e}")
                    logger.error(traceback.format_exc())
                    continue
        
        # 檢查是否需要爬取其他 URL
        logger.info("檢查是否有未找到的數據點")
        missing_data_keys = get_data_keys()
        
        if missing_data_keys:
            logger.info(f"還有 {len(missing_data_keys)} 個數據點未找到，嘗試爬取其他 URL")
            additional_findings = process_additional_urls(messages)
            all_findings.update(additional_findings)
        
        # 輸出最終結果
        logger.info("===== 最終結果 =====")
        for dp in data_points:
            status = "已找到" if dp["value"] is not None else "未找到"
            logger.info(f"{dp['name']}: {status} - 值: {dp['value']}, 來源: {dp['reference']}")
            print(colored(f"{dp['name']}: {status} - 值: {dp['value']}, 來源: {dp['reference']}", "green" if dp["value"] else "red"))
        
        return all_findings

    except Exception as e:
        logger.error(f"主執行過程中發生錯誤: {e}")
        logger.error(traceback.format_exc())
        print(colored(f"執行錯誤: {e}", "red"))

if __name__ == "__main__":
    main()