import json
import uuid
import streamlit as st
import requests
import os
from ui import (
    load_css,
    sidebar_section,
)
API_URL = os.getenv(
    "API_URL",
    "http://127.0.0.1:8000"
)

load_css()
# ============================================================
# Utilities
# ============================================================
def generate_thread_id():
    response = requests.post(f"{API_URL}/threads")
    response.raise_for_status()
    return response.json()["thread_id"]

def reset_chat():
    thread_id = generate_thread_id()
    st.session_state["thread_id"] = thread_id
    add_thread(thread_id)
    st.session_state["message_history"] = []

def add_thread(thread_id):
    if thread_id not in st.session_state["chat_threads"]:
        st.session_state["chat_threads"].append(thread_id)

def load_conversation(thread_id):
    response = requests.get(f"{API_URL}/threads/{thread_id}")
    response.raise_for_status()
    return response.json()["messages"]

# ============================================================
# Session Initialization
# ============================================================
if "message_history" not in st.session_state:
    st.session_state["message_history"] = []

if "thread_id" not in st.session_state:
    st.session_state["thread_id"] = generate_thread_id()

if "chat_threads" not in st.session_state:
    response = requests.get(f"{API_URL}/threads")
    response.raise_for_status()
    st.session_state["chat_threads"] = (response.json()["threads"])

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
st.sidebar.text("🔦CHAT HISTORY")
# ------------------------------------------------------------
# New Chat
# ------------------------------------------------------------
if st.sidebar.button("➕ New Chat",use_container_width=True):
    reset_chat()
    st.rerun()
# ------------------------------------------------------------
# Current Thread
# ------------------------------------------------------------

# ------------------------------------------------------------
# PDF Upload
# ------------------------------------------------------------
sidebar_section("📄 PDF Document")

if thread_docs:
    latest_doc = list(thread_docs.values())[-1]
    
else:
    st.sidebar.info(
        "No PDF indexed for this chat."
    )

uploaded_pdf = st.sidebar.file_uploader(
    "Upload PDF for this chat",
    type=["pdf"]
)

if uploaded_pdf:

    if uploaded_pdf.name in thread_docs:
        st.sidebar.info(
            f"`{uploaded_pdf.name}` is already processed "
            "for this chat.")
    else:
        with st.sidebar.status("📚 Indexing PDF...",expanded=True) as status_box:
            try:
                response = requests.post(f"{API_URL}/documents/upload",
                    params={"thread_id": thread_key},
                    files={
                        "file": (
                            uploaded_pdf.name,
                            uploaded_pdf.getvalue(),
                            "application/pdf"
                        )
                    },
                    timeout=300
                )
                response.raise_for_status()
                data = response.json()
                summary = data["summary"]
                thread_docs[uploaded_pdf.name] = summary
                status_box.update(
                    label="✅ PDF indexed successfully",
                    state="complete",
                    expanded=False
                )
            except Exception as e:

                status_box.update(label="❌ PDF indexing failed",state="error",expanded=True)

                st.sidebar.error(str(e))
# ------------------------------------------------------------
# Past Conversations
# ------------------------------------------------------------


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
st.markdown(
    "<h1 style='font-weight: 1000;'>🤖 Multi Utility Chatbot</h1>",
    unsafe_allow_html=True
)

st.caption(
    "Ask questions, search the web, or analyze your documents."
)
# ============================================================
# Display Current Chat
# ============================================================
for message in st.session_state["message_history"]:

    with st.chat_message(message["role"]):

        st.markdown(message["content"])

# ============================================================
# Chat Input
# ============================================================
user_input = st.chat_input(
    "Ask something..."
)

