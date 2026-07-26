AI Video & Meeting Assistant with RAG
A completely free, local, and production-ready AI Video and Meeting Assistant built in Python. This tool automates the tedious post-meeting workflow: it accepts video/audio files or YouTube URLs, transcribes them using local Whisper models or the Sarvam AI API, generates structured summarisations via Mistral AI, extracts actionable insights (tasks, owners, deadlines), and indexes everything into Chroma DB to let you have interactive Q&A chats with your videos and meetings.

🚀 Features
Multi-Source Ingestion: Process YouTube URLs directly or upload local files including .mp3, .mp4, and .wav formats.
100% Free & Local Transcription: Run OpenAI's Whisper model locally on your standard CPU (8GB+ RAM required, no GPU needed) to transcribe audio without cloud costs.
High-Quality Hindi Transcription: Supports Hindi-to-English translation using local Whisper or the Sarvam AI API (utilising the saaras:v2.5 model) to handle multilingual conversations flawlessly.
Automated Summarisation & Title Generation: Leverages Mistral AI (mistral-small-latest) via LangChain LCEL pipelines to generate structured bullet-point summaries and short professional titles.
Actionable Insight Extraction: Automatically identifies and pulls key decisions, open questions, and action items (complete with task descriptions, responsible owners, and deadlines).
RAG-Powered Q&A Chat: Splits full transcripts into manageable chunks, generates local vector embeddings (Hugging Face all-MiniLM-L6-v2), indexes them in Chroma DB, and enables interactive, context-grounded chatting with your meetings.
Export Capabilities: Export meeting summaries, discussions, and action items directly to structured PDF reports.
Interactive Web UI: A beautiful, single-page dashboard built entirely with Streamlit.
📁 Project Structure
.
├── core/
│   ├── transcriber.py     # Local Whisper & Sarvam AI transcription logic
│   ├── summarize.py       # Mistral AI-driven meeting summarisation & title generation
│   ├── extractor.py       # Action items, key decisions, and questions extractor
│   ├── vector_store.py    # Hugging Face embeddings and Chroma DB vector storage
│   └── rag_engine.py      # LangChain RAG pipeline and Q&A chat engine
├── utils/
│   └── audio_processor.py # YouTube downloading (yt-dlp + ffmpeg), audio conversion & chunking
├── app.py                 # Streamlit web-based user interface
├── main.py                # Command-line pipeline orchestrator
├── requirements.txt       # Python dependencies
└── .env                   # Environment API keys
🛠️ Tech Stack & Libraries
Programming Language: Python 3.12
Orchestration: LangChain (LCEL pipelines, RunnablePassThrough, RunnableLambda)
Speech-to-Text: OpenAI Whisper (Local), Sarvam AI API (saaras:v2.5 model)
Large Language Model: Mistral AI (mistral-small-latest via ChatMistralAI)
Vector Database: Chroma DB
Embeddings: Hugging Face sentence-transformers (all-MiniLM-L6-v2 running locally)
Utilities: yt-dlp (for downloading YouTube videos), ffmpeg, pydub (for audio segmenting & mono/16kHz conversion)
PDF Export: fpdf2
UI Framework: Streamlit
⚙️ Installation & Setup
1. Clone the Repository
git clone https://github.com/your-username/ai-video-assistant-rag.git
cd ai-video-assistant-rag
2. Set Up a Virtual Environment
It is highly recommended to use a virtual environment to manage dependencies. We use uv as a super-fast package manager.

# Create the environment
uv venv venv_video_agent

# Activate the environment
# On macOS/Linux:
source venv_video_agent/bin/activate
# On Windows:
venv_video_agent\Scripts\activate
3. Install Dependencies
uv pip install -r requirements.txt
(Make sure you have ffmpeg installed on your local machine as it is required for audio processing).

4. Configure Environment Variables
Create a .env file in the root directory and add your API keys:

MISTRAL_API_KEY="your_free_mistral_api_key"
SARVAM_API_KEY="your_sarvam_api_key" # Optional, only needed for Hindi transcription
WISPER_MODEL="small" # Options: tiny, small, medium, large (controls speed vs accuracy)
💻 Usage
Streamlit Web App
To run the fully-featured interactive dashboard, execute:

streamlit run app.py
Command Line Pipeline
To run the orchestrator and test the pipeline directly in the terminal:

python main.py
You will be prompted to enter a YouTube URL or a local file path, select the language (English or Hindi), and then chat with the meeting via terminal.

🔬 Architecture Flow
Input Processing: Audio is extracted from local files or downloaded from YouTube using yt-dlp & ffmpeg.
Audio Standardisation: pydub converts the audio to mono-channel and downsamples it to 16kHz (the sweet spot for Whisper AI).
Chunking: Large audio files are sliced into 10-minute chunks to prevent memory overload during local Whisper processing.
Transcription: Chunks are processed sequentially through Whisper (English/Default) or Sarvam AI's Saaras model (for Hindi).
Summarisation & Extraction: Mistral AI generates a bullet-point summary and extracts action items, key decisions, and follow-up questions.
Vector Search (RAG): The transcript is split into 500-character segments with overlapping text, embedded using Hugging Face models, and persistent vectors are saved in a local Chroma DB instance (vector_db/).
Interactive Chat: Streamlit or terminal prompts use similarity searches to find relevant sections, appending the matching context to the prompt for accurate, hallucination-free QA.
