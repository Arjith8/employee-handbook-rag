"""HTML -> PDF converter for handbook test data.

Each handbook is intentionally saved in a different encoding
to test encoding handling in the RAG ingest pipeline:

  handbook.html          -> utf-8
  handbook-swe.html      -> windows-1252
  handbook-c-suite.html  -> utf-16 (with BOM)

Usage:
  uv run python test_data/convert.py
  uv run python test_data/convert.py --out test_data/pdf
"""

from __future__ import annotations

import argparse
from pathlib import Path

from weasyprint import HTML

HERE = Path(__file__).parent

ENCODINGS: dict[str, str] = {
    "handbook.html": "utf-8",
    "handbook-swe.html": "windows-1252",
    "handbook-c-suite.html": "utf-16",
}


def convert_one(src: Path, encoding: str, dest: Path) -> Path:
    """Read HTML with explicit encoding, write PDF."""
    html_text = src.read_bytes().decode(encoding)
    dest.parent.mkdir(parents=True, exist_ok=True)
    HTML(string=html_text, base_url=str(src.parent)).write_pdf(str(dest))
    return dest


def convert_all(out_dir: Path) -> list[Path]:
    made: list[Path] = []
    for name, enc in ENCODINGS.items():
        src = HERE / name
        if not src.exists():
            print(f"SKIP missing {src}")
            continue
        dest = out_dir / (src.stem + ".pdf")
        convert_one(src, enc, dest)
        print(f"OK {src.name} [{enc}] -> {dest} ({dest.stat().st_size} bytes)")
        made.append(dest)
    return made


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument(
        "--out",
        default=str(HERE / "pdf"),
        help="output dir for PDFs (default: test_data/pdf)",
    )
    args = ap.parse_args()
    convert_all(Path(args.out).resolve())


if __name__ == "__main__":
    main()
