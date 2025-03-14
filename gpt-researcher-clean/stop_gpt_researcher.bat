@echo off
echo 正在停止 GPT Researcher 服務...
echo.

cd /d D:\Github_items\LLMs_Amazing_courses_Langchain_LlamaIndex\gpt-researcher-clean
docker-compose down

echo.
echo GPT Researcher 服務已停止！
echo.
echo 按任意鍵關閉此視窗...
pause > nul
