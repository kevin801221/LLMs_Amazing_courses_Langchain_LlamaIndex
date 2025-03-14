@echo off
echo 正在啟動 GPT Researcher 服務...
echo.

cd /d D:\Github_items\LLMs_Amazing_courses_Langchain_LlamaIndex\gpt-researcher-clean
docker-compose up -d

echo.
echo GPT Researcher 服務已啟動！
echo 請在瀏覽器中訪問 http://localhost:3000 使用服務
echo.
echo 按任意鍵打開瀏覽器...
pause > nul
start http://localhost:3000
