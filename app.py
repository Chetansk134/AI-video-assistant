import os
import tempfile
import streamlit as st
from dotenv import load_dotenv

load_dotenv()

from utils.audio_processor import process_input
from core.transcriber import transcribe_all
from core.summarize import summarize, generate_title
from core.extractor import extract_actionable_items, extract_key_decisions, extract_questions
from core.rag_engine import build_rag_chain, ask_question



# ============================================================
# Page config
# ============================================================
st.set_page_config(
    page_title="AI Video Assistant",
    page_icon="\U0001F39B\uFE0F",
    layout="wide",
)

# ============================================================
# Design system -- "Control Room" identity
# Void #12151A / Panel #1B1F26 / Raised #232830
# Signal-red #FF4438 / Tape-amber #F2A93B
# Ink-bright #ECE9E2 / Ink-muted #8B93A1
# ============================================================
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Big+Shoulders+Display:wght@600;700;800&family=Inter:wght@400;500;600&family=JetBrains+Mono:wght@400;500;600&display=swap');

    :root {
        --void: #12151A;
        --panel: #1B1F26;
        --raised: #232830;
        --signal: #FF4438;
        --amber: #F2A93B;
        --ink: #ECE9E2;
        --ink-muted: #8B93A1;
        --line: #2E343D;
    }

    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }

    .stApp {
        background-color: var(--void);
        color: var(--ink);
    }

    section[data-testid="stSidebar"] {
        background-color: var(--panel);
        border-right: 1px solid var(--line);
    }
    section[data-testid="stSidebar"] .stMarkdown,
    section[data-testid="stSidebar"] label {
        color: var(--ink) !important;
    }

    .console-label {
        font-family: 'JetBrains Mono', monospace;
        font-size: 11px;
        letter-spacing: 0.14em;
        text-transform: uppercase;
        color: var(--ink-muted);
        margin-bottom: 4px;
        margin-top: 18px;
    }

    .hero {
        background: linear-gradient(180deg, var(--panel) 0%, var(--void) 100%);
        border: 1px solid var(--line);
        border-radius: 14px;
        padding: 28px 32px;
        margin-bottom: 28px;
        display: flex;
        align-items: center;
        justify-content: space-between;
    }
    .hero-title {
        font-family: 'Big Shoulders Display', sans-serif;
        font-weight: 800;
        font-size: 44px;
        letter-spacing: 0.03em;
        text-transform: uppercase;
        line-height: 1;
        color: var(--ink);
        margin: 0;
    }
    .hero-title span {
        color: var(--signal);
    }
    .hero-sub {
        font-family: 'JetBrains Mono', monospace;
        font-size: 12.5px;
        color: var(--ink-muted);
        letter-spacing: 0.04em;
        margin-top: 8px;
    }
    .rec-tag {
        font-family: 'JetBrains Mono', monospace;
        font-size: 11px;
        letter-spacing: 0.12em;
        color: var(--ink-muted);
        display: flex;
        align-items: center;
        gap: 6px;
        margin-bottom: 10px;
    }
    .rec-dot {
        width: 8px;
        height: 8px;
        border-radius: 50%;
        background: var(--signal);
        display: inline-block;
        animation: blink 1.4s ease-in-out infinite;
    }
    @keyframes blink {
        0%, 100% { opacity: 1; }
        50% { opacity: 0.25; }
    }

    .waveform {
        display: flex;
        align-items: flex-end;
        gap: 3px;
        height: 40px;
    }
    .waveform span {
        width: 4px;
        background: var(--amber);
        border-radius: 2px;
        animation: meter 1.2s ease-in-out infinite;
    }
    .waveform span:nth-child(1) { height: 30%; animation-delay: 0.0s; }
    .waveform span:nth-child(2) { height: 65%; animation-delay: 0.1s; }
    .waveform span:nth-child(3) { height: 100%; animation-delay: 0.2s; background: var(--signal); }
    .waveform span:nth-child(4) { height: 45%; animation-delay: 0.3s; }
    .waveform span:nth-child(5) { height: 80%; animation-delay: 0.4s; }
    .waveform span:nth-child(6) { height: 35%; animation-delay: 0.5s; }
    .waveform span:nth-child(7) { height: 60%; animation-delay: 0.6s; }
    @keyframes meter {
        0%, 100% { transform: scaleY(0.4); opacity: 0.6; }
        50% { transform: scaleY(1); opacity: 1; }
    }

    .stButton > button {
        background-color: var(--signal) !important;
        color: var(--void) !important;
        font-family: 'JetBrains Mono', monospace;
        font-weight: 600;
        letter-spacing: 0.05em;
        text-transform: uppercase;
        font-size: 12.5px;
        border: none;
        border-radius: 8px;
        padding: 10px 16px;
        transition: filter 0.15s ease;
    }
    .stButton > button:hover {
        filter: brightness(1.12);
    }

    .stTabs [data-baseweb="tab-list"] {
        gap: 4px;
        border-bottom: 1px solid var(--line);
    }
    .stTabs [data-baseweb="tab"] {
        font-family: 'JetBrains Mono', monospace;
        font-size: 12.5px;
        letter-spacing: 0.03em;
        color: var(--ink-muted);
        background-color: transparent;
        border-radius: 6px 6px 0 0;
        padding: 10px 14px;
    }
    .stTabs [aria-selected="true"] {
        color: var(--ink) !important;
        border-bottom: 2px solid var(--signal) !important;
    }

    div[data-testid="stStatusWidget"],
    .stAlert {
        background-color: var(--panel) !important;
        border: 1px solid var(--line) !important;
        border-radius: 10px !important;
    }

    h2, h3 {
        font-family: 'Big Shoulders Display', sans-serif;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.02em;
        color: var(--ink);
    }

    .stTextArea textarea {
        font-family: 'JetBrains Mono', monospace !important;
        background-color: var(--raised) !important;
        color: var(--ink) !important;
        border: 1px solid var(--line) !important;
    }

    div[data-testid="stChatMessage"] {
        background-color: var(--panel);
        border: 1px solid var(--line);
        border-radius: 10px;
    }

    hr {
        border-color: var(--line) !important;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# ============================================================
# Session state initialization
# ============================================================
if "results" not in st.session_state:
    st.session_state.results = None
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []


def waveform_html():
    return '<div class="waveform">' + "".join(["<span></span>"] * 7) + "</div>"


# ============================================================
# Hero header -- signature element
# ============================================================
st.markdown(
    f"""
    <div class="hero">
        <div>
            <div class="rec-tag"><span class="rec-dot"></span> ON AIR -- READY</div>
            <div class="hero-title">AI VIDEO<span>.</span>ASSISTANT</div>
            <div class="hero-sub">TRANSCRIBE // SUMMARIZE // ASK ANYTHING</div>
        </div>
        {waveform_html()}
    </div>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# Core pipeline runner
# ============================================================
def run_pipeline(source: str, language: str = "english") -> dict:
    status = st.status("REC -- Starting AI Video Assistant...", expanded=True)

    status.update(label="REC -- Processing audio input...")
    chunks = process_input(source)

    status.update(label="REC -- Transcribing audio (this can take a few minutes)...")
    transcript = transcribe_all(chunks, language=language)

    status.update(label="REC -- Generating title...")
    title = generate_title(transcript)

    status.update(label="REC -- Summarizing meeting...")
    summary = summarize(transcript)

    status.update(label="REC -- Extracting action items...")
    action_items = extract_actionable_items(transcript)

    status.update(label="REC -- Extracting key decisions...")
    decisions = extract_key_decisions(transcript)

    status.update(label="REC -- Extracting open questions...")
    questions = extract_questions(transcript)

    status.update(label="REC -- Building RAG chain for chat...")
    rag_chain = build_rag_chain(transcript)

    status.update(label="STOP -- Processing complete", state="complete", expanded=False)

    return {
        "title": title,
        "transcript": transcript,
        "summary": summary,
        "action_items": action_items,
        "key_decisions": decisions,
        "open_questions": questions,
        "rag_chain": rag_chain,
    }


# ============================================================
# Sidebar -- input controls
# ============================================================
with st.sidebar:
    st.markdown('<div class="console-label">Input source</div>', unsafe_allow_html=True)
    input_mode = st.radio("Input source", ["YouTube URL", "Upload audio/video file"], label_visibility="collapsed")

    source = None
    temp_file_path = None

    if input_mode == "YouTube URL":
        source = st.text_input("YouTube URL", placeholder="https://www.youtube.com/watch?v=...", label_visibility="collapsed")
    else:
        uploaded_file = st.file_uploader(
            "Upload audio or video file",
            type=["mp3", "wav", "m4a", "mp4", "mov", "webm"],
            label_visibility="collapsed",
        )
        if uploaded_file is not None:
            suffix = os.path.splitext(uploaded_file.name)[1]
            with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
                tmp.write(uploaded_file.read())
                temp_file_path = tmp.name
            source = temp_file_path

    st.markdown('<div class="console-label">Language</div>', unsafe_allow_html=True)
    language = st.selectbox("Language", ["english", "hinglish"], index=0, label_visibility="collapsed")

    st.markdown("<br>", unsafe_allow_html=True)
    run_clicked = st.button("Run Assistant", type="primary", use_container_width=True)

    st.divider()
    st.markdown(
        '<div style="font-family:JetBrains Mono; font-size:10.5px; color:#8B93A1; letter-spacing:0.05em;">'
        "LANGCHAIN . WHISPER . CHROMADB . STREAMLIT</div>",
        unsafe_allow_html=True,
    )


# ============================================================
# Run pipeline on button click
# ============================================================
if run_clicked:
    if not source:
        st.sidebar.error("Please provide a YouTube URL or upload a file first.")
    else:
        try:
            st.session_state.results = run_pipeline(source, language=language)
            st.session_state.chat_history = []
            st.success("Processing complete -- see results below.")
        except Exception as e:
            st.error(f"Something went wrong: {e}")


# ============================================================
# Main area -- results
# ============================================================
results = st.session_state.results

if results is None:
    st.markdown(
        '<div style="font-family:JetBrains Mono; color:#8B93A1; font-size:13px;">'
        "Add a YouTube URL or upload a file in the sidebar, then hit RUN ASSISTANT to get started."
        "</div>",
        unsafe_allow_html=True,
    )
else:
    st.markdown(f"## {results['title']}")

    tabs = st.tabs([
        "SUMMARY",
        "ACTION ITEMS",
        "KEY DECISIONS",
        "OPEN QUESTIONS",
        "TRANSCRIPT",
        "CHAT",
        "EXPORT",
    ])

    with tabs[0]:
        st.write(results["summary"])

    with tabs[1]:
        st.write(results["action_items"])

    with tabs[2]:
        st.write(results["key_decisions"])

    with tabs[3]:
        st.write(results["open_questions"])

    with tabs[4]:
        st.text_area("Transcript", results["transcript"], height=400, label_visibility="collapsed")

    with tabs[5]:
        for msg in st.session_state.chat_history:
            with st.chat_message(msg["role"]):
                st.write(msg["content"])

        user_question = st.chat_input("Ask a question about the meeting...")
        if user_question:
            st.session_state.chat_history.append({"role": "user", "content": user_question})
            with st.chat_message("user"):
                st.write(user_question)

            with st.chat_message("assistant"):
                with st.spinner("thinking..."):
                    answer = ask_question(results["rag_chain"], user_question)
                    st.write(answer)
            st.session_state.chat_history.append({"role": "assistant", "content": answer})

    with tabs[6]:
        export_text = (
            f"# {results['title']}\n\n"
            f"## Summary\n{results['summary']}\n\n"
            f"## Action Items\n{results['action_items']}\n\n"
            f"## Key Decisions\n{results['key_decisions']}\n\n"
            f"## Open Questions\n{results['open_questions']}\n\n"
            f"## Full Transcript\n{results['transcript']}\n"
        )

        col1, col2 = st.columns(2)

        with col1:
            st.download_button(
                label="Download TXT",
                data=export_text,
                file_name=f"{results['title']}.txt",
                mime="text/plain",
                use_container_width=True,
            )

        with col2:
            try:
                from fpdf import FPDF

                def sanitize_for_pdf(text):
                    replacements = {
                        "\u2018": "'", "\u2019": "'",
                        "\u201c": '"', "\u201d": '"',
                        "\u2013": "-", "\u2014": "-",
                        "\u2022": "-",
                        "\u2026": "...",
                    }
                    for orig, repl in replacements.items():
                        text = text.replace(orig, repl)
                    return text.encode("latin-1", "replace").decode("latin-1")

                export_text_clean = sanitize_for_pdf(export_text)

                pdf = FPDF()
                pdf.add_page()
                pdf.set_font("Helvetica", size=12)
                for line in export_text_clean.split("\n"):
                    if line.strip():
                        pdf.multi_cell(0, 8, line)
                    else:
                        pdf.ln(4)
                pdf_bytes = bytes(pdf.output(dest="S"))
                st.download_button(
                    label="Download PDF",
                    data=pdf_bytes,
                    file_name=f"{results['title']}.pdf",
                    mime="application/pdf",
                    use_container_width=True,
                )
            except Exception as e:
                st.warning(f"PDF export unavailable: {e}")

if temp_file_path and run_clicked:
    try:
        os.remove(temp_file_path)
    except Exception:
        pass
