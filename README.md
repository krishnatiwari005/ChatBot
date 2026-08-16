# 🤖 LangGraph AI Chatbot

A conversational AI chatbot built with **Python, LangChain, LangGraph, and Streamlit**.

The project uses **LangGraph** to manage the chatbot workflow through a graph-based architecture, while **Streamlit** provides an interactive web interface for users to communicate with the chatbot.

---

## 🚀 Features

* 💬 Interactive AI chatbot
* 🧠 LangGraph-based conversation workflow
* 🔗 LangChain integration
* 🖥️ Streamlit web interface
* 🔄 State-based message handling
* 🔐 Secure API key management using environment variables
* 🐍 Python virtual environment
* 📦 Dependency management using `requirements.txt`
* 🧩 Separate backend and frontend architecture

---

## 🛠️ Tech Stack

| Technology        | Purpose                         |
| ----------------- | ------------------------------- |
| **Python**        | Core programming language       |
| **LangGraph**     | Graph-based chatbot workflow    |
| **LangChain**     | LLM application framework       |
| **Streamlit**     | Interactive chatbot frontend    |
| **LLM API**       | Generates AI responses          |
| **python-dotenv** | Environment variable management |
| **Git & GitHub**  | Version control                 |

---

# 📂 Project Structure

```text
Chatbot/
│
├── myenv/                    # Python virtual environment
│
├── langgraph_backend.py      # LangGraph chatbot backend
│
├── streamlit_frontend.py     # Streamlit chatbot interface
│
├── requirements.txt          # Project dependencies
│
├── .env                      # API keys and environment variables
│
├── .gitignore                # Git ignored files
│
└── README.md                 # Project documentation
```

### Backend

`langgraph_backend.py`

Responsible for:

* Creating the LangGraph workflow
* Managing chatbot state
* Processing user messages
* Calling the LLM
* Generating chatbot responses

### Frontend

`streamlit_frontend.py`

Responsible for:

* Providing the chatbot UI
* Accepting user input
* Displaying conversation messages
* Communicating with the backend

---

# ⚙️ Installation & Setup

## 1. Clone the Repository

```bash
git clone https://github.com/your-username/your-repository-name.git
```

Navigate to the project:

```bash
cd Chatbot
```

---

## 2. Create a Virtual Environment

Create a Python virtual environment:

```bash
python -m venv myenv
```

---

## 3. Activate the Virtual Environment

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

## 4. Install Dependencies

Install the required packages:

```bash
pip install -r requirements.txt
```

---

# 🔐 Environment Variables

Create a `.env` file in the project root.

Add the API key required by the LLM provider.

For example:

```env
OPENAI_API_KEY=your_api_key_here
```

Use the variable name required by the model provider implemented in your backend.

### ⚠️ Security

Never upload your actual `.env` file to GitHub.

The project `.gitignore` excludes:

```text
.env
myenv/
```

For a public repository, you can create:

```text
.env.example
```

with only the required variable names.

---

# 🧠 LangGraph Architecture

The core of this project is the **LangGraph backend**.

LangGraph represents the chatbot workflow as a graph consisting of:

* **State**
* **Nodes**
* **Edges**
* **START**
* **END**

The current architecture separates the chatbot's processing logic from the user interface.

---

# 🔄 Complete Chatbot Flow

```text
                         ┌───────────────────┐
                         │    User Input     │
                         └─────────┬─────────┘
                                   │
                                   ▼
                         ┌───────────────────┐
                         │ Streamlit Frontend│
                         │streamlit_frontend│
                         │       .py        │
                         └─────────┬─────────┘
                                   │
                                   ▼
                         ┌───────────────────┐
                         │ LangGraph Backend │
                         │langgraph_backend │
                         │       .py        │
                         └─────────┬─────────┘
                                   │
                                   ▼
                         ┌───────────────────┐
                         │   Graph State     │
                         │                   │
                         │    Messages       │
                         └─────────┬─────────┘
                                   │
                                   ▼
                         ┌───────────────────┐
                         │   Chatbot Node    │
                         │                   │
                         │       LLM         │
                         └─────────┬─────────┘
                                   │
                                   ▼
                         ┌───────────────────┐
                         │   AI Response     │
                         └─────────┬─────────┘
                                   │
                                   ▼
                         ┌───────────────────┐
                         │ Streamlit Display │
                         └─────────┬─────────┘
                                   │
                                   ▼
                              👤 User
```

