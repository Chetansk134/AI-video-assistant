import os
import glob
import yt_dlp

from pathlib import Path
from pydub import AudioSegment
from yt_dlp.utils import DownloadError


DOWNLOAD_DIR = "downloads"
os.makedirs(DOWNLOAD_DIR, exist_ok=True)


def download_youtube_audio(url: str) -> str:
    """
    Download audio from a YouTube URL and convert it to WAV.

    Returns:
        Path to the generated WAV file.

    Raises:
        RuntimeError: If downloading or conversion fails.
    """

    output_template = os.path.join(
        DOWNLOAD_DIR,
        "%(id)s.%(ext)s"
    )

    ydl_opts = {
        "format": "bestaudio/best",
        "outtmpl": output_template,
        "noplaylist": True,
        "postprocessors": [
            {
                "key": "FFmpegExtractAudio",
                "preferredcodec": "wav",
            }
        ],
        "quiet": True,
        "no_warnings": True,
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)

            video_id = info.get("id")

            if not video_id:
                raise RuntimeError(
                    "Could not identify the downloaded video."
                )

            wav_path = os.path.join(
                DOWNLOAD_DIR,
                f"{video_id}.wav"
            )

            if not os.path.isfile(wav_path):
                raise RuntimeError(
                    "The download finished, but the WAV file "
                    "was not found. Check FFmpeg and the "
                    "yt-dlp postprocessing logs."
                )

            return wav_path

    except DownloadError as exc:
        error_message = str(exc)

        if "403" in error_message or "Forbidden" in error_message:
            raise RuntimeError(
                "YouTube refused the audio download (HTTP 403). "
                "The video may require authentication, or "
                "YouTube may be blocking requests from the "
                "current hosting environment. Try uploading "
                "the audio/video file directly."
            ) from exc

        raise RuntimeError(
            f"Unable to download YouTube audio: {error_message}"
        ) from exc

    except Exception as exc:
        if isinstance(exc, RuntimeError):
            raise

        raise RuntimeError(
            f"Audio download or conversion failed: {exc}"
        ) from exc


def convert_to_wav(input_path: str) -> str:
    """
    Convert a local audio/video file to mono 16 kHz WAV.
    """

    if not os.path.isfile(input_path):
        raise FileNotFoundError(
            f"Input file does not exist: {input_path}"
        )

    output_path = (
        os.path.splitext(input_path)[0] + "_converted.wav"
    )

    try:
        audio = AudioSegment.from_file(input_path)

        audio = (
            audio
            .set_channels(1)
            .set_frame_rate(16000)
        )

        audio.export(output_path, format="wav")

        return output_path

    except Exception as exc:
        raise RuntimeError(
            f"Unable to convert the input file to WAV: {exc}"
        ) from exc


def chunk_audio(
    wav_path: str,
    chunk_minutes: int = 10
) -> list:
    """
    Split a WAV file into smaller WAV chunks.
    """

    if not os.path.isfile(wav_path):
        raise FileNotFoundError(
            f"Audio file does not exist: {wav_path}"
        )

    if chunk_minutes <= 0:
        raise ValueError(
            "chunk_minutes must be greater than zero."
        )

    audio = AudioSegment.from_wav(wav_path)

    chunk_ms = chunk_minutes * 60 * 1000
    chunks = []

    for i, start in enumerate(
        range(0, len(audio), chunk_ms)
    ):
        chunk = audio[start:start + chunk_ms]

        chunk_path = (
            f"{os.path.splitext(wav_path)[0]}_chunk_{i}.wav"
        )

        chunk.export(chunk_path, format="wav")
        chunks.append(chunk_path)

    return chunks


def process_input(source: str) -> list:
    """
    Process either a YouTube URL or a local audio/video file.
    """

    if not source:
        raise ValueError("Please provide a URL or input file.")

    if source.startswith(("http://", "https://")):
        print("Detected URL. Downloading audio...")

        wav_path = download_youtube_audio(source)

    else:
        print("Detected local file. Converting to WAV...")

        wav_path = convert_to_wav(source)

    print("Chunking audio...")

    chunks = chunk_audio(wav_path)

    print(
        f"Audio ready — {len(chunks)} chunk(s) created."
    )

    return chunks