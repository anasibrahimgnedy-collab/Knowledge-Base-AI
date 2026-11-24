"""Render docs/FINAL_REPORT.md to docs/FINAL_REPORT.pdf (Markdown -> HTML -> headless Chromium print).

Needs `pip install markdown` and a Chromium/Chrome binary (set CHROME_BIN to override discovery).
"""
import os
import shutil
import subprocess
import tempfile
from pathlib import Path

import markdown

ROOT = Path(__file__).resolve().parents[1]
CSS = """
@page { size: A4; margin: 18mm 16mm; }
body { font: 10.5pt/1.45 "DejaVu Sans", Arial, sans-serif; color: #1a1a1a; }
h1 { font-size: 20pt; border-bottom: 2px solid #1f4e79; padding-bottom: 4px; color: #1f4e79; }
h2 { font-size: 14pt; color: #1f4e79; margin-top: 18px; }
h3 { font-size: 11.5pt; }
table { border-collapse: collapse; width: 100%; margin: 8px 0; font-size: 9pt; }
th, td { border: 1px solid #b8c4d0; padding: 4px 6px; vertical-align: top; text-align: left; }
th { background: #e8eef5; }
tr { page-break-inside: avoid; }
code { font: 9pt "DejaVu Sans Mono", monospace; background: #f1f3f5; padding: 0 2px; }
blockquote { margin: 8px 0; padding: 4px 12px; border-left: 3px solid #1f4e79; background: #f6f8fa; font-size: 9.5pt; }
"""


def main() -> Path:
    md_text = (ROOT / "docs" / "FINAL_REPORT.md").read_text(encoding="utf-8")
    body = markdown.markdown(md_text, extensions=["tables", "sane_lists"])
    html = f"<!doctype html><html><head><meta charset='utf-8'><style>{CSS}</style></head><body>{body}</body></html>"
    out = ROOT / "docs" / "FINAL_REPORT.pdf"
    chrome = os.environ.get("CHROME_BIN") or next(
        (c for c in ("/opt/pw-browsers/chromium", "chromium", "chromium-browser", "google-chrome", "chrome")
         if shutil.which(c)), None)
    if chrome is None:
        raise SystemExit("No Chromium/Chrome found; set CHROME_BIN")
    with tempfile.TemporaryDirectory() as tmp:
        src = Path(tmp) / "report.html"
        src.write_text(html, encoding="utf-8")
        subprocess.run([chrome, "--headless", "--no-sandbox", "--disable-gpu", "--no-pdf-header-footer",
                        f"--print-to-pdf={out}", src.as_uri()], check=True, capture_output=True)
    return out


if __name__ == "__main__":
    print(main())
