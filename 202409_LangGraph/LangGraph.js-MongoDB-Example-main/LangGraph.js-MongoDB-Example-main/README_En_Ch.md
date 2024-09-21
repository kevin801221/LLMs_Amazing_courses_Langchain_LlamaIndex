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

