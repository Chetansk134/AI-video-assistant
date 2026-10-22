# 🎬 AI Video & Meeting Assistant

An AI-powered application that transforms audio and video content into structured, searchable information using speech transcription, large language models (LLMs), and retrieval-augmented generation (RAG).

<p align="center">
  <a href="https://ai-video-assistant-t4gdlfhn37sx44gd4kbcpt.streamlit.app/">
    <img src="https://static.streamlit.io/badges/streamlit_badge_black_white.svg" alt="Open Live Demo">
  </a>
</p>

<p align="center">
  <a href="https://ai-video-assistant-t4gdlfhn37sx44gd4kbcpt.streamlit.app/">
    🚀 <strong>Try the Live Demo</strong>
  </a>
  &nbsp; | &nbsp;
  <a href="https://github.com/Chetansk134/AI-video-assistant">
    💻 <strong>View Source Code</strong>
  </a>
</p>

<p align="center">
  <strong>Transcribe · Summarize · Extract Insights · Ask Questions</strong>
</p>

---

## 📌 Overview

The AI Video & Meeting Assistant automates the process of understanding long videos, lectures, interviews, presentations, and meetings.

Users can upload audio/video files or provide a YouTube URL to generate transcripts, summaries, action items, key decisions, and answers to questions about the content.

The application combines speech recognition, LLM-powered analysis, vector search, and conversational question answering in a single interface.

### 🎯 Project Objectives

* Automate audio and video transcription.
* Generate concise, structured summaries.
* Extract actionable tasks and important decisions.
* Identify unresolved questions and discussion points.
* Enable context-aware question answering.
* Reduce the time required to review long recordings.

---

## ✨ Features

### 🎥 1. Multiple Input Sources

* Upload local audio and video files.
* Provide a YouTube URL for audio retrieval when supported.
* Convert media files into WAV audio.
* Split long audio recordings into smaller chunks.

### 🎙️ 2. Speech-to-Text Transcription

* Transcribe audio using Whisper-based models.
* Support the configured Sarvam AI transcription integration.
* Process long recordings through audio chunking.
* Generate text that can be used by downstream AI components.

### 📝 3. AI-Powered Summarization

* Generate descriptive titles for processed content.
* Produce structured summaries.
* Highlight important topics and discussion points.
* Make lengthy recordings easier to understand.

### ✅ 4. Action Item Extraction

Extract actionable information from transcripts, including:

* Tasks and follow-up activities.
* Responsibilities mentioned in the discussion.
* Deadlines and time-related commitments, when stated.

### 📌 5. Key Decision Extraction

Identify important decisions, conclusions, and agreements discussed in the recording.

### ❓ 6. Open Question Detection

Identify unresolved questions and topics that may require further clarification.

### 💬 7. Conversational Question Answering

* Ask questions about the processed recording.
* Retrieve relevant transcript information.
* Generate context-aware answers using Groq and RAG.

### 🔎 8. Retrieval-Augmented Generation (RAG)

* Store transcript information in ChromaDB.
* Retrieve relevant context for user questions.
* Use retrieved information to support answer generation.

### 📄 9. Export

Export supported results, including transcript and summary information, using the available TXT and PDF export functionality.

---

## 🛠️ Technology Stack

| Component                 | Technology                     |
| ------------------------- | ------------------------------ |
| Programming Language      | Python                         |
| Frontend / User Interface | Streamlit                      |
| Speech Recognition        | Whisper / faster-whisper       |
| Alternative Transcription | Sarvam AI                      |
| Large Language Model API  | Groq API                       |
| LLM Integration           | LangChain                      |
| Vector Database           | ChromaDB                       |
| Audio Processing          | PyDub                          |
| YouTube Audio Retrieval   | yt-dlp                         |
| Audio Extraction          | FFmpeg                         |
| PDF Generation            | FPDF2 / configured PDF library |
| Deployment                | Streamlit Community Cloud      |
| Version Control           | Git and GitHub                 |

---

## 🏗️ System Architecture

