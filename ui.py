import streamlit as st


# ============================================================
# LOAD UI
# ============================================================

def load_css():

    st.markdown(
        """
        <style>

        /* ====================================================
           REMOVE STREAMLIT DEFAULT TOP HEADER
           ==================================================== */

        header[data-testid="stHeader"] {
            background: transparent !important;
            height: 0rem !important;
            visibility: hidden !important;
        }

        [data-testid="stHeader"] {
            background: transparent !important;
        }

        [data-testid="stDecoration"] {
            display: none !important;
        }

        [data-testid="stToolbar"] {
            display: none !important;
        }

        #MainMenu {
            display: none !important;
        }

        footer {
            display: none !important;
        }


        /* ====================================================
           GLOBAL APP
           ==================================================== */

        .stApp {

            background:
                radial-gradient(
                    circle at 15% 10%,
                    rgba(99, 102, 241, 0.10),
                    transparent 30%
                ),
                radial-gradient(
                    circle at 85% 90%,
                    rgba(139, 92, 246, 0.08),
                    transparent 30%
                ),
                #0b1020;

            color: #f8fafc;

            min-height: 100vh;
        }


        /* ====================================================
           MAIN CONTENT
           ==================================================== */

        .main .block-container {

            max-width: 1000px;

            padding-top: 2rem;
            padding-bottom: 7rem;

            padding-left: 2rem;
            padding-right: 2rem;
        }


        /* ====================================================
           MAIN HEADING
           ==================================================== */

        h1 {

            font-size: 2rem !important;

            font-weight: 700 !important;

            letter-spacing: -0.5px;

            color: #ffffff !important;

            margin-top: 0 !important;

            margin-bottom: 0.25rem !important;
        }


        /* ====================================================
           CAPTION
           ==================================================== */

        .stCaption {

            color: #94a3b8 !important;

            font-size: 0.85rem !important;
        }


        /* ====================================================
           SIDEBAR
           ==================================================== */

        section[data-testid="stSidebar"] {

            background: #0a0f1d;

            border-right:
                1px solid
                rgba(255, 255, 255, 0.07);
        }


        section[data-testid="stSidebar"] > div {

            padding:
                1.2rem 1rem;
        }


        section[data-testid="stSidebar"] h1 {

            font-size: 1.15rem !important;

            font-weight: 700 !important;

            color: #ffffff !important;
        }


        section[data-testid="stSidebar"] h2,
        section[data-testid="stSidebar"] h3 {

            font-size: 0.75rem !important;

            font-weight: 700 !important;

            text-transform: uppercase;

            letter-spacing: 0.08em;

            color: #818cf8 !important;

            margin-top: 1.4rem !important;
        }


        /* ====================================================
           SIDEBAR BUTTONS
           ==================================================== */

        section[data-testid="stSidebar"]
        .stButton > button {

            width: 100%;

            min-height: 42px;

            border-radius: 10px;

            border:
                1px solid
                rgba(255, 255, 255, 0.08);

            background:
                rgba(255, 255, 255, 0.04);

            color: #e2e8f0;

            font-size: 0.78rem;

            transition: all 0.2s ease;
        }


        section[data-testid="stSidebar"]
        .stButton > button:hover {

            background:
                rgba(99, 102, 241, 0.15);

            border-color:
                rgba(129, 140, 248, 0.4);

            color: #ffffff;

            transform: translateY(-1px);
        }


        /* ====================================================
           FILE UPLOADER
           ==================================================== */

        [data-testid="stFileUploader"] {

            background:
                rgba(255, 255, 255, 0.025);

            border:
                1px dashed
                rgba(129, 140, 248, 0.35);

            border-radius: 12px;

            padding: 0.5rem;
        }


        [data-testid="stFileUploaderDropzone"] {

            background:
                rgba(255, 255, 255, 0.015);

            border: none;
        }


        /* ====================================================
           SIDEBAR ALERTS
           ==================================================== */

        section[data-testid="stSidebar"]
        div[data-testid="stAlert"] {

            border-radius: 10px;

            font-size: 0.75rem;
        }


        /* ====================================================
           CHAT MESSAGES
           ==================================================== */

        div[data-testid="stChatMessage"] {

            border-radius: 15px;

            margin-bottom: 10px;

            padding:
                0.8rem 1rem;

            border:
                1px solid
                rgba(255, 255, 255, 0.06);

            background:
                rgba(255, 255, 255, 0.025);
        }


        /* ====================================================
           CHAT TEXT
           ==================================================== */

        div[data-testid="stChatMessage"]
        .stMarkdown {

            color: #e2e8f0;

            font-size: 0.92rem;

            line-height: 1.65;
        }


        /* ====================================================
           USER AVATAR
           ==================================================== */

        div[data-testid="stChatMessageAvatarUser"] {

            background: #6366f1;
        }


        /* ====================================================
           ASSISTANT AVATAR
           ==================================================== */

        div[data-testid="stChatMessageAvatarAssistant"] {

            background: #1e293b;
        }


        /* ====================================================
           CHAT INPUT
           ==================================================== */

        div[data-testid="stChatInput"] {

            background:
                rgba(10, 16, 31, 0.96);

            border:
                1px solid
                rgba(255, 255, 255, 0.10);

            border-radius: 15px;

            box-shadow:
                0 10px 35px
                rgba(0, 0, 0, 0.25);
        }


        div[data-testid="stChatInput"] textarea {

            color: #ffffff !important;

            font-size: 0.9rem !important;
        }


        div[data-testid="stChatInput"]
        textarea::placeholder {

            color: #64748b !important;
        }


        /* ====================================================
           TOOL STATUS
           ==================================================== */

        div[data-testid="stStatusWidget"] {

            border-radius: 12px;

            background:
                rgba(255, 255, 255, 0.035);

            border:
                1px solid
                rgba(255, 255, 255, 0.07);
        }


        /* ====================================================
           CODE BLOCKS
           ==================================================== */

        pre {

            border-radius: 10px !important;

            border:
                1px solid
                rgba(255, 255, 255, 0.08) !important;

            background:
                #080d18 !important;
        }


        /* ====================================================
           INLINE CODE
           ==================================================== */

        code {

            border-radius: 5px;

            background:
                rgba(99, 102, 241, 0.12);
        }


        /* ====================================================
           LINKS
           ==================================================== */

        a {

            color: #a5b4fc !important;
        }


        /* ====================================================
           DIVIDERS
           ==================================================== */

        hr {

            border-color:
                rgba(255, 255, 255, 0.06);
        }


        /* ====================================================
           SCROLLBAR
           ==================================================== */

        ::-webkit-scrollbar {

            width: 6px;

            height: 6px;
        }


        ::-webkit-scrollbar-track {

            background: transparent;
        }


        ::-webkit-scrollbar-thumb {

            background:
                rgba(255, 255, 255, 0.12);

            border-radius: 10px;
        }


        ::-webkit-scrollbar-thumb:hover {

            background:
                rgba(255, 255, 255, 0.22);
        }


        /* ====================================================
           MOBILE
           ==================================================== */

        @media (max-width: 768px) {

            .main .block-container {

                padding-left: 0.8rem;
                padding-right: 0.8rem;

                padding-top: 1.2rem;
            }


            h1 {

                font-size: 1.6rem !important;
            }


            div[data-testid="stChatMessage"] {

                padding:
                    0.65rem 0.8rem;
            }

        }

        </style>
        """,
        unsafe_allow_html=True
    )


# ============================================================
# HEADER
# ============================================================

def render_header():

    st.title("🤖 Multi Utility Chatbot")

    st.caption(
        "AI assistant for questions, web search, "
        "and document analysis"
    )


# ============================================================
# SIDEBAR SECTION
# ============================================================

def sidebar_section(title):

    st.sidebar.subheader(title)


# ============================================================
# THREAD ID
# ============================================================

def render_thread_id(thread_id):

    pass


# ============================================================
# DOCUMENT CARD
# ============================================================

def render_document_card(
    filename,
    pages,
    chunks
):

    pass