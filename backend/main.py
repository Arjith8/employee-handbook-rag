from pathlib import Path
from typing import Annotated

from fastapi import FastAPI, File, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)

UPLOAD_DIR = Path(__file__).parent / "uploads"
UPLOAD_DIR.mkdir(exist_ok=True)


class UploadResponse(BaseModel):
    filename: str
    size_bytes: int
    content_type: str | None
    path: str


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/upload", response_model=UploadResponse)
async def upload(
    file: Annotated[UploadFile, File()],
):
    if not file.filename:
        raise HTTPException(status_code=400, detail="No filename provided")

    filename = Path(file.filename).name
    if not filename:
        raise HTTPException(status_code=400, detail="Invalid filename")

    if Path(filename).suffix.lower() != ".pdf" or file.content_type != "application/pdf":
        raise HTTPException(status_code=415, detail="Only PDF files are supported")

    dest = UPLOAD_DIR / filename
    contents = await file.read()
    _ = dest.write_bytes(contents)

    return {
        "filename": filename,
        "size_bytes": len(contents),
        "content_type": file.content_type,
        "path": str(dest),
    }
