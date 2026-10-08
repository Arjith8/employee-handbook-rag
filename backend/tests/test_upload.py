from pathlib import Path

from fastapi.testclient import TestClient

from main import UPLOAD_DIR, app

client = TestClient(app)


def test_upload(tmp_path=None):
    content = b"hello handbook"
    response = client.post(
        "/upload",
        files={"file": ("handbook.txt", content, "text/plain")},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["filename"] == "handbook.txt"
    assert data["size_bytes"] == len(content)

    saved = Path(data["path"])
    assert saved.exists()
    assert saved.read_bytes() == content

    # cleanup uploaded fixture
    saved.unlink(missing_ok=True)


def test_upload_no_filename():
    response = client.post(
        "/upload",
        files={"file": ("", b"empty", "text/plain")},
    )
    assert response.status_code in (400, 422)
    assert UPLOAD_DIR.exists()