```text
                 USER INPUT
                     |
          +----------+----------+
          |                     |
     YouTube URL          Audio/Video Upload
          |                     |
          v                     v
     yt-dlp Download       Media Processing
          |                     |
          +----------+----------+
                     |
                     v
             Audio Conversion
                     |
                     v
              Audio Chunking
                     |
                     v
                Transcription
              Whisper / Sarvam
                     |
                     v
                Full Transcript
                     |
          +----------+----------+
          |          |          |
          v          v          v
       Summary    Action Items  Decisions
          |          |          |
          +----------+----------+
                     |
                     v
             ChromaDB Vector Store
                     |
                     v
              Relevant Context
                 Retrieval
                     |
                     v
                  Groq API
                     |
                     v
             Question Answering
```

**Note:** The YouTube input path depends on whether the video can be accessed and downloaded. On Streamlit Community Cloud, uploading an audio/video file is the recommended alternative when direct YouTube downloading fails.

---

## 🔄 How It Works

1. **Input:** The user uploads an audio/video file or provides a YouTube URL.
2. **Audio Processing:** The application retrieves or extracts audio and converts it into a suitable format.
3. **Chunking:** Long recordings are divided into smaller audio segments.
4. **Transcription:** Whisper or the configured Sarvam AI integration converts speech into text.
5. **Summarization:** Groq generates a title and structured summary.
6. **Insight Extraction:** The application extracts action items, decisions, and open questions.
7. **Vector Storage:** Transcript information is indexed using ChromaDB.
8. **Question Answering:** Relevant context is retrieved and supplied to the language model.
9. **Results:** The user can review, query, and export the generated information.

---

## ⚠️ Known Limitation: YouTube Downloads

**Direct YouTube audio downloading may fail on Streamlit Community Cloud with HTTP 403: Forbidden.**

This project uses `yt-dlp` to retrieve audio from YouTube URLs. YouTube may reject automated download requests from cloud-hosting environments.

During testing, YouTube URL processing worked in the local development environment but returned HTTP 403 errors in the deployed Streamlit application.

### Local Environment

YouTube URL processing may work locally when:

* The video is accessible.
* The installed downloader is compatible.
* YouTube permits the download request.
* No additional authentication or access restrictions prevent retrieval.

### Streamlit Community Cloud

Direct YouTube downloads may fail because of hosting-environment restrictions, authentication requirements, or changes to YouTube's download mechanisms.

Updating `yt-dlp` can resolve some compatibility problems, but it does not guarantee that every video will download successfully.

### Recommended Workaround

When YouTube downloading fails:

1. Obtain an audio/video file that you are authorized to process.
2. Select **Upload audio/video file** in the application.
3. Upload the file.
4. Click **RUN ASSISTANT**.

The uploaded-file workflow allows users to continue using the transcription, summarization, action-item extraction, decision extraction, and question-answering features without relying on direct YouTube downloads.

**Important:** The live demo is available, but YouTube URL processing may be limited. Use file uploads when direct downloads fail.

---

## 📂 Project Structure

The following is an illustrative structure. The actual files in the repository may differ.

```text
AI-video-assistant/
│
├── app.py
├── requirements.txt
├── packages.txt
├── README.md
│
├── core/
│   ├── summarize.py
│   ├── extractor.py
│   ├── rag_engine.py
│   ├── transcriber.py
│   └── vector_store.py
│
├── utils/
│   └── audio_processor.py
│
├── downloads/
│
└── .streamlit/
    └── config.toml
```

### Important Files

| File                       | Purpose                                          |
| -------------------------- | ------------------------------------------------ |
| `app.py`                   | Main Streamlit application                       |
| `requirements.txt`         | Python dependencies                              |
| `packages.txt`             | System packages required for deployment          |
| `core/summarize.py`        | Title generation and summarization               |
| `core/extractor.py`        | Action items, decisions, and question extraction |
| `core/rag_engine.py`       | Retrieval-based question answering               |
| `core/transcriber.py`      | Audio transcription                              |
| `utils/audio_processor.py` | Audio downloading, conversion, and chunking      |

The exact filenames and responsibilities should be adjusted to match the current repository.

---

## ⚙️ Installation and Setup

### Prerequisites

Install the following:

* Python 3.11 or another Python version compatible with the project's dependencies.
* Git.
* FFmpeg.
* A Groq API key.
* A Sarvam AI API key if you use the Sarvam transcription integration.

### Step 1: Clone the Repository

```bash
git clone https://github.com/Chetansk134/AI-video-assistant.git
```

Navigate to the project directory:

```bash
cd AI-video-assistant
```

### Step 2: Create a Virtual Environment

On Windows:

