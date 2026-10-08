from pathlib import Path

from fastapi import FastAPI, File, HTTPException, UploadFile

app = FastAPI()

UPLOAD_DIR = Path(__file__).parent / "uploads"
UPLOAD_DIR.mkdir(exist_ok=True)


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/upload")
async def upload(file: UploadFile = File(...)):
    if not file.filename:
        raise HTTPException(status_code=400, detail="No filename provided")

    filename = Path(file.filename).name
    if not filename:
        raise HTTPException(status_code=400, detail="Invalid filename")

    dest = UPLOAD_DIR / filename
    contents = await file.read()
    dest.write_bytes(contents)

    return {
        "filename": filename,
        "size_bytes": len(contents),
        "content_type": file.content_type,
        "path": str(dest),
    }
