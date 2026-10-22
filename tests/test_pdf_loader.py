from app.loader import pdf_loader
from app.loader.pdf_loader import PDFLoader


class _Page:
    def __init__(self, text):
        self._text = text

    def extract_text(self):
        return self._text


class _Reader:
    def __init__(self, pages):
        self.pages = pages


def test_pages_are_joined_and_empty_pages_skipped(monkeypatch):
    pages = [_Page("page one"), _Page(None), _Page(""), _Page("page two")]
    monkeypatch.setattr(pdf_loader, "PdfReader", lambda path: _Reader(pages))
    assert PDFLoader().load("any.pdf") == "page one\npage two\n"


def test_pdf_without_text_returns_empty_string(monkeypatch):
    monkeypatch.setattr(pdf_loader, "PdfReader", lambda path: _Reader([_Page(None)]))
    assert PDFLoader().load("scan.pdf") == ""
