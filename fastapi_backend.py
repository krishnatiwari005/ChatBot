import uuid
import json

from fastapi import (
    FastAPI,
    UploadFile,
    File,
    HTTPException,
)
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from pydantic import BaseModel

from langchain_core.messages import (
    HumanMessage,
    AIMessage,
    ToolMessage,
)

from langgraph_backend import (
    chat_graph,
    retrieve_all_threads,
    load_conversation,
    ingest_pdf,
    thread_document_metadata,
)


# ============================================================
# FastAPI App
# ============================================================

app = FastAPI(
    title="Multi Utility Chatbot API",
    version="1.0.0",
)


# ============================================================
# CORS
# ============================================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ============================================================
# Request Models
# ============================================================

class ChatRequest(BaseModel):
    thread_id: str
    message: str


# ============================================================
# Health
# ============================================================

@app.get("/")
def root():

    return {
        "status": "online",
        "message": "Multi Utility Chatbot API"
    }


@app.get("/health")
def health():

    return {
        "status": "ok"
    }


# ============================================================
# Create Thread
# ============================================================

@app.post("/threads")
def create_thread():

    thread_id = str(uuid.uuid4())

    return {
        "thread_id": thread_id
    }


# ============================================================
# Get All Threads
# ============================================================

@app.get("/threads")
def get_threads():

    try:

        threads = retrieve_all_threads()

        return {
            "threads": threads
        }

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


# ============================================================
# Get Conversation
# ============================================================

@app.get("/threads/{thread_id}")
def get_conversation(thread_id: str):

    try:

        messages = load_conversation(thread_id)

        result = []

        for message in messages:

            if isinstance(message, HumanMessage):

                role = "user"

            elif isinstance(message, AIMessage):

                role = "assistant"

            elif isinstance(message, ToolMessage):

                continue

            else:

                continue

            if isinstance(message.content, str):

                content = message.content

            else:

                content = str(message.content)

            result.append({
                "role": role,
                "content": content
            })

        return {
            "thread_id": thread_id,
            "messages": result
        }

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


# ============================================================
# Chat Streaming
# ============================================================

@app.post("/chat")
def chat_endpoint(request: ChatRequest):

    def generate():

        config = {
            "configurable": {
                "thread_id": str(request.thread_id)
            },
            "metadata": {
                "thread_id": str(request.thread_id)
            },
            "run_name": "chat_turn",
        }

        try:

            for message_chunk, metadata in chat_graph.stream(
                {
                    "messages": [
                        HumanMessage(
                            content=request.message
                        )
                    ]
                },
                config=config,
                stream_mode="messages",
            ):

                # --------------------------------------------
                # Tool message
                # --------------------------------------------

                if isinstance(
                    message_chunk,
                    ToolMessage
                ):

                    tool_name = getattr(
                        message_chunk,
                        "name",
                        "tool"
                    )

                    yield json.dumps({
                        "type": "tool",
                        "name": tool_name
                    }) + "\n"

                # --------------------------------------------
                # AI message
                # --------------------------------------------

                elif isinstance(
                    message_chunk,
                    AIMessage
                ):

                    if message_chunk.content:

                        yield json.dumps({
                            "type": "content",
                            "content": message_chunk.content
                        }) + "\n"

            # --------------------------------------------
            # Finished
            # --------------------------------------------

            yield json.dumps({
                "type": "done"
            }) + "\n"

        except Exception as e:

            yield json.dumps({
                "type": "error",
                "error": str(e)
            }) + "\n"

    return StreamingResponse(
        generate(),
        media_type="application/x-ndjson"
    )


# ============================================================
# PDF Upload
# ============================================================

@app.post("/documents/upload")
async def upload_pdf(
    thread_id: str,
    file: UploadFile = File(...)
):

    if not file.filename.lower().endswith(".pdf"):

        raise HTTPException(
            status_code=400,
            detail="Only PDF files are supported."
        )

    try:

        file_bytes = await file.read()

        summary = ingest_pdf(
            file_bytes=file_bytes,
            thread_id=str(thread_id),
            filename=file.filename,
        )

        return {
            "success": True,
            "thread_id": thread_id,
            "summary": summary,
        }

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


# ============================================================
# Document Metadata
# ============================================================

@app.get("/threads/{thread_id}/documents")
def get_documents(thread_id: str):

    try:

        metadata = thread_document_metadata(
            str(thread_id)
        )

        return {
            "thread_id": thread_id,
            "document": metadata
        }

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )