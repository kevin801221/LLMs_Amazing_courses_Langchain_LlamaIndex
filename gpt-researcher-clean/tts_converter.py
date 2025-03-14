import os
import json
import argparse
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
        
        print(f"正在處理第 {i+1}/{len(segments)} 段文本...")
        
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
    print("正在合併音頻文件...")
    os.system(f'ffmpeg -f concat -safe 0 -i {list_file} -c copy {output_file}')
    
    # 刪除臨時文件
    for audio_file in audio_files:
        os.remove(audio_file)
    os.remove(list_file)
    
    return output_file

def process_research_report(json_file, voice="alloy"):
    """
    處理研究報告，轉換為語音
    
    參數:
    - json_file: 研究報告 JSON 文件路徑
    - voice: 語音類型
    """
    # 讀取 JSON 文件
    try:
        with open(json_file, "r", encoding="utf-8") as f:
            report_data = json.load(f)
        
        # 從 JSON 中提取報告內容
        content = report_data.get("content", "")
        
        # 如果沒有 content 字段，嘗試其他可能的字段
        if not content and "report" in report_data:
            content = report_data["report"]
        
        # 提取標題
        title = os.path.basename(json_file).replace(".json", "")
        if "task_" in title:
            title = title.split("_", 1)[1]  # 移除 task_id 前綴
        
        if not content:
            print(f"錯誤：無法從 JSON 文件中提取報告內容")
            print(f"JSON 文件結構：{list(report_data.keys())}")
            return None
        
        # 創建輸出目錄
        audio_dir = Path("audio_outputs")
        audio_dir.mkdir(exist_ok=True)
        
        # 設置輸出文件路徑
        output_file = audio_dir / f"{Path(json_file).stem}.mp3"
        
        print(f"正在將報告《{title}》轉換為語音...")
        print(f"報告內容長度：{len(content)} 字符")
        
        # 轉換為語音
        audio_file = convert_to_speech(content, output_file, voice)
        
        print(f"語音文件已生成: {audio_file}")
        print(f"您可以在 {os.path.abspath(audio_file)} 找到語音文件")
        
        return audio_file
    except Exception as e:
        print(f"處理報告時出錯：{e}")
        import traceback
        traceback.print_exc()
        return None

def main():
    parser = argparse.ArgumentParser(description="將研究報告轉換為語音")
    parser.add_argument("json_file", help="研究報告 JSON 文件路徑")
    parser.add_argument("--voice", default="alloy", help="語音類型 (alloy, echo, fable, onyx, nova, shimmer)")
    
    args = parser.parse_args()
    
    process_research_report(args.json_file, args.voice)

if __name__ == "__main__":
    main()
