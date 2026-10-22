🎬 AI Video & Meeting Assistant with RAG
![Python](https://img.shields.io/badge/Python-3.12-blue?logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-App-FF4B4B?logo=streamlit&logoColor=white)
![LangChain](https://img.shields.io/badge/LangChain-LCEL-1C3C3C?logo=chainlink&logoColor=white)
![ChromaDB](https://img.shields.io/badge/ChromaDB-VectorStore-6E56CF)
![Groq API](https://img.shields.io/badge/Mistral%20AI-LLM-FF7000)
![License](https://img.shields.io/badge/License-MIT-green)
A completely free, local-first, and production-ready AI Video and Meeting Assistant built in Python. It automates the tedious post-meeting workflow: accepting video/audio files or YouTube URLs, transcribing them with local Whisper models or the Sarvam AI API, generating structured summaries via Groq API, extracting actionable insights (tasks, owners, deadlines), and indexing everything into ChromaDB for interactive, context-grounded Q&A chat.
🔗 Live Demo  |  💻 Source Code
---
📸 Demo
> _Add a screenshot or GIF of the Control Room UI here — e.g. `docs/demo.gif` — showing upload → transcription → summary → chat in action. This is the single highest-impact addition you can make to this README._
---
🚀 Features
Multi-Source Ingestion — process YouTube URLs directly or upload local files (`.mp3`, `.mp4`, `.wav`)
100% Free & Local Transcription — runs OpenAI's Whisper locally on a standard CPU (8GB+ RAM, no GPU needed)
High-Quality Hindi Transcription — Hindi-to-English translation via local Whisper or the Sarvam AI API (`saaras:v2.5`)
Automated Summarization & Title Generation — Groq API (`openai/gpt-oss-20b`) via LangChain LCEL pipelines
Actionable Insight Extraction — auto-identifies key decisions, open questions, and action items (with owners & deadlines)
RAG-Powered Q&A Chat — chunked transcripts, local embeddings (`all-MiniLM-L6-v2`), ChromaDB indexing, and grounded conversational retrieval
Export Capabilities — download meeting summaries and transcripts as TXT or PDF
Interactive Web UI — a custom "Control Room" dashboard built entirely with Streamlit
---
🏗️ Architecture
```
YouTube URL / File Upload
        │
        ▼
 ┌─────────────────┐
 │  Audio Extract   │  yt-dlp + ffmpeg → pydub (mono, 16kHz)
 └────────┬────────┘
          ▼
 ┌─────────────────┐
 │  Chunking        │  10-min segments (memory-safe local processing)
 └────────┬────────┘
          ▼
 ┌─────────────────┐
 │  Transcription   │  faster-whisper (local) or Sarvam AI (Hindi)
 └────────┬────────┘
          ▼
 ┌─────────────────┐         ┌──────────────────────┐
 │  Summarization   │────────▶  Action Items /       │
 │  (Groq LCEL)  │         │  Key Decisions /      │
 └────────┬────────┘         │  Open Questions       │
          ▼                  └──────────────────────┘
 ┌─────────────────┐
 │  Vector Store    │  HF embeddings → ChromaDB (persistent, local)
 └────────┬────────┘
          ▼
 ┌─────────────────┐
 │  RAG Chat        │  similarity search → grounded LLM response
 └─────────────────┘
```
Input Processing — audio is extracted from local files or downloaded from YouTube via `yt-dlp` & `ffmpeg`
Audio Standardization — `pydub` converts audio to mono-channel, 16kHz (Whisper's sweet spot)
Chunking — large files are sliced into 10-minute segments to avoid memory overload
Transcription — processed via Whisper (English/default) or Sarvam AI's Saaras model (Hindi)
Summarization & Extraction — Groq API generates a structured summary plus action items, decisions, and questions
Vector Search (RAG) — transcript is split into 500-character overlapping chunks, embedded, and persisted in a local ChromaDB instance (`vector_db/`)
Interactive Chat — similarity search retrieves relevant chunks, grounding responses to reduce hallucination
---
🛠️ Tech Stack
Layer	Technology
Language	Python 3.12
Orchestration	LangChain (LCEL, RunnablePassthrough, RunnableLambda)
Speech-to-Text	OpenAI Whisper / faster-whisper (local), Sarvam AI (`saaras:v2.5`)
LLM	Groq API (`openai/gpt-oss-20b` via ChatGroq)
Vector Database	ChromaDB
Embeddings	HuggingFace `sentence-transformers/all-MiniLM-L6-v2` (local)
Media Utilities	`yt-dlp`, `ffmpeg`, `pydub`
PDF Export	`fpdf2`
UI	Streamlit
Deployment	Streamlit Community Cloud
---
📁 Project Structure
```
.
├── core/
│   ├── transcriber.py     # Local Whisper & Sarvam AI transcription logic
│   ├── summarize.py       # Groq API-driven summarization & title generation
│   ├── extractor.py       # Action items, key decisions, and questions extractor
│   ├── vector_store.py    # HuggingFace embeddings and ChromaDB storage
│   └── rag_engine.py      # LangChain RAG pipeline and Q&A chat engine
├── utils/
│   └── audio_processor.py # YouTube downloading, audio conversion & chunking
├── app.py                 # Streamlit web UI
├── main.py                # CLI pipeline orchestrator
├── requirements.txt        # Python dependencies
├── packages.txt             # System-level dependencies (ffmpeg) for cloud deployment
└── .env                    # Environment API keys (not committed)
```
---
⚙️ Installation & Setup
1. Clone the Repository
```bash
git clone https://github.com/Chetansk134/AI-video-assistant.git
cd AI-video-assistant
```
2. Set Up a Virtual Environment
```bash
uv venv venv_video_agent

# macOS/Linux
source venv_video_agent/bin/activate
# Windows
venv_video_agent\Scripts\activate
```
3. Install Dependencies
```bash
uv pip install -r requirements.txt
```
> Requires `ffmpeg` installed locally for audio processing.
4. Configure Environment Variables
Create a `.env` file in the root directory:
```env
GROQ_API_KEY="your_groq_api_key"
SARVAM_API_KEY="your_sarvam_api_key"   # optional, only for Hindi transcription
SARVAM_STT_MODEL="saaras:v3"
WHISPER_MODEL="base"                    # tiny, base, small, medium, large
```
---
💻 Usage
Streamlit Web App
```bash
streamlit run app.py
```
Command Line Pipeline
```bash
python main.py
```
Enter a YouTube URL or local file path, select the language, and chat with the meeting directly in the terminal.
---
⚠️ Known Limitation: YouTube URLs on Cloud Deployment
The live deployed demo cannot download YouTube videos directly. This is a deliberate, documented tradeoff — not an application bug:
> YouTube's anti-bot system flags requests from cloud/datacenter IP ranges (AWS, GCP, Streamlit Cloud, etc.) and requires proof-of-origin authentication that client-spoofing alone cannot bypass. This affects any app hosted on cloud infrastructure that tries to fetch YouTube content programmatically — it's an IP-reputation restriction, not a code defect.
Workarounds considered and why they were skipped:
Cookie-based auth — requires uploading a real, logged-in session's cookies to a public app; a security risk and a Terms-of-Service gray area for public deployments
Third-party PO-token providers — adds a second service and non-trivial infrastructure for a demo-scoped project
Practical resolution: the app fully supports direct file upload (`.mp3`, `.mp4`, `.wav`) as its primary path in the deployed version, and this is the recommended way to try the live demo. YouTube URL support works normally when running the app locally, since home/residential IPs aren't subject to this restriction.
---
🗺️ Roadmap
[ ] Streaming chat responses (token-by-token)
[ ] Speaker diarization (who said what)
[ ] Multi-video comparison and cross-video RAG chat
[ ] Source-grounding indicators in chat answers
---
📄 License
MIT
