from fastapi import FastAPI

app = FastAPI(title="AI Meeting Summarizer")

@app.get("/health")
def health():
    return {"ok": True}