if user_input:

    # ========================================================
    # Add user message to Streamlit UI
    # ========================================================

    st.session_state["message_history"].append(
        {
            "role": "user",
            "content": user_input
        }
    )

    with st.chat_message("user"):
        st.markdown(user_input)

    # ========================================================
    # Assistant response
    # ========================================================

    with st.chat_message("assistant"):

        status_holder = {
            "box": None
        }

        def api_stream():

            try:

                # ------------------------------------------------
                # Send message to FastAPI
                # ------------------------------------------------

                response = requests.post(
                    f"{API_URL}/chat",
                    json={
                        "thread_id": thread_key,
                        "message": user_input
                    },
                    stream=True,
                    timeout=300
                )

                # Raise error if FastAPI returned 4xx/5xx
                response.raise_for_status()

                # ------------------------------------------------
                # Receive streaming response
                # ------------------------------------------------

                for line in response.iter_lines(
                    decode_unicode=True
                ):

                    if not line:
                        continue

                    try:

                        data = json.loads(line)

                    except json.JSONDecodeError:

                        continue

                    # ============================================
                    # Tool is being used
                    # ============================================

                    if data.get("type") == "tool":

                        tool_name = data.get(
                            "name",
                            "tool"
                        )

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

                    # ============================================
                    # AI response chunk
                    # ============================================

                    elif data.get("type") == "content":

                        content = data.get(
                            "content",
                            ""
                        )

                        if content:

                            yield content

                    # ============================================
                    # Error from FastAPI
                    # ============================================

                    elif data.get("type") == "error":

                        error_message = data.get(
                            "error",
                            "Unknown backend error"
                        )

                        raise Exception(
                            error_message
                        )

                    # ============================================
                    # Stream finished
                    # ============================================

                    elif data.get("type") == "done":

                        break

            except requests.exceptions.Timeout:

                raise Exception(
                    "The backend took too long to respond."
                )

            except requests.exceptions.ConnectionError:

                raise Exception(
                    "Could not connect to the FastAPI backend."
                )

            except requests.exceptions.HTTPError as e:

                try:

                    error_data = response.json()

                    error_message = error_data.get(
                        "detail",
                        str(e)
                    )

                except Exception:

                    error_message = str(e)

                raise Exception(
                    f"Backend error: {error_message}"
                )

        # ========================================================
        # Display streaming response
        # ========================================================

        try:

            ai_message = st.write_stream(
                api_stream()
            )

        except Exception as e:

            ai_message = ""

            st.error(
                f"❌ {str(e)}"
            )

        # ========================================================
        # Finish tool status
        # ========================================================

        if status_holder["box"] is not None:

            status_holder["box"].update(
                label="✅ Tool finished",
                state="complete",
                expanded=False
            )

    # ========================================================
    # Save assistant response
    # ========================================================

    if ai_message:

        st.session_state["message_history"].append(
            {
                "role": "assistant",
                "content": ai_message
            }
        )

    # ========================================================
    # Get document metadata from FastAPI
    # ========================================================

    try:

        response = requests.get(
            f"{API_URL}/threads/{thread_key}/documents",
            timeout=30
        )

        response.raise_for_status()

        data = response.json()

        doc_meta = data.get(
            "document",
            {}
        )

    except Exception:

        doc_meta = {}

    # ========================================================
    # Display document information
    # ========================================================

    if doc_meta:

        filename = doc_meta.get(
            "filename",
            "Unknown"
        )

        chunks = doc_meta.get(
            "chunks",
            0
        )

        pages = doc_meta.get(
            "documents",
            0
        )

        st.caption(
            f"📄 Document indexed: "
            f"{filename} "
            f"(chunks: {chunks}, "
            f"pages: {pages})"
        )
# ============================================================
# Load Selected Conversation
# ============================================================

if selected_thread:

    # Set selected thread as current thread
    st.session_state["thread_id"] = str(selected_thread)

    # Convert thread ID to string
    thread_key = str(selected_thread)

    # --------------------------------------------------------
    # Load conversation from FastAPI
    # --------------------------------------------------------

    try:

        messages = load_conversation(thread_key)

        st.session_state["message_history"] = messages

    except Exception as e:

        st.error(
            f"❌ Could not load conversation: {e}"
        )

    # --------------------------------------------------------
    # Initialize document storage for this thread
    # --------------------------------------------------------

    st.session_state["ingested_docs"].setdefault(
        thread_key,
        {}
    )

    # --------------------------------------------------------
    # Refresh the Streamlit UI
    # --------------------------------------------------------

    st.rerun()