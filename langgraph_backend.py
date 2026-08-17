from langgraph.graph import StateGraph,START,END
from langchain_groq import ChatGroq
from typing import TypedDict,Annotated
from langchain_core.messages import BaseMessage,HumanMessage
from langgraph.graph.message import add_messages
from langgraph.checkpoint.memory import InMemorySaver
from dotenv import load_dotenv
import os

load_dotenv()

model=ChatGroq(model="openai/gpt-oss-120b")
api_key=os.getenv("GROQ_API_KEY")

class ChatbotState(TypedDict):
    messages:Annotated[list[BaseMessage],add_messages]

def chat_node(state:ChatbotState):
    messages=state['messages']
    response=model.invoke(messages)
    return {'messages':response}

checkpointer=InMemorySaver()

graph=StateGraph(ChatbotState)
graph.add_node('chat_node',chat_node)

graph.add_edge(START,'chat_node')
graph.add_edge('chat_node',END)

chat=graph.compile(checkpointer=checkpointer)