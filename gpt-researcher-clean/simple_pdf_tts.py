import os
import sys
import PyPDF2
from pathlib import Path
import openai
from dotenv import load_dotenv

# 加載環境變數
load_dotenv()

# 設置 OpenAI API 金鑰
openai_api_key = os.getenv("OPENAI_API_KEY")
if not openai_api_key:
    print("錯誤：未找到 OPENAI_API_KEY 環境變數")
    sys.exit(1)

openai.api_key = openai_api_key

def main():
    if len(sys.argv) < 2:
        print("用法: python simple_pdf_tts.py <PDF文件路徑>")
        sys.exit(1)
    
    pdf_path = sys.argv[1]
    
    # 確保 PDF 文件存在
    if not os.path.exists(pdf_path):
        print(f"錯誤：PDF 文件 {pdf_path} 不存在")
        sys.exit(1)
    
    # 提取 PDF 文本
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
        
        # 打印提取的文本
        print("\n提取的文本樣本（前500字符）：")
        print("-" * 50)
        print(text[:500])
        print("-" * 50)
        print(f"總字符數：{len(text)}")
        
        # 創建輸出目錄
        audio_dir = Path("audio_outputs")
        audio_dir.mkdir(exist_ok=True)
        
        # 設置輸出文件路徑
        output_file = audio_dir / f"{Path(pdf_path).stem}.mp3"
        
        # 限制文本長度（如果太長）
        max_length = 4000
        if len(text) > max_length:
            print(f"文本太長（{len(text)}字符），將只轉換前{max_length}字符")
            text = text[:max_length]
        
        # 轉換為語音
        print("正在調用 OpenAI TTS API...")
        response = openai.audio.speech.create(
            model="tts-1",
            voice="alloy",
            input=text
        )
        
        # 保存音頻文件
        print(f"正在保存音頻文件到 {output_file}...")
        response.stream_to_file(str(output_file))
        
        print(f"完成！語音文件已保存到：{os.path.abspath(output_file)}")
    
    except Exception as e:
        print(f"錯誤：{e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
