import os
import json
import argparse
from datetime import datetime
from anthropic import Anthropic

# 嘗試導入dotenv，如果安裝了的話
try:
    from dotenv import load_dotenv
    load_dotenv()  # 從.env文件加載環境變量
except ImportError:
    print("提示: 安裝python-dotenv可以從.env文件加載API密鑰")
    print("pip install python-dotenv")

# 可用的Claude模型
AVAILABLE_MODELS = {
    "opus": "claude-3-opus-20240229",
    "sonnet": "claude-3-sonnet-20240229",
    "haiku": "claude-3-haiku-20240307"
}

def save_conversation(conversation_history, filename=None):
    """將對話保存到文件"""
    if not filename:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"conversation_{timestamp}.json"
    
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(conversation_history, f, ensure_ascii=False, indent=2)
    
    print(f"對話已保存至: {filename}")

def load_conversation(filename):
    """從文件加載對話"""
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"找不到文件: {filename}")
        return []
    except json.JSONDecodeError:
        print(f"無法解析文件: {filename}")
        return []

def print_help():
    """顯示可用命令"""
    print("\n可用命令:")
    print("/exit 或 /quit - 退出程序")
    print("/save [filename] - 保存當前對話")
    print("/load <filename> - 加載之前的對話")
    print("/clear - 清除當前對話歷史")
    print("/model <model_name> - 切換模型 (opus/sonnet/haiku)")
    print("/help - 顯示此幫助信息")

def main():
    # 設置命令行參數
    parser = argparse.ArgumentParser(description='Claude簡易對話程式')
    parser.add_argument('--model', type=str, default='sonnet', choices=AVAILABLE_MODELS.keys(),
                        help='使用的Claude模型 (opus/sonnet/haiku)')
    parser.add_argument('--max-tokens', type=int, default=1000,
                        help='回應的最大token數量')
    parser.add_argument('--temperature', type=float, default=0.7,
                        help='回應的溫度參數 (0.0-1.0)')
    parser.add_argument('--load', type=str, help='加載之前保存的對話文件')
    
    args = parser.parse_args()
    
    # 獲取API密鑰
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    
    if not api_key:
        print("請設置ANTHROPIC_API_KEY環境變量")
        print("方法1: export ANTHROPIC_API_KEY='your-api-key'")
        print("方法2: 創建.env文件並添加 ANTHROPIC_API_KEY=your-api-key")
        return
    
    # 初始化Anthropic客戶端
    client = Anthropic(api_key=api_key)
    
    # 當前使用的模型
    current_model = AVAILABLE_MODELS[args.model]
    max_tokens = args.max_tokens
    temperature = args.temperature
    
    print(f"歡迎使用Claude簡易對話程式！")
    print(f"當前模型: {args.model} ({current_model})")
    print(f"輸入 /help 查看可用命令")
    
    # 保存對話歷史
    conversation_history = []
    
    # 如果指定了加載文件
    if args.load:
        conversation_history = load_conversation(args.load)
        if conversation_history:
            print(f"已加載對話，共 {len(conversation_history)} 條消息")
            # 顯示最後幾條消息
            for msg in conversation_history[-4:]:
                role = "您" if msg["role"] == "user" else "Claude"
                print(f"{role}: {msg['content'][:50]}..." if len(msg['content']) > 50 else f"{role}: {msg['content']}")
    
    while True:
        # 獲取用戶輸入
        user_input = input("\n您: ")
        
        # 處理命令
        if user_input.startswith("/"):
            cmd_parts = user_input.split()
            cmd = cmd_parts[0].lower()
            
            if cmd in ["/exit", "/quit", "/退出"]:
                print("感謝使用，再見！")
                break
                
            elif cmd == "/save":
                filename = cmd_parts[1] if len(cmd_parts) > 1 else None
                save_conversation(conversation_history, filename)
                continue
                
            elif cmd == "/load":
                if len(cmd_parts) > 1:
                    new_history = load_conversation(cmd_parts[1])
                    if new_history:
                        conversation_history = new_history
                        print(f"已加載對話，共 {len(conversation_history)} 條消息")
                else:
                    print("請指定要加載的文件名")
                continue
                
            elif cmd == "/clear":
                conversation_history = []
                print("對話歷史已清除")
                continue
                
            elif cmd == "/model":
                if len(cmd_parts) > 1 and cmd_parts[1] in AVAILABLE_MODELS:
                    args.model = cmd_parts[1]
                    current_model = AVAILABLE_MODELS[args.model]
                    print(f"已切換到模型: {args.model} ({current_model})")
                else:
                    print(f"可用模型: {', '.join(AVAILABLE_MODELS.keys())}")
                continue
                
            elif cmd == "/help":
                print_help()
                continue
        
        # 將用戶輸入添加到對話歷史
        conversation_history.append({"role": "user", "content": user_input})
        
        try:
            print("Claude思考中...")
            # 調用Claude API
            response = client.messages.create(
                model=current_model,
                max_tokens=max_tokens,
                temperature=temperature,
                messages=conversation_history
            )
            
            # 獲取Claude的回應
            assistant_response = response.content[0].text
            print(f"\nClaude: {assistant_response}")
            
            # 將Claude的回應添加到對話歷史
            conversation_history.append({"role": "assistant", "content": assistant_response})
            
        except Exception as e:
            print(f"發生錯誤: {e}")
            
if __name__ == "__main__":
    main()
