from pathlib import Path

from playwright.sync_api import Browser


def render_to_pdf(html_path: Path, pdf_path: Path, browser: Browser) -> None:
    """Open a downloaded filing from disk and export it to PDF."""
    page = browser.new_page()
    try:
        page.goto(html_path.resolve().as_uri(), wait_until="load", timeout=60_000)
        page.pdf(
            path=str(pdf_path),
            format="A4",
            print_background=True,
            margin={"top": "1cm", "bottom": "1cm", "left": "1cm", "right": "1cm"},
        )
    finally:
        page.close()
