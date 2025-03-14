import os
import json
import smtplib
import argparse
from email.mime.multipart import MIMEMultipart
from email.mime.audio import MIMEAudio
from email.mime.text import MIMEText
from pathlib import Path
import openai
import time
from dotenv import load_dotenv

# 加載環境變數
load_dotenv()

# 設置 OpenAI API 金鑰
openai.api_key = os.getenv("OPENAI_API_KEY")

def convert_to_speech(text, output_file, voice="alloy"):
    """
    使用 OpenAI 的 TTS API 將文本轉換為語音
    
    參數:
    - text: 要轉換的文本
    - output_file: 輸出的音頻文件路徑
    - voice: 語音類型 (alloy, echo, fable, onyx, nova, shimmer)
    """
    # 如果文本太長，分段處理
    max_length = 4000  # OpenAI TTS API 的最大文本長度限制
    
    if len(text) <= max_length:
        segments = [text]
    else:
        # 按句子分割文本
        sentences = text.split('. ')
        segments = []
        current_segment = ""
        
        for sentence in sentences:
            if len(current_segment) + len(sentence) + 2 <= max_length:
                if current_segment:
                    current_segment += ". " + sentence
                else:
                    current_segment = sentence
            else:
                segments.append(current_segment + ".")
                current_segment = sentence
        
        if current_segment:
            segments.append(current_segment)
    
    # 處理每個文本段落
    audio_files = []
    for i, segment in enumerate(segments):
        segment_file = f"{output_file.stem}_part{i}{output_file.suffix}"
        segment_path = output_file.parent / segment_file
        
        response = openai.audio.speech.create(
            model="tts-1",
            voice=voice,
            input=segment
        )
        
        response.stream_to_file(str(segment_path))
        audio_files.append(segment_path)
        
        # 避免 API 限制
        if i < len(segments) - 1:
            time.sleep(1)
    
    # 如果只有一個段落，直接返回
    if len(audio_files) == 1:
        os.rename(audio_files[0], output_file)
        return output_file
    
    # 如果有多個段落，需要合併音頻文件
    # 這裡需要使用 ffmpeg 合併音頻文件
    # 創建一個包含所有音頻文件的列表文件
    list_file = output_file.parent / "filelist.txt"
    with open(list_file, "w") as f:
        for audio_file in audio_files:
            f.write(f"file '{audio_file.name}'\n")
    
    # 使用 ffmpeg 合併音頻文件
    os.system(f'ffmpeg -f concat -safe 0 -i {list_file} -c copy {output_file}')
    
    # 刪除臨時文件
    for audio_file in audio_files:
        os.remove(audio_file)
    os.remove(list_file)
    
    return output_file

def send_email(recipient, subject, body, attachment_path):
    """
    發送帶有附件的電子郵件
    
    參數:
    - recipient: 收件人電子郵件地址
    - subject: 郵件主題
    - body: 郵件正文
    - attachment_path: 附件路徑
    """
    # 郵件設置
    sender_email = os.getenv("EMAIL_ADDRESS")
    sender_password = os.getenv("EMAIL_PASSWORD")
    smtp_server = os.getenv("SMTP_SERVER", "smtp.gmail.com")
    smtp_port = int(os.getenv("SMTP_PORT", "587"))
    
    # 創建郵件
    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = recipient
    message["Subject"] = subject
    
    # 添加郵件正文
    message.attach(MIMEText(body, "plain"))
    
    # 添加附件
    with open(attachment_path, "rb") as attachment:
        part = MIMEAudio(attachment.read(), "mp3")
        part.add_header(
            "Content-Disposition",
            f"attachment; filename={os.path.basename(attachment_path)}",
        )
        message.attach(part)
    
    # 發送郵件
    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()
        server.login(sender_email, sender_password)
        server.send_message(message)

def process_research_report(json_file, recipient_email, voice="alloy"):
    """
    處理研究報告，轉換為語音並發送電子郵件
    
    參數:
    - json_file: 研究報告 JSON 文件路徑
    - recipient_email: 收件人電子郵件地址
    - voice: 語音類型
    """
    # 讀取 JSON 文件
    with open(json_file, "r", encoding="utf-8") as f:
        report_data = json.load(f)
    
    # 提取報告內容
    title = report_data.get("title", "研究報告")
    content = report_data.get("report", "")
    
    if not content:
        print("報告內容為空")
        return
    
    # 創建輸出目錄
    audio_dir = Path("audio_outputs")
    audio_dir.mkdir(exist_ok=True)
    
    # 設置輸出文件路徑
    output_file = audio_dir / f"{Path(json_file).stem}.mp3"
    
    print(f"正在將報告轉換為語音: {title}")
    
    # 轉換為語音
    audio_file = convert_to_speech(content, output_file, voice)
    
    print(f"語音文件已生成: {audio_file}")
    
    # 發送電子郵件
    if recipient_email:
        email_subject = f"研究報告語音版: {title}"
        email_body = f"您好，\n\n這是您請求的研究報告《{title}》的語音版本。\n\n祝好，\nGPT-Researcher"
        
        print(f"正在發送電子郵件到: {recipient_email}")
        send_email(recipient_email, email_subject, email_body, audio_file)
        print("電子郵件已發送")

def main():
    parser = argparse.ArgumentParser(description="將研究報告轉換為語音並通過電子郵件發送")
    parser.add_argument("json_file", help="研究報告 JSON 文件路徑")
    parser.add_argument("--email", help="收件人電子郵件地址")
    parser.add_argument("--voice", default="alloy", help="語音類型 (alloy, echo, fable, onyx, nova, shimmer)")
    
    args = parser.parse_args()
    
    process_research_report(args.json_file, args.email, args.voice)

if __name__ == "__main__":
    main()