```powershell
python -m venv .venv
```

Activate it:

```powershell
.venv\Scripts\Activate.ps1
```

If PowerShell blocks activation, use the appropriate activation command for your terminal or system policy.

### Step 3: Install Dependencies

Upgrade pip:

```bash
python -m pip install --upgrade pip
```

Install the project's dependencies:

```bash
python -m pip install -r requirements.txt
```

Ensure FFmpeg is installed and available on your system PATH.

If the project requires additional system dependencies, configure them as documented in `packages.txt`.

### Step 4: Configure API Keys

For local development, configure your API keys using environment variables or the secrets configuration supported by your application.

For Streamlit Community Cloud, open your application's settings and configure the required secrets.

Example Streamlit Secrets configuration:

```toml
GROQ_API_KEY = "your_groq_api_key"
SARVAM_API_KEY = "your_sarvam_api_key"
```

Add any other settings required by your implementation.

**Security precautions:**

* Never commit real API keys to GitHub.
* Do not publish `.env` files containing credentials.
* Keep API keys private.
* Configure secrets separately for local development and cloud deployment.

### Step 5: Run the Application

From the project root, run:

```bash
python -m streamlit run app.py
```

Open the local URL displayed in the terminal, usually:

```text
http://localhost:8501
```

---

## ☁️ Deployment on Streamlit Community Cloud

To deploy the project:

1. Push the source code to GitHub.
2. Open Streamlit Community Cloud.
3. Create an application connected to your GitHub repository.
4. Select the correct repository, branch, and entry-point file.
5. Configure the required API keys under **App settings → Secrets**.
6. Deploy the application.
7. Review the deployment logs.
8. Test file uploads, transcription, summarization, and question answering.

### Deployment Considerations

* Local and cloud environments may behave differently.
* Direct YouTube downloads may return HTTP 403.
* Uploaded files are the recommended alternative when YouTube downloads fail.
* Local environment variables do not automatically transfer to Streamlit Cloud.
* API keys must be configured separately in the deployed application's secrets.
* Ensure all required Python and system dependencies are available.

---

## 🧪 Testing Checklist

Use this checklist to verify the application.

* [ ] Application launches successfully.
* [ ] MP3 audio upload works.
* [ ] WAV audio upload works.
* [ ] Supported video uploads work.
* [ ] Audio conversion works.
* [ ] Transcription produces readable text.
* [ ] Title generation works.
* [ ] Summary generation works.
* [ ] Action items are extracted.
* [ ] Key decisions are identified.
* [ ] Open questions are extracted.
* [ ] Chat answers questions about the transcript.
* [ ] Supported TXT and PDF exports work.
* [ ] YouTube URL processing works locally for accessible videos.
* [ ] Cloud deployment handles YouTube download failures gracefully.
* [ ] API keys are stored securely.

---

## 🔐 Security and Privacy

* Store API keys using environment variables or Streamlit Secrets.
* Do not commit credentials to GitHub.
* Avoid publishing private authentication cookies or tokens.
* Remove temporary media files when they are no longer required.
* Process only content you have permission to access and use.
* Review the privacy policies of any external AI services used by the application.

---

## 🚀 Future Enhancements

* Add transcript retrieval as a fallback when captions are available and accessible.
* Improve error handling for YouTube download failures.
* Add caching to reduce repeated transcription and API usage.
* Improve processing of long recordings using hierarchical summarization.
* Add more language options.
* Improve progress indicators for long-running tasks.
* Implement automatic cleanup of temporary audio files.
* Add comprehensive logging and automated tests.
* Improve resilience to temporary API rate limits.
* Add support for more audio and video sources.

---

## 📄 License

This project is described as using the MIT License. Refer to the repository's `LICENSE` file for the authoritative license terms.

---

## 👨‍💻 Author

**Chetan Kalamadi**

AI Video & Meeting Assistant

A project demonstrating speech transcription, LLM-powered summarization, information extraction, vector search, and retrieval-augmented question answering.

### 🔗 Project Links

* **Live Demo:** https://ai-video-assistant-t4gdlfhn37sx44gd4kbcpt.streamlit.app/
* **GitHub Repository:** https://github.com/Chetansk134/AI-video-assistant

---

<p align="center">
  <strong>Built with Python, Streamlit, Whisper, Groq, LangChain, and ChromaDB.</strong>
</p>
