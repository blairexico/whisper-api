# main.py: Whisper Streaming Transcriber

from fastapi import FastAPI, WebSocket
from faster_whisper import WhisperModel
import tempfile
import os
import logging

logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)


app = FastAPI()

# Load Whisper model (adjust size as needed)
log.info("Loading Whisper model...")
model = WhisperModel("medium", compute_type="float16")
log.info("Model loaded.")

@app.websocket("/stream")
async def transcribe_stream(websocket: WebSocket):
    log.info("WebSocket connected.")
    await websocket.accept()
    audio_bytes = bytearray()

    try:
        while True:
            try:
                data = await websocket.receive_bytes()
                log.info(f"Received chunk: {len(data)} bytes")
                audio_bytes.extend(data)
            except Exception as inner_e:
                log.info(f"Receive ended or error: {inner_e}")
                break  # client closed or errored

        log.info(f"Total bytes received: {len(audio_bytes)}")

        if len(audio_bytes) < 1000:
            log.info("Too little data received, skipping transcription.")
            await websocket.send_text("[Error: Not enough audio data]")
            return

        # Write to temporary WAV file
        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmpfile:
            tmpfile.write(audio_bytes)
            tmpfile.flush()
            tmpfile_path = tmpfile.name

        log.info(f"Wrote audio to temp file: {tmpfile_path}")
        log.info("Starting transcription...")

        segments, _ = model.transcribe(tmpfile_path)
        text = " ".join([seg.text for seg in segments])
        log.info("Transcription complete:", text)

        await websocket.send_text(text)

        os.remove(tmpfile_path)
        log.info("Temp file deleted.")

    except Exception as e:
        log.info("Server error:", e)
        await websocket.send_text(f"[Server error: {str(e)}]")
    finally:
        await websocket.close()
        log.info("WebSocket closed.")
