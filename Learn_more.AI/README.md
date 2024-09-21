# LermoAI：個性化學習的 AI 代理

## 重新定義學習的方式 🌟

LermoAI 是一個開源專案，旨在徹底改變你學習的方式！這個智慧型學習助手透過生成符合你個人偏好的內容，讓學習變得高效又有趣。無論你喜歡閱讀文章、收聽播客，還是觀看視頻，LermoAI 都能為你量身定制專屬的學習材料。選擇你的 AI 代理，開始一段完美契合你需求的學習之旅吧！

## 特色功能 🚀

- **AI 代理**：智能幫助你學習，隨時隨地為你提供支援。
- **文章生成**：根據你的喜好創建定制文章。
- **播客生成**：生動有趣的播客內容，讓學習隨行。
- **支持多種 LLM**：包括 OpenAI、Mistral、Llama、Groq 和 Claude 等。
- **學習路徑**：為你制定專屬學習計畫。
- **聊天代理**：隨時解答你的問題。
- **視頻生成**：製作吸引人的學習視頻。
- **自定義代理**：根據需求打造個性化的 AI 代理。
- **搜索代理**：快速找到你需要的學習資源。

## 如何開始 🛠️

### 需求
- Node.js
- Next.js
- React
- Python
- Web

### 設置前端
進入前端應用資料夾：

```bash
cd apps/frontend/apps/lermo-gen-web
```

安裝依賴：

```bash
pnpm i
```

啟動應用：

```bash
pnpm run dev
```

### 設置 API
進入 API 資料夾：

```bash
cd apps/api/core-api
```

安裝依賴：

```bash
pip install -r requirements.txt
pip install git+https://github.com/myshell-ai/MeloTTS.git
python -m unidic download
```

啟動 API：

```bash
python main.py
```

### Docker 設置
編輯環境變量以使用 OpenAI 或自托管的 LLM：

```yaml
# OpenAI
args:
  - OPENAI_API_BASE=https://api.openai.com/v1
  - OPENAI_API_KEY=sk-proj-xxx
```

或使用 Hugging Face：

```yaml
# Hugging Face
args:
  - OPENAI_API_BASE=https://llama-cpp.hf.space
  - OPENAI_API_KEY=llama-key
```

啟動 Docker 容器：

```bash
docker-compose up
```

## 免費開放，人人可用 🎉

在 Lermo，我們相信教育應該對所有人開放。因此，我們的服務完全免費，旨在推動教育的民主化，為每位學習者提供平等的機會。

## 支持我們 🙌


## Lermo 的使命 ✨

想像一個突破性教育系統，超越障礙，為所有人提供無限的知識訪問。這個系統體現了包容和平等，使全球的學習者能夠充分發揮潛力，追逐夢想。讓我們一起追求一個屬於每個人的教育系統，成為希望和賦能的燈塔，啟發未來的世代，創造積極的影響。

---

### 參考出處
[原始資料來源](https://github.com/myshell-ai/LermoAI)

--- 

### LermoAI: Your AI Agent for Personalized Learning

## Redefining the Way You Learn 🌟

LermoAI is an open-source project that aims to revolutionize the way you learn! This smart learning assistant generates content tailored to your personal preferences, making learning efficient and enjoyable. Whether you prefer reading articles, listening to podcasts, or watching videos, LermoAI creates custom learning materials just for you. Choose your AI agent and embark on a learning journey perfectly suited to your needs!

## Features 🚀

- **AI Agent**: Your intelligent learning companion, ready to assist anytime, anywhere.
- **Article Generation**: Create custom articles based on your interests.
- **Podcast Generation**: Engaging podcast content to learn on the go.
- **Supports Various LLMs**: Including OpenAI, Mistral, Llama, Groq, and Claude.
- **Learning Path**: A personalized learning plan just for you.
- **Chat Agent**: Get your questions answered in real time.
- **Video Generation**: Produce captivating learning videos.
- **Custom Agent**: Build a personalized AI agent tailored to your needs.
- **Search Agent**: Quickly find the learning resources you need.

## Getting Started 🛠️

### Requirements
- Node.js
- Next.js
- React
- Python
- Web

### Setting Up the Frontend
Navigate to the frontend application folder:

```bash
cd apps/frontend/apps/lermo-gen-web
```

Install dependencies:

```bash
pnpm i
```

Start the application:

```bash
pnpm run dev
```

### Setting Up the API
Navigate to the API folder:

```bash
cd apps/api/core-api
```

Install dependencies:

```bash
pip install -r requirements.txt
pip install git+https://github.com/myshell-ai/MeloTTS.git
python -m unidic download
```

Start the API:

```bash
python main.py
```

### Docker Setup
Edit the environment variables to use either OpenAI or your self-hosted LLM:

```yaml
# OpenAI
args:
  - OPENAI_API_BASE=https://api.openai.com/v1
  - OPENAI_API_KEY=sk-proj-xxx
```

Or for Hugging Face:

```yaml
# Hugging Face
args:
  - OPENAI_API_BASE=https://llama-cpp.hf.space
  - OPENAI_API_KEY=llama-key
```

Start the Docker containers:

```bash
docker-compose up
```

## Free and Open for Everyone 🎉

At Lermo, we believe in making education accessible to all. That's why our services are completely free, aimed at democratizing education and providing equal opportunities for all learners.

## Support Us 🙌


## Lermo's Mission ✨

"Picture a groundbreaking education system that transcends barriers, offering boundless access to knowledge for all. It embodies inclusivity and equality, empowering learners worldwide to embrace their potential and pursue dreams without constraints. In this educational utopia, knowledge fuels curiosity, ignites intellect, and fosters a love for learning, shaping a brighter, enlightened future for humanity. Let's dare to envision and strive for an education system that belongs to everyone—a beacon of hope and empowerment, inspiring generations to flourish and make a positive impact."

---

### Reference
[Original Source](https://github.com/myshell-ai/LermoAI)

---

