from dotenv import load_dotenv
from core import summarize
from utils.audio_processor import process_input
from core.transcriber import transcribe_all
from core.summarize import summarize, generate_title
from core.extractor import extract_actionable_items, extract_key_decisions, extract_questions
from core.rag_engine import build_rag_chain, ask_question

load_dotenv()  
def run_pipeline(source: str, language: str = "english") -> dict:
    print("Starting Ai video Assistant ...")
    chunks = process_input(source)
    
    transcript = transcribe_all(chunks, language=language)
    print(f"raw transcription (first 300 characters) {transcript[:300]}")
    title = generate_title(transcript)

    summary = summarize(transcript)
    action_items = extract_actionable_items(transcript)

    decisions = extract_key_decisions(transcript)
    questions = extract_questions(transcript)

    # Build the RAG chain
    rag_chain = build_rag_chain(transcript)

    return {
        "title": title,
        "transcript": transcript,
        "summary": summary,
        "action_items": action_items,
        "key_decisions": decisions,
        "open_questions": questions,
        "rag_chain": rag_chain
    }