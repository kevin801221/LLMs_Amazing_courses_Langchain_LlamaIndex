#!/bin/bash

# 設置工作目錄
cd /Users/kevinluo/application/LLMs_Amazing_courses_Langchain_LlamaIndex

# 確保目標目錄存在
mkdir -p prompt-eng-interactive-tutorial/Anthropic\ 1P/

# 從 Git 歷史中恢復筆記本文件並移除敏感 API 密鑰
NOTEBOOKS=(
    "prompt-eng-interactive-tutorial/Anthropic 1P/00_Tutorial_How-To.ipynb"
    "prompt-eng-interactive-tutorial/Anthropic 1P/01_Basic_Prompt_Structure.ipynb"
    "prompt-eng-interactive-tutorial/Anthropic 1P/02_Being_Clear_and_Direct.ipynb"
    "prompt-eng-interactive-tutorial/Anthropic 1P/03_Assigning_Roles_Role_Prompting.ipynb"
    "prompt-eng-interactive-tutorial/Anthropic 1P/04_Separating_Data_and_Instructions.ipynb"
    "prompt-eng-interactive-tutorial/Anthropic 1P/05_Formatting_Output_and_Speaking_for_Claude.ipynb"
    "prompt-eng-interactive-tutorial/Anthropic 1P/06_Precognition_Thinking_Step_by_Step.ipynb"
    "prompt-eng-interactive-tutorial/Anthropic 1P/07_Using_Examples_Few-Shot_Prompting.ipynb"
    "prompt-eng-interactive-tutorial/Anthropic 1P/08_Avoiding_Hallucinations.ipynb"
    "prompt-eng-interactive-tutorial/Anthropic 1P/09_Complex_Prompts_from_Scratch.ipynb"
    "prompt-eng-interactive-tutorial/Anthropic 1P/10.1_Appendix_Chaining Prompts.ipynb"
    "prompt-eng-interactive-tutorial/Anthropic 1P/10.2_Appendix_Tool Use.ipynb"
    "prompt-eng-interactive-tutorial/Anthropic 1P/10.3_Appendix_Search & Retrieval.ipynb"
)

for notebook in "${NOTEBOOKS[@]}"; do
    echo "處理 $notebook..."
    
    # 從 Git 歷史中恢復筆記本文件
    git show 760562f2:"$notebook" > "/tmp/$(basename "$notebook")"
    
    # 使用 Python 處理筆記本文件，移除敏感 API 密鑰
    python -c "
import json
import sys
import re

# 讀取筆記本文件
with open('/tmp/$(basename "$notebook")', 'r', encoding='utf-8') as f:
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
                cell['source'][i] = re.sub(r'sk-ant-api[^\"]+', 'your_anthropic_api_key_here', source)
                modified = True

# 保存修改後的筆記本文件
with open('$notebook', 'w', encoding='utf-8') as f:
    json.dump(notebook, f, indent=1)

print('已清理 API 密鑰' if modified else '未發現 API 密鑰')
"
done

echo "所有筆記本文件已恢復並清理完成！"
