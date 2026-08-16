# 🤖 LangGraph AI Chatbot

A simple conversational AI chatbot built using **Python, LangGraph, LangChain, Groq, and Streamlit**.

The project uses **LangGraph** to manage the chatbot workflow and **Streamlit** to create the user interface.

---

## ✨ Features

* 💬 Interactive AI chatbot
* 🧠 LangGraph workflow
* ⚡ Groq LLM for fast responses
* 🔗 LangChain integration
* 🧵 Thread-based conversation state
* 💾 In-memory checkpointing
* 🖥️ Streamlit chat interface
* 🔐 Secure API key management
* 📦 Separate frontend and backend

---

## 🛠️ Tech Stack

| Technology    | Purpose                         |
| ------------- | ------------------------------- |
| Python        | Main programming language       |
| LangGraph     | Chatbot workflow                |
| LangChain     | LLM application framework       |
| ChatGroq      | Connects application with Groq  |
| Groq          | AI model inference              |
| Streamlit     | Chat interface                  |
| python-dotenv | Environment variable management |
| Git & GitHub  | Version control                 |

---

## 📂 Project Structure

```text
Chatbot/
│
├── myenv/
├── langgraph_backend.py
├── streamlit_frontend.py
├── requirements.txt
├── .env
├── .gitignore
└── README.md
```

### Backend

`langgraph_backend.py` handles:

* LangGraph workflow
* Chatbot state
* Chatbot node
* Groq model
* Conversation checkpointing

### Frontend

`streamlit_frontend.py` handles:

* Chat interface
* User input
* Message display
* Communication with backend

---

## 🔄 Project Flow

```text
User
  ↓
Streamlit
  ↓
LangGraph
  ↓
Chatbot Node
  ↓
Groq LLM
  ↓
AI Response
  ↓
Streamlit
```

---

## 🧠 LangGraph Workflow

```text
START
  ↓
Chatbot Node
  ↓
END
```

The chatbot node receives the messages, sends them to the Groq model, and returns the AI response.

---

## 💾 Conversation State

The project uses `InMemorySaver` to maintain conversation state.

A `thread_id` identifies a conversation.

```text
User Message
     ↓
Thread ID
     ↓
LangGraph State
     ↓
Chatbot Node
     ↓
Groq LLM
     ↓
AI Response
```

Example:

```python
config = {
    "configurable": {
        "thread_id": "thread-1"
    }
}
```

---

## 🧩 Main Components

### State

Stores the conversation messages.

```python
class ChatbotState(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages]
```

### Chatbot Node

```python
def chat_node(state: ChatbotState):
    messages = state["messages"]
    response = model.invoke(messages)

    return {
        "messages": response
    }
```

### Graph

```text
START
  ↓
chat_node
  ↓
END
```

### Checkpointing

The project uses:

```python
InMemorySaver()
```

to maintain conversation state in memory.

---

## 🔗 Frontend & Backend

```text
          CHATBOT
             │
      ┌──────┴──────┐
      ↓             ↓
  Frontend       Backend
  Streamlit      LangGraph
      │             │
      │          LangChain
      │             │
      │          ChatGroq
      │             │
      └──────┬──────┘
             ↓
        AI Response
```

---

## 🎯 Project Objective

The objective of this project is to learn how to build a **stateful AI chatbot using LangGraph**.

### What I Learned

* LangGraph
* LangChain
* Groq LLM integration
* Graph-based workflows
* Conversation state
* Streamlit
* Environment variables
* Python virtual environments
* Dependency management
* Frontend and backend separation

---

## 🚀 Future Improvements

* 🧠 Long-term memory
* 📄 PDF question answering
* 🔍 RAG
* 🛠️ Tool calling
* 🔀 Conditional routing
* 🤖 AI agents
* 🗃️ Database chat history
* 🔐 User authentication
* 📊 LangSmith monitoring
* 🌐 Cloud deployment

---

## 👨‍💻 Author

### Krishna Tiwari

**B.Tech Computer Science & Engineering | AI & ML**

**AI • Machine Learning • NLP • LLMs • AI Agents**

---

<details>
<summary>⚙️ Installation & Setup</summary>

<br>

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/your-username/your-repository-name.git
cd Chatbot
```

### 2️⃣ Create Virtual Environment

```bash
python -m venv myenv
```

### 3️⃣ Activate Virtual Environment

**Windows PowerShell**

```powershell
.\myenv\Scripts\Activate.ps1
```

**Windows CMD**

```cmd
myenv\Scripts\activate
```

After activation, you should see:

```text
(myenv) PS C:\...\Chatbot>
```

### 4️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

### 5️⃣ Setup Groq API Key

Create a `.env` file in the project root:

```env
GROQ_API_KEY=your_groq_api_key
```

The application loads this key using `python-dotenv`.

### 6️⃣ Protect Your API Key

Make sure `.gitignore` contains:

```text
.env
myenv/
__pycache__/
*.pyc
```

**Never upload your real `.env` file to GitHub.**

### 7️⃣ Run the Application

```bash
streamlit run streamlit_frontend.py
```

The Streamlit application will start and provide a local URL.

### 📦 Main Dependencies

```text
streamlit
langgraph
langchain
langchain-groq
langchain-core
python-dotenv
```

You can install them manually with:

```bash
pip install streamlit langgraph langchain langchain-groq langchain-core python-dotenv
```

</details>

---

⭐ **If you like this project, consider giving it a star!**
