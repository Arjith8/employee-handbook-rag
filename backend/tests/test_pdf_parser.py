from pathlib import Path

import pytest

from pdf_parser import PdfParser


class TestPdfParser:
    def test_page_count_and_text(self, pdf_file: Path):
        with PdfParser(pdf_file) as parser:
            assert parser.page_count == 2
            assert "hello" in parser.page_text(0)
            assert "world" in parser.page_text(1)

    def test_iter_and_full_text(self, pdf_file: Path):
        with PdfParser(pdf_file) as parser:
            assert [i for i, _ in parser.iter_pages()] == [0, 1]
            assert "hello" in parser.full_text()
            assert "world" in parser.full_text()

    def test_requires_open(self, pdf_file: Path):
        with pytest.raises(RuntimeError):
            PdfParser(pdf_file).page_count
