"""PDF text access behind a stable interface.

Callers use PdfParser only — the PyMuPDF engine is an implementation
detail confined to this module, so swapping engines later means
rewriting here, not everywhere.
"""

from collections.abc import Iterator
from pathlib import Path

import pymupdf


class PdfParser:
    def __init__(self, path: str | Path) -> None:
        self._path = Path(path)
        self._doc: pymupdf.Document | None = None

    def open(self) -> "PdfParser":
        if self._doc is None:
            self._doc = pymupdf.open(self._path)
        return self

    def close(self) -> None:
        if self._doc is not None:
            self._doc.close()
            self._doc = None

    def __enter__(self) -> "PdfParser":
        return self.open()

    def __exit__(self, *exc_info: object) -> None:
        self.close()

    def _require_open(self) -> pymupdf.Document:
        if self._doc is None:
            raise RuntimeError("PdfParser is not open; call open() or use 'with'")
        return self._doc

    @property
    def page_count(self) -> int:
        return len(self._require_open())

    def page_text(self, index: int) -> str:
        return self._require_open()[index].get_text()

    def iter_pages(self) -> Iterator[tuple[int, str]]:
        doc = self._require_open()
        for i, page in enumerate(doc):
            yield i, page.get_text()

    def full_text(self) -> str:
        return "\n".join(text for _, text in self.iter_pages())
