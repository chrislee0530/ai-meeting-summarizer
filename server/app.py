import os, tempfile
from pathlib import Path

from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

from .services.speech_service import transcribe_file

load_dotenv()

SPEECH_KEY = os.getenv("SPEECH_KEY")
SPEECH_REGION = os.getenv("SPEECH_REGION")

app = FastAPI(title="AI Meeting Summarizer")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], allow_credentials=True,
    allow_methods=["*"], allow_headers=["*"],
)

@app.get("/health")
def health():
    return {"ok": True}

@app.post("/transcribe")
async def transcribe(file: UploadFile = File(...)):
    if file.content_type not in [
        "audio/wav","audio/x-wav","audio/mpeg","audio/mp3","audio/x-m4a","audio/mp4"
    ]:
        raise HTTPException(status_code=400, detail="Upload a .wav, .mp3, or .m4a file.")

    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=f"_{file.filename}") as tmp:
            data = await file.read()
            tmp.write(data)
            tmp_path = tmp.name

        text = transcribe_file(tmp_path, SPEECH_KEY, SPEECH_REGION)
        Path(tmp_path).unlink(missing_ok=True)

        if not text.strip():
            raise HTTPException(status_code=422, detail="No speech recognized. Try a clearer/longer clip.")
        return {"transcript": text}

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Transcription error: {e}")

