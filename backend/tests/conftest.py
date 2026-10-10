from pathlib import Path

import pymupdf
import pytest


@pytest.fixture
def pdf_file(tmp_path: Path) -> Path:
    """A two-page PDF with distinct text per page for parser/upload tests."""
    dest = tmp_path / "handbook.pdf"
    doc = pymupdf.open()
    for text in ["hello", "world"]:
        page = doc.new_page()
        page.insert_text((72, 72), text)
    doc.save(dest)
    doc.close()
    return dest