---

# 🔗 LangGraph Workflow

At the backend level, the workflow follows:

```text
START
  │
  ▼
Chatbot Node
  │
  ▼
LLM
  │
  ▼
Updated State
  │
  ▼
END
```

The graph receives the user's message, processes it through the chatbot node, generates an LLM response, updates the state, and returns the response.

---

# 🖥️ Streamlit Frontend

The Streamlit application provides the user-facing chatbot interface.

The overall application can be viewed as:

```text
             ┌─────────────────────┐
             │      USER           │
             └──────────┬──────────┘
                        │
                        ▼
             ┌─────────────────────┐
             │ Streamlit Frontend  │
             │                     │
             │ streamlit_frontend  │
             │       .py           │
             └──────────┬──────────┘
                        │
                        ▼
             ┌─────────────────────┐
             │  LangGraph Backend  │
             │                     │
             │ langgraph_backend   │
             │       .py           │
             └──────────┬──────────┘
                        │
                        ▼
             ┌─────────────────────┐
             │        LLM          │
             └──────────┬──────────┘
                        │
                        ▼
             ┌─────────────────────┐
             │   Generated Reply   │
             └──────────┬──────────┘
                        │
                        ▼
             ┌─────────────────────┐
             │ Streamlit Interface │
             └─────────────────────┘
```

This separation makes the project easier to maintain because the **UI and AI processing logic are kept separate**.

---

# ▶️ Running the Application

After installing the dependencies and activating the virtual environment, start the Streamlit application using:

```bash
streamlit run streamlit_frontend.py
```

Streamlit will start the local web application.

You can then open the displayed local URL in your browser.

---

# 📦 Managing Dependencies

All required packages are stored in:

```text
requirements.txt
```

Install them with:

```bash
pip install -r requirements.txt
```

If you install a new package during development, update the requirements file:

```bash
pip freeze > requirements.txt
```

---

# 🔒 Git & Security

The project uses `.gitignore` to prevent unnecessary and sensitive files from being committed.

Important ignored files include:

```text
myenv/
.env
__pycache__/
*.pyc
```

This keeps the repository clean and prevents API credentials from accidentally being pushed to GitHub.

---

# 🔮 Future Enhancements

The current chatbot provides a foundation for developing a more advanced AI agent.

Potential improvements include:

* 🧠 Persistent conversation memory
* 🔍 Retrieval-Augmented Generation (RAG)
* 📄 PDF and document question answering
* 🛠️ Tool calling
* 🔀 Conditional LangGraph routing
* 🤖 Multi-agent workflows
* 🌐 FastAPI backend
* 🔐 User authentication
* 📊 LangSmith tracing and monitoring
* 🗃️ Database-backed chat history
* 🚀 Cloud deployment

---

# 🎯 Learning Outcomes

This project demonstrates practical understanding of:

* LangGraph
* LangChain
* LLM application development
* Graph-based AI workflows
* State management
* Streamlit application development
* Python virtual environments
* Environment variable management
* Dependency management
* Git and GitHub

---

# 👨‍💻 Author

## Krishna Tiwari

**B.Tech Computer Science & Engineering | AI & ML**

Interested in:

**Artificial Intelligence • Machine Learning • NLP • LLMs • AI Agents**

---

## ⭐ Project Objective

The objective of this project is to understand and implement a **graph-based conversational AI system** using LangGraph, while building a clean interactive interface with Streamlit.

The project serves as a foundation for developing more advanced **stateful AI agents, RAG systems, and multi-step LLM workflows**.
