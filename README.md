# 🤖 Multi-Utility AI Chatbot

A conversational AI chatbot built using **Python, LangGraph, LangChain, Groq, Streamlit, and RAG**.

The application combines a stateful LangGraph workflow with multiple tools, web search, stock-price lookup, mathematical calculations, and **PDF question answering using Retrieval-Augmented Generation (RAG)**.

The frontend is built with **Streamlit**, while the chatbot workflow and tools are implemented in a separate **LangGraph backend**.

---

## ✨ Features

* 💬 Interactive AI chatbot
* 🧠 LangGraph-based conversational workflow
* ⚡ Groq LLM for fast inference
* 🔗 LangChain integration
* 🧵 Thread-based conversation management
* 💾 Persistent conversation checkpointing using SQLite
* 🛠️ Tool calling with LangGraph
* 🔍 DuckDuckGo web search
* 📈 Stock price lookup using Alpha Vantage
* 🧮 Basic mathematical calculations
* 📄 PDF document upload
* 📚 PDF question answering using RAG
* 🔎 FAISS vector database for document retrieval
* 🤗 HuggingFace sentence-transformer embeddings
* 📑 Automatic PDF chunking
* 🗂️ Per-thread document storage
* 🖥️ Streamlit chat interface
* 🔐 Environment variable support for API keys
* 📡 Streaming AI responses
* 🔧 Tool execution status shown in the UI
* 📂 Separate frontend and backend architecture

---

## 🛠️ Tech Stack

| Technology                     | Purpose                                    |
| ------------------------------ | ------------------------------------------ |
| Python                         | Main programming language                  |
| LangGraph                      | Stateful chatbot workflow and tool routing |
| LangChain                      | LLM application framework                  |
| ChatGroq                       | Groq LLM integration                       |
| Groq                           | AI model inference                         |
| LangChain Community            | Search and document-loading tools          |
| DuckDuckGo                     | Web search                                 |
| Alpha Vantage                  | Stock price API                            |
| HuggingFace Embeddings         | Text embeddings                            |
| Sentence Transformers          | Embedding model                            |
| FAISS                          | Vector similarity search                   |
| PyPDFLoader                    | PDF document loading                       |
| RecursiveCharacterTextSplitter | Document chunking                          |
| SQLite                         | Conversation checkpoint storage            |
| Streamlit                      | Frontend and chat interface                |
| python-dotenv                  | Environment variable management            |
| Requests                       | HTTP API requests                          |
| Git & GitHub                   | Version control                            |

---

## 📂 Project Structure

```text
Chatbot/
│
├── myenv/
│
├── langgraph_backend.py
├── streamlit_frontend.py
├── ui.py
│
├── chatbot.db
├── requirements.txt
├── .env
├── .gitignore
└── README.md
```

### Backend — `langgraph_backend.py`

The backend is responsible for:

* LangGraph workflow
* Chatbot state
* Groq LLM
* Tool calling
* SQLite checkpointing
* DuckDuckGo search
* Stock price retrieval
* Calculator tool
* PDF ingestion
* PDF chunking
* HuggingFace embeddings
* FAISS vector store
* RAG retrieval
* Thread-specific document management

### Frontend — `streamlit_frontend.py`

The frontend is responsible for:

* Streamlit UI
* Chat input
* Chat message display
* Chat history
* Creating new conversations
* Selecting previous conversations
* PDF upload
* PDF indexing status
* Tool execution status
* Streaming AI responses
* Displaying document metadata

### UI — `ui.py`

Contains reusable Streamlit UI functionality such as:

* Custom CSS
* Sidebar sections
* UI styling

---

# 🔄 Application Flow

```text
                         USER
                           │
                           ▼
                    Streamlit Frontend
                           │
                           ▼
                    LangGraph Backend
                           │
                           ▼
                       chat_node
                           │
                    ┌──────┴──────┐
                    │             │
                 AI Answer      Tool Call
                    │             │
                    │             ▼
                    │          ToolNode
                    │             │
                    │     ┌───────┼────────┐
                    │     │       │        │
                    │   Search Calculator Stock
                    │     │       │        │
                    │     │       │        │
                    │     └───────┼────────┘
                    │             │
                    │             ▼
                    │         chat_node
                    │
                    ▼
                AI Response
                    │
                    ▼
                Streamlit UI
```

