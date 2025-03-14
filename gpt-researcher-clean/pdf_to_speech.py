import os
import argparse
from pathlib import Path
import openai
import time
from dotenv import load_dotenv
import PyPDF2
import traceback

# 加載環境變數
load_dotenv()

# 設置 OpenAI API 金鑰
openai_api_key = os.getenv("OPENAI_API_KEY")
if not openai_api_key:
    print("警告：未找到 OPENAI_API_KEY 環境變數")
else:
    print(f"已找到 OPENAI_API_KEY 環境變數：{openai_api_key[:5]}...")
    openai.api_key = openai_api_key

def extract_text_from_pdf(pdf_path):
    """
    從 PDF 文件中提取文本
    
    參數：
    - pdf_path: PDF 文件路徑
    
    返回：
    - 提取的文本
    """
    try:
        print(f"嘗試打開 PDF 文件：{pdf_path}")
        text = ""
        with open(pdf_path, "rb") as file:
            print("PDF 文件已成功打開")
            reader = PyPDF2.PdfReader(file)
            num_pages = len(reader.pages)
            
            print(f"PDF 文件共有 {num_pages} 頁")
            
            for page_num in range(num_pages):
                print(f"正在處理第 {page_num + 1}/{num_pages} 頁...")
                page = reader.pages[page_num]
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n\n"
                    print(f"第 {page_num + 1} 頁提取了 {len(page_text)} 個字符")
                else:
                    print(f"警告：第 {page_num + 1} 頁沒有提取到文本")
        
        print(f"PDF 文本提取完成，共 {len(text)} 個字符")
        if len(text) > 0:
            print(f"文本樣本：{text[:100]}...")
        return text
    except Exception as e:
        print(f"提取 PDF 文本時出錯：{e}")
        traceback.print_exc()
        return None

def convert_to_speech(text, output_file, voice="alloy"):
    """
    使用 OpenAI 的 TTS API 將文本轉換為語音
    
    參數：
    - text: 要轉換的文本
    - output_file: 輸出的音頻文件路徑
    - voice: 語音類型 (alloy, echo, fable, onyx, nova, shimmer)
    """
    try:
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
                # 如果段落本身超過最大長度，需要進一步分割
                if len(paragraph) > max_length:
                    # 按句子分割
                    sentences = paragraph.replace(". ", ".\n").replace("! ", "!\n").replace("? ", "?\n").split("\n")
                    for sentence in sentences:
                        if len(current_segment) + len(sentence) + 2 <= max_length:
                            if current_segment:
                                current_segment += " " + sentence
                            else:
                                current_segment = sentence
                        else:
                            segments.append(current_segment)
                            current_segment = sentence
                else:
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
        
        print(f"文本已分割為 {len(segments)} 個段落")
        
        # 處理每個文本段落
        audio_files = []
        for i, segment in enumerate(segments):
            segment_file = f"{output_file.stem}_part{i}{output_file.suffix}"
            segment_path = output_file.parent / segment_file
            
            print(f"正在處理第 {i+1}/{len(segments)} 段文本...")
            print(f"段落長度：{len(segment)} 字符")
            print(f"段落樣本：{segment[:50]}...")
            
            try:
                print("調用 OpenAI TTS API...")
                response = openai.audio.speech.create(
                    model="tts-1",
                    voice=voice,
                    input=segment
                )
                
                print(f"API 調用成功，正在保存音頻文件到：{segment_path}")
                response.stream_to_file(str(segment_path))
                audio_files.append(segment_path)
                print(f"音頻文件已保存：{segment_path}")
                
                # 避免 API 限制
                if i < len(segments) - 1:
                    print("等待 1 秒以避免 API 限制...")
                    time.sleep(1)
            except Exception as e:
                print(f"處理第 {i+1} 段文本時出錯：{e}")
                traceback.print_exc()
                continue
        
        if not audio_files:
            print("沒有成功生成任何音頻文件")
            return None
        
        # 如果只有一個段落，直接返回
        if len(audio_files) == 1:
            print(f"只有一個音頻文件，重命名為：{output_file}")
            os.rename(audio_files[0], output_file)
            return output_file
        
        # 如果有多個段落，需要合併音頻文件
        try:
            # 這裡需要使用 ffmpeg 合併音頻文件
            # 創建一個包含所有音頻文件的列表文件
            list_file = output_file.parent / "filelist.txt"
            print(f"創建文件列表：{list_file}")
            with open(list_file, "w") as f:
                for audio_file in audio_files:
                    f.write(f"file '{audio_file.name}'\n")
            
            # 使用 ffmpeg 合併音頻文件
            print("正在使用 ffmpeg 合併音頻文件...")
            ffmpeg_cmd = f'ffmpeg -f concat -safe 0 -i {list_file} -c copy {output_file}'
            print(f"執行命令：{ffmpeg_cmd}")
            os.system(ffmpeg_cmd)
            
            # 檢查輸出文件是否存在
            if os.path.exists(output_file):
                print(f"合併成功，輸出文件：{output_file}")
            else:
                print(f"警告：合併後的文件 {output_file} 不存在")
            
            # 刪除臨時文件
            print("刪除臨時文件...")
            for audio_file in audio_files:
                os.remove(audio_file)
            os.remove(list_file)
            
            return output_file
        except Exception as e:
            print(f"合併音頻文件時出錯：{e}")
            traceback.print_exc()
            # 如果合併失敗，返回第一個音頻文件
            if audio_files:
                print(f"合併失敗，返回第一個音頻文件：{audio_files[0]}")
                return audio_files[0]
            return None
    except Exception as e:
        print(f"轉換文本為語音時出錯：{e}")
        traceback.print_exc()
        return None

def pdf_to_speech(pdf_file, voice="alloy"):
    """
    將 PDF 文件轉換為語音
    
    參數：
    - pdf_file: PDF 文件路徑
    - voice: 語音類型
    """
    try:
        # 提取 PDF 文本
        print(f"正在從 PDF 文件提取文本：{pdf_file}")
        text = extract_text_from_pdf(pdf_file)
        
        if not text:
            print("無法從 PDF 文件中提取文本")
            return None
        
        print(f"成功提取文本，共 {len(text)} 字符")
        
        # 創建輸出目錄
        audio_dir = Path("audio_outputs")
        print(f"確保輸出目錄存在：{audio_dir}")
        audio_dir.mkdir(exist_ok=True)
        
        # 設置輸出文件路徑
        output_file = audio_dir / f"{Path(pdf_file).stem}.mp3"
        print(f"輸出文件路徑：{output_file}")
        
        print(f"正在將 PDF 文本轉換為語音...")
        
        # 轉換為語音
        audio_file = convert_to_speech(text, output_file, voice)
        
        if audio_file:
            print(f"語音文件已生成: {audio_file}")
            print(f"您可以在 {os.path.abspath(audio_file)} 找到語音文件")
        else:
            print("語音文件生成失敗")
        
        return audio_file
    except Exception as e:
        print(f"PDF 轉語音過程中出錯：{e}")
        traceback.print_exc()
        return None

def main():
    parser = argparse.ArgumentParser(description="將 PDF 文件轉換為語音")
    parser.add_argument("pdf_file", help="PDF 文件路徑")
    parser.add_argument("--voice", default="alloy", help="語音類型 (alloy, echo, fable, onyx, nova, shimmer)")
    
    args = parser.parse_args()
    
    print(f"開始處理 PDF 文件：{args.pdf_file}")
    print(f"使用語音類型：{args.voice}")
    
    pdf_to_speech(args.pdf_file, args.voice)

if __name__ == "__main__":
    main()
