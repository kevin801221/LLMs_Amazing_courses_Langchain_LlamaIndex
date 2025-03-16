#!/usr/bin/env python3
import json
import os
import glob

# 定義要清理的筆記本文件路徑
notebooks_dir = "/Users/kevinluo/application/LLMs_Amazing_courses_Langchain_LlamaIndex/prompt-eng-interactive-tutorial/Anthropic 1P"
notebooks = glob.glob(os.path.join(notebooks_dir, "*.ipynb"))

# 敏感 API 密鑰的替代文本
api_key_replacement = "your_anthropic_api_key_here"

# 處理每個筆記本文件
for notebook_path in notebooks:
    print(f"Processing {notebook_path}...")
    
    # 讀取筆記本文件
    with open(notebook_path, 'r', encoding='utf-8') as f:
        notebook = json.load(f)
    
    # 標記是否修改了文件
    modified = False
    
    # 遍歷所有單元格
    for cell in notebook.get('cells', []):
        if cell.get('cell_type') == 'code':
            # 遍歷代碼單元格的源代碼
            for i, source in enumerate(cell.get('source', [])):
                # 檢查是否包含 API 密鑰
                if 'sk-ant-api' in source:
                    # 替換 API 密鑰
                    cell['source'][i] = source.replace(
                        source.split('sk-ant-api')[0] + 'sk-ant-api' + source.split('sk-ant-api')[1].split('"')[0] + '"',
                        f'"{api_key_replacement}"'
                    )
                    modified = True
    
    # 如果文件被修改，保存更改
    if modified:
        with open(notebook_path, 'w', encoding='utf-8') as f:
            json.dump(notebook, f, indent=1)
        print(f"Cleaned API keys from {notebook_path}")
    else:
        print(f"No API keys found in {notebook_path}")

print("All notebooks processed.")