---

# 🧠 LangGraph Workflow

The chatbot uses a conditional LangGraph workflow.

```text
                 START
                   │
                   ▼
              chat_node
                   │
             ┌─────┴─────┐
             │           │
        Tool required   No tool
             │           │
             ▼           ▼
          ToolNode      END
             │
             ▼
         chat_node
             │
             ▼
            END
```

The `chat_node` sends the conversation to the Groq model.

If the model decides that a tool is required, LangGraph routes execution to the `ToolNode`.

After the tool finishes, the result is sent back to the `chat_node`, allowing the model to generate the final response.

---

# 🧩 Chatbot State

The conversation state stores the messages exchanged during a conversation.

```python
class ChatbotState(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages]
```

The `add_messages` reducer allows new messages to be added to the existing conversation state.

---

# 🤖 Groq LLM

The chatbot uses `ChatGroq` for model inference.

```python
model = ChatGroq(
    model="openai/gpt-oss-120b"
)
```

The model is then connected to the available tools:

```python
llm_with_tool = model.bind_tools(tools)
```

This allows the LLM to decide when it should call a tool.

---

# 🛠️ Available Tools

The chatbot currently provides four tools.

## 1. 🔍 Web Search

Powered by DuckDuckGo.

```python
search_tool = DuckDuckGoSearchRun()
```

The AI can use web search when information needs to be retrieved from the internet.

---

## 2. 🧮 Calculator

The calculator supports basic arithmetic operations:

* Addition
* Subtraction
* Multiplication
* Division

Example:

```text
User:
What is 25 × 8?

AI:
200
```

The calculator is implemented using LangChain's `@tool` decorator.

---

## 3. 📈 Stock Price

The chatbot can retrieve stock information using the Alpha Vantage API.

```python
@tool
def get_stock_price(symbol: str) -> dict:
    ...
```

Example:

```text
User:
What is the current stock price of AAPL?

AI:
Uses the stock price tool to retrieve the latest available quote.
```

The Alpha Vantage API key is loaded from the environment.

---

## 4. 📄 PDF RAG Tool

The chatbot can answer questions based on an uploaded PDF.

The RAG pipeline works as follows:

```text
PDF Upload
    ↓
PyPDFLoader
    ↓
Document Extraction
    ↓
Text Chunking
    ↓
HuggingFace Embeddings
    ↓
FAISS Vector Store
    ↓
Retriever
    ↓
User Question
    ↓
Relevant Chunks
    ↓
LLM
    ↓
Answer
```

The PDF retriever is stored separately for each conversation thread.

---

# 📚 PDF RAG System

The chatbot supports document-based question answering.

## Step 1 — Upload PDF

The user uploads a PDF from the Streamlit sidebar.

```python
uploaded_pdf = st.sidebar.file_uploader(
    "Upload PDF for this chat",
    type=["pdf"]
)
```

---

## Step 2 — Load PDF

The application uses `PyPDFLoader`.

```python
loader = PyPDFLoader(temp_path)

docs = loader.load()
```

---

## Step 3 — Split Documents

The extracted content is divided into smaller chunks.

```python
splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=200
)
```

This improves retrieval by allowing the system to search smaller relevant sections of the document.

---

## Step 4 — Create Embeddings

The project uses:

```text
sentence-transformers/all-MiniLM-L6-v2
```

through HuggingFace embeddings.

```python
embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)
```

---

## Step 5 — Store in FAISS

The chunks are converted into vectors and stored using FAISS.

```python
vector_store = FAISS.from_documents(
    chunks,
    embeddings
)
```

A retriever is then created:

```python
retriever = vector_store.as_retriever(
    search_type="similarity",
    search_kwargs={"k": 4}
)
```

The system retrieves the four most relevant chunks for a query.

---

# 🧵 Thread-Based PDF Retrieval

Each conversation has its own `thread_id`.

The application maintains:

```python
_THREAD_RETRIEVERS
```

and:

