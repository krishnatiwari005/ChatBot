from langgraph.graph import StateGraph,START,END
from langchain_groq import ChatGroq
from typing import TypedDict,Annotated,Dict,Any,Optional
from langchain_core.messages import BaseMessage,HumanMessage
from langgraph.graph.message import add_messages
from langgraph.checkpoint.sqlite import SqliteSaver
from dotenv import load_dotenv
from langgraph.prebuilt import ToolNode,tools_condition
from langchain_community.tools import DuckDuckGoSearchRun
from langchain_core.tools import tool, InjectedToolArg
from langchain_core.runnables import RunnableConfig
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.vectorstores import FAISS
from langchain_text_splitters import RecursiveCharacterTextSplitter
import tempfile
import os
import sqlite3
import requests


load_dotenv()

model=ChatGroq(model="openai/gpt-oss-120b")
api_key=os.getenv("GROQ_API_KEY")
embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

stock_api_key=os.getenv("api_key")
# -------------------
# 2. PDF retriever store (per thread)
# -------------------

_THREAD_RETRIEVERS: Dict[str, Any] = {}
_THREAD_METADATA: Dict[str, dict] = {}

def _get_retriever(thread_id: Optional[str]):
    """Fetch the retriever for a thread if available."""

    if thread_id and thread_id in _THREAD_RETRIEVERS:
        return _THREAD_RETRIEVERS[thread_id]

    return None


def ingest_pdf(file_bytes: bytes,thread_id: str,filename: Optional[str] = None) -> dict:
    """
    Build a FAISS retriever for the uploaded PDF
    and store it for the thread.

    Returns a summary dictionary.
    """
    if not file_bytes:
        raise ValueError("No bytes received for ingestion.")

    # -------------------
    # Save PDF temporarily
    # -------------------

    with tempfile.NamedTemporaryFile(delete=False,suffix=".pdf") as temp_file:
        temp_file.write(file_bytes)
        temp_path = temp_file.name

    try:

        # -------------------
        # Load PDF
        # -------------------

        loader = PyPDFLoader(temp_path)

        docs = loader.load()

        # -------------------
        # Split PDF into chunks
        # -------------------

        splitter = RecursiveCharacterTextSplitter(chunk_size=1000,chunk_overlap=200,separators=["\n\n","\n"," ",""])

        chunks = splitter.split_documents(docs)

        # -------------------
        # Create FAISS vector store
        # -------------------

        vector_store = FAISS.from_documents(chunks,embeddings)

        # -------------------
        # Create retriever
        # -------------------

        retriever = vector_store.as_retriever(search_type="similarity",search_kwargs={"k": 4})

        # -------------------
        # Store retriever
        # -------------------

        thread_key = str(thread_id)

        _THREAD_RETRIEVERS[thread_key] = retriever

        _THREAD_METADATA[thread_key] = {
            "filename": filename or os.path.basename(temp_path),
            "documents": len(docs),
            "chunks": len(chunks),
        }

        # -------------------
        # Return information
        # -------------------

        return {
            "filename": filename or os.path.basename(temp_path),
            "documents": len(docs),
            "chunks": len(chunks),
        }

    finally:

        # -------------------
        # Delete temporary PDF
        # -------------------

        try:
            os.remove(temp_path)
        except OSError:
            pass

#tools
search_tool=DuckDuckGoSearchRun()

@tool
def calculate(first_num:float,second_num:float,operation:str)->dict:
    "perform basic arithmetic operation on two numbber supported operation are add, sub, divide, multiply"
    try:
        if operation=='add':
             result=first_num+second_num
        elif operation=='sub':
            result=first_num-second_num
        elif operation=='mul':
            result=first_num*second_num
        else:
            if second_num==0:
                return {"error"}
            result=first_num/second_num
        return {"result":result}
    except Exception as e:
        return {'error':str(e)}

@tool 
def get_stock_price(symbol:str)->dict:
    "fetch latest stock price for a given sumbol (eg: AAPL,TSLA)using alpha vantage api key "
    url= f"https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={symbol}&apikey={stock_api_key}"
    r=requests.get(url)
    return r.json

@tool
def rag_tool(query: str, config:Annotated[RunnableConfig,InjectedToolArg]) -> dict:
    """
    Retrieve relevant information from the uploaded PDF for this chat thread.
    Always include the thread_id when calling this tool.
    """
    thread_id = config.get("configurable", {}).get("thread_id")
    retriever = _get_retriever(thread_id)
    if retriever is None:
        return {
            "error": "No document indexed for this chat. Upload a PDF first.",
            "query": query,
        }

    result = retriever.invoke(query)
    context = [doc.page_content for doc in result]
    metadata = [doc.metadata for doc in result]

    return {
        "query": query,
        "context": context,
        "metadata": metadata,
        "source_file": _THREAD_METADATA.get(str(thread_id), {}).get("filename"),
    }

tools=[get_stock_price,search_tool,calculate,rag_tool]
llm_with_tool=model.bind_tools(tools)


class ChatbotState(TypedDict):
    messages:Annotated[list[BaseMessage],add_messages]

def chat_node(state:ChatbotState):
    """llm node that may answer or request a tool call"""
    messages=state['messages']
    response=llm_with_tool.invoke(messages)
    return {'messages':response}
tool_node=ToolNode(tools)

conn=sqlite3.connect(database="chatbot.db",check_same_thread=False)
checkpointer=SqliteSaver(conn=conn)

graph=StateGraph(ChatbotState)
graph.add_node('chat_node',chat_node)
graph.add_node('tools',tool_node)
graph.add_edge(START,'chat_node')
graph.add_conditional_edges('chat_node',tools_condition)
graph.add_edge('tools','chat_node')

chat=graph.compile(checkpointer=checkpointer)

def retrieve_all_threads():
    all_threads=set()
    for checkpoint in checkpointer.list(None):
        thread_id=checkpoint.config.get('configurable',{}).get('thread_id')
        if thread_id:
          all_threads.add(thread_id)
    return list(all_threads)    

def thread_has_document(thread_id: str) -> bool:
    return str(thread_id) in _THREAD_RETRIEVERS

def thread_document_metadata(thread_id: str) -> dict:
    return _THREAD_METADATA.get(str(thread_id), {})