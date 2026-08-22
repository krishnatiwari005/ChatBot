import uuid
import streamlit as st
from langgraph_backend import (chat,retrieve_all_threads,ingest_pdf,thread_document_metadata,)
from langchain_core.messages import (HumanMessage,AIMessage,ToolMessage,)
# ============================================================
# Utilities
# ============================================================
def generate_thread_id():
    return uuid.uuid4()

def reset_chat():
    thread_id = generate_thread_id()
    st.session_state["thread_id"] = thread_id
    add_thread(thread_id)
    st.session_state["message_history"] = []

def add_thread(thread_id):
    if thread_id not in st.session_state["chat_threads"]:
        st.session_state["chat_threads"].append(thread_id)

def load_conversation(thread_id):
    state = chat.get_state(
        config={"configurable": {"thread_id": thread_id}}
    )
    if not state or not state.values:
        return []
    return state.values.get("messages", [])
# ============================================================
# Session Initialization
# ============================================================
if "message_history" not in st.session_state:
    st.session_state["message_history"] = []

if "thread_id" not in st.session_state:
    st.session_state["thread_id"] = generate_thread_id()

if "chat_threads" not in st.session_state:
    st.session_state["chat_threads"] = retrieve_all_threads()

# Store uploaded PDFs separately for each thread
if "ingested_docs" not in st.session_state:
    st.session_state["ingested_docs"] = {}

# Make sure current thread exists
add_thread(st.session_state["thread_id"])

# Current thread ID as string
thread_key = str(st.session_state["thread_id"])

# Get documents belonging to current thread
thread_docs = st.session_state["ingested_docs"].setdefault(
    thread_key,
    {}
)
# ============================================================
# Sidebar
# ============================================================
st.sidebar.title("CHAT HISTORY")
# ------------------------------------------------------------
# New Chat
# ------------------------------------------------------------
if st.sidebar.button("➕ New Chat",use_container_width=True):
    reset_chat()
    st.rerun()
# ------------------------------------------------------------
# Current Thread
# ------------------------------------------------------------
st.sidebar.markdown(
    f"**Thread ID:** `{thread_key}`"
)
# ------------------------------------------------------------
# PDF Upload
# ------------------------------------------------------------
st.sidebar.subheader("📄 PDF Document")

if thread_docs:
    latest_doc = list(thread_docs.values())[-1]
    st.sidebar.success(
        f"Using `{latest_doc.get('filename')}`\n\n"
        f"Pages: {latest_doc.get('documents')}\n\n"
        f"Chunks: {latest_doc.get('chunks')}"
    )
else:
    st.sidebar.info(
        "No PDF indexed for this chat."
    )

uploaded_pdf = st.sidebar.file_uploader(
    "Upload PDF for this chat",
    type=["pdf"]
)

if uploaded_pdf:
    # Check whether this PDF was already processed
    if uploaded_pdf.name in thread_docs:
        st.sidebar.info(
            f"`{uploaded_pdf.name}` is already processed "
            "for this chat."
        )

    else:
        with st.sidebar.status("📚 Indexing PDF...",expanded=True) as status_box:
            try:
                summary = ingest_pdf(
                    uploaded_pdf.getvalue(),
                    thread_id=thread_key,
                    filename=uploaded_pdf.name,
                )
                # Save metadata in Streamlit session
                thread_docs[uploaded_pdf.name] = summary
                status_box.update(
                    label="✅ PDF indexed successfully",
                    state="complete",
                    expanded=False
                )
            except Exception as e:
                status_box.update(
                    label="❌ PDF indexing failed",
                    state="error",
                    expanded=True
                )
                st.sidebar.error(str(e))
# ------------------------------------------------------------
# Past Conversations
# ------------------------------------------------------------
st.sidebar.subheader("💬 Conversations")


threads = st.session_state["chat_threads"][::-1]
selected_thread = None
if not threads:
    st.sidebar.write(
        "No past conversations yet."
    )
else:
    for thread_id in threads:
        if st.sidebar.button(
            str(thread_id),
            key=f"thread-{thread_id}",
            use_container_width=True
        ):
            selected_thread = thread_id
# ============================================================
# Main UI
# ============================================================
st.title("Multi Utility Chatbot")
# ============================================================
# Display Current Chat
# ============================================================
for message in st.session_state["message_history"]:

    with st.chat_message(message["role"]):

        st.text(message["content"])

# ============================================================
# Chat Input
# ============================================================
user_input = st.chat_input(
    "Ask something..."
)

if user_input:
    # --------------------------------------------------------
    # Add user message
    # --------------------------------------------------------
    st.session_state["message_history"].append(
        {
            "role": "user",
            "content": user_input
        }
    )
    with st.chat_message("user"):

        st.text(user_input)
    # --------------------------------------------------------
    # LangGraph configuration
    # --------------------------------------------------------
    config = {
        "configurable": {"thread_id": thread_key},
        "metadata": {"thread_id": thread_key},
        "run_name": "chat_turn",
    }
    # --------------------------------------------------------
    # Assistant response
    # --------------------------------------------------------
    with st.chat_message("assistant"):

        status_holder = {
            "box": None
        }

        def ai_only_stream():
            for message_chunk, metadata in chat.stream(
                {"messages": [HumanMessage(content=user_input)]},
                config=config,
                stream_mode="messages"
            ):
                # --------------------------------------------
                # Tool execution
                # --------------------------------------------
                if isinstance(message_chunk,ToolMessage):
                    tool_name = getattr(message_chunk,"name","tool")
                    if status_holder["box"] is None:
                        status_holder["box"] = st.status(
                            f"🔧 Using `{tool_name}`...",
                            expanded=True
                        )
                    else:
                        status_holder["box"].update(
                            label=f"🔧 Using `{tool_name}`...",
                            state="running",
                            expanded=True
                        )
                # --------------------------------------------
                # AI response
                # --------------------------------------------
                if isinstance(message_chunk,AIMessage):
                    if message_chunk.content:
                        yield message_chunk.content
        # Stream response
        ai_message = st.write_stream(ai_only_stream())
        # --------------------------------------------
        # Finish tool status
        # --------------------------------------------
        if status_holder["box"] is not None:
            status_holder["box"].update(
                label="✅ Tool finished",
                state="complete",
                expanded=False
            )
    # --------------------------------------------------------
    # Save assistant message
    # --------------------------------------------------------
    st.session_state["message_history"].append(
        {
            "role": "assistant",
            "content": ai_message
        }
    )
    # --------------------------------------------------------
    # Show document metadata
    # --------------------------------------------------------
    doc_meta = thread_document_metadata(
        thread_key
    )
    if doc_meta:
        st.caption(
            f"📄 Document indexed: "
            f"{doc_meta.get('filename')} "
            f"(chunks: {doc_meta.get('chunks')}, "
            f"pages: {doc_meta.get('documents')})"
        )
# ============================================================
# Load Selected Conversation
# ============================================================
if selected_thread:
    st.session_state["thread_id"] = selected_thread
    messages = load_conversation(selected_thread)
    temp_messages = []
    for message in messages:
        if isinstance(message,HumanMessage):
            role = "user"
        else:
            role = "assistant"
        temp_messages.append({
                "role": role,
                "content": message.content
            }
        )
    st.session_state["message_history"] = (temp_messages)
    # Initialize document storage
    st.session_state["ingested_docs"].setdefault(str(selected_thread),{})
    st.rerun()