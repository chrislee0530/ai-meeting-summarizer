from fastapi import FastAPI, File, UploadFile

app = FastAPI(title="AI Meeting Summarizer")

@app.get("/health")
def health():
    return {"ok": True}

@app.post("/transcribe")
async def transcribe(file: UploadFile = File(...)):
    return {"filename": file.filename}

