# GPT-Researcher TTS 和電子郵件功能設置指南

這個指南將幫助您設置 GPT-Researcher 的文本轉語音 (TTS) 和電子郵件功能，讓您可以將研究報告轉換為語音並通過電子郵件發送。

## 步驟 1: 更新 .env 文件

請在您的 `.env` 文件中添加以下配置：

```
# 電子郵件設置
EMAIL_ADDRESS=您的電子郵件地址
EMAIL_PASSWORD=您的電子郵件密碼或應用專用密碼
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
```

注意：
- 如果您使用 Gmail，建議使用「應用專用密碼」而不是您的實際密碼
- 不同的電子郵件服務提供商可能有不同的 SMTP 設置

## 步驟 2: 安裝所需的依賴

您需要安裝以下 Python 包：

```bash
pip install openai python-dotenv
```

如果您需要合併多個音頻文件，還需要安裝 FFmpeg：
- Windows: 從 https://ffmpeg.org/download.html 下載並安裝
- 安裝後確保 FFmpeg 在您的系統 PATH 中

## 步驟 3: 使用 TTS 和電子郵件功能

使用以下命令將研究報告轉換為語音並發送電子郵件：

```bash
python tts_email_sender.py 報告文件路徑.json --email 收件人電子郵件地址 --voice 語音類型
```

例如：

```bash
python tts_email_sender.py outputs/task_1741930008_特斯拉.json --email example@example.com --voice alloy
```

可用的語音類型：
- alloy: 中性語音
- echo: 男性語音
- fable: 男性語音，適合講故事
- onyx: 男性語音，專業風格
- nova: 女性語音
- shimmer: 女性語音，友好風格

## 注意事項

1. 語音文件將保存在 `audio_outputs` 目錄中
2. 大型報告將被分割成多個部分處理，以符合 OpenAI TTS API 的限制
3. 確保您的 OpenAI API 金鑰有足夠的額度來使用 TTS 服務
