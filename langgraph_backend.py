from langgraph.graph import StateGraph,START,END
from langchain_groq import ChatGroq
from typing import TypedDict,Annotated
from langchain_core.messages import BaseMessage,HumanMessage
from langgraph.graph.message import add_messages
from langgraph.checkpoint.sqlite import SqliteSaver
from dotenv import load_dotenv
import os
import sqlite3

load_dotenv()

model=ChatGroq(model="openai/gpt-oss-120b")
api_key=os.getenv("GROQ_API_KEY")

class ChatbotState(TypedDict):
    messages:Annotated[list[BaseMessage],add_messages]

def chat_node(state:ChatbotState):
    messages=state['messages']
    response=model.invoke(messages)
    return {'messages':response}

conn=sqlite3.connect(database="chatbot.db",check_same_thread=False)
checkpointer=SqliteSaver(conn=conn)

graph=StateGraph(ChatbotState)
graph.add_node('chat_node',chat_node)

graph.add_edge(START,'chat_node')
graph.add_edge('chat_node',END)

chat=graph.compile(checkpointer=checkpointer)

def retrieve_all_threads():
    all_threads=set()
    for checkpoint in checkpointer.list(None):
        thread_id=checkpoint.config.get('configurable',{}).get('thread_id')
        if thread_id:
          all_threads.add(thread_id)
    return list(all_threads)    