# Claude 簡易對話程式

這是一個簡單的命令行程式，用於與Anthropic的Claude AI模型進行對話。

## 功能特點

- 支援多種Claude模型（Opus、Sonnet、Haiku）
- 保存和加載對話歷史
- 自定義回應參數（max_tokens、temperature）
- 簡單的命令行界面

## 安裝

1. 確保已安裝Python 3.8+
2. 安裝所需依賴：

```bash
pip install -r requirements.txt
```

## 設置API密鑰

在使用前，您需要設置Anthropic API密鑰。有兩種方式：

1. 環境變量：
```bash
export ANTHROPIC_API_KEY='your-api-key'
```

2. 創建.env文件：
```
ANTHROPIC_API_KEY=your-api-key
```

您可以從[Anthropic Console](https://console.anthropic.com/)獲取API密鑰。

## 使用方法

### 基本使用

```bash
python app.py
```

### 指定模型和參數

```bash
python app.py --model sonnet --max-tokens 2000 --temperature 0.8
```

可用的模型選項：
- `opus` (Claude 3 Opus)
- `sonnet` (Claude 3 Sonnet)
- `haiku` (Claude 3 Haiku)

### 加載之前的對話

```bash
python app.py --load conversation_20250315_123456.json
```

## 對話中的命令

在對話過程中，您可以使用以下命令：

- `/help` - 顯示幫助信息
- `/exit` 或 `/quit` - 退出程序
- `/save [filename]` - 保存當前對話
- `/load <filename>` - 加載之前的對話
- `/clear` - 清除當前對話歷史
- `/model <model_name>` - 切換模型 (opus/sonnet/haiku)

## 範例

```
您: 你好，請介紹一下自己

Claude: 您好！我是Claude，一個由Anthropic開發的AI助手。我被設計用來提供有幫助、無害且誠實的對話體驗。我可以協助回答問題、提供資訊、進行創意寫作、討論各種主題，以及完成許多其他任務。

我的目標是成為一個有用的工具，幫助人們更有效地完成工作、學習新知識或探索想法。我不斷學習和改進，但我也有局限性，有時可能無法回答特定問題或可能出錯。

有什麼我可以幫您的嗎？

您: /model haiku

已切換到模型: haiku (claude-3-haiku-20240307)

您: 現在你是哪個模型？

Claude思考中...

Claude: 我是Claude 3 Haiku模型，這是Anthropic的Claude 3系列中的一個版本。Haiku模型設計為更快速、更輕量，適合需要快速回應的對話和任務。
```

## 注意事項

- 使用API會產生費用，請參考[Anthropic的價格頁面](https://www.anthropic.com/pricing)
- 請確保您的API密鑰保密，不要將其分享或提交到公共代碼庫
