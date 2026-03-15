from html.parser import HTMLParser
from pathlib import Path

# Tags whose content we discard entirely (not just the tags)
_SKIP_TAGS = {"script", "style", "nav", "header", "footer"}


class _TextExtractor(HTMLParser):
    def __init__(self):
        super().__init__()
        self._skip_depth = 0
        self._parts = []

    def handle_starttag(self, tag, attrs):
        if tag in _SKIP_TAGS:
            self._skip_depth += 1

    def handle_endtag(self, tag):
        if tag in _SKIP_TAGS and self._skip_depth > 0:
            self._skip_depth -= 1

    def handle_data(self, data):
        if self._skip_depth == 0:
            text = data.strip()
            if text:
                self._parts.append(text)

    def get_text(self) -> str:
        return "\n".join(self._parts)


def parse_html(path: str) -> str:
    """
    Read a saved LinkedIn profile HTML file and return clean plain text.

    Strips script, style, nav, header, and footer content, then extracts
    all remaining visible text.
    """
    html_path = Path(path)

    if not html_path.exists():
        raise FileNotFoundError(f"HTML file not found: {html_path}")

    if html_path.suffix.lower() not in {".html", ".htm"}:
        raise ValueError(f"Expected an HTML file, got: {html_path.name}")

    html = html_path.read_text(encoding="utf-8", errors="replace")

    extractor = _TextExtractor()
    extractor.feed(html)
    return extractor.get_text()
