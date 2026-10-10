from pathlib import Path

from fastapi.testclient import TestClient

from main import UPLOAD_DIR, UploadResponse, app

client = TestClient(app)


class TestUpload:
    def test_upload(self):
        content = b"%PDF-1.4 fake handbook"
        response = client.post(
            "/upload",
            files={"file": ("handbook.pdf", content, "application/pdf")},
        )
        assert response.status_code == 200
        data = UploadResponse.model_validate(response.json())
        assert data.filename == "handbook.pdf"
        assert data.size_bytes == len(content)

        saved = Path(data.path)
        assert saved.exists()
        assert saved.read_bytes() == content

        saved.unlink(missing_ok=True)

    def test_upload_rejects_non_pdf(self):
        response = client.post(
            "/upload",
            files={"file": ("handbook.txt", b"hello", "text/plain")},
        )
        assert response.status_code == 415

    def test_upload_no_filename(self):
        response = client.post(
            "/upload",
            files={"file": ("", b"empty", "text/plain")},
        )
        assert response.status_code in (400, 422)
        assert UPLOAD_DIR.exists()
