# LangGraph.js - MongoDB Adventure!

Welcome to the **LangGraph.js-MongoDB-Example** repository! 🚀 This project is your gateway to building and managing AI agents and conversational applications using an agentic approach with the power of LangGraph and MongoDB.

## 🛠️ Features

- **Agentic Conversations:** Harness LangGraph to manage engaging conversational flows in TypeScript.
- **Data Persistence:** Integrate with MongoDB Atlas to store and retrieve conversation data seamlessly.
- **RESTful API:** Create a dynamic chat experience using Express.js.
- **Smart Responses:** Utilize OpenAI's GPT model and Anthropic's API to generate witty replies.
- **Employee Lookup Tool:** Discover employee information using MongoDB Atlas's vector search!

## 📋 Prerequisites

Before diving in, make sure you have the following ready:
- [Node.js and npm](https://nodejs.org/)
- [MongoDB Atlas account](https://www.mongodb.com/cloud/atlas)
- [OpenAI API key](https://platform.openai.com/account/api-keys)
- [Anthropic API key](https://www.anthropic.com/claude)

## 🚀 Installation

1. **Clone the repository:**

   ```bash
   git clone https://github.com/mongodb-developer/LangGraph-MongoDB-Example.git 
   cd LangGraph-MongoDB-Example
   ```

2. **Install the required dependencies:**

   ```bash
   npm install
   ```

3. **Set up your environment variables:**
   - Create a `.env` file in the root directory.
   - Add your API keys and MongoDB URI:

   ```plaintext
   OPENAI_API_KEY=your_openai_api_key_here
   ANTHROPIC_API_KEY=your_anthropic_api_key_here
   MONGODB_ATLAS_URI=your_mongodb_atlas_uri_here
   ```

## 🌱 Seed the Database

1. Run the seed script to populate your database with some friendly faces:

   ```bash
   npm run seed
   ```

## 💻 Usage

1. **Start the server:**

   ```bash
   npm run dev
   ```

2. **Interact with the API:**

   - **Start a new conversation:**
     ```bash
     curl -X POST -H "Content-Type: application/json" -d '{"message": "Your message here"}' http://localhost:3000/chat
     ```
   - **Continue an existing conversation:**
     ```bash
     curl -X POST -H "Content-Type: application/json" -d '{"message": "Your follow-up message"}' http://localhost:3000/chat/{threadId}
     ```

## 🗂️ Project Structure

- `index.ts`: The magical entry point that sets up the Express server and API routes.
- `agent.ts`: Where the LangGraph agent is born, defining tools and conversation flow.
- `seed-database.ts`: The wizard that generates and seeds synthetic employee data into MongoDB.

## 🔍 How It Works

1. The seed script in `seed-database.ts` conjures synthetic employee data and populates the MongoDB database.
2. The LangGraph agent comes to life in `agent.ts`, complete with a conversation graph structure and tools.
3. MongoDB operations are seamlessly integrated into the agent for easy data management.
4. The Express server in `index.ts` provides API endpoints for starting and continuing conversations.
5. User inputs flow through the LangGraph agent, generating clever responses and updating the conversation state.
6. Conversation data is stored in MongoDB Atlas, ensuring smooth continuity across sessions.

## 📚 Case Study

1. **Testing API Endpoints on Windows:**
   ```bash
   curl -X POST -H "Content-Type: application/json" -d "{\"message\": \"Hello, how can I help you today?\"}" http://localhost:3000/chat
   ```
   - Response:
   ```json
   {
     "threadId": "1726900588939",
     "response": "Hello! As an HR Chatbot Agent, I'm here to assist you with any HR-related questions or inquiries you may have. How can I help you today? Is there anything specific you'd like to know about employee information, policies, or any other HR matters?"
   }
   ```

   ```bash
   curl -X POST -H "Content-Type: application/json" -d "{\"message\": \"Your follow-up message\"}" http://localhost:3000/chat
   ```

2. **Testing API Endpoints on macOS:**
   ```bash
   curl -X POST -H "Content-Type: application/json" -d '{"message": "Hello, how can I help you today?"}' http://localhost:3000/chat
   ```

3. **Testing API Endpoints on PowerShell:**
   ```powershell
   $body = @{
       user_id = "12345"
       timestamp = "2024-09-21T10:00:00Z"
       conversation_context = @{
           topic = "product inquiry"
           previous_messages = @(
               @{ from = "user"; message = "I'm interested in your latest product." }
               @{ from = "agent"; message = "Sure! Which product are you referring to?" }
           )
       }
       message = "Can you provide more details about the features and pricing?"
   }

   $response = Invoke-RestMethod -Uri "http://localhost:3000/chat" -Method Post -Body ($body | ConvertTo-Json) -ContentType "application/json"
   $response | ConvertTo-Json -Depth 10 | Out-File -FilePath response.json
   ```
   - This will return a `response.json` file in your workspace, allowing you to see the full response.

## 🤝 Contributing

We welcome contributions with open arms! Feel free to submit a Pull Request and join the fun.

## 📜 License

This project is licensed under the Apache License 2.0 - see the [LICENSE](LICENSE) file for details.




# LangGraph.js - MongoDB 冒險！

歡迎來到 **LangGraph.js-MongoDB-Example** 倉庫！🚀 這個專案是你構建和管理 AI 代理及對話應用的通行證，運用 LangGraph 和 MongoDB 的力量。

## 🛠️ 功能

- **代理對話：** 利用 LangGraph 管理引人入勝的對話流程，使用 TypeScript。
- **資料持久性：** 無縫整合 MongoDB Atlas，存取對話數據。
- **RESTful API：** 使用 Express.js 創建動態的聊天體驗。
- **智能回覆：** 利用 OpenAI 的 GPT 模型和 Anthropic 的 API 生成聰明的回覆。
- **員工查詢工具：** 使用 MongoDB Atlas 的向量搜尋來發現員工信息！

## 📋 前置條件

在開始之前，請確保您已經準備好以下內容：
- [Node.js 和 npm](https://nodejs.org/)
- [MongoDB Atlas 帳戶](https://www.mongodb.com/cloud/atlas)
- [OpenAI API 密鑰](https://platform.openai.com/account/api-keys)
- [Anthropic API 密鑰](https://www.anthropic.com/claude)

## 🚀 安裝

1. **克隆倉庫：**

   ```bash
   git clone https://github.com/mongodb-developer/LangGraph-MongoDB-Example.git 
   cd LangGraph-MongoDB-Example
   ```

2. **安裝所需的依賴：**

   ```bash
   npm install
   ```

3. **設置環境變量：**
   - 在根目錄創建一個 `.env` 文件。
   - 添加你的 API 密鑰和 MongoDB URI：

   ```plaintext
   OPENAI_API_KEY=your_openai_api_key_here
   ANTHROPIC_API_KEY=your_anthropic_api_key_here
   MONGODB_ATLAS_URI=your_mongodb_atlas_uri_here
   ```

## 🌱 填充數據庫

1. 執行填充腳本，以一些友好的面孔填充你的數據庫：

   ```bash
   npm run seed
   ```

## 💻 使用

1. **啟動伺服器：**

   ```bash
   npm run dev
   ```

2. **與 API 互動：**

   - **開始新對話：**
     ```bash
     curl -X POST -H "Content-Type: application/json" -d '{"message": "Your message here"}' http://localhost:3000/chat
     ```
   - **繼續現有對話：**
     ```bash
     curl -X POST -H "Content-Type: application/json" -d '{"message": "Your follow-up message"}' http://localhost:3000/chat/{threadId}
     ```

## 🗂️ 專案結構

- `index.ts`：神奇的入口點，設置 Express 伺服器和 API 路由。
- `agent.ts`：LangGraph 代理的誕生地，定義工具和對話流程。
- `seed-database.ts`：產生並填充合成員工數據到 MongoDB 的魔法師。

## 🔍 工作原理

1. `seed-database.ts` 中的填充腳本生成合成的員工數據，並填充到 MongoDB 數據庫。
2. LangGraph 代理在 `agent.ts` 中賦予生命，包括對話圖結構和工具。
3. MongoDB 操作直接整合到代理中，方便數據管理。
4. `index.ts` 中的 Express 伺服器提供 API 端點，啟動和繼續對話。
5. 用戶輸入通過 LangGraph 代理處理，生成適當的回應並更新對話狀態。
6. 對話數據保存在 MongoDB Atlas 中，確保會話之間的連續性。

## 📚 案例分享

1. **在 Windows 上測試 API 端點：**
   ```bash
   curl -X POST -H "Content-Type: application/json" -d "{\"message\": \"Hello, how can I help you today?\"}" http://localhost:3000/chat
   ```
   - 回應：
   ```json
   {
     "threadId": "1726900588939",
     "response": "Hello! As an HR Chatbot Agent, I'm here to assist you with any HR-related questions or inquiries you may have. How can I help you today? Is there anything specific you'd like to know about employee information, policies, or any other HR matters?"
   }
   ```

   ```bash
   curl -X POST -H "Content-Type: application/json" -d "{\"message\": \"Your follow-up message\"}" http://localhost:3000/chat
   ```

2. **在 macOS 上測試 API 端點：**
   ```bash
   curl -X POST -H "Content-Type: application/json" -d '{"message": "Hello, how can I help you today?"}' http://localhost:3000/chat
   ```

3. **在 PowerShell 上測試 API 端點：**
   ```powershell
   $body = @{
       user_id = "12345"
       timestamp = "2024-09-21T10:00:00Z"
       conversation_context = @{
           topic = "product inquiry"
           previous_messages = @(
               @{ from = "user"; message = "I'm interested in your latest product." }
               @{ from = "agent"; message = "Sure! Which product are you referring to?" }
           )
       }
       message = "Can you provide more details about the features and pricing?"
   }

   $response = Invoke-RestMethod -Uri "http://localhost:3000/chat" -Method Post -Body ($body | ConvertTo-Json) -ContentType "application/json"
   $response | ConvertTo-Json -Depth 10 | Out-File -FilePath response.json
   ```
   - 這樣會在您的工作區生成 `response.json` 文件，方便您查看完整回應。

## 🤝 貢獻

我們熱忱歡迎貢獻！隨時提交 Pull Request，加入我們的行列。