```python
_THREAD_METADATA
```

This allows PDFs to be associated with individual conversations.

For example:

```text
Chat 1
 ├── thread_id: A
 └── PDF: Machine Learning.pdf

Chat 2
 ├── thread_id: B
 └── PDF: Python.pdf
```

Questions in Chat 1 use the retriever associated with Chat 1.

Questions in Chat 2 use the retriever associated with Chat 2.

---

# 💾 Conversation Checkpointing

The application uses **SQLite-based checkpointing** rather than in-memory checkpointing.

```python
conn = sqlite3.connect(
    database="chatbot.db",
    check_same_thread=False
)

checkpointer = SqliteSaver(
    conn=conn
)
```

The graph is compiled with:

```python
chat = graph.compile(
    checkpointer=checkpointer
)
```

This allows LangGraph to maintain conversation state using a persistent SQLite database.

---

# 🧵 Conversation Threads

Each conversation receives a unique thread ID.

```python
def generate_thread_id():
    return uuid.uuid4()
```

The thread ID is passed to LangGraph:

```python
config = {
    "configurable": {
        "thread_id": thread_key
    }
}
```

This allows multiple conversations to maintain separate histories.

```text
Thread A
 ├── User message
 ├── AI response
 ├── User message
 └── AI response

Thread B
 ├── User message
 ├── AI response
 └── User message
```

---

# 🔧 Tool Calling Flow

The application uses LangGraph's built-in:

```python
ToolNode
```

and:

```python
tools_condition
```

The workflow is:

```text
User Question
      ↓
   chat_node
      ↓
Does AI need a tool?
      │
   ┌──┴──┐
   │     │
  Yes    No
   │     │
   ▼     ▼
ToolNode END
   │
   ▼
chat_node
   │
   ▼
  END
```

This creates an agent-like workflow where the model can dynamically decide whether a tool is needed.

---

# 🖥️ Streamlit Interface

The Streamlit frontend provides:

### 💬 Chat

Users can ask questions through:

```python
st.chat_input()
```

### 🗂️ Chat History

Previous conversations are displayed in the sidebar.

Users can select a previous thread to load its messages.

### ➕ New Chat

The application generates a new UUID and starts a new conversation.

### 📄 PDF Upload

Users can upload a PDF directly from the sidebar.

The UI displays:

```text
📚 Indexing PDF...
```

and then:

```text
✅ PDF indexed successfully
```

### 🔧 Tool Status

When a tool is being executed, the interface displays information such as:

```text
🔧 Using `search_tool`...
```

After completion:

```text
✅ Tool finished
```

### 📡 Streaming

AI responses are streamed to the Streamlit interface using:

```python
st.write_stream()
```

---

# 🔐 Environment Variables

Create a `.env` file in the project root.

```env
GROQ_API_KEY=your_groq_api_key
api_key=your_alpha_vantage_api_key
```

The application loads environment variables using:

```python
from dotenv import load_dotenv

load_dotenv()
```

### ⚠️ Important

Do not commit your real API keys to GitHub.

Add the following to `.gitignore`:

```text
.env
myenv/
__pycache__/
*.pyc
chatbot.db
```

---

# 📦 Installation & Setup

<details>

<summary>⚙️ Click to expand installation instructions</summary>

<br>

## 1️⃣ Clone the Repository

```bash
git clone https://github.com/your-username/your-repository-name.git

cd Chatbot
```

---

## 2️⃣ Create Virtual Environment

```bash
python -m venv myenv
```

---

## 3️⃣ Activate Virtual Environment

### Windows PowerShell

```powershell
.\myenv\Scripts\Activate.ps1
```

### Windows CMD

```cmd
myenv\Scripts\activate
```

After activation:

```text
(myenv) PS C:\...\Chatbot>
```

---

## 4️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 5️⃣ Configure API Keys

Create:

```text
.env
```

and add:

```env
GROQ_API_KEY=your_groq_api_key
api_key=your_alpha_vantage_api_key
```

---

## 6️⃣ Run the Application

```bash
streamlit run streamlit_frontend.py
```

Streamlit will provide a local URL where the chatbot can be accessed.

</details>

---

