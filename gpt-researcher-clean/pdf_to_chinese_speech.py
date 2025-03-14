import os
import sys
import PyPDF2
from pathlib import Path
import openai
from dotenv import load_dotenv
import time

# 加載環境變數
load_dotenv()

# 設置 OpenAI API 金鑰
openai_api_key = os.getenv("OPENAI_API_KEY")
if not openai_api_key:
    print("錯誤：未找到 OPENAI_API_KEY 環境變數")
    sys.exit(1)

openai.api_key = openai_api_key

def extract_text_from_pdf(pdf_path):
    """從 PDF 文件中提取文本"""
    try:
        text = ""
        with open(pdf_path, "rb") as file:
            reader = PyPDF2.PdfReader(file)
            num_pages = len(reader.pages)
            
            print(f"PDF 文件共有 {num_pages} 頁")
            
            for page_num in range(num_pages):
                page = reader.pages[page_num]
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n\n"
                print(f"已處理第 {page_num + 1}/{num_pages} 頁")
        
        return text
    except Exception as e:
        print(f"提取 PDF 文本時出錯：{e}")
        import traceback
        traceback.print_exc()
        return None

def translate_to_chinese(text):
    """將文本翻譯成中文"""
    try:
        print("正在將文本翻譯成中文...")
        
        # 如果文本太長，分段處理
        max_length = 4000
        if len(text) <= max_length:
            segments = [text]
        else:
            # 按段落分割文本
            paragraphs = text.split("\n\n")
            segments = []
            current_segment = ""
            
            for paragraph in paragraphs:
                if len(current_segment) + len(paragraph) + 2 <= max_length:
                    if current_segment:
                        current_segment += "\n\n" + paragraph
                    else:
                        current_segment = paragraph
                else:
                    segments.append(current_segment)
                    current_segment = paragraph
            
            if current_segment:
                segments.append(current_segment)
        
        print(f"文本已分割為 {len(segments)} 個段落進行翻譯")
        
        # 翻譯每個段落
        translated_segments = []
        for i, segment in enumerate(segments):
            print(f"正在翻譯第 {i+1}/{len(segments)} 段文本...")
            
            response = openai.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "你是一個專業的翻譯，將以下文本準確地翻譯成中文之外你還可以再濃縮重點。保持原文的格式和段落結構。"},
                    {"role": "user", "content": f"請將以下文本翻譯成中文：\n\n{segment}"}
                ]
            )
            
            translated_text = response.choices[0].message.content
            translated_segments.append(translated_text)
            
            # 避免 API 限制
            if i < len(segments) - 1:
                time.sleep(1)
        
        # 合併翻譯後的段落
        translated_text = "\n\n".join(translated_segments)
        
        print("翻譯完成！")
        return translated_text
    
    except Exception as e:
        print(f"翻譯文本時出錯：{e}")
        import traceback
        traceback.print_exc()
        return None

def text_to_speech(text, output_file, voice="alloy"):
    """將文本轉換為語音"""
    try:
        print("正在將中文文本轉換為語音...")
        
        # 如果文本太長，分段處理
        max_length = 4000  # OpenAI TTS API 的最大文本長度限制
        
        if len(text) <= max_length:
            segments = [text]
        else:
            # 按段落分割文本
            paragraphs = text.split("\n\n")
            segments = []
            current_segment = ""
            
            for paragraph in paragraphs:
                if len(current_segment) + len(paragraph) + 2 <= max_length:
                    if current_segment:
                        current_segment += "\n\n" + paragraph
                    else:
                        current_segment = paragraph
                else:
                    segments.append(current_segment)
                    current_segment = paragraph
            
            if current_segment:
                segments.append(current_segment)
        
        print(f"文本已分割為 {len(segments)} 個段落進行語音轉換")
        
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
        
        if not audio_files:
            print("沒有成功生成任何音頻文件")
            return None
        
        # 如果只有一個段落，直接返回
        if len(audio_files) == 1:
            os.rename(audio_files[0], output_file)
            return output_file
        
        # 如果有多個段落，需要合併音頻文件
        try:
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
        except Exception as e:
            print(f"合併音頻文件時出錯：{e}")
            # 如果合併失敗，返回第一個音頻文件
            if audio_files:
                return audio_files[0]
            return None
    
    except Exception as e:
        print(f"轉換文本為語音時出錯：{e}")
        import traceback
        traceback.print_exc()
        return None

def pdf_to_chinese_speech(pdf_file, voice="alloy"):
    """將 PDF 文件轉換為中文語音"""
    # 提取 PDF 文本
    print(f"正在從 PDF 文件提取文本：{pdf_file}")
    text = extract_text_from_pdf(pdf_file)
    
    if not text:
        print("無法從 PDF 文件中提取文本")
        return None
    
    print(f"成功提取文本，共 {len(text)} 字符")
    print("\n提取的文本樣本（前200字符）：")
    print("-" * 50)
    print(text[:200])
    print("-" * 50)
    
    # 翻譯成中文
    chinese_text = translate_to_chinese(text)
    
    if not chinese_text:
        print("無法將文本翻譯成中文")
        return None
    
    print("\n翻譯後的中文文本樣本（前200字符）：")
    print("-" * 50)
    print(chinese_text[:200])
    print("-" * 50)
    
    # 創建輸出目錄
    audio_dir = Path("audio_outputs")
    audio_dir.mkdir(exist_ok=True)
    
    # 設置輸出文件路徑
    output_file = audio_dir / f"{Path(pdf_file).stem}_chinese.mp3"
    
    # 轉換為語音
    audio_file = text_to_speech(chinese_text, output_file, voice)
    
    if audio_file:
        print(f"中文語音文件已生成: {audio_file}")
        print(f"您可以在 {os.path.abspath(audio_file)} 找到語音文件")
        
        # 保存翻譯後的中文文本
        text_file = audio_dir / f"{Path(pdf_file).stem}_chinese.txt"
        with open(text_file, "w", encoding="utf-8") as f:
            f.write(chinese_text)
        print(f"翻譯後的中文文本已保存到: {text_file}")
    else:
        print("語音文件生成失敗")
    
    return audio_file

def main():
    if len(sys.argv) < 2:
        print("用法: python pdf_to_chinese_speech.py <PDF文件路徑> [--voice 語音類型]")
        sys.exit(1)
    
    pdf_file = sys.argv[1]
    voice = "alloy"  # 默認語音類型
    
    # 解析命令行參數
    for i in range(2, len(sys.argv)):
        if sys.argv[i] == "--voice" and i + 1 < len(sys.argv):
            voice = sys.argv[i + 1]
    
    print(f"開始處理 PDF 文件：{pdf_file}")
    print(f"使用語音類型：{voice}")
    
    pdf_to_chinese_speech(pdf_file, voice)

if __name__ == "__main__":
    main()
