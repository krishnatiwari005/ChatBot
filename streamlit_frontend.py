import streamlit as st
from langgraph_backend import chat,retrieve_all_threads
from langchain_core.messages import HumanMessage,AIMessage,ToolMessage
import uuid

def generate_thread_id():
    thread_id=uuid.uuid4()
    return thread_id

def reset_chat():
    thread_id=generate_thread_id()
    st.session_state['thread_id']=thread_id
    add_thread(st.session_state['thread_id'])
    st.session_state['message_history']=[]

def add_thread(thread_id):
    if thread_id not in st.session_state['chat_threads']:
        st.session_state['chat_threads'].append(thread_id) 

def load_conversation(thread_id):
    state=chat.get_state(config={'configurable':{'thread_id':thread_id}})
    if not state or not state.values:
        return []
    return state.values.get('messages',[]) 

if 'message_history' not in st.session_state:
    st.session_state['message_history']=[]

if 'thread_id' not in st.session_state:
    st.session_state['thread_id']=generate_thread_id()

if 'chat_threads' not in st.session_state:
    st.session_state['chat_threads']=retrieve_all_threads()

add_thread(st.session_state['thread_id'])

# side bar UI

st.sidebar.title("CHAT HISTORY")

if st.sidebar.button("New Chat"):
    reset_chat()

st.sidebar.header("Conversations")
#----------------------------------

for thread_id in st.session_state['chat_threads'][::-1]:
    if st.sidebar.button(str(thread_id)):
        st.session_state['thread_id']=thread_id
        messages=load_conversation(thread_id)

        temp_messages=[]

        for message in messages:
            if isinstance(message,HumanMessage):
                role='user'
            else:
                role='assistant'
            temp_messages.append({'role':role,'content':message.content})
        st.session_state['message_history']=temp_messages

for message in st.session_state['message_history']:
    with st.chat_message(message['role']):
        st.text(message['content'])


user_input=st.chat_input('Type here')

if user_input:
    st.session_state['message_history'].append({'role':'user','content':user_input})
    with st.chat_message('user'):
        st.text(user_input)

    config={
            'configurable':{'thread_id':st.session_state['thread_id']},
            "metadata":{
                "thread_id":st.session_state['thread_id']
                },
            "run_name":"chat_turn",
            }    

    
    with st.chat_message('assistant'):
        status_holder={'box':None}
        def ai_only_stream():
            for message_chunk,metadata in chat.stream(
                 {'messages':[HumanMessage(content=user_input)]},
                    config=config,
                    stream_mode='messages'                
            ):
                if isinstance(message_chunk,ToolMessage):
                    tool_name=getattr(message_chunk,"name","tool")
                    if status_holder['box'] is None:
                        status_holder['box']=st.status(
                            f"using{tool_name}...",
                            expanded=True,
                        )
                    else:
                        status_holder['box'].update(
                            label=f"using{tool_name}...",
                            state='running',
                            expanded=True,                        
                        )
                if isinstance(message_chunk,AIMessage):        
                    yield message_chunk.content
        ai_message=st.write_stream(ai_only_stream())        

    st.session_state['message_history'].append({'role':'assistant','content':ai_message})