# 📦 Main Dependencies

The project uses packages including:

```text
langgraph
langchain
langchain-groq
langchain-community
langchain-core
langchain-text-splitters
langchain-huggingface
langgraph-checkpoint-sqlite
streamlit
python-dotenv
sentence-transformers
faiss-cpu
duckduckgo-search
requests
pypdf
```

Install all dependencies using:

```bash
pip install -r requirements.txt
```

---

# 📊 Complete Architecture

```text
                         ┌──────────────────────┐
                         │       USER           │
                         └──────────┬───────────┘
                                    │
                                    ▼
                         ┌──────────────────────┐
                         │  Streamlit Frontend │
                         └──────────┬───────────┘
                                    │
                                    ▼
                         ┌──────────────────────┐
                         │    LangGraph        │
                         │     Workflow        │
                         └──────────┬───────────┘
                                    │
                                    ▼
                         ┌──────────────────────┐
                         │     Chat Node        │
                         │     ChatGroq         │
                         └──────────┬───────────┘
                                    │
                         ┌──────────┴──────────┐
                         │                     │
                    Normal Answer          Tool Call
                         │                     │
                         │                     ▼
                         │              ┌─────────────┐
                         │              │  ToolNode   │
                         │              └──────┬──────┘
                         │                     │
                         │        ┌────────────┼─────────────┐
                         │        │            │             │
                         │        ▼            ▼             ▼
                         │      Search     Calculator      Stock
                         │
                         │                     │
                         │                     ▼
                         │                RAG Tool
                         │                     │
                         │              ┌──────┴──────┐
                         │              │             │
                         │             FAISS     Embeddings
                         │              │
                         │              ▼
                         │          PDF Context
                         │
                         └──────────────┬──────────────┘
                                        │
                                        ▼
                                Final AI Response
                                        │
                                        ▼
                                Streamlit Frontend
```

---

# 🎯 Project Objective

The objective of this project is to build a **stateful, tool-using AI chatbot using LangGraph** and extend it with document-based RAG capabilities.

The project demonstrates how multiple AI application concepts can be combined into a single system.

---

# 🧠 What I Learned

Through this project, I worked with:

* LangGraph
* LangChain
* Groq LLMs
* Tool calling
* Conditional graph routing
* LangGraph `ToolNode`
* Conversation state
* SQLite checkpointing
* Thread-based conversations
* Streamlit
* Web search
* API integration
* PDF processing
* RAG
* Vector databases
* FAISS
* HuggingFace embeddings
* Sentence Transformers
* Environment variables
* Python virtual environments
* Dependency management
* Frontend/backend separation
* Streaming AI responses

---

# 🚀 Future Improvements

Possible future improvements include:

* 🧠 Long-term memory
* 💬 Improved conversation management
* 📚 Multiple-document RAG
* 🗃️ Persistent FAISS indexes
* 🔐 User authentication
* 👤 User-specific document storage
* 📊 LangSmith monitoring
* ⚡ Better streaming experience
* 🧠 Advanced agent workflows
* 🔀 More sophisticated conditional routing
* 🌐 FastAPI backend
* ☁️ Cloud deployment
* 📱 Responsive UI
* 🗂️ Document management system
* 🧾 Source citations for RAG answers
* 🧪 Automated testing

---

# 👨‍💻 Author

## Krishna Tiwari

**B.Tech Computer Science & Engineering | AI & ML**

**AI • Machine Learning • NLP • LLMs • AI Agents • RAG**

---

## ⭐ Project Highlights

This project combines several important concepts in modern AI application development:

```text
LLM
 │
 ├── LangGraph
 │     ├── State Management
 │     ├── Tool Routing
 │     └── Checkpointing
 │
 ├── Tools
 │     ├── Web Search
 │     ├── Calculator
 │     └── Stock API
 │
 ├── RAG
 │     ├── PDF Loader
 │     ├── Chunking
 │     ├── Embeddings
 │     ├── FAISS
 │     └── Retrieval
 │
 └── Streamlit
       ├── Chat UI
       ├── Chat History
       ├── PDF Upload
       └── Streaming
```

⭐ **If you like this project, consider giving it a star!**